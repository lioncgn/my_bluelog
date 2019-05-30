#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os

import click
from flask import Flask, render_template

from extensions import bootstrap, db, ckeditor, mail, moment
from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.blog import blog_bp
from settings import config



#使用flask run 运行程序时，Flask的自动发现程序实例机制，会自动从环境变量FLASK_APP的值定义的模块中寻找
# create_app or make_app的工厂函数，自动调用工厂函数创建程序实例并运行；
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        
    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging(app)  #注册日志处理器
    register_extensions(app)  #注册扩展 (完成初始化)
    register_blueprints(app) #注册蓝本
    register_commands(app)  #注册自定义flask 命令
    register_errors(app)  #注册错误处理函数
    register_shell_context(app)  #注册shell上下文处理函数
    register_template_context(app)  #注册模板上下文处理函数
    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

def register_blueprints(app):
    #注册蓝本
    app.register_blueprint(blog_bp)
    #为蓝本中所欲的视图添加URL前缀
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_commands(app):
    @app.cli.command()
    @click.optin('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

def register_errors(app):

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass



