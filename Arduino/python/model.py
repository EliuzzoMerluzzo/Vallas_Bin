from arduino.app_bricks.llm import LargeLanguageModel
from db import Bins
import json
_model = LargeLanguageModel()


PROMPT = """You predict when smart waste bins will be full.

You receive a list of bins. Each has:
- "id" and "zona"
- "capacita": current fill level in percent (0-100)
- "fill_last_24h": how many percentage points the bin filled in the last 24 hours

For each bin:
1. rate = fill_last_24h / 24 (percent per hour)
2. hours_to_full = (100 - capacita) / rate
3. If rate is 0, hours_to_full is null.
4. If capacita is 100, hours_to_full is 0.

Sort the bins by hours_to_full, smallest first, with null at the end.
Round hours_to_full to 1 decimal.

Reply with ONLY a JSON array, with no other text, no explanations and no code fences:
[{"id": <id>, "hours_to_full": <number or null>}]

Use only the data provided."""

class UsageAnalysis:
    @staticmethod
    def GetPredictions():
        dati = Bins.GetForecast()
        print( _model.chat(PROMPT + "\n\nDATA:\n" + json.dumps(dati)))


        
        

