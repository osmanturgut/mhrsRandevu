import hashlib
import json

# Veri yapısı
data = {
    "totalItemCount": 0,
    "value": {
        "id": 13442401,
        "isActive": True,
        "firstname": "SELİM",
        "lastname": "ERDİNÇ",
        "email": "SERDINC10@GMAIL.COM",
        "mobilePhone": "+9053******67",
        "userId": 13468947,
        "userName": "SERDINC10@GMAIL.COM",
        "isCorporate": False,
        "haveLoyaltyCard": True,
        "isFirstLogin": False,
        "isAgreement": False,
        "unMaskedMobilePhone": "+905315714367",
        "nationalId": "10415314234"
    },
    "isError": False,
    "resultCode": 0
}

# JSON verisini string'e dönüştür
json_data = json.dumps(data)

# Tarih bilgisini string'e dönüştür
date_string = '11.02.2024-17:44:22'

# Tarih bilgisini ve JSON verisini birleştir
combined_info = date_string + json_data

# Hash algoritmasını kullanarak hash'i hesapla
hashed_code = hashlib.sha256(combined_info.encode()).hexdigest()

print("Oluşturulan kod:", hashed_code)
