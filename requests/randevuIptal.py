import json
import requests
from concurrent.futures import ThreadPoolExecutor
from hastanePayload import get_hospital_payload
import logging
import os

class Authentication:
    def __init__(self, user_info, hospital_payload, log_directory):
        self.BASE_URL = 'https://prd.mhrs.gov.tr/api/'
        self.tckn = user_info["tckn"]
        self.password = user_info["password"]
        self.userName = user_info.get("userName")
        self.headers = {}
        self.hospital_payload = hospital_payload
        self.log_directory = log_directory
        self.logger = None
        self.cancelled = False
        self.get_token()


    def get_logger(self):
        if self.logger is None:
            self.logger = logging.getLogger(self.tckn)
            self.logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            log_file = os.path.join(self.log_directory, f"{self.tckn}_log.txt")

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        return self.logger

    def get_token(self):
        payload = {
            "kullaniciAdi": self.tckn,
            "parola": self.password,
            "islemKanali": "VATANDAS_WEB",
            "girisTipi": "PAROLA",
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self
                .BASE_URL + "vatandas/login", headers=headers, json=payload)

        if response.status_code == 200:
            tokens = response.json()['data']['jwt']
            self.headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {tokens}'
            }
            if self.userName:
                self.user_login_with_parent_user()
            self.randevuIptal()
        else:
            self.get_logger().error('Token alınamadı')

    def user_login_with_parent_user(self):
        if self.userName:
            ad_aranan = f"{self.userName}"
            yetkili_get = requests.get(self
                    .BASE_URL + "vatandas/vatandas/yetkili-kisiler", headers=self.headers)
            yetkili_get.raise_for_status()
            bulunan_veri = next((veri for veri in yetkili_get.json()["data"] if veri["ad"].upper() == ad_aranan.upper()), None)

            if bulunan_veri:
                uuid_degeri = bulunan_veri["uuid"]
                yetkili = {"uuid": f"{uuid_degeri}", "islemKanali": "VATANDAS_WEB"}
                yetkili_gecis_post = requests.post(self
                                .BASE_URL + "vatandas/vatandas/yetkili-hesaba-gec", headers=self.headers, json=yetkili)

                if yetkili_gecis_post.json().get('success'):
                    self.get_logger().info("Ebeveyn kullanıcıya geçiş başarılı.")

    def randevuIptal(self):
        self.get_logger().info("Aktif randevuları iptal etmeye başlama...")
        iptalEdilecekRandevu = requests.get(self
                        .BASE_URL + "kurum/randevu/randevu-gecmisi", headers=self.headers)
        veri = iptalEdilecekRandevu.json()
        if veri.get('success') and veri.get('data'):
            aktifRandevuList = veri['data']['aktifRandevuDtoList']
            if not aktifRandevuList:
                self.get_logger().warning("Aktif randevunuz bulunmamaktadır.")
                return
            for randevu in aktifRandevuList:
                if not self.cancelled:
                    hastaneRandevuNumarasi = randevu['hastaRandevuNumarasi']
                    response = self.iptalEt(hastaneRandevuNumarasi)
                    if response.get('success'):
                        self.get_logger().info(f"*****************Randevu {hastaneRandevuNumarasi} başarıyla iptal edildi.*****************")
                    else:
                        self.get_logger().warning(f"Hata: Randevu {hastaneRandevuNumarasi} iptal edilemedi.")


    def iptalEt(self, randevuNumarasi):
        if self.cancelled:
            return {"success": False, "message": "Randevu zaten iptal edildi."}

        url = (self.BASE_URL + f"kurum/randevu/iptal-et/{randevuNumarasi}")
        response = requests.get(url, headers=self.headers)
        if response.json().get('success'):
            self.cancelled = True  # İptal edildi
        return response.json()

def process_user(user_info, log_directory):
    payload_name = user_info.get("hastaneBilgisi")
    hospital_payload = get_hospital_payload(payload_name)
    jwtToken = Authentication(user_info, hospital_payload, log_directory)

if __name__ == '__main__':
    log_directory = '/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/log'
    users = [

        {"tckn": "33790402648", "password": "Trgtosmn23", "hastaneBilgisi": "testElazig1"},
        {"tckn": "33808402042", "password": "Bahar.23", "hastaneBilgisi": "testElazig1"},
        {"tckn": "14455884436", "password": "Busra111C", "hastaneBilgisi": "testElazig1"},
        {"tckn": "12097654868", "password": "Sahra2019", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    ]
    """
        {'ip': '104.239.108.19', 'port': 6254, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
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
        {'ip': '104.239.108.124', 'port': 6359, 'user': 'AxKN3fd4', 'password': 'AxKN3fd4'},
    """

    for user_info in users:
        process_user(user_info, log_directory)
