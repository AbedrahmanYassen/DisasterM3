import requests
import json
from pathlib import Path

# Create output folder
output_dir = Path("monitrs_sample")
output_dir.mkdir(exist_ok=True)

url = (
    "https://datasets-server.huggingface.co/rows"
    "?dataset=ShreelekhaR%2FMONITRS"
    "&config=default"
    "&split=test"
    "&offset=0"
    "&length=100"
)

response = requests.get(url)
response.raise_for_status()

data = response.json()

rows = [item["row"] for item in data["rows"]]

output_file = output_dir / "monitrs_test_first_100.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"Saved {len(rows)} samples to {output_file}")