"""
File:forms.py
Author:Tcyw
Date:2020-03-13
Connect:741047561@qq.com
Description:

"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名',validators=[Length(0,64)])
    location = StringField('用户地址',validators=[Length(0,64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('更改资料')








