# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from flask import Blueprint, render_template
from flask.ext.login import login_required
from kraken.all_settings.forms import AllSettings
from kraken.all_settings.models import AlarmSetting
from kraken.utils import flash_errors
from kraken.database import db

blueprint = Blueprint("setting", __name__, url_prefix='/settings',
                        static_folder="../static")


@blueprint.route("/", methods=['GET', 'POST'])
@login_required
def all():
    a = AlarmSetting()
    alarm_status = a.get_pair('alarm_status')
    if alarm_status:
        status_val=alarm_status.value
    else:
        status_val=1

    b = AlarmSetting()
    alarm_hours = b.get_pair('alarm_hours')
    if alarm_hours:
        alarm_hrs=alarm_hours.value
    else:
        alarm_hrs=6

    c = AlarmSetting()
    alarm_minutes = c.get_pair('alarm_minutes')
    if alarm_minutes:
        alarm_mins=alarm_minutes.value
    else:
        alarm_mins=0

    form = AllSettings(request.form, alarm_status=status_val, alarm_hours=alarm_hrs,
                            alarm_minutes=alarm_mins, csrf_enabled=False)

    form.alarm_hours.choices=range(0,24)
    for v in form.alarm_hours.choices:
        form.alarm_hours.choices[v] = (str(v), str(v))

        form.alarm_minutes.choices=range(0,60)
    for v in form.alarm_minutes.choices:
        form.alarm_minutes.choices[v] = (str(v), str(v))
    
    if form.validate_on_submit():
        if not alarm_status:
            alarm_status = a.create(name='alarm_status',
                            label='Alarm Status',
                            value=form.alarm_status.data)
        else:
            alarm_status = alarm_status.update(value=form.alarm_status.data)

        if not alarm_hours:
            alarm_hours = b.create(name='alarm_hours',
                            label='Alarm Hours',
                            value=form.alarm_hours.data)
        else:
            alarm_hours = alarm_hours.update(value=form.alarm_hours.data)

        if not alarm_minutes:
            alarm_minutes = c.create(name='alarm_minutes',
                            label='Alarm Minutes',
                            value=form.alarm_minutes.data)
        else:
                    alarm_minutes = alarm_minutes.update(value=form.alarm_minutes.data)

        flash("Settings Saved!", 'success')
        return redirect(url_for('setting.all'))
    else:
        flash_errors(form)
    return render_template("settings/all.html", form=form)
