from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sandbox_system import db

chats = Blueprint('chats', __name__)

@chats.route('/chat_index')
@login_required
def chat_index():
    return render_template('chat/chat_index.html')