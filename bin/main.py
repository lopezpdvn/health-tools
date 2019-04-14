from glob import iglob
from datetime import datetime, timedelta
from pprint import pprint
import json

from timeman import DEFAULT_DATETIME_FMT

FILES_FP_PATTERN = 'data/**/*json'
DATETIME_KEY = 'datetime'

data = []

def get_data(fp_pattern=FILES_FP_PATTERN, recursive=True):
    data = []

    for month in sorted(iglob(fp_pattern, recursive=recursive)):
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

def get_recent_averages(prop_retriever, sample_range):
    return tuple(
        (i, sum(prop_retriever(x) for x in data[-i:]) / i)
        for i in sample_range)

def main_rpt(prop_retriever, sample_range):
    pprint(get_recent_averages(prop_retriever, sample_range))

data = get_data()
