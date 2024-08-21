import asyncio
from myUserRequests import main
"""
    {"tckn": "31540279540", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "24485738944", "password": "Ucel5432", "hastaneBilgisi": "gaziosmanpasaEAH"},
    {"tckn": "47392303494", "password": "Ucel5432", "hastaneBilgisi": "gaziosmanpasaEAH"},
    {"tckn": "17837318390", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "36217675748", "password": "Ucel1234", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},

"""
users = [

    {"tckn": "12097654868", "password": "Sahra2019", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
   # {"tckn": "48991942770", "password": "Ada123456", "hastaneBilgisi": "gaziosmanpasaEAH"},
    {"tckn": "33767450016", "password": "İkizler34", "hastaneBilgisi": "buyukCekmeceMimarSinanDevletHast"},

]

ip_infos =[
    {'ip': '104.239.108.33', 'port': 6268, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.244', 'port': 6479, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.124', 'port': 6359, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.202', 'port': 6437, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.207', 'port': 6442, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.81', 'port': 6316, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.91', 'port': 6326, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.26', 'port': 6261, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.92', 'port': 6327, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.143', 'port': 6378, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.5', 'port': 6240, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.209', 'port': 6444, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.19', 'port': 6254, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.149', 'port': 6384, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.77', 'port': 6312, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.178', 'port': 6413, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.177', 'port': 6412, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},
    {'ip': '104.239.108.94', 'port': 6329, 'user': 'hrhsxjqr', 'password': 'gr9p1s6mvw2v'},


]

if __name__ == "__main__":
    asyncio.run(main(users, ip_infos))
    log_directory = '/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/log'
