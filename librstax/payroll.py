import copy
import functools

from .numbers import round_percent
from .consts import CONSTS as constants

def enrich_payroll(payroll):
    result = copy.deepcopy(payroll)
    result["Tax on transportation (sum)"] = sum(result["Tax on transportation"].values()) 
    return result

def invariants_of_year(year: int):
    year = str(year)
    if year not in constants:
        raise Exception(f"no invariants for the year {year}")
    
    base_for_contributions = lambda payroll: min(payroll["Base for contributions"], payroll["Total gross salary"])
    
    return {
        "Total gross salary": (
            lambda payroll: payroll["Total gross salary"],
            lambda payroll: sum(payroll["Wage type"].values()),
        ),
        "Base for contributions": (
            lambda payroll: payroll["Base for contributions"],
            lambda _: constants[year]["Base for contributions"],
        ),
        "Pension insurance EE": (
            lambda payroll: payroll["Employee contributions"]["Pension insurance EE"],
            lambda payroll: round_percent(14.0, base_for_contributions(payroll)),
        ),
        "Health insurance EE": (
            lambda payroll: payroll["Employee contributions"]["Health insurance EE"],
            lambda payroll: round_percent(5.15, base_for_contributions(payroll)),
        ),
        "Unemployment insurance EE": (
            lambda payroll: payroll["Employee contributions"]["Unemployment insurance EE"],
            lambda payroll: round_percent(0.75, base_for_contributions(payroll)),
        ),
        "Total employee contributions": (
            lambda payroll: payroll["Total employee contributions"],
            lambda payroll: sum(payroll["Employee contributions"].values()),
        ),
        "Non-taxable amount": (
            lambda payroll: payroll["Tax calculation"]["Non-taxable amount"],
            lambda _: constants[year]["Non-taxable amount"],
        ),
        "Base for tax calculation": (
            lambda payroll: payroll["Tax calculation"]["Base for tax calculation"],
            lambda payroll: payroll["Total gross salary"] - 
                payroll["Tax calculation"]["Non-taxable amount"],
        ),
        "PIT": (
            lambda payroll: payroll["Tax calculation"]["PIT"],
            lambda payroll: round_percent(10.00, payroll["Tax calculation"]["Base for tax calculation"]),
        ),
        "Net salary with benefits": (
            lambda payroll: payroll.get("Net salary with benefits", 0),
            lambda payroll: payroll["Total gross salary"] 
                - payroll["Total employee contributions"] 
                - payroll["Tax calculation"]["PIT"],
            lambda payroll: "Net salary with benefits" not in payroll #skip condition
        ),
        "Net benefits": (
            lambda payroll: payroll.get("Net benefits", 0),
            lambda payroll: round_percent(90.00, 
                functools.reduce(
                    lambda a, b: a + payroll["Wage type"][b],
                    filter(lambda key: int(key.split(' ')[0]) >=600, payroll["Wage type"].keys()),
                    0
                )),
        ),
        "Net salary": (
            lambda payroll: payroll["Net salary"],
            lambda payroll: payroll.get("Net salary with benefits", 0) - payroll.get("Net benefits", 0),
            lambda payroll: "Net salary with benefits" not in payroll #skip condition
        ),
        "Total compensation": (
            lambda payroll: payroll.get("Total compensation", 0),
            lambda payroll: sum(payroll.get("Compensation of costs and other personal income", {}).values())
        ),
        "Total deductions": (
            lambda payroll: payroll.get("Total deductions", 0),
            lambda payroll: sum(payroll.get("Deductions", {}).values()),
        ),
        "Net salary for payment": (
            lambda payroll: payroll.get("Net salary for payment", 0),
            lambda payroll: payroll["Net salary"] + payroll.get("Total compensation", 0) + payroll.get("Total deductions", 0)
        ),
        "Pension insurance ER": (
            lambda payroll: payroll["Employer contributions"]["Pension insurance ER"],
            lambda payroll: round_percent(10.00, base_for_contributions(payroll)),
        ),
        "Health insurance ER": (
            lambda payroll: payroll["Employer contributions"]["Health insurance ER"],
            lambda payroll: round_percent(5.15, base_for_contributions(payroll)),
        ),
        "Total employer contributions": (
            lambda payroll: payroll["Total employer contributions"],
            lambda payroll: sum(payroll["Employer contributions"].values())
        ),
        "Tax on transportation/Commute allowance taxable": (
            lambda payroll: round_percent(100, 1/9 * payroll.get("Compensation of costs and other personal income", {}).get("801 Commute allowance taxable", 0)),
            lambda payroll: payroll.get("Tax on transportation", {}).get("Commute allowance taxable", 0),
        ),
    }