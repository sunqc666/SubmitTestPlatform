"""

======================

@author:sunqiucheng

@time:2022/9/30:5:31 下午

======================

"""
from flask import Flask


from flask_migrate import Migrate
from flask_mail import Mail
from flask import Flask
from STPService.apis.getOffWork import get_off_work
from STPService.apis.user import app_user
from STPService.apis.product import app_product
from STPService.apis.application import app_application
from STPService.apis.testmanager import test_manager
from STPService.apis.dashboard import test_dashboard
from STPService.apis.updateEs import app_updateEs
from STPService.apis.mytest import mytest
from STPService.apis.mydev import mydev
from flask_cors import CORS
from STPService.apis.newPage import app_newpage
from flask_migrate import Migrate
from STPService.comment.loger import getLogHandler
from STPService.comment.models import db

def app_config(obj):
    app=Flask(__name__)
    app.config.from_object(obj)
    app.logger.addHandler(getLogHandler())
    # 激活上下文
    ctx = app.app_context()
    ctx.push()
    CORS(app)
    from STPService.comment.models import db

    # 初始化SQLALchemy
    db.init_app(app)
    app.register_blueprint(get_off_work)
    app.register_blueprint(mytest)
    app.register_blueprint(mydev)
    app.register_blueprint(app_user)
    app.register_blueprint(app_product)
    app.register_blueprint(app_application)
    app.register_blueprint(test_manager)
    app.register_blueprint(test_dashboard)
    app.register_blueprint(app_newpage)
    app.register_blueprint(app_updateEs)
    # 初始化migrate之后，可以执行命令
    # flask db init
    # flask db migrate
    # flask db upgrade
    # 直接执行上面3哥命令，需要默认的Flask项目入口文件（app.py）
    # 当前项目没有默认的flask项目入口文件，需要设置环境变量：
    Migrate(app, db)
    Mail(app)
    return app



