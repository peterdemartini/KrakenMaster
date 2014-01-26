# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from flask import Blueprint, render_template
from flask.ext.login import login_required
from kraken.all_settings.forms import AllSettings
from kraken.all_settings.models import AlarmSetting # this is include in Skynet
from kraken.utils import flash_errors
from kraken.database import db
import json

blueprint = Blueprint("setting", __name__, url_prefix='/settings',
                        static_folder="../static")


@blueprint.route("/", methods=['GET', 'POST'])
@login_required
def all():
    fields = [{'field': 'alarm_status', 'label' : 'Alarm Status', 'default' : 1},
                {'field': 'alarm_minutes', 'label' : 'Alarm Minutes', 'default' : 0},
                {'field': 'alarm_hours', 'label' : 'Alarm Hours', 'default' : 6},
                {'field': 'snooze_minutes', 'label' : 'Snooze Minutes', 'default' : 10},
                {'field': 'alarm_text', 'label' : 'Alarm Text', 'default' : 'ALARM!'}]
    settings = []
    default = {} 
    for field in fields:
        setting = field
        setting['model'] = AlarmSetting()
        setting['data'] = setting['model'].get_pair(setting['field'])
        if setting['data']:
            setting['default'] = setting['data'].value
        default[setting['field']] = setting['default']
        settings.append(setting)

    form = AllSettings(request.form, alarm_status=default['alarm_status'], alarm_hours=default['alarm_hours'],
                            snooze_minutes=default['snooze_minutes'], alarm_text=default['alarm_text'],
                            alarm_minutes=default['alarm_minutes'], csrf_enabled=False)

    form.alarm_hours.choices=range(0,24)
    for v in form.alarm_hours.choices:
        form.alarm_hours.choices[v] = (str(v), str(v))
    
    form.alarm_minutes.choices=range(0,60)
    for v in form.alarm_minutes.choices:
        form.alarm_minutes.choices[v] = (str(v), str(v))

    form.snooze_minutes.choices=range(0,60)
    for v in form.snooze_minutes.choices:
        form.snooze_minutes.choices[v] = (str(v), str(v))
    
    if form.validate_on_submit():
        for setting in settings:
            if not setting['data']:
                setting['data'] = setting['model'].create(name=setting['field'],
                                    label=setting['label'],
                                    value=form[setting['field']].data)
            else:
                setting['data'] = setting['data'].update(value=form[setting['field']].data)

        from kraken.helpers.Skynet import Skynet
        skynet = Skynet()
        devices = skynet.search_devices({'name' : 'KrakenAlarm'});
        if devices:
            skynet.send_message(devices, { 'request' : 'update_settings' })
        flash("Settings Saved!", 'success')
        return redirect(url_for('setting.all'))
    else:
        flash_errors(form)
    return render_template("settings/all.html", form=form)

@blueprint.route("/api/retrieve", methods=['GET'])
def get():
    fields = [{'field': 'alarm_status', 'label' : 'Alarm Status', 'value' : 1},
                {'field': 'alarm_minutes', 'label' : 'Alarm Minutes', 'value' : 0},
                {'field': 'alarm_hours', 'label' : 'Alarm Hours', 'value' : 6},
                {'field': 'snooze_minutes', 'label' : 'Snooze Minutes', 'value' : 10},
                {'field': 'alarm_text', 'label' : 'Alarm Text', 'value' : 'ALARM!'}]
    settings = {}
    for field in fields:
        model = AlarmSetting()
        data = model.get_pair(field['field'])
        value = field['value']
        if data:
            value = data.value
        settings[field['field']] = value 

    return json.dumps(settings)
   
