"""
File:views.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
# 2)应用蓝图
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.auth import auth
from app.auth.forms import RegisterationForm,LoginForm
from app.email import send_mail
from app.models import User, Role



@auth.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 判断用户是否存在，并且密码是否正确
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            user.ping() # 更新用户最后登陆时间
            flash('用户%s登陆成功' %(user.username),category='success')
            return redirect(url_for('todo.index'))
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
        # 提交数据库之后才能赋予新用户 id 值,而确认令牌需要用到 id ,所以不能延后提交。
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(to=[user.email],subject='请激活你的任务管理平台帐号',
                  filename='confirm',user=user,token=token
                  )
        flash('平台验证消息已经发送到你的邮箱, 请确认后登录',category='success')
        return redirect(url_for('auth.login'))

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
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    1.判度账户是否验证，如果已经验证，跳转到主页
    2.如果没有验证，执行验证函数，更新账户的confirm值
    :param token:
    :return:
    """
    if current_user.confirmed:
        return redirect(url_for('todo.index'))
    if current_user.confirm(token):
        flash('验证邮箱通过', category='success')
        return redirect(url_for('todo.index'))
    else:
        flash('验证连接失效', category='error')


@auth.before_app_request
def before_request():
    # 判断当前用户有已经登陆，并且没有认证成功，并且请求的不是auth里面的
    #任何一个视图函数，并且访问的不是静态信息
    # request.endpoint:/login === 'auth.login'
    # 判断是不是auth蓝图里边的
   if current_user.is_authenticated \
           and not current_user.confirmed \
           and request.endpoint[:5] != 'auth.' \
           and request.endpoint != 'static':
       return redirect(url_for('auth.unconfirmed'))
@auth.route('/unconfirmed')
def unconfirmed():
   # 如果当前用户是匿名用户或者已经验证的用户, 则访问主页, 否则进入未验证界面;
   if current_user.is_anonymous or current_user.confirmed:
       return redirect(url_for('todo.index'))
   token = current_user.generate_confirmation_token()
   return render_template('unconfirmed.html')

@auth.route('/reconfirm')
@login_required
def resend_confirmation():
   token = current_user.generate_confirmation_token()
   try:
       send_mail([current_user.email], '请激活你的任务管理平台帐号',
                 'confirm', user=current_user, token=token)
   except Exception as e:
       print(e)
       flash(str(e), category='error')
       return redirect(url_for('auth.register'))
   else:
       flash('新的平台验证消息已经发送到你的邮箱, 请确认后登录.', category='success')
       return redirect(url_for('todo.index'))