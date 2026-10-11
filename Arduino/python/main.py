from arduino.app_utils import App, Bridge
from db import Bins
import time
from model import UsageAnalysis

angle: int = 0

# def loop():
#     global angle
#     Bridge.call("servo", 90, angle)
#     time.sleep(0.5)
#     angle += 10
    

# send_fullness()
# Bins.GetBins()
# print(Bins.GetRecords())
UsageAnalysis.GetPredictions()
# App.run(user_loop=loop)
App.run()