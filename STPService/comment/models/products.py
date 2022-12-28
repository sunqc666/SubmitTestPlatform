"""

======================

@author:sunqiucheng

@time:2022/10/27:2:40 下午

======================

"""
from STPService.comment.models import db
from datetime import datetime
class Products(db.Model):
    __tablename__='products'
    """
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号自增',
  `keyCode` varchar(200) NOT NULL COMMENT '项目唯一编号',
  `title` varchar(200) NOT NULL COMMENT '中文项目名',
  `desc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '描述',
  `status` int NOT NULL DEFAULT '0' COMMENT '状态',
  `operator` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作者',
  `update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
    """
    id = db.Column(db.INTEGER,autoincrement=True, nullable=False, unique=True, primary_key=True, comment='自增id')
    keyCode = db.Column(db.String(200), nullable=False, comment='项目唯一编号')
    title = db.Column(db.String(200),default=None, comment='中文项目名')
    desc = db.Column(db.String(500),default=None,comment='描述')
    status = db.Column(db.INTEGER, default=0, comment='状态')
    operator = db.Column(db.String(50), nullable=False, comment='操作者')
    update = db.Column(db.DateTime, default=datetime.now, comment='操作时间')
    version = db.Column(db.INTEGER,default=0,comment='数据版本')

    # def __init__(self, keyCode, title, desc, status, operator):
    #     self.keyCode = keyCode
    #     self.title = title
    #     self.desc = desc
    #     self.status = status
    #     self.operator = operator