import sys

from librstax import invariants_of_year, read_json


if __name__ == '__main__':
    data = read_json(sys.argv[1])
    year = sys.argv[2]

    invariants = invariants_of_year(year)

    for month_idx in data["payrolls"]:
        payroll = data["payrolls"][month_idx]
        result = {
            "success": 0,
            "failed": 0,
            "skip": 0
        }
        report = []
        for invname in invariants:
            inv = invariants[invname]
            checkSkip = lambda x: False
            if len(inv) > 2:
                checkSkip = inv[2]
            
            if checkSkip(payroll):
                result["skip"] += 1
                report.append("\t⏭️  " + invname)
                continue

            actual = inv[0](payroll)
            expected = inv[1](payroll)
            if abs(expected - actual) < 0.011:
                report.append("\t✅ " + invname)
                result["success"] += 1
            else:
                report.append(f"\t❌ {invname}:\n\t\texpected {expected}\n\t\tgot      {actual}\n\t\tdiff={expected-actual}")
                result["failed"] += 1

        report_printable = "\n".join(report)
        if result["failed"] == 0:
            skipped = f""
            if result["skip"] != 0:
                skipped = f""", skipped { result["skip"] }"""
            print(f"""✅ month {month_idx}: success {result["success"]} / {sum(result.values())}{ skipped }""")
        else:
            print(f"""❌ month {month_idx}: success {result["success"]}, failed {result["failed"]}, skipped {result["skip"]}, total {
                sum(result.values())
            }""")
            print(report_printable)
        
