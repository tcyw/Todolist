"""
File:views.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
# 2)应用蓝图
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app import db
from app.auth import auth
from app.auth.forms import RegisterationForm,LoginForm
from app.models import User, Role



@auth.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 判断用户是否存在，并且密码是否正确
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('用户%s登陆成功' %(user.username),category='success')
            return redirect(url_for('auth.index'))
        else:
            flash('用户%s登陆失败' %(form.email.data),category='error')
            return redirect(url_for('auth.login'))
    return render_template('login.html',form=form)
@auth.route('/register/',methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.role = Role.query.filter_by(name='普通会员').first()
        db.session.add(user)
        flash('用户%s注册成功' %(user.username),category='success')
        return redirect('/login')

    return render_template('register.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('用户注销成功',category='success')
    return redirect(url_for('auth.index'))

@auth.route('/')
def index():
    return render_template('index.html')