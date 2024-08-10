from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sandbox_system import db
from sandbox_system.models import User
from sandbox_system.users.form import RegistrationForm, LoginForm, UpdateUserForm

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, administrator='0')
        db.session.add(user)
        db.session.commit()
        flash('ユーザーが登録されました')
        return redirect(url_for('users.index'))
    return render_template('user/register.html', form=form)

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
            flash('入力されたユーザーは存在しません')
    return render_template('user/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.index'))

@users.route('/')
def index():
    return render_template('index.html')

@users.route('/my_page')
@login_required
def my_page():
    return render_template('user/my_page/profile.html')

@users.route('/favorite')
@login_required
def favorite():
    return render_template('user/my_page/favorite.html')

@users.route('/my_blog')
@login_required
def my_blog():
    return render_template('user/my_page/my_blog.html')

@users.route('/user_maintenance')
@login_required
def user_maintenance():
    if not current_user.is_administrator():
        abort(403)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('maintenance/user_maintenance.html', users=users)