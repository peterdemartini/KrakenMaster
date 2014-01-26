# -*- coding: utf-8 -*-
import datetime as dt

from kraken.database import db, CRUDMixin
from kraken.extensions import bcrypt


class AlarmSetting(CRUDMixin,  db.Model):

    __tablename__ = 'settings'
    name = db.Column(db.String(80), unique=True, nullable=False)
    label = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name=None, label=None, value=None):
        self.name = name
        self.value = value
        self.label = label

    def get_pair(self, name=None):
        if name:
            return self.query.filter_by(name=name).first()	
        return None
