from glob import iglob
from datetime import datetime, timedelta
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

def get_average_from_now(prop_retriever, ndays):
    start = datetime.today() - timedelta(days=ndays)
    range_samples = list(
            prop_retriever(x) for x in data if x[DATETIME_KEY] >= start)
    nrange_samples = len(range_samples)
    return (sum(range_samples) / nrange_samples, nrange_samples)

def get_average_from_then(prop_retriever, start):
    start = datetime.strptime(start, DEFAULT_DATETIME_FMT)
    range_samples = list(
            prop_retriever(x) for x in data if x[DATETIME_KEY] >= start)
    nrange_samples = len(range_samples)
    return (sum(range_samples) / nrange_samples, nrange_samples)

data = get_2017_data()
