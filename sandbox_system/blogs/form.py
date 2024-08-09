from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, ValidationError
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from sandbox_system.models import BlogCategory


class BlogForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    summary = StringField('要約', validators=[DataRequired()])
    category = SelectField('カテゴリ', coerce=int)
    text = TextAreaField('本文', validators=[DataRequired()])
    picture = FileField('アイキャッチ画像', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('投稿')

    def _set_category(self):
        blog_categories = BlogCategory.query.all()
        self.category.choices = [(blog_category.id, blog_category.category) for blog_category in blog_categories]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_category()


class BlogSearchForm(FlaskForm):
    searchtext = StringField('検索テキスト', validators=[DataRequired()])
    submit = SubmitField('🔍')


class BlogCategoryForm(FlaskForm):
    category = StringField('カテゴリ名', validators=[DataRequired()])
    submit = SubmitField('保存')

    def validater_category(self, field):
        if BlogCategory.query.order_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリ名はすでに使われています')