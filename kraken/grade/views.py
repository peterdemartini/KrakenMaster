# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from kraken.grade.models import Grade
import json
from kraken.helpers.Skynet import Skynet

blueprint = Blueprint("grade", __name__, url_prefix='/grades',
		static_folder="../static")

@blueprint.route("/recent/")
@login_required
def recent():
	grades = Grade.get_recent(100, Grade.created_at);
	return render_template("grades/recent.html", grades = grades)
@blueprint.route("/create/", methods=['POST'])
@login_required
def create():
	newGrade = Grade.create(start=int(request.form['start']),
		end=int(request.form['end']),
		snoozes=int(request.form['snooze_count']))
	return render_template("grades/result.html", grade=newGrade)
@blueprint.route("/api/create", methods=['POST'])
def api_create():
    if 'start' in request.json and 'end' in request.json and 'snooze_count' in request.json:
        newGrade = Grade.create(start=int(request.json['start']),
		    end=int(request.json['end']),
            snoozes=int(request.json['snooze_count']))
    else:
        return json.dumps({'success' : False, 'error' : 'Invalid Request'})
    return json.dumps({'success' : True})
