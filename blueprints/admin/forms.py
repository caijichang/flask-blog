from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from flask_ckeditor import CKEditorField
from blueprints.models import  CategoryCc

'''
***************
77的表单
***************
'''
class PostSevenForm(FlaskForm):
    body = CKEditorField('文章', validators=[DataRequired()])
    submit = SubmitField('提交')


'''
***************
CC的表单
***************
'''
class PostCCForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)], render_kw={'style': 'width: 100%'})
    photo = FileField('封面', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    category = SelectField('分类', coerce=int, default=1, render_kw={'style': 'width: 100%'})
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(PostCCForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in CategoryCc.query.order_by(CategoryCc.name).all()]

class CategoryCCForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if CategoryCc.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')
'''
***************
Life的表单
***************
'''
class PostLifeForm(FlaskForm):
    body = CKEditorField('文章', validators=[DataRequired()])
    submit = SubmitField('提交')

'''
***************
Journal的表单
***************
'''
class PostJournalForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)], render_kw={'style': 'width: 100%'})
    photo = FileField('封面', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('提交')

'''
***************
Album的表单
***************
'''
class AlbumForm(FlaskForm):
    name = StringField('相册名', validators=[DataRequired(), Length(1, 10)], render_kw={'style': 'width: 100%'})
    description = StringField('相册描述', validators=[DataRequired(), Length(1, 10)], render_kw={'style': 'width: 100%;'})
    photo = FileField('选择文件', validators=[ FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('提交')

'''
***************
Vlog的表单
***************
'''
class VlogForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 10)], render_kw={'style': 'width: 100%'})
    description = StringField('Vlog描述', validators=[DataRequired(), Length(1, 12)], render_kw={'style': 'width: 100%;'})
    vlog = FileField('选择文件', validators=[FileAllowed(['mp4', 'mov'])])
    submit = SubmitField('提交')

