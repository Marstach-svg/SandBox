from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user
from sandbox_system import db
from sandbox_system.events.form import EventForm


events = Blueprint('events', __name__)


@events.route('/event_index', methods=['GET'])
def event_index():
    return render_template('event/event_index.html')