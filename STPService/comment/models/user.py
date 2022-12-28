"""

======================

@author:sunqiucheng

@time:2022/10/27:2:41 下午

======================

"""
from STPService.comment.models import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    mail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    password_md5 = db.Column(db.String(1000), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # def __init__(self,user_name,mail,password,password_md5):
    #     self.user_name = user_name
    #     self.mail=mail
    #     self.password=password
    #     self.password_md5=password_md5