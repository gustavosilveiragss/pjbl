from flask import Blueprint, redirect, url_for, render_template
from models import Read
from flask_login import current_user

iot = Blueprint("iot",__name__,
                static_folder="./static/",
                template_folder="./templates/")

@iot.route('/messages')
def check_messages():
    return render_template("list_reads.html",reads=Read.query.all())
