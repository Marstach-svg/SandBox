from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo
from sandbox_system.models import User


class RegistrationForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください')])
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('pass_confirm', message='パスワードが一致していません')])
    pass_confirm = PasswordField('パスワード（確認）', validators=[DataRequired()])
    submit = SubmitField('登録')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('入力されたユーザー名はすでに使われています')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('入力されたメールアドレスはすでに登録されています')


class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください')])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class UserUpdateForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください')])
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('pass_confirm', message='パスワードが一致していません')])
    pass_confirm = PasswordField('パスワード（確認）', validators=[DataRequired()])
    introduce = TextAreaField('自己紹介', validators=[DataRequired()])
    tech = StringField('技術', validators=[DataRequired()])
    job = StringField('主な仕事', validators=[DataRequired()])
    picture = FileField('アイコン画像', validators=[DataRequired()])
    submit = SubmitField('更新')

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = user_id

    def validate_username(self, field):
        if User.query.filter(User.id != self.id).filter_by(username=field.data).first():
            raise ValidationError('入力されたユーザー名はすでに使われています')

    def validate_email(self, field):
        if User.query.filter(User.id != self.id).filter_by(email=field.data).first():
            raise ValidationError('入力されたメールアドレスはすでに登録されています')