import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time

def get_exchange_rate():
    api_key = "3cdf806fabe8cc052f36f16b"  
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print("API yaniti:", data)

        if "conversion_rates" in data and "TRY" in data["conversion_rates"]:
            return data["conversion_rates"]["TRY"]
        else:
            print("Hata: 'conversion_rates' veya 'TRY' anahtari bulunamadi.")
            return None
    except Exception as e:
        print("Kur verisi alinirken hata olustu:", str(e))
        return None

bucket = "kurverisi"
org = "SeninOrganizasyonAdin"
token = "gUuHipgQXTnDss5QGklJ2vGEzazbP7_qM3XeZdgGfVPU1P8wNjIiSvzK6bzTXKvyrzG9ff9KCISQaHeRa9w0EA=="  
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_to_influx(rate):
    try:
        point = Point("kur").field("usd_try", rate)
        write_api.write(bucket=bucket, org=org, record=point)
        print("Veri InfluxDB'ye yazildi.")
    except Exception as e:
        print("InfluxDB yazma hatasi:", str(e))


while True:
    rate = get_exchange_rate()
    if rate is not None:
        print("USD/TRY:", rate)
        write_to_influx(rate)
    else:
        print("Veri yazilmadi (gecersiz kur verisi).")
    time.sleep(120)  


#gUuHipgQXTnDss5QGklJ2vGEzazbP7_qM3XeZdgGfVPU1P8wNjIiSvzK6bzTXKvyrzG9ff9KCISQaHeRa9w0EA==  yeni
#B9XaMd5YBLN3VEok8fORdnPUV85PoRqhEbtFqjUfnhXAZTuCgXyxyJf0dNiYMB-RwoMtX-JMyRfZYsaqJY7yDA==   eski