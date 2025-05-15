import asyncio
import aiohttp
from telegram import Bot
import logging
import random
import pytz
from datetime import datetime, timedelta

from hastanePayload import get_hospital_payload

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Authentication:
    def __init__(self, session, user_info, hospital_payload, selected_ip):
        self.BASE_URL = 'https://prd.mhrs.gov.tr/api/'
        self.tckn = user_info["tckn"]
        self.userName = user_info.get("userName", "")
        self.password = user_info["password"]
        self.hospital = user_info["hastaneBilgisi"]
        self.session = session
        self.hospital_payload = hospital_payload
        self.selected_ip = selected_ip
        self.headers = {}
        self.last_selected_slot = None
        self.randevu_alindi = False
        self.notification_queue = []

    async def get_token(self):
        payload = {
            "kullaniciAdi": self.tckn,
            "parola": self.password,
            "islemKanali": "VATANDAS_WEB",
            "girisTipi": "PAROLA",
        }
        async with self.session.post(self.BASE_URL + "vatandas/login", json=payload, verify_ssl=False, proxy=self.selected_ip) as response:
            if response.status == 200:
                data = await response.json()
                tokens = data['data']['jwt']
                self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {tokens}'}
                if self.userName:
                    await self.ebeveynden_cocuga_gecis()
                await self.randevulari_filtrele()
            else:
                raise Exception('Token alınamadı')

    async def ebeveynden_cocuga_gecis(self):
        ad_aranan = f"{self.userName}"
        async with self.session.get(self.BASE_URL + "vatandas/vatandas/yetkili-kisiler", headers=self.headers, verify_ssl=False, proxy=self.selected_ip) as response:
            data = await response.json()
            bulunan_veri = next((veri for veri in data["data"] if veri["ad"].upper() == ad_aranan.upper()), None)
            if bulunan_veri:
                uuid_degeri = bulunan_veri["uuid"]
                yetkili = {"uuid": f"{uuid_degeri}", "islemKanali": "VATANDAS_WEB"}
                await self.session.post(self.BASE_URL + "vatandas/vatandas/yetkili-hesaba-gec", headers=self.headers, json=yetkili, verify_ssl=False, proxy=self.selected_ip)

    async def randevu_arama(self):
        async with self.session.post(self.BASE_URL + "kurum-rss/randevu/slot-sorgulama/slot", headers=self.headers,
                                     json=self.hospital_payload, verify_ssl=False, proxy=self.selected_ip) as response:
            if response.status == 200:
                data = await response.json()
                if data:  # Eğer data boş değilse, yani randevu bulunmuşsa
                    logging.info(f"Randevu bulundu: {data}")
                return data

    async def randevulari_filtrele(self):
        local_available_slots = []  # Uygun randevuları burada tutacağız
        max_bekleme_suresi = timedelta(hours=14)  # Maksimum bekleme süresi, dışarıdan dinamik olarak değiştirilebilir

        while not self.randevu_alindi:
            logger.info(f"randevu aranıyor. {self.tckn} IP={self.selected_ip.split('@')[1]}")
            slotListRequest = await self.randevu_arama()  # Randevu araması yapılır
            if slotListRequest and slotListRequest.get('success'):
                for hekim_slot in slotListRequest['data'][0]['hekimSlotList']:
                    for muayene_yeri_slot in hekim_slot['muayeneYeriSlotList']:
                        for slot in muayene_yeri_slot['saatSlotList']:
                            for slotListKalanKullanim in slot['slotList']:
                                if slotListKalanKullanim['slot'][
                                    'kalanKullanim'] > 0:  # Kullanılabilir randevuları kontrol et
                                    baslangic_zamani_str = slotListKalanKullanim['slot']['baslangicZamani']
                                    baslangic_zamani = datetime.strptime(baslangic_zamani_str, "%Y-%m-%d %H:%M:%S")
                                    baslangic_zamani = baslangic_zamani.replace(tzinfo=pytz.timezone("Europe/Istanbul"))
                                    local_now = datetime.now(pytz.timezone("Europe/Istanbul"))
                                    fark = baslangic_zamani - local_now  # Zaman farkını hesapla

                                    # Eğer fark 15 saatin altındaysa aramaya devam et
                                    if fark <= max_bekleme_suresi:
                                        continue  # 15 saatten azsa, geç ve aramaya devam et

                                    # 15 saatten fazla bir randevu bulduğunda bunu local_available_slots'a ekle
                                    local_available_slots.append(slotListKalanKullanim)  # 15 saatten fazla randevuyu al

                                    # Loglama: Kalan süreyi hesapla ve logla
                                    fark_hours, remainder = divmod(fark.seconds, 3600)
                                    fark_minutes, _ = divmod(remainder, 60)
                                    formatted_fark = f"{fark_hours} Saat {fark_minutes} Dakika"
                                    logger.info(
                                        f"Randevunun Başlangıç Zamanı: {baslangic_zamani} | Kalan Süre: {formatted_fark}")

                                    # Telegram'a bildirim gönder
                                    await self.send_telegram_notification(
                                        [f"Randevu Tarihi: {baslangic_zamani} | Kalan Süre: {formatted_fark}"])

            # Eğer uygun bir randevu varsa, onu al
            if local_available_slots:
                try:
                    selected_slot = random.choice(local_available_slots)  # Uygun bir randevu seç
                    await self.randevuTanimla(selected_slot)  # Randevu tanımla (almaya başla)
                    self.randevu_alindi = True  # Randevu alındı
                    logger.info(f"Randevu alındı: {selected_slot}")
                except Exception as e:
                    logger.error(f"Exception in randevuTanimla: {e}")

    async def randevuTanimla(self, slotListKalanKullanim):
        slot = slotListKalanKullanim['slot']
        payload3 = {
            "fkSlotId": slot['id'],
            "fkCetvelId": slot['fkCetvelId'],
            "muayeneYeriId": slot['muayeneYeriId'],
            "baslangicZamani": slot['baslangicZamani'],
            "bitisZamani": slot['bitisZamani'],
            "yenidogan": False,
            "randevuNotu": ""
        }
        self.last_selected_slot = payload3
        logger.info(
            f" 'Randevu Bulundu.   Kullanıcıya Ekleniyor: {self.tckn} #'  |**| 'Randevu Tarihi :{payload3['baslangicZamani']}' 'IP={self.selected_ip.split('@')[1]}' |**|")

        async with self.session.post(self.BASE_URL + "kurum/randevu/randevu-ekle", headers=self.headers, json=payload3,
                                     verify_ssl=False, proxy=self.selected_ip) as randevuEkle:
            if randevuEkle.status == 200:
                logger.info(
                    f" |RANDEVU BAŞARIYLA ALINDI|   #  Kullanıcı: {self.tckn} #   |**| 'Randevu Tarihi :{payload3['baslangicZamani']}' 'IP={self.selected_ip.split('@')[1].split(':')[1]}' |**|")
                self.notification_queue.append(
                    f"|RANDEVU BAŞARIYLA ALINDI| \nKullanıcı : {self.tckn}\nAlınan Hastane: {self.hospital} \nRandevu Tarihi: {payload3['baslangicZamani']} \nCihaz : {self.selected_ip.split('@')[1].split(':')[1]}")
                self.randevu_alindi = True

            elif randevuEkle.status == 428:
                logger.critical(
                    f"Aktif Randevu Bulunmaktadır ..!  Kullanıcı: {self.tckn}")
                self.notification_queue.append(f"Aktif Randevu Bulunmaktadır ..!  Kullanıcı: {self.tckn}")
                self.randevu_alindi = True
            elif randevuEkle.status == 400:
                error_message = await randevuEkle.json()
                logger.critical(
                    f"{error_message['errors'][0]['mesaj']} <<MHRS Tarafından Bloklandı..! {self.tckn} |**|TARİH :{payload3['baslangicZamani']} fkSlotId={payload3['fkSlotId']} IP={self.selected_ip.split('@')[1]} |**|")
                self.notification_queue.append(f"{error_message['errors'][0]['mesaj']}")
            else:
                logger.error(
                    f"Bilinmeyen bir hata kodu döndü: {randevuEkle.status}. Hata mesajı: {await randevuEkle.text()}")
                self.notification_queue.append(f"Bilinmeyen bir hata kodu döndü: {randevuEkle.status}. Hata mesajı: {await randevuEkle.text()}")
    async def send_telegram_notification(self, messages):
        bot_token = '6939284616:AAE4sBlGfQ4pG197XG35y5wm-4dE3-Xe-ks'
        chat_id = '5843254010'
        bot = Bot(token=bot_token)
        for message in messages:
            await bot.send_message(chat_id=chat_id, text=message)

    async def process_notifications(self):
        if self.notification_queue:
            await self.send_telegram_notification(self.notification_queue)
            self.notification_queue = []  # Bildirim kuyruğunu temizleme

async def process_user(session, user_info, primary_hospital_payload, secondary_hospital_payload, ip_info):
    try:
        async with aiohttp.ClientSession() as session:
            auth = Authentication(session, user_info, primary_hospital_payload, f"http://{ip_info['user']}:{ip_info['password']}@{ip_info['ip']}:{ip_info['port']}")
            await auth.get_token()

            if 'ikinciHastaneBilgisi' in user_info:
                secondary_selected_ip = f"http://{ip_info['user']}:{ip_info['password']}@{ip_info['ip']}:{ip_info['port']}"
                secondary_auth = Authentication(session, user_info, secondary_hospital_payload, secondary_selected_ip)
                await secondary_auth.get_token()

    except Exception as e:
        logger.error(f"Hata oluştu: {e}. Kullanıcı işlenemedi: {user_info['tckn']}")
    else:
        await auth.process_notifications()

async def dateTime(users, ip_infos):
    primary_hospital_payloads = [get_hospital_payload(user["hastaneBilgisi"]) for user in users]
    secondary_hospital_payloads = [get_hospital_payload(user.get("ikinciHastaneBilgisi")) for user in users]

    tasks = []
    async with aiohttp.ClientSession() as session:
        for user, primary_payload, secondary_payload, ip_info in zip(users, primary_hospital_payloads, secondary_hospital_payloads, ip_infos):
            task = asyncio.create_task(process_user(session, user, primary_payload, secondary_payload, ip_info))
            tasks.append(task)
        await asyncio.gather(*tasks)
