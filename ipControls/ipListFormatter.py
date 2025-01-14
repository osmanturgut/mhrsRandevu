# Define the given IP strings
ip_strings = [
    "104.239.108.34:6269:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.133:6368:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.155:6390:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.247:6482:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.107:6342:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.138:6373:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.51:6286:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.159:6394:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.208:6443:wjuxh3ZK:r4197bqezuc9",
    "104.239.108.203:6438:wjuxh3ZK:r4197bqezuc9",
]

# Convert to the desired dictionary format
formatted_ips = [
    {
        "ip": ip.split(":")[0],
        "port": int(ip.split(":")[1]),
        "user": ip.split(":")[2],
        "password": ip.split(":")[3],
    }
    for ip in ip_strings
]

# Print each dictionary with a comma at the end
for ip_data in formatted_ips:
    print(f"{ip_data},")
