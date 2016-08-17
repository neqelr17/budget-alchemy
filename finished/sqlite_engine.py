#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Remove and create a dev database.

Contains dev engine.
Main will remove test db and create new one with any updates in models.py
"""

import errno
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import BASE, User, BudgetGroup, Budget, Transaction, Item


__author__ = 'Brett R. Ward'

# Constants
DB_NAME = 'budget.db'
TEST_DATA = 'test_data.json'

# Create ENGINE
ENGINE = create_engine('sqlite:///{}'.format(DB_NAME))

# Create SESSION
SESSION = sessionmaker(bind=ENGINE)


def main():
    """Delete test sqlite db and create new one with.

    This is only for dev! This just makes it easy to remove
    and create a new test db.
    """
    # Remove old db
    remove_test_db(DB_NAME)

    print('Creating Tables')
    BASE.metadata.create_all(ENGINE, checkfirst=True)
    print('Success!')

    # Open up test data json and load data to database.
    if len(sys.argv) < 2:
        insert_test_data()


def insert_test_data():
    """Insert Data into test database."""
    with open(TEST_DATA, 'r') as fh_users:
        data = json.load(fh_users)
    with session_scope() as session:
        add_users(data, session)
        add_budgets(data, session)


def add_budgets(data, session):
    """Add budgets from json file.

    Used for development to import test data to database.
    """
    # Add Groups
    for group in data['groups']:
        budget_group = BudgetGroup(name=group['name'])
        for budget in group['budgets']:
            temp_budget = Budget(name=budget['name'])
            temp_budget.budget_amount = budget['amount']
            temp_budget.budget_group = budget_group
            session.add(temp_budget)

    # Add Transactions
    for tran in data['transactions']:
        transaction = Transaction(
            name=tran['name'],
            date=datetime.strptime(tran['date'], '%Y-%m-%d %H:%M:%S.%f'))
        transaction.user = session.query(User).filter_by(
            user_name=tran['user']).one()
        for item in tran['items']:
            temp_item = Item(name=item['name'])
            temp_item.amount = item['amount']
            temp_item.budget = session.query(Budget).filter_by(
                name=item['budget']).one()
            temp_item.transaction = transaction
            session.add(temp_item)


def add_users(data, session):
    """Add users from json file.

    Used for development to import test data to database.
    """
    for user in data['users']:
        session.add(User(
            user_name=user['user_name'],
            first_name=user['first_name'],
            middle_name=user['middle_name'],
            last_name=user['last_name'],
            password=user['password']
        ))


def remove_test_db(filename):
    """Quietly removes the database file if it exists."""
    try:
        os.remove(filename)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise
    else:
        print('Old database file removed.')


@contextmanager
def session_scope():
    """Provide a transactional scope for a series of database interactions.

    Used to automatically handle the commiting and rollback on errors.
    """
    session = SESSION()
    try:
        yield session
        session.commit()
    except Exception as exc:
        print(exc)
        session.rollback()
        raise exc
    finally:
        session.close()


if __name__ == "__main__":
    main()
