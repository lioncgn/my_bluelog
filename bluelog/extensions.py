#!/usr/bin/env python
# -*- coding=utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension


bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
toolbar = DebugToolbarExtension()

#当调用current_user对象，Flask-Login会调用用户加载函数并返回对应的用户对象；
@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user = Admin.query.get(int(user_id))
    return user

#未登录的用户访问使用了login_required 装饰器的视图时，程序自动重定向到登录视图，设置登录视图的端点
login_manager.login_view = 'auth.login'
#设置消息的分类，默认message
login_manager.login_message_category = 'warning'
#设置提示消息的内容
login_manager.login_message = 'Please log in to access this page.'


