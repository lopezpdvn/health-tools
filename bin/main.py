from glob import iglob
import json

data = []

for month in sorted(iglob('data/2017/*json')):
    with open(month) as f:
        data.extend(json.load(f))
