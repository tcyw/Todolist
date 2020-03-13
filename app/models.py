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
from datetime import datetime

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
    # 新添加的用户资料
    name = db.Column(db.String(64)) # 用户的真实姓名
    location = db.Column(db.String(64)) # 用户的位置
    about_me = db.Column(db.Text()) # 自我介绍
    # 注册日期
    # default 参数可以接受函数的默认值
    # 所以每次生成默认值时db.column()都会调用指定的函数
    create_time = db.Column(db.DateTime,default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # 外键关联
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean,default=False)
    # 反向引用 1)。User添加属性todos 2)Todo添加属性user
    todos = db.relationship('Todo',backref='user')
    # 反向引用 1)。User添加属性category 2)category添加属性user
    categories = db.relationship('Category', backref='user')


    def ping(self):
        """刷新用户的最后访问事件"""
        self.last_seen = datetime.utcnow()
        from flask_login import current_user
        db.session.add(current_user)

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
            self.confirmed = True
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

# 任务和分类的关系: 一对多
# 分类是一, 任务是多, 外键写在多的一端
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.String(100))  # 任务内容
    status = db.Column(db.Boolean, default=False)  # 任务的状态
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # User:Todo = 1:N
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    # Category:Todo=1:N
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))

    def __repr__(self):
       return "<Todo %s>" % (self.content[:6])

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # User:Category = 1:N
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    # 反向引用
    todos = db.relationship('Todo',backref='category')
    def __repr__(self):
       return "<Category %s>" % (self.name)


