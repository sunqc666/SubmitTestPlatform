"""

======================

@author:sunqiucheng

@time:2022/9/30:11:25 上午

======================

"""

# from datetime import datetime
# from STPService.apps import db
#
#
# class UserModel(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
#     user_name = db.Column(db.String(100), nullable=False, unique=True)
#     mail = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(1000), nullable=False)
#     password_md5 = db.Column(db.String(1000), nullable=False)
#     join_time = db.Column(db.DateTime, default=datetime.now)
#
#     # def __init__(self,user_name,mail,password,password_md5):
#     #     self.user_name = user_name
#     #     self.mail=mail
#     #     self.password=password
#     #     self.password_md5=password_md5
#
#
# class Products(db.Model):
#     __tablename__='products'
#     """
#   `id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号自增',
#   `keyCode` varchar(200) NOT NULL COMMENT '项目唯一编号',
#   `title` varchar(200) NOT NULL COMMENT '中文项目名',
#   `desc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '描述',
#   `status` int NOT NULL DEFAULT '0' COMMENT '状态',
#   `operator` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作者',
#   `update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
#     """
#     id = db.Column(db.INTEGER,autoincrement=True, nullable=False, unique=True, primary_key=True, comment='自增id')
#     keyCode = db.Column(db.String(200), nullable=False, comment='项目唯一编号')
#     title = db.Column(db.String(200),default=None, comment='中文项目名')
#     desc = db.Column(db.String(500),default=None,comment='描述')
#     status = db.Column(db.INTEGER, default=0, comment='状态')
#     operator = db.Column(db.String(50), nullable=False, comment='操作者')
#     update = db.Column(db.DateTime, default=datetime.now, comment='操作时间')
#
#     # def __init__(self, keyCode, title, desc, status, operator):
#     #     self.keyCode = keyCode
#     #     self.title = title
#     #     self.desc = desc
#     #     self.status = status
#     #     self.operator = operator
#
#
# class Apps(db.Model):
#     __tablename__='apps'
#     """
#   `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',
#   `appId` varchar(50) DEFAULT NULL COMMENT '应用服务ID',
#   `productId` bigint DEFAULT NULL COMMENT '外键关联产品所属',
#   `note` varchar(100) DEFAULT NULL COMMENT '应用描述',
#   `tester` varchar(300) DEFAULT NULL COMMENT '测试负责人',
#   `developer` varchar(300) DEFAULT NULL COMMENT '默认研发负责人',
#   `producer` varchar(300) DEFAULT NULL COMMENT '默认产品经理',
#   `CcEmail` varchar(500) DEFAULT NULL COMMENT '默认抄送邮件或组',
#   `gitCode` varchar(200) DEFAULT NULL COMMENT '代码地址',
#   `wiki` varchar(200) DEFAULT NULL COMMENT '项目说明地址',
#   `more` text COMMENT '更多的信息',
#   `status` tinyint(1) DEFAULT '0' COMMENT '提测状态：1-已提测 2-测试中 3-通过 4-失败 9-废弃',
#   `isDel` tinyint(1) DEFAULT '0' COMMENT '状态0正常1删除',
#   `createUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '创建人',
#   `createDate` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `updateUser` varchar(20) DEFAULT NULL COMMENT '修改人',
#   `updateDate` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
#     """
#     id = db.Column(db.INTEGER, autoincrement=True, nullable=False, unique=True, primary_key=True, comment='自增id')
#     appId = db.Column(db.String(50), nullable=False, comment='应用服务ID')
#     productId = db.Column(db.INTEGER, db.ForeignKey('products.id'))
#     note = db.Column(db.String(100), default=None, comment='应用描述')
#     tester = db.Column(db.String(500), nullable=False, comment='测试负责人')
#     developer = db.Column(db.String(500), nullable=False, comment='默认研发负责人')
#     producer = db.Column(db.String(500), nullable=False, comment='默认产品经理')
#     CcEmail = db.Column(db.String(500), default=None, comment='默认抄送邮件或组')
#     gitCode = db.Column(db.String(500), default=None, comment='代码地址')
#     wiki = db.Column(db.String(500), default=None, comment='')
#     more = db.Column(db.String(1000),default=None, comment='更多')
#     status = db.Column(db.INTEGER, default=0, comment='提测状态：1-已提测 2-测试中 3-通过 4-失败 9-废弃')
#     isDel = db.Column(db.INTEGER, default=0, comment='状态0正常1删除')
#     createUser = db.Column(db.String(100), nullable=False, comment='创建人')
#     createDate = db.Column(db.DateTime, default=datetime.now)
#     updateUser = db.Column(db.String(100), default=None, comment='更新人')
#     updateDate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
#     product=db.relationship("Products",backref="app")
#
#
#     # def __init__(self, appId, productId, note, tester, developer, producer, CcEmail, gitCode, wiki, more, status,
#     #              createUser=None,updateUser=None):
#     #     self.status=status
#     #     self.appId = appId
#     #     self.productId = productId
#     #     self.note = note
#     #     self.tester = tester
#     #     self.developer = developer
#     #     self.producer = producer
#     #     self.CcEmail = CcEmail
#     #     self.gitCode = gitCode
#     #     self.wiki = wiki
#     #     self.more=more
#     #     self.createUser=createUser
#     #     self.updateUser=updateUser
#
#
#
#
# class SubmitTestInfo(db.Model):
#     __tablename__='submit_test_info'
#     """
#     `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
#   `title` varchar(200) DEFAULT NULL COMMENT '提测标题',
#   `appId` varchar(50) DEFAULT NULL COMMENT '应用服务',
#   `developer` varchar(255) DEFAULT NULL COMMENT '提测RD',
#   `tester` varchar(255) DEFAULT NULL COMMENT '测试QA',
#   `CcMail` varchar(500) DEFAULT NULL COMMENT '关系人',
#   `version` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '提测版本',
#   `type` tinyint(1) DEFAULT NULL COMMENT '提测类型 1.功能 2.性能 3.安全',
#   `scope` text COMMENT '测试说明',
#   `gitCode` varchar(200) DEFAULT NULL COMMENT '项目代码',
#   `wiki` varchar(200) DEFAULT NULL COMMENT '产品文档',
#   `more` text COMMENT '是否发送邮件，0未操作，1成功，2失败',
#   `status` tinyint(1) DEFAULT NULL COMMENT '测试状态 1-已提测 2-测试中 3-通过 4-失败 9-废弃',
#   `sendEmail` tinyint(1) DEFAULT NULL COMMENT '是否发送消息，0未操作，1成功，2失败',
#   `isDel` tinyint(1) DEFAULT '0' COMMENT '状态0正常1删除',
#   `createUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '创建人',
#   `createDate` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `updateUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '修改人',
#   `updateDate` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
#   `test_desc` varchar(2000) DEFAULT '' COMMENT '结论描述',
#   `test_risks` varchar(2000) DEFAULT '' COMMENT '风险提示',
#   `test_cases` varchar(2000) DEFAULT '' COMMENT '测试用例描述',
#   `test_bugs` varchar(1000) DEFAULT '' COMMENT '缺陷列表',
#   `test_file` varchar(255) DEFAULT '' COMMENT '附件文件地址',
#   `test_note` varchar(1000) DEFAULT '' COMMENT '报告备注',
#   `test_email` tinyint(1) DEFAULT '0' COMMENT '是否发送消息，0未操作，1成功，2失败',
#     """
#     id = db.Column(db.INTEGER, autoincrement=True, nullable=False, unique=True, primary_key=True, comment='自增id')
#     title = db.Column(db.String(200), unique=True, nullable=False, comment='提测标题')
#     appId = db.Column(db.INTEGER, db.ForeignKey('apps.id'), comment='应用服务')
#     developer=db.Column(db.String(500),default=None,comment='提测rd')
#     tester=db.Column(db.String(500),default=None,comment='qa')
#     CcMail=db.Column(db.String(500),default=None,comment='关系人')
#     version=db.Column(db.String(500),default=None,comment='提测版本')
#     type=db.Column(db.INTEGER,nullable=False,comment='提测类型 1.功能 2.性能 3.安全')
#     scope=db.Column(db.String(1000),default=None,comment='测试说明')
#     gitCode=db.Column(db.String(500),default=None,comment='项目代码')
#     wiki=db.Column(db.String(500),default=None,comment='产品文档')
#     more=db.Column(db.TEXT,default=None,comment='更多')
#     status=db.Column(db.INTEGER,default=0,comment='测试状态 1-已提测 2-测试中 3-通过 4-失败 9-废弃')
#     sendEmail=db.Column(db.INTEGER,default=None,comment='是否发送消息，0未操作，1成功，2失败')
#     isDel=db.Column(db.INTEGER,default=0,comment='状态0正常1删除')
#     createUser=db.Column(db.String(500),nullable=False,comment='创建人')
#     createDate=db.Column(db.DateTime,default=datetime.now,comment='创建时间')
#     updateUser=db.Column(db.String(500),nullable=False,comment='更新人')
#     updateDate=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment='更新时间')
#     test_desc=db.Column(db.String(500),default=None,comment='结论描述')
#     test_risks=db.Column(db.String(500),default=None,comment='风险提示')
#     test_cases=db.Column(db.String(500),default=None,comment='测试用例描述')
#     test_bugs=db.Column(db.String(500),default=None,comment='缺陷列表')
#     test_file=db.Column(db.String(500),default=None,comment='附件文件地址')
#     test_note=db.Column(db.String(500),default=None,comment='报告备注')
#     test_email=db.Column(db.String(500),default=0,comment='是否发送消息，0未操作，1成功，2失败')
#     app=db.relationship("Apps", backref="submitTestInfo")
#
#     # def __init__(self,title,appId,developer,tester,CcMail,version,type,scope,gitCode,wiki,more,
#     #              status,sendEmail,isDel,createUser,createDate,updateUser,updateDate,test_desc,test_risks,test_cases,
#     #              test_bugs,test_file,test_note,test_email):
#     #     self.title=title
#     #     self.appId=appId
#     #     self.developer=developer
#     #     self.tester=tester
#     #     self.CcMail=CcMail
#     #     self.version=version
#     #     self.type=type
#     #     self.scope=scope
#     #     self.gitCode=gitCode
#     #     self.wiki=wiki
#     #     self.more=more
#     #     self.status=status
#     #     self.sendEmail=sendEmail
#     #     self.isDel=isDel
#     #     self.createUser=createUser
#     #     self.createDate=createDate
#     #     self.updateUser=updateUser
#     #     self.updateDate=updateDate
#     #     self.test_desc=test_desc
#     #     self.test_risks=test_risks
#     #     self.test_cases=test_cases
#     #     self.test_bugs=test_bugs
#     #     self.test_file=test_file
#     #     self.test_note=test_note
#     #     self.test_email=test_email





