"""
File:views.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
# 2)应用蓝图
from app.todo import todo

@todo.route('/')
def index():
    return 'index'