import json
import sys
import copy

from tabulate import tabulate

from librstax import flatten_dict, merge_flat_dicts, enrich_payroll, ppppo_funcs, ppppo_codes, ppppo_columns, read_json

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    payrolls = [flatten_dict(enrich_payroll(data["payrolls"][x])) for x in data["payrolls"]]
    summary = merge_flat_dicts(payrolls, lambda a, b: a + b, 0, 0, skip_keys=["tags"])

    headers = sorted(ppppo_columns.keys())
    expected_p4o = []
    for code in ppppo_funcs:
        row = [code]
        for column in ppppo_funcs[code]:
            val = ppppo_funcs[code][column](summary)
            row.append(f"{val:.0f}")
        expected_p4o.append(row)

    print(tabulate(expected_p4o, headers=headers, tablefmt="rounded_grid", stralign="right"))

    tax_base = sum([
        ppppo_funcs[code]["3.4"](summary)
        - ppppo_funcs[code]["3.5"](summary)
        - ppppo_funcs[code]["3.6"](summary)
        for code in ppppo_funcs])

    print(tabulate([[f"{tax_base:.0f}"]], headers=["tax base"], tablefmt="rounded_grid", stralign="right"))

