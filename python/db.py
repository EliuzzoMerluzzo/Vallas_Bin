import requests
from arduino.app_utils import *
BASE_URL = "http://192.168.23.50:8000/api"

class Bins:
    @staticmethod
    def GetBins():
        try: 
            response = requests.get(f"{BASE_URL}/cestini", timeout=10)
            return response.json()
        except Exception as e:
            print(e)
    @staticmethod
    def GetRecords():
        try: 
            response = requests.get(f"{BASE_URL}/records", timeout=10)
            return response.json()
        except Exception as e:
            print(e)
    @staticmethod
    def GetForecast():
        response = requests.get(f"{BASE_URL}/forecast", timeout=10)
        response.raise_for_status()
        return response.json()

def send_fullness():
    fullness = int(Bridge.call("read_ultrasound")) * 100 / 255
    
    try: 
        response = requests.post(f"{BASE_URL}/registrazioni", json={"idCestino": 1, "capacita": fullness}, timeout=10)

        if response.status_code != 200:
            print(response.json())
    except Exception as e:
        print(e)