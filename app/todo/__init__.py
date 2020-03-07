"""
File:__init__.py.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
# 1)创建蓝图
from flask import Blueprint
todo = Blueprint('todo',__name__)
from . import views