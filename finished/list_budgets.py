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
    with session_scope() as session:
        budgets = session.query(Budget)
        header = '""\t'
        budget_amounts = '"Budgeted"\t'
        total_spent = '"Total Spent"\t'
        for budget in budgets:
            header += '"{}"\t'.format(budget.name)
            budget_amounts += '"${:.2f}"\t'.format(budget.budget_amount)
            amount = 0
            for item in budget.items:
                amount += item.amount_in_cents
            total_spent += '"${:.2f}"\t'.format(amount / 100)
        print(header)
        print(budget_amounts)
        print(total_spent)


if __name__ == "__main__":
    main()
