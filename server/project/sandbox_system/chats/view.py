from datetime import datetime
from pytz import timezone
from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user

from sandbox_system import db
from sandbox_system.models import User, ChatChannel, ChatMessage


chats = Blueprint('chats', __name__)


#チャットトップページ
@chats.route('/chat_index', methods=['GET', 'POST'])
@login_required
def chat_index():
    chats = ChatMessage.query.all()
    channels = ChatChannel.query.order_by(ChatChannel.id.asc()).all()
    return render_template('chat/chat_index.html', chats=chats, channels=channels)

#チャットルーム（チャットページ）
@chats.route('/<int:channel_id>/chat_room', methods=['GET', 'POST'])
@login_required
def chat_room(channel_id):
    users = User.query.order_by(User.id.asc()).all()
    number_of_users = len(users)
    chats = ChatMessage.query.all()
    channel_chats = ChatMessage.query.filter_by(channel_id=channel_id).order_by(ChatMessage.id.asc()).all()
    room_channel = ChatChannel.query.filter_by(id=channel_id).first()
    channels = ChatChannel.query.order_by(ChatChannel.id.asc()).all()
    return render_template('chat/chat_room.html', number_of_users=number_of_users, channel_chats=channel_chats, channels=channels, channel_id=channel_id, room_channel=room_channel, chats=chats)

#チャットメッセージ追加
@chats.route('/<int:channel_id>/chat_message', methods=['GET', 'POST'])
@login_required
def chat_message(channel_id):
    message = request.form.get('chat_message')
    if message:
        chat = ChatMessage(channel_id=channel_id, user_id=current_user.id, date=datetime.now(timezone('Asia/Tokyo')), message=message)
        db.session.add(chat)
        db.session.commit()
        return redirect(url_for('chats.chat_room', channel_id=channel_id))
    else:
        return redirect(url_for('chats.chat_room', channel_id=channel_id))

#チャットメッセージ削除
@chats.route('/<int:chat_message_id>/delete_chat_message', methods=['GET', 'POST'])
@login_required
def delete_chat_message(chat_message_id):
    chat_message = ChatMessage.query.get_or_404(chat_message_id)
    channel_id = chat_message.channel_id
    if not current_user.id == chat_message.user_id :
        if not current_user.is_administrator():
            abort(403)
    db.session.delete(chat_message)
    db.session.commit()
    flash('メッセージが削除されました')
    return redirect(url_for('chats.chat_room',channel_id=channel_id))
