"""
File: models.py
Author: tcyw
Date: 2020-03-07
Connect: 741047561@qq.com
Description:
设计数据库模型:
    1). 用户信息： User
    2). 用户角色信息: Role
    3). 用户角色: 用户 = 1:n, 一对多关系，外键写在多的一端。
"""
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from flask_login import UserMixin


# Flask中一个Model子类就是数据库中的一个表。默认表名'User'.lower() ===> user
class User(UserMixin,db.Model):
    """
    因为继承了Usermixin自动继承了里面的属性和方法
    """
    __tablename__ = 'users'  # 自定义数据表的表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(50))
    # 外键关联
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    conformed = db.Column(db.Boolean,default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # generate_password_hash(password, method= pbkdf2:sha1 , salt_length=8):密码加密的散列值。
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # check_password_hash(hash, password) :密码散列值和用户输入的密码是
        return check_password_hash(self.password_hash, password)
    def generate_confirmation_token(self,expire=3600):
        """生成一个令牌，默认3600秒"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],expire)
        return s.dumps({'confirm':self.id})
    def confirm(self,token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token) # {confirm : 1}
        except Exception as e:
            return False
        else:
            self.conformed = True
            db.session.add(self)  # 把当前信息存入到缓存中
            db.session.commit() # 并且提交到数据库
            return True
    def __repr__(self):
        return "<User: %s>" % (self.username)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 做了两件事情: 1). Role添加属性users    2). User添加属性role
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role: %s>" %(self.name)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))