# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

blueprint = Blueprint("setting", __name__, url_prefix='/settings',
                        static_folder="../static")


@blueprint.route("/settings/", methods=['GET', 'POST'])
@login_required
def all():
    return render_template("settings/all.html")
