"""

======================

@author:sunqiucheng

@time:2022/10/27:11:37 上午

======================

"""
from STPService.apps import app_config
from STPService.comment.loger import getLogHandler
from STPService.configs.config import DevelopmentConfig,ProductmentConfig
from STPService.comment.models.user import UserModel
from STPService.comment.models.submit_test_info import SubmitTestInfo
from STPService.comment.models.products import Products
from STPService.comment.models.apps import Apps
app=app_config(DevelopmentConfig)
# app1=app1(DevelopmentConfig)
if __name__ == '__main__':

    app.run(host="0.0.0.0",port=5000,debug=True)
    # print(app1.config.get("MYSQL_PORT"))
    # app1.run(port=5003)
