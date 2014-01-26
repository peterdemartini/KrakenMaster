# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from kraken.database import db, CRUDMixin
from kraken.extensions import bcrypt


class User(UserMixin, CRUDMixin,  db.Model):

    __tablename__ = 'users'
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # The hashed password
    created_at = db.Column(db.DateTime(), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())
   # grades = db.relationship('Grade', backref='grade', lazy='dynamic')

    def __init__(self, username=None, email=None, password=None,
                first_name=None, last_name=None,
                 active=False, is_admin=False):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
        self.active = active
        self.is_admin = is_admin
        self.created_at = dt.datetime.utcnow()
        self.first_name = first_name
        self.last_name = last_name

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User "{username}">'.format(username=self.username)
