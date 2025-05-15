# Yardımcı fonksiyon: String formatındaki veriyi dict formatına dönüştürme
def convert_to_dict(entry):
    if isinstance(entry, str):  # Eğer stringse
        entries = entry.split(":")
        if len(entries) == 4:
            ip, port, user, password = entries
            return {'ip': ip.strip(), 'port': int(port), 'user': user.strip(), 'password': password.strip()}
    elif isinstance(entry, dict):  # Eğer dict formatında ise direkt döndürelim
        return entry
    return {}

# list1'deki veriyi uygun formata çevirmek
list1 = [
    """
    104.239.108.42:6277:mbxkenmx:iaulboo6lqri
104.239.108.208:6443:mbxkenmx:iaulboo6lqri
104.239.108.203:6438:mbxkenmx:iaulboo6lqri
104.239.108.51:6286:mbxkenmx:iaulboo6lqri
104.239.108.159:6394:mbxkenmx:iaulboo6lqri
104.239.108.51:6286:otosqucj:y0b6ko53xy1t
104.239.108.159:6394:otosqucj:y0b6ko53xy1t
104.239.108.138:6373:otosqucj:y0b6ko53xy1t
104.239.108.247:6482:otosqucj:y0b6ko53xy1t
104.239.108.18:6253:otosqucj:y0b6ko53xy1t
104.239.108.138:6373:mbxkenmx:iaulboo6lqr
104.239.108.159:6394:mbxkenmx:iaulboo6lqrii
104.239.108.42:6277:mbxkenmx:iaulboo6lqri
104.239.108.208:6443:mbxkenmx:iaulboo6lqri
104.239.108.203:6438:mbxkenmx:iaulboo6lqri
104.239.108.9:6244:mbxkenmx:iaulboo6lqri
104.239.108.192:6427:mbxkenmx:iaulboo6lqri
104.239.108.29:6264:mbxkenmx:iaulboo6lqri
104.239.108.89:6324:mbxkenmx:iaulboo6lqri
104.239.108.105:6340:mbxkenmx:iaulboo6lqri

    """
    ,


]

list2 = [
    {'ip': '104.239.108.42', 'port': 6277, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.208', 'port': 6443, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.203', 'port': 6438, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.51', 'port': 6286, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.159', 'port': 6394, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.51', 'port': 6286, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.159', 'port': 6394, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.138', 'port': 6373, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.247', 'port': 6482, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.18', 'port': 6253, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.144', 'port': 6379, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.208', 'port': 6443, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.227', 'port': 6462, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.238', 'port': 6473, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.237', 'port': 6472, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.49', 'port': 6284, 'user': 'mbxkenmx', 'password': 'iaulboo6lqri'},
    {'ip': '104.239.108.34', 'port': 6269, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.200', 'port': 6435, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.242', 'port': 6477, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.237', 'port': 6472, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.238', 'port': 6473, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.133', 'port': 6368, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.227', 'port': 6462, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.155', 'port': 6390, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'},
    {'ip': '104.239.108.175', 'port': 6410, 'user': 'wjuxh3ZK', 'password': 'r4197bqezuc9'}

]

# Cevirilmis list1
cevrilmis_list = []

# list1'deki her öğeyi uygun dict formatına dönüştürme
for entry in list1:
    if isinstance(entry, str):
        entries = entry.split("\n")  # Her satırı ayırma
        for item in entries:
            item = item.strip()  # Satırdaki gereksiz boşlukları temizle
            if item:  # Boş satırları atla
                dict_entry = convert_to_dict(item)
                if dict_entry:  # Boş olmayan öğeleri ekleyelim
                    cevrilmis_list.append(dict_entry)
    else:
        dict_entry = convert_to_dict(entry)
        if dict_entry:  # Boş olmayan öğeleri ekleyelim
            cevrilmis_list.append(dict_entry)

# Cevirilmis list'i ekrana yazdırma
print("Cevirilmis_list:")
for item in cevrilmis_list:
    print(item)
# Verileri karşılaştırma
equal = [entry for entry in cevrilmis_list if entry in list2]
different = [entry for entry in cevrilmis_list if entry not in list2] + [entry for entry in list2 if entry not in cevrilmis_list]

# Sonuçları yazdırma
print(f"Eşit Olanlar ({len(equal)}):")
for item in equal:
    print(item ,",")

print(f"\nFarklı Olanlar ({len(different)}):")
for item in different:
    print(item ,",")

# Toplamda kaç öğe var
total = len(equal) + len(different)
print(f"\nToplam ({total}):")
for item in equal + different:
    print(item ,",")
