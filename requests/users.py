import asyncio
from myUserRequests import main

users = [
    {"tckn": "36712688472", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "23714784400", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "37396637510", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
]

ip_infos = [
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
]

if __name__ == "__main__":
    asyncio.run(main(users, ip_infos))
