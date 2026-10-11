import requests
from arduino.app_utils import *
BASE_URL = "http://192.168.23.50:8000/api"

class Bins:
    @staticmethod
    def GetBins():
        try: 
            response = requests.get("/cestini", timeout=10)
            return response.json()
        except Exception as e:
            print(e)
    @staticmethod
    def GetRecords():
        try: 
            response = requests.get("http://192.168.23.50:8000/api/registrazioni", timeout=10)
            return response.json()
        except Exception as e:
            print(e)


def send_fullness():
    fullness = int(Bridge.call("read_ultrasound")) * 100 / 255
    
    try: 
        response = requests.post("http://192.168.23.50:8000/api/registrazioni", json={"idCestino": 1, "capacita": fullness}, timeout=10)

        if response.status_code != 200:
            print(response.json())
    except Exception as e:
        print(e)