# -*- coding: utf-8 -*-
import datetime as dt
import time
import calendar

from kraken.database import db, CRUDMixin
from kraken.extensions import bcrypt


class Grade(CRUDMixin,  db.Model):

    __tablename__ = 'grades'
    grade = db.Column(db.String(1), nullable=True) # Grade [A,B,C,D,E,F]
    snoozes = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Integer, nullable=False) 
    created_at = db.Column(db.DateTime(), nullable=False)
    deleted = db.Column(db.Boolean())

    def __init__(self, start=False, end=False, snoozes=None, deleted=False):
	self.snoozes = snoozes;
	if start and end:
		self.total_time = end - start
		self.set_grade()
        self.created_at = dt.datetime.utcnow()
	self.deleted = deleted

    def set_grade(self):
	snz = self.snoozes
	secs = self.total_time
	if snz == 0 and secs < 60: # wake up first try
		grade = 'A'
	elif snz == 1 and secs < 12 * 60: # 1 snooze and less than 12 minutes
		grade = 'B'	
	elif snz == 2 and secs < 22 * 60: # 2 snooze and less than 22 minutes
		grade = 'C'	
	elif snz >= 3 and snz <= 5 and secs <  60 * 60: # 2 snooze and less than 1 hour
		grade = 'D'	
	else: #Any snoozes more than 5 and more than hour gets an F
		grade = 'F'	
	self.grade = grade

    @property
    def minutes(self):
	    msg = str( ( self.total_time / 60 ) ) + ' Minutes'
	    return msg

    @property
    def motivation(self):
	    if self.grade == 'A':
		    msg = 'You are the best!'
	    elif self.grade == 'B':
		    msg = 'Oh boy! Decent job.'
	    elif self.grade == 'C':
		    msg = 'Well, not bad... Better luck next time.'
	    elif self.grade == 'D':
		    msg = 'Ha, why did you even try?'
	    elif self.grade == 'F':
		    msg = 'You failed. You wish you were cool.'
	    return msg
