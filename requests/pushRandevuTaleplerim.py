import aiohttp
import logging
import random
import asyncio
from telegram import Bot
from hastanePayload import get_hospital_payload

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Authentication:
    def __init__(self, session, user_info, hospital_payload, selected_ip):
        self.BASE_URL = 'https://prd.mhrs.gov.tr/api/'
        self.tckn = user_info["tckn"]
        self.userName = user_info.get("userName", "")
        self.password = user_info["password"]
        self.hospital = user_info["hastaneBilgisi"]  # Eklenen satır
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
        async with self.session.post(self.BASE_URL + "kurum-rss/randevu/slot-sorgulama/slot", headers=self.headers, json=self.hospital_payload, verify_ssl=False, proxy=self.selected_ip) as response:
            if response.status == 200:
                return await response.json()

    async def randevulari_filtrele(self):
        local_available_slots = []
        while not self.randevu_alindi:
            logger.info(f"randevu aranıyor. {self.tckn} IP={self.selected_ip.split('@')[1]}")
            slotListRequest = await self.randevu_arama()
            if slotListRequest and slotListRequest.get('success'):
                for hekim_slot in slotListRequest['data'][0]['hekimSlotList']:
                    for muayene_yeri_slot in hekim_slot['muayeneYeriSlotList']:
                        for slot in muayene_yeri_slot['saatSlotList']:
                            for slotListKalanKullanim in slot['slotList']:
                                if slotListKalanKullanim['slot']['kalanKullanim'] > 0:
                                    local_available_slots.append(slotListKalanKullanim)

                if local_available_slots:
                    try:
                        selected_slot = random.choice(local_available_slots)
                        await self.randevuTanimla(selected_slot)
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
                    f" |RANDEVU BAŞARIYLA ALINDI|   #  Kullanıcı: {self.tckn} #   |**| 'Randevu Tarihi :{payload3['baslangicZamani']}' 'IP={self.selected_ip.split('@')[1]}' |**|")
                self.notification_queue.append(f"|RANDEVU BAŞARIYLA ALINDI| \nKullanıcı : {self.tckn}\nAlınan Hastane: {self.hospital} \nRandevu Tarihi: {payload3['baslangicZamani']}")  # Değiştirilen satır

                self.randevu_alindi = True
            elif randevuEkle.status == 428:
                logger.critical(
                    f"Aktif Randevu Bulunmaktadır ..!  Kullanıcı: {self.tckn}")
                self.randevu_alindi = True
            elif randevuEkle.status == 400:
                error_message = await randevuEkle.json()
                logger.critical(
                    f"{error_message['errors'][0]['mesaj']} <<MHRS Tarafından Bloklandı..! {self.tckn} |**|TARİH :{payload3['baslangicZamani']} fkSlotId={payload3['fkSlotId']} IP={self.selected_ip.split('@')[1]} |**|")

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
        """
        {"tckn": "70981195392", "password": "Yavuz2056552", "hastaneBilgisi": "basaksehirCamveSakuraSehirHast"},# 21 nisan
        #{"tckn": "55834690392", "password": "Edatuana.1", "hastaneBilgisi": "basaksehirCamveSakuraSehirHast"},# 21 nisan
        {"tckn": "76681005238", "password": "5354Hilal", "hastaneBilgisi": "basaksehirCamveSakuraSehirHast"},# 21 nisan
        {"tckn": "42038152566", "password": "5354Zeynep", "hastaneBilgisi": "basaksehirCamveSakuraSehirHast"}, # 21 nisan
        {"tckn": "60034576124", "password": "Esraaras21", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "27311672740", "password": "Ecmel061", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "36712688472", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "17228308764", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},

        """
async def main():
    users = [
                {"tckn": "69715177148", "password": "Serhat73", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "25478648318", "password": "Serhat73", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "60016500154", "password": "Serhat73", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "27070399322", "password": "Songül.55", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "72043099228", "password": "Songül.55", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "73855039044", "password": "Songül.55", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "27070399322", "password": "Songül.55", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "67789241352", "password": "Songül.55", "hastaneBilgisi": "sirnakDevletHastanesi"},
                {"tckn": "62596414210", "password": "Songül.55", "hastaneBilgisi": "sirnakDevletHastanesi"},

    ]
    ip_infos = [
        {'ip': '104.239.108.94', 'port': 6329, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.149', 'port': 6384, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.5', 'port': 6240, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.143', 'port': 6378, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.92', 'port': 6327, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.202', 'port': 6437, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.207', 'port': 6442, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.33', 'port': 6268, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.91', 'port': 6326, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.26', 'port': 6261, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
        {'ip': '104.239.108.244', 'port': 6479, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},

    ]

    primary_hospital_payloads = [get_hospital_payload(user["hastaneBilgisi"]) for user in users]
    secondary_hospital_payloads = [get_hospital_payload(user.get("ikinciHastaneBilgisi")) for user in users]

    tasks = []
    async with aiohttp.ClientSession() as session:
        for user, primary_payload, secondary_payload, ip_info in zip(users, primary_hospital_payloads, secondary_hospital_payloads, ip_infos):
            task = asyncio.create_task(process_user(session, user, primary_payload, secondary_payload, ip_info))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
