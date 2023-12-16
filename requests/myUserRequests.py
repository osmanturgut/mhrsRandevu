import requests
from concurrent.futures import ThreadPoolExecutor
from hastanePayload import get_hospital_payload
import logging
import random
from threading import Event, Lock

# Logger ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Authentication:
    def __init__(self, user_info, hospital_payload, selected_ip, lock):
        self.BASE_URL = 'https://prd.mhrs.gov.tr/api/'
        self.tckn = user_info["tckn"]
        self.userName = user_info.get("userName", "")
        self.password = user_info["password"]
        self.headers = {}
        self.hospital_payload = hospital_payload
        self.selected_ip = selected_ip
        self.randevu_alindi = Event()  # Her bir kullanıcı için ayrı bir Event oluşturuldu
        self.lock = lock  # lock ekledik
        self.get_token()

    def get_token(self):
        payload = {
            "kullaniciAdi": self.tckn,
            "parola": self.password,
            "islemKanali": "VATANDAS_WEB",
            "girisTipi": "PAROLA",
        }
        proxies = {
            "https": self.selected_ip
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.BASE_URL + "vatandas/login", headers=headers, json=payload, proxies=proxies, verify=True)
        if response.status_code == 200:
            tokens = response.json()['data']['jwt']
            self.headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {tokens}'
            }

            if self.userName:
                self.user_login_with_parent_user()

            self.randevu_ekle()
        else:
            raise Exception('Token alınamadı')

    def user_login_with_parent_user(self):
        ad_aranan = f"{self.userName}"
        yetkili_get = requests.get(self.BASE_URL + "vatandas/vatandas/yetkili-kisiler", headers=self.headers)
        yetkili_get.raise_for_status()
        bulunan_veri = next((veri for veri in yetkili_get.json()["data"] if veri["ad"].upper() == ad_aranan.upper()), None)

        if bulunan_veri:
            uuid_degeri = bulunan_veri["uuid"]
            yetkili = {"uuid": f"{uuid_degeri}", "islemKanali": "VATANDAS_WEB"}
            yetkili_gecis_post = requests.post(self.BASE_URL + "vatandas/vatandas/yetkili-hesaba-gec", headers=self.headers, json=yetkili)

            if yetkili_gecis_post.json()['success']:
                return yetkili_gecis_post

    def randevu_search(self):
        payload2 = self.hospital_payload
        proxies = {
            "https": self.selected_ip
        }
        slotListRequest = requests.post(self.BASE_URL + "kurum-rss/randevu/slot-sorgulama/slot", headers=self.headers,json=payload2, proxies=proxies, verify=True)
        if slotListRequest.status_code == 200:
            return slotListRequest.json()

    def randevu_ekle(self):
        local_available_slots = []
        while not self.randevu_alindi.is_set():
            logger.info(f"randevu aranıyor. {self.tckn} IP={self.selected_ip.split('@')[1]}")
            slotListRequest = self.randevu_search()
            if slotListRequest and slotListRequest.get('success'):
                for hekim_slot in slotListRequest['data'][0]['hekimSlotList']:
                    for muayene_yeri_slot in hekim_slot['muayeneYeriSlotList']:
                        for slot in muayene_yeri_slot['saatSlotList']:
                            for slotListKalanKullanim in slot['slotList']:
                                if slotListKalanKullanim['slot']['kalanKullanim'] > 0:
                                    local_available_slots.append(slotListKalanKullanim)

                if local_available_slots:
                    with self.lock:
                        if not self.randevu_alindi.is_set():
                            try:
                                selected_slot = random.choice(local_available_slots)
                                self.make_randevu(selected_slot)
                            except Exception as e:
                                logger.error(f"Exception in make_randevu: {e}")

        # Tüm işlemler bittikten sonra uygun randevuları logla
        #self.aktifRandevuList(self.tckn, local_available_slots)

    def aktifRandevuList(self, tckn, available_slots):
        with (self.lock):
            for selected_slot in available_slots:
                log_message = f" USERS: {tckn}",\
                              f"id={selected_slot['slot']['id']}, " \
                              f"fkCetvelId={selected_slot['slot']['fkCetvelId']}, " \
                              f"baslangicZamani={selected_slot['slot']['baslangicZamani']}, " \
                              f"bitisZamani={selected_slot['slot']['bitisZamani']}"
                logger.info(log_message)
    def make_randevu(self, slotListKalanKullanim):
        slot = slotListKalanKullanim['slot']
        payload3 = {
            "fkSlotId": slot['id'],
            "fkCetvelId": slot['fkCetvelId'],
            "muayeneYeriId": slot['muayeneYeriId'],
            "baslangicZamani": slot['baslangicZamani'],
            "bitisZamani": slot['bitisZamani'],
        }

        logger.info(
            f"Uygun Randevu Bulundu. {self.tckn} Kullanıcıya Ekleniyor.. ***TARİH :{payload3['baslangicZamani']} fkSlotId={payload3['fkSlotId']} IP={self.selected_ip.split('@')[1]} ***")
        proxies = {
            "https": self.selected_ip
        }
        randevuEkle = requests.post(self.BASE_URL + "kurum/randevu/randevu-ekle", headers=self.headers, json=payload3,proxies=proxies, verify=True)

        if randevuEkle.status_code == 200:
            logger.info(f"RANDEVU BAŞARIYLA ALINDI  - Kullanıcı: {self.tckn}  ***TARİH :{payload3['baslangicZamani']} fkSlotId={payload3['fkSlotId']} İstek atılan IP={self.selected_ip.split('@')[1]} ***")
            self.randevu_alindi.set()

        elif randevuEkle.status_code == 428:
            logger.critical(f"Aktif Randevu Bulunmaktadır ..!  Kullanıcı: {self.tckn}")
            self.randevu_alindi.set()

        elif randevuEkle.status_code == 400:
            logger.critical(f"{self.tckn} {randevuEkle.json()['errors'][0]['mesaj']} <<MHRS Tarafından Bloklandı..! {self.tckn} ***TARİH :{payload3['baslangicZamani']} fkSlotId={payload3['fkSlotId']}İstek atılan IP={self.selected_ip.split('@')[1]} ***")


def process_user(user_info, ip_info, lock):
    payload_name = user_info.get("hastaneBilgisi")
    hospital_payload = get_hospital_payload(payload_name)

    selected_ip = f"http://{ip_info['user']}:{ip_info['password']}@{ip_info['ip']}:{ip_info['port']}"
    jwtToken = Authentication(user_info, hospital_payload, selected_ip, lock)
    jwtToken.randevu_ekle()

if __name__ == '__main__':
    users = [

        {"tckn": "32194456622", "password": "Muhammed23", "hastaneBilgisi": "ElazigFethisekin"},
    ]

    ip_infos = [

        {'ip': '104.239.108.202', 'port': 6437, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.207', 'port': 6442, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.33', 'port': 6268, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '216.173.84.63', 'port': 5978, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.91', 'port': 6326, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},
        {'ip': '104.239.108.26', 'port': 6261, 'user': 'iokycxec', 'password': 'e80lfjzqkbal'},

    ]

    lock = Lock()
    with ThreadPoolExecutor(max_workers=len(users)) as executor:
        executor.map(process_user, users, ip_infos, [lock] * len(users))