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

    def __init__(self, **kwds):
        """Set created time on new objects."""
        super().__init__(**kwds)
        self.created = datetime.datetime.utcnow()
        self.salt = self.create_salt()
        self.password = self.get_password(self.password)

    # Relationships
    # transactions = relationship(
    #     'Transaction', order_by='desc(Transaction.date)', backref='user')

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
