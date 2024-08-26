from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sandbox_system import db
from sandbox_system.models import User, Blog, BlogFavorite, BlogComment, ChatMessage
from sandbox_system.users.form import RegistrationForm, LoginForm, UserUpdateForm
from sandbox_system.blogs.image import add_image

users = Blueprint('users', __name__)

#ユーザー登録
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, introduce='例 よろしくお願いします。', tech='例 Python独学1年', job='例 フロントエンドエンジニア', image='', password=form.password.data, administrator='0')
        db.session.add(user)
        db.session.commit()
        flash('ユーザーが登録されました')
        login_user(user)
        return redirect(url_for('users.index'))
    return render_template('user/register.html', form=form)

#ログイン
@users.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('users.index')
                return redirect(next)
            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは登録されていません')
    return render_template('user/login.html', form=form)

#編集（ユーザー情報更新）
@users.route('/<int:user_id>/user_update', methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    form = UserUpdateForm(user_id)
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        user.username = form.username.data
        if form.picture.data:
            user.image = add_image(form.picture.data)
        user.email = form.email.data
        user.introduce = form.introduce.data
        user.tech = form.tech.data
        user.job = form.job.data
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        flash('ユーザー情報が更新されました')
        return redirect(url_for('users.my_page', user_id=user.id))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.introduce.data = user.introduce
        form.tech.data = user.tech
        form.job.data = user.job
        form.picture.data = user.image
    return render_template('user/user_update.html', form=form)

#ユーザー削除確認ページ
@users.route('/<int:user_id>/delete_confirm', methods=['GET', 'POST'])
@login_required
def delete_confirm(user_id):
    if not current_user.is_administrator():
        abort(403)
    return render_template('user/delete_user.html', user_id=user_id)

#ユーザー削除
@users.route('/<int:user_id>/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_administrator():
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.administrator == '1':
        flash('管理者ユーザーは削除できません')
        return redirect(url_for('users.user_maintenance'))
    blogs = Blog.query.filter_by(user_id=user_id).all()
    chats = ChatMessage.query.filter_by(user_id=user_id).all()
    favorite_blogs = ''
    blog_comments = ''
    if blogs:
        for blog in blogs:
            if BlogFavorite.query.filter_by(blog_id=blog.id).first():
                favorite_blogs = BlogFavorite.query.filter_by(blog_id=blog.id).all()
            else:
                favorite_blogs = ''
            if BlogComment.query.filter_by(blog_id=blog.id).first():
                blog_comments = BlogComment.query.filter_by(blog_id=blog.id).all()
            else:
                blog_comments = ''
    if BlogFavorite.query.filter_by(favorite_user_id=user_id).first():
        my_favorite_blogs = BlogFavorite.query.filter_by(favorite_user_id=user_id).all()
    else:
        my_favorite_blogs = ''
    if BlogComment.query.filter_by(user_id=user_id).first():
        my_blog_comments = BlogComment.query.filter_by(user_id=user_id).all()
    else:
        my_blog_comments = ''
    #BlogFavoriteがBlogに外部キーでつながっているため、外部キーエラーを避けるためにBlogFavoriteのデータを先にdeleteしなければならない
    if blog_comments:
        for blog_comment in blog_comments:
            db.session.delete(blog_comment)
            db.session.commit()
    if my_blog_comments:
        for my_blog_comment in my_blog_comments:
            db.session.delete(my_blog_comment)
            db.session.commit()
    if favorite_blogs:
        for favorite_blog in favorite_blogs:
            db.session.delete(favorite_blog)
            db.session.commit()
    if my_favorite_blogs:
        for my_favorite_blog in my_favorite_blogs:
            db.session.delete(my_favorite_blog)
            db.session.commit()
    if blogs:
        for blog in blogs:
            db.session.delete(blog)
            db.session.commit()
    if chats:
        for chat in chats:
            db.session.delete(chat)
            db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.user_maintenance'))

#ログアウト
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.index'))

#トップページ（ホームページ）
@users.route('/')
def index():
    return render_template('index.html')

#マイページ
@users.route('/<int:user_id>/my_page')
@login_required
def my_page(user_id):
    if not current_user.id == user_id:
        abort(403)
    profile = User.query.filter_by(id=user_id).first()
    return render_template('user/my_page/my_profile.html', profile=profile)

#公開プロフィール
@users.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    profile = User.query.filter_by(id=user_id).first()
    return render_template('user/my_page/profile.html', profile=profile)

#ユーザー管理ページ
@users.route('/user_maintenance')
@login_required
def user_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('maintenance/user_maintenance.html', users=users)

#公開ユーザー一覧
@users.route('/user_list')
@login_required
def user_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('user/user_list.html', users=users)