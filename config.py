"""
File:config.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
# config.py
"""
存储配置;
"""
import os
# 获取当前项目的绝对路径;
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    """
    所有配置环境的基类, 包含通用配置
    """
    # 尤其是涉及登陆、注册提交敏感信息时，一定要加（只有有flask-wtf）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'westos secret key'
    # 搜索flask-sqlchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # 设置自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[西部开源]'
    FLASKY_MAIL_SENDER = '741047561@qq.com'
    MAIL_SERVER = 'smtp.163.com'        # 邮件服务器
    MAIL_PORT = 25      # 邮件端口
    MAIL_USERNAME = 'yw17392517656@163.com'
    MAIL_PASSWORD = 'syyy1995713'

    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    """
    开发环境的配置信息
    """
    # 启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器。
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '976131979'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '密码'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'datadev.sqlite')
class TestingConfig(Config):
    """
    测试环境的配置信息
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'datatest.sqlite')
class ProductionConfig(Config):
    """
    生产环境的配置信息
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
    'data.sqlite')
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}