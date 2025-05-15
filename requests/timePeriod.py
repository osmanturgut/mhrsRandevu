import asyncio
from userStartTime import dateTime
users3 = [
    {"tckn": "33790402648", "password": "Trgtosmn23", "hastaneBilgisi": "HaydarpasaNumuneHastDahiliyeYeldegirmeni"},

]

ip_infos = [
    {'ip': '104.239.108.238', 'port': 6473, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.18', 'port': 6253, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.159', 'port': 6394, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.144', 'port': 6379, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.154', 'port': 6389, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.247', 'port': 6482, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.237', 'port': 6472, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.227', 'port': 6462, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.49', 'port': 6284, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.208', 'port': 6443, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
]



if __name__ == "__main__":
    asyncio.run(dateTime(users3, ip_infos))