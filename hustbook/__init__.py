'''
@Description: 
@Author: Wu Xie
@Github: https://github.com/shiehng
@Date: 2019-07-23 23:41:45
'''
import os

from flask import Flask, render_template

from hustbook.blueprints.auth import auth_bp
from hustbook.blueprints.admin import admin_bp
from hustbook.blueprints.blog import blog_bp

from hustbook.settings import config

from hustbook.extensions import bootstrap, db, moment, ckeditor, mail

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('hustbook')
    app.config.from_object(config[config_name])

    register_logging(app) # 注册日志处理器
    register_extensions(app) # 注册扩展（扩展初始化）
    register_blueprints(app) # 注册蓝本
    register_commands(app) # 注册自定义shell命令
    register_errors(app) # 注册错误处理函数
    register_shell_context(app) # 注册shell上下文处理函数
    register_template_context(app) # 注册模板上下文处理函数
    
    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):
    pass

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html', 400)
    
def register_commands(app):
    pass