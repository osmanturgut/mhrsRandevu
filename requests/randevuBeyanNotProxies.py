import aiohttp
import logging
from hastanePayload import get_hospital_payload

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Authentication:
    def __init__(self, session, user_info, hospital_payload):
        self.BASE_URL = 'https://prd.mhrs.gov.tr/api/'
        self.tckn = user_info["tckn"]
        self.userName = user_info.get("userName", "")
        self.password = user_info["password"]
        self.session = session
        self.hospital_payload = hospital_payload
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
        async with self.session.post(self.BASE_URL + "vatandas/login", json=payload, ssl=False) as response:
            if response.status == 200:
                data = await response.json()
                tokens = data['data']['jwt']
                self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {tokens}'}
                await self.check_login_uyari()
            else:
                response_text = await response.text()
                logger.error(f"{self.tckn} - Failed to get token: {response.status}, {response_text}")
                raise Exception('Token alınamadı')

    async def check_login_uyari(self):
        async with self.session.get(self.BASE_URL + "vatandas/bildirim/login-uyari", headers=self.headers, ssl=False) as response:
            if response.status == 200:
                data = await response.json()
                randevuBeyan = data["data"]["randevuBeyan"]
                logger.info(f"{self.tckn} - randevuBeyan: {randevuBeyan}")
                if randevuBeyan["durum"] and len(randevuBeyan["randevuBeyan"]) > 0:
                    logger.info(f"{self.tckn} - *** RANDEVU BEYANİ DOLU ***:")
                    logger.info(f"{self.tckn} - {randevuBeyan['randevuBeyan']}")
                    for beyan in randevuBeyan["randevuBeyan"]:
                        await self.onayla(beyan["fkRandevuId"])
                else:
                    logger.info(f"{self.tckn} - Randevu Beyanı Bulunmamakta..!")
            else:
                response_text = await response.text()
                logger.error(f"{self.tckn} - Failed to get Login Uyari: {response.status}, {response_text}")
                raise Exception('Login Uyari bilgisi alınamadı')

    async def onayla(self, randevu_id):
        payload = {
            "fkRandevuId": randevu_id,
            "lrandevuBeyanDurumu": 1
        }
        async with self.session.post(self.BASE_URL + "kurum/randevu-beyan/onayla", headers=self.headers, json=payload, ssl=False) as response:
            if response.status == 200:
                logger.info(f"{self.tckn} - ###### Randevu Beyanı {randevu_id} başarıyla onaylandı. #####")
            else:
                response_text = await response.text()
                logger.error(f"{self.tckn} - Failed to confirm Randevu Beyanı {randevu_id}: {response.status}, {response_text}")
                raise Exception('Randevu Beyanı onaylanamadı')

async def process_user(session, user_info):
    try:
        payload_name = user_info.get("hastaneBilgisi")
        hospital_payload = get_hospital_payload(payload_name)
        jwtToken = Authentication(session, user_info, hospital_payload)
        await jwtToken.get_token()
    except Exception as e:
        logger.error(f"Hata oluştu: {e}. Kullanıcı işlenemedi: {user_info['tckn']}")

if __name__ == '__main__':
    users = [

        {"tckn": "30185571088", "password": "Egehan4848", "hastaneBilgisi": "bakirkoySadiKonukEAH"},
        {"tckn": "55831713766", "password": "Cınar3435", "hastaneBilgisi": "bakirkoySadiKonukEAH"},
        {"tckn": "17219990244", "password": "Eymen3434", "hastaneBilgisi": "basaksehirCamveSakuraSehirHast"},
        {"tckn": "21326191128", "password": "Ucel1234", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "12097654868", "password": "Sahra2019", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "48439269230", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "24680556220", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "48049270138", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "31540279540", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "17837318390", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "36217675748", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "24485738944", "password": "Ucel5432", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "47392303494", "password": "Ucel5432", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "31540279540", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "17837318390", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "36217675748", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "24485738944", "password": "Ucel5432", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "47392303494", "password": "Ucel5432", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},


    ]

    import asyncio
    async def main():
        async with aiohttp.ClientSession() as session:
            for user in users:
                await process_user(session, user)

    asyncio.run(main())
