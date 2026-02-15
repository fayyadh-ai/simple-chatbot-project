from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
Data=BASE/"data"
Basic_data=Data/"basic"

keys_basic=Basic_data/"keys_basic.json"
responses_basic=Basic_data/"responses_basic.json"

ENCODING="utf-8"