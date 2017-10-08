from glob import iglob
import json

FILES_FP_PATTERN = 'data/2017/*json'

data = []

def get_2017_data(fp_pattern=FILES_FP_PATTERN):
    data = []
    for month in sorted(iglob('data/2017/*json')):
        with open(month) as f:
            data.extend(json.load(f))
    return data

def get_average(prop, ndays):
    return sum(x[prop] for x in data[-ndays:]) / ndays

data = get_2017_data()
