import aiohttp
import logging
import random
from hastanePayload import get_hospital_payload

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Authentication:
    def __init__(self, session, user_info, hospital_payload, selected_ip):
        self.BASE_URL = 'https://prd.mhrs.gov.tr/api/'
        self.tckn = user_info["tckn"]
        self.userName = user_info.get("userName", "")
        self.password = user_info["password"]
        self.session = session
        self.hospital_payload = hospital_payload
        self.selected_ip = selected_ip
        self.headers = {}
        self.last_selected_slot = None
        self.randevu_alindi = False

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
        }
        self.last_selected_slot = payload3
        logger.info(
            f" 'Randevu Bulundu.   Kullanıcıya Ekleniyor: {self.tckn} #'  |**| 'Randevu Tarihi :{payload3['baslangicZamani']}' 'IP={self.selected_ip.split('@')[1]}' |**|")

        async with self.session.post(self.BASE_URL + "kurum/randevu/randevu-ekle", headers=self.headers, json=payload3, verify_ssl=False, proxy=self.selected_ip) as randevuEkle:
            if randevuEkle.status == 200:
                logger.info(
                    f" |RANDEVU BAŞARIYLA ALINDI|   #  Kullanıcı: {self.tckn} #   |**| 'Randevu Tarihi :{payload3['baslangicZamani']}' 'IP={self.selected_ip.split('@')[1]}' |**|")
                self.randevu_alindi = True
            elif randevuEkle.status == 428:
                logger.critical(
                    f"Aktif Randevu Bulunmaktadır ..!  Kullanıcı: {self.tckn}")
                self.randevu_alindi = True
            elif randevuEkle.status == 400:
                error_message = await randevuEkle.json()
                logger.critical(
                    f"{error_message['errors'][0]['mesaj']} <<MHRS Tarafından Bloklandı..! {self.tckn} |**|TARİH :{payload3['baslangicZamani']} fkSlotId={payload3['fkSlotId']} IP={self.selected_ip.split('@')[1]} |**|")

async def process_user(session, user_info, ip_info):
    try:
        payload_name = user_info.get("hastaneBilgisi")
        hospital_payload = get_hospital_payload(payload_name)
        selected_ip = f"http://{ip_info['user']}:{ip_info['password']}@{ip_info['ip']}:{ip_info['port']}"
        async with aiohttp.ClientSession() as session:
            jwtToken = Authentication(session, user_info, hospital_payload, selected_ip)
            await jwtToken.get_token()
    except Exception as e:
        logger.error(f"Hata oluştu: {e}. Kullanıcı işlenemedi: {user_info['tckn']}")

if __name__ == '__main__':
    users = [
        {"tckn": "64483411944", "password": "Umut3434", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "16404030390", "password": "Furkan3434", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "15914352404", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "17232002726", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
    ]
    ip_infos = [
        {'ip': '104.239.108.244', 'port': 6479, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.124', 'port': 6359, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.81', 'port': 6316, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '216.173.84.123', 'port': 6038, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.143', 'port': 6378, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.5', 'port': 6240, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.149', 'port': 6384, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.94', 'port': 6329, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.77', 'port': 6312, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
    ]

    import asyncio
    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [process_user(session, user, ip_info) for user, ip_info in zip(users, ip_infos)]
            await asyncio.gather(*tasks)

    asyncio.run(main())
