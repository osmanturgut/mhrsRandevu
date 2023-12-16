import requests
from bs4 import BeautifulSoup

def get_ip_list():
    response = requests.get("https://www.freeproxy.world/?country=TR")
    soup = BeautifulSoup(response.content, "html.parser")

    ip_elements = soup.find_all("td", class_="show-ip-div")
    port_links = soup.find_all("a", href=lambda href: href and "/?port=" in href)

    ip_list = []

    for ip_element, port_link in zip(ip_elements, port_links):
        ip_address = ip_element.get_text(strip=True)
        port = port_link.get_text(strip=True)
        ip_and_port = f"{ip_address}:{port}"
        ip_list.append(ip_and_port)

    return ip_list

# IP listesini ekrana yazdır
ip_list = get_ip_list()
#for ip in ip_list:
    #print(ip)
