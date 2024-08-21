from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sandbox_system import db
from sandbox_system.models import User

chats = Blueprint('chats', __name__)

@chats.route('/chat_index')
@login_required
def chat_index():
    users = User.query.order_by(User.id.asc()).all()
    number_of_users = len(users)
    return render_template('chat/chat_index.html', users=users, number_of_users=number_of_users)