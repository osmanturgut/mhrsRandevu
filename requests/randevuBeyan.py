import aiohttp
import logging
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
        async with self.session.post(self.BASE_URL + "vatandas/login", json=payload, ssl=False, proxy=self.selected_ip) as response:
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
                    logger.info(f"{self.tckn} - Randevu Beyanı dolu:")
                    logger.info(f"{self.tckn} - {randevuBeyan['randevuBeyan']}")
                    for beyan in randevuBeyan["randevuBeyan"]:
                        await self.onayla(beyan["fkRandevuId"])
                else:
                    logger.info(f"{self.tckn} - Randevu Beyanı dolu değil.")
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
                logger.info(f"{self.tckn} - Randevu Beyanı {randevu_id} başarıyla onaylandı.")
            else:
                response_text = await response.text()
                logger.error(f"{self.tckn} - Failed to confirm Randevu Beyanı {randevu_id}: {response.status}, {response_text}")
                raise Exception('Randevu Beyanı onaylanamadı')

async def process_user(session, user_info, ip_info):
    try:
        payload_name = user_info.get("hastaneBilgisi")
        hospital_payload = get_hospital_payload(payload_name)
        selected_ip = f"http://{ip_info['user']}:{ip_info['password']}@{ip_info['ip']}:{ip_info['port']}"
        jwtToken = Authentication(session, user_info, hospital_payload, selected_ip)
        await jwtToken.get_token()
    except Exception as e:
        logger.error(f"Hata oluştu: {e}. Kullanıcı işlenemedi: {user_info['tckn']}")

if __name__ == '__main__':
    users = [
        {"tckn": "24200067304", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "55435629302", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "64363133256", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "56065708412", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "36077373242", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "47791981804", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "29996181432", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "49105246012", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "56269700038", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "51907132356", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "36941047408", "password": "saziye", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "28400470094", "password": "Sahra2019", "hastaneBilgisi": "bakirkoySadiKonukEAH"},
        {"tckn": "12097654868", "password": "Sahra2019", "hastaneBilgisi": "kucukCekmeceKanuniSultanSuleymanEAH"},
        {"tckn": "27017663226", "password": "Beyazinci1", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "53557098822", "password": "Beyazinci1", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "11007208818", "password": "Beyazinci1", "hastaneBilgisi": "gaziosmanpasaEAH"},
        {"tckn": "31735825330", "password": "Beyazinci1", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
        {"tckn": "74461018720", "password": "Serhat73", "hastaneBilgisi": "sirnakDevletHastanesi"},
        {"tckn": "45964968720", "password": "Serhat73", "hastaneBilgisi": "cizreDevletHastanesi"},
    ]
    ip_infos = [
        {'ip': '104.239.108.143', 'port': 6378, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.92', 'port': 6327, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.202', 'port': 6437, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.207', 'port': 6442, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.19', 'port': 6254, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.178', 'port': 6413, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.77', 'port': 6312, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.177', 'port': 6412, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.94', 'port': 6329, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.149', 'port': 6384, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.5', 'port': 6240, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.33', 'port': 6268, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.91', 'port': 6326, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.26', 'port': 6261, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.244', 'port': 6479, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.124', 'port': 6359, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.81', 'port': 6316, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '209.99.134.194', 'port': 5890, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '209.99.129.112', 'port': 6100, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '206.41.168.175', 'port': 6840, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.143', 'port': 6378, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.92', 'port': 6327, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.202', 'port': 6437, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.207', 'port': 6442, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.19', 'port': 6254, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.178', 'port': 6413, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.77', 'port': 6312, 'user': '39BhSyY5', 'password': '39BhSyY5'},
        {'ip': '104.239.108.177', 'port': 6412, 'user': '39BhSyY5', 'password': '39BhSyY5'},
    ]

    import asyncio
    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [process_user(session, user, ip_info) for user, ip_info in zip(users, ip_infos)]
            await asyncio.gather(*tasks)

    asyncio.run(main())