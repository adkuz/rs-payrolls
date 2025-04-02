import json
import functools


def read_json(filename: str):
    data = {}
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def flatten_dict(d, parent_key='', sep='/'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def merge_flat_dicts(dicts, reducer, initial=None, default=None):
    all_keys = set().union(*dicts)  # Collect all unique keys from the dictionaries
    merged = {}

    for key in all_keys:
        values = [d.get(key, default) for d in dicts]
        merged[key] = functools.reduce(reducer, values, initial)

    return merged