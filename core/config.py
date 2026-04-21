from pathlib import Path

BASE=Path(__file__).resolve().parent.parent

Data=BASE/"data"

Basic_data=Data/"basic"
Film_data=Data/"film"

keys_basic=Basic_data/"keys_basic.json"
responses_basic=Basic_data/"responses_basic.json"

keys_film=Film_data/"keys_film.json"
list_film=Film_data/"list_film.json"
responses_film=Film_data/"response_film.json"

ENCODING="utf-8"