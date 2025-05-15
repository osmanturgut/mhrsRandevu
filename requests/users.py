import asyncio
from myUserRequests import main

"""
TODO 

"""
users = [
    {"tckn": "15018076558", "password": "Sahra2019", "hastaneBilgisi": "bakirkoySadiKonukEAH"},
    {"tckn": "62794468220", "password": "Sahra2019", "hastaneBilgisi": "sisliCemilTasciogluSehirHast"},

]

ip_infos = [
    {'ip': '104.239.108.29', 'port': 6264, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.89', 'port': 6324, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.105', 'port': 6340, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.183', 'port': 6418, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.42', 'port': 6277, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.242', 'port': 6477, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.203', 'port': 6438, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.34', 'port': 6269, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.133', 'port': 6368, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.175', 'port': 6410, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.18', 'port': 6253, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.144', 'port': 6379, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.138', 'port': 6373, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.247', 'port': 6482, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.208', 'port': 6443, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.155', 'port': 6390, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.51', 'port': 6286, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.159', 'port': 6394, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.200', 'port': 6435, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.238', 'port': 6473, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.237', 'port': 6472, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.227', 'port': 6462, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.49', 'port': 6284, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.99', 'port': 6334, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.12', 'port': 6247, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.54', 'port': 6289, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.193', 'port': 6428, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.174', 'port': 6409, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.142', 'port': 6377, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.160', 'port': 6395, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.212', 'port': 6447, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.9', 'port': 6244, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.192', 'port': 6427, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},

]

if __name__ == "__main__":
    asyncio.run(main(users, ip_infos))
#  log_directory =