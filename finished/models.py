#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""SQLalchemy models for budget application.

This is the database interaction model. To interact with the database,
create an engine to specify the database that can use these models.
"""

import datetime
from hashlib import sha1, sha256


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Sequence
from sqlalchemy.types import DateTime, Integer, String


__author__ = 'Brett R. Ward'


# Constants
ENCODING = 'utf-8'

# Create base for model objects to inherit.
BASE = declarative_base()


class User(BASE):
    """A user represents a person that interfaces with the database."""

    __tablename__ = 'users'

    # Columns
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    user_name = Column(String(64), unique=True, nullable=False)
    first_name = Column(String(64))
    middle_name = Column(String(64))
    last_name = Column(String(64))
    created = Column(DateTime)
    salt = Column(String(40))
    password = Column(String(64))

    def __init__(self, *args, **kwargs):
        """Set created time on new objects."""
        super().__init__(*args, **kwargs)
        self.created = datetime.datetime.utcnow()
        self.salt = self.create_salt()
        self.password = self.get_password(self.password)

    # Relationships
    transactions = relationship(
        'Transaction', order_by='desc(Transaction.date)', backref='user')

    def __str__(self):
        """Print User pretty when called as a string."""
        return '<User(user_name={}, first_name={}, created={})>'.format(
            self.user_name,
            self.first_name,
            self.created)

    def __repr__(self):
        """Print User pretty when called in python repl."""
        return self.__str__()

    @staticmethod
    def create_salt():
        """Create a new salt value."""
        return sha1(
            str(datetime.datetime.utcnow()).encode(ENCODING)).hexdigest()

    def get_password(self, password):
        """Return hashed password."""
        temp = '{}{}'.format(self.salt, password)
        return sha256(temp.encode(ENCODING)).hexdigest()


class BudgetGroup(BASE):
    """A budget group is a collection of budgets.

    Used for reporting by category.
    """

    __tablename__ = 'budget_groups'

    # Columns
    id = Column(Integer, Sequence('budget_groups_id'), primary_key=True)
    name = Column(String(64), nullable=False)

    # Relationships
    budgets = relationship(
        'Budget', order_by='asc(Budget.id)', backref='budget_group')

    def __str__(self):
        """Print BudgetGroup pretty when called as a string."""
        return 'BudgetGroup<id={}, name={}>'.format(self.id, self.name)

    def __repr__(self):
        """Print BudgetGroup pretty when called in python repl."""
        return self.__str__()


class Budget(BASE):
    """Itemization's are categorized in budgets."""

    __tablename__ = 'budgets'

    # Columns
    id = Column(Integer, Sequence('budget_id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('budget_groups.id'))
    name = Column(String(64), nullable=False)
    budget_amount_in_cents = Column(Integer)

    # Relationships
    items = relationship('Item', order_by='asc(Item.id)', backref='budget')

    def __str__(self):
        """Print Budget pretty when called as a string."""
        return 'Budget<id={}, name={}, group={}>'.format(
            self.id,
            self.name,
            self.budget_group.name)

    def __repr__(self):
        """Print Budget pretty when called in python repl."""
        return self.__str__()

    @property
    def budget_amount(self):
        """Return dollar budget_amount."""
        return self.budget_amount_in_cents / 100

    @budget_amount.setter
    def budget_amount(self, budget_amount):
        """Set amount_in_cents from a dollar budget_amount."""
        self.budget_amount_in_cents = float(budget_amount) * 100


class Transaction(BASE):
    """A transaction that can be related to a physical receipt or bank account.

    Each transaction will contain at least one itemization that will tie it to
    a budget.
    """

    __tablename__ = 'transactions'

    # Columns
    id = Column(Integer, Sequence('transaction_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(64), nullable=False)
    date = Column(DateTime)

    # Relationships
    items = relationship(
        'Item', order_by='asc(Item.id)', backref='transaction')

    def __str__(self):
        """Print Transaction pretty when called as a string."""
        return 'Transaction<id={}, name={}>'.format(
            self.id,
            self.name
            )

    def __repr__(self):
        """Print Transaction pretty when called in python repl."""
        return self.__str__()


class Item(BASE):
    """Item is an itemization of a transaction tied to a Budget."""

    __tablename__ = 'itemizations'

    # Columns
    id = Column(Integer, Sequence('item_id'), primary_key=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'))
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    name = Column(String(64), nullable=False)
    amount_in_cents = Column(Integer)

    def __str__(self):
        """Print Item pretty when called as a string."""
        return 'Item<id={}, name={}, amount=${:.2f}>'.format(
            self.id,
            self.name,
            self.amount
            )

    def __repr__(self):
        """Print Item pretty when called in python repl."""
        return self.__str__()

    @property
    def amount(self):
        """Return dollar amount."""
        return self.amount_in_cents / 100

    @amount.setter
    def amount(self, amount):
        """Set amount_in_cents from a dollar amount."""
        self.amount_in_cents = float(amount) * 100
