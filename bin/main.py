from glob import iglob
from datetime import datetime, timedelta
from pprint import pprint
import json
import sys

from timeman import DEFAULT_DATETIME_FMT

FILES_FP_PATTERN = 'data/**/*json'
DATETIME_KEY = 'datetime'

data = []

def get_data(fp_pattern=FILES_FP_PATTERN, recursive=True):
    data = []

    for month in sorted(iglob(fp_pattern, recursive=recursive)):
        with open(month) as f:
            try:
                data.extend(json.load(f))
            except json.decoder.JSONDecodeError:
                print(month, file=sys.stderr)
                raise

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
    pprint(tuple(
        (day, '{:.2f}'.format(avg_weight)) for day, avg_weight in
        get_recent_averages(prop_retriever, sample_range)))

def sleep_rpt(take_k=10):
    x = [(str(e['datetime']), e['total_sleep'],
          e['total_sleep'] / e['time_in_bed'])
         for e in data[-take_k:]]
    pprint(x)

data = get_data()
