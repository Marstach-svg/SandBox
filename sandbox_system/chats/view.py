from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user
from sandbox_system import db
from sandbox_system.models import User, Chat


chats = Blueprint('chats', __name__)


@chats.route('/chat_index', methods=['GET', 'POST'])
@login_required
def chat_index():
    users = User.query.order_by(User.id.asc()).all()
    chats = Chat.query.order_by(Chat.id.asc()).all()
    number_of_users = len(users)
    return render_template('chat/chat_index.html', number_of_users=number_of_users, chats=chats)

@chats.route('/chat_message', methods=['GET', 'POST'])
@login_required
def chat_message():
    message = request.form.get('chat_message')
    if message:
        chat = Chat(user_id=current_user.id, message=message)
        db.session.add(chat)
        db.session.commit()
        return redirect(url_for('chats.chat_index'))
    else:
        return redirect(url_for('chats.chat_index'))