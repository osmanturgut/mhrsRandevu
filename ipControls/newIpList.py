# İlk verilen IP listesi
ip_list1 = [
    {"ip": "216.173.84.104", "port": 6019, "user": "uenbwoqj", "password": "1ix92sa4tdh1"},
    {"ip": "104.239.108.241", "port": 6476, "user": "uenbwoqj", "password": "1ix92sa4tdh1"},
    {"ip": "216.173.84.17", "port": 5932, "user": "uenbwoqj", "password": "1ix92sa4tdh1"},
    {"ip": "104.239.108.139", "port": 6374, "user": "uenbwoqj", "password": "1ix92sa4tdh1"},
    {"ip": "216.19.205.113", "port": 6434, "user": "uenbwoqj", "password": "1ix92sa4tdh1"},
    {"ip": "216.173.84.191", "port": 6106, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.134.215", "port": 5911, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.173.84.153", "port": 6068, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "206.41.168.102", "port": 6767, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.92", "port": 6327, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "206.41.168.250", "port": 6915, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.19.205.232", "port": 6553, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.129.188", "port": 6176, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.209", "port": 6444, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.19.205.18", "port": 6339, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.173.84.136", "port": 6051, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.129.240", "port": 6228, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.202", "port": 6437, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.129.206", "port": 6194, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.207", "port": 6442, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.33", "port": 6268, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "206.41.168.254", "port": 6919, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.173.84.63", "port": 5978, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.91", "port": 6326, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "104.239.108.26", "port": 6261, "user": "iokycxec", "password": "e80lfjzqkbal"}
]

# İkinci verilen IP listesi
ip_list2 = [
    {"ip": "209.99.134.215", "port": 5911, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "206.41.168.102", "port": 6767, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "206.41.168.250", "port": 6915, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.19.205.232", "port": 6553, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.129.188", "port": 6176, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.19.205.18", "port": 6339, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.129.240", "port": 6228, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "209.99.129.206", "port": 6194, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "206.41.168.254", "port": 6919, "user": "iokycxec", "password": "e80lfjzqkbal"},
    {"ip": "216.19.205.113", "port": 6434, "user": "uenbwoqj", "password": "1ix92sa4tdh1"},
    # Diğer IP adresleri buraya eklenecek
]

# İki listeden ortak elemanları çıkar
result_list = [ip for ip in ip_list1 if ip not in ip_list2]

# Sonucu ekrana yazdır
for ip in result_list:
    print(ip, end=",\n")
