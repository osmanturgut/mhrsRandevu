import asyncio
from myUserRequests import main
"""
TODO 

"""
users3 = [
    {"tckn": "30541865462", "password": "Sahra2019", "hastaneBilgisi": "bakirkoySadiKonukEAH"},
    {"tckn": "15018076558", "password": "Sahra2019", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "62794468220", "password": "Sahra2019", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "10587224256", "password": "Altinkoza34", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "35083725328", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "26027015902", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "41408195462", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "13043457984", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "16031339590", "password": "Ada123456", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},
    {"tckn": "63529459698", "password": "Altinkoza34", "hastaneBilgisi": "sultanGaziFatihHasekiEAH"},
    {"tckn": "66610356890", "password": "Altinkoza34.", "hastaneBilgisi": "sultanGaziFatihHasekiEAH"},
    {"tckn": "29048608894", "password": "Altinkoza34", "hastaneBilgisi": "sultangaziHasekiEAH"},
    {"tckn": "14816389976", "password": "Ucel1234", "hastaneBilgisi": "gaziosmanpasaEAH"},

]

ip_infos =[

    {'ip': '104.239.108.144', 'port': 6379, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.138', 'port': 6373, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.247', 'port': 6482, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.18', 'port': 6253, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.34', 'port': 6269, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.238', 'port': 6473, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.159', 'port': 6394, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.227', 'port': 6462, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.49', 'port': 6284, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.42', 'port': 6277, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.51', 'port': 6286, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.208', 'port': 6443, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.200', 'port': 6435, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.208', 'port': 6443, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.242', 'port': 6477, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.237', 'port': 6472, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.203', 'port': 6438, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.34', 'port': 6269, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.238', 'port': 6473, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.159', 'port': 6394, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.133', 'port': 6368, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.155', 'port': 6390, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.175', 'port': 6410, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
]

if __name__ == "__main__":
    asyncio.run(main(users3, ip_infos))
  #  log_directory = '/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/log'
