from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class EventForm(FlaskForm):
    category = StringField('ハッカソンまたは就活と記入', validators=[DataRequired()])
    title = StringField('タイトル（35字以内）', validators=[DataRequired(), Length(max=38, message='タイトルの制限字数を超えています')])
    summary = StringField('要約(60字以内)', validators=[DataRequired(), Length(max=64, message='要約の制限字数を超えています')])
    text = TextAreaField('本文', validators=[DataRequired()])
    url = StringField('ページ先URL', validators=[DataRequired()])
    picture = FileField('アイキャッチ画像', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('投稿')


class EventSearchForm(FlaskForm):
    searchtext = StringField('検索テキスト', validators=[DataRequired()])
    submit = SubmitField('🔍')