#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""List out the budgets in the database.

List budgets with the budgeted amount and current totals.
"""

# import sys


# import 3rd pary


from sqlite_engine import session_scope
from models import User, BudgetGroup, Budget, Transaction, Item


__author__ = 'Brett R. Ward'

# Constants


def main():
    """Create budget report.

    Get budgets and print them out to a report.
    """
    report_dict = {}
    with session_scope() as session:
        for user in session.query(User):
            report_dict[user.user_name] = {}
            for tran in user.transactions:
                for item in tran.items:
                    if item.budget.budget_group.name in report_dict[user.user_name]:
                        report_dict[user.user_name][item.budget.budget_group.name] += item.amount_in_cents
                    else:
                        report_dict[user.user_name][item.budget.budget_group.name] = item.amount_in_cents

    for user in report_dict.items():
        print(user)


if __name__ == "__main__":
    main()
