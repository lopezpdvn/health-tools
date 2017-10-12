from glob import iglob
from datetime import datetime
import json

from timeman import DEFAULT_DATETIME_FMT

FILES_FP_PATTERN = 'data/2017/*json'
DATETIME_KEY = 'datetime'

data = []

def get_2017_data(fp_pattern=FILES_FP_PATTERN):
    data = []
    for month in sorted(iglob(fp_pattern)):
        with open(month) as f:
            data.extend(json.load(f))
    for x in data:
        x[DATETIME_KEY] = datetime.strptime(x[DATETIME_KEY],
                DEFAULT_DATETIME_FMT)
    return data

def get_average(prop, ndays):
    return sum(x[prop] for x in data[-ndays:]) / ndays

data = get_2017_data()
