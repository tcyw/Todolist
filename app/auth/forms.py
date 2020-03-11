"""
File:forms.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User

class RegisterationForm(FlaskForm):
    email = StringField(label='电子邮件',
                        validators=[
                            DataRequired(),Length(1,64),Email()],
                        render_kw={
                            'class': 'layui-input',
                            'placeholder': "电子邮箱"
                        }
                        )
    username = StringField(label='用户名',validators=[
        DataRequired(),Length(1,64),Regexp('^\w*$',message='用户名只能由字母数字下划线组成')
    ],
                           render_kw={
                               'class': 'layui-input',
                               'placeholder': "用户名"
                           }
                           )
    password = PasswordField(label='密码',validators=[
        DataRequired(),EqualTo('repassword',message='密码不一致')
    ],
                             render_kw={
                                 'class': 'layui-input',
                                 'placeholder': "密码"
                             }
                             )
    repassword = PasswordField('确认密码',validators=[
        DataRequired()
    ],
                               render_kw={
                                   'class': 'layui-input',
                                   'placeholder': "确认密码"
                               }
                               )
    submit = SubmitField('注册')
    # 两个自定义的验证函数, 以validate_ 开头且跟着字段名的方法,这个方法和常规的验证函数一起调用。
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            # 自定义的验证函数要想表示验证失败,可以抛出 ValidationError 异常,其参数就是错误消息。
            raise ValidationError('电子邮箱已经注册')
    def validata_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被占用')

class LoginForm(FlaskForm):
    """用户登录表单"""
    email = StringField('电子邮箱',
                        validators=[DataRequired(),
                        Length(1, 64),
                        Email()],
                        # 給前端标签添加下面的属性信息
                        render_kw={
                            'class':'layui-input',
                            'placeholder':"电子邮箱"
                        }
                        )
    password = PasswordField('密码', validators=[DataRequired()],
                             # 給前端标签添加下面的属性信息
                             render_kw={
                                 'class': 'layui-input',
                                 'placeholder': "密码"
                             }
                             )
    submit = SubmitField('登录')









