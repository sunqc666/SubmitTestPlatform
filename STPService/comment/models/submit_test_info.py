"""

======================

@author:sunqiucheng

@time:2022/10/27:2:41 下午

======================

"""

from STPService.comment.models import db
from datetime import datetime
class SubmitTestInfo(db.Model):
    __tablename__='submit_test_info'
    """
    `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(200) DEFAULT NULL COMMENT '提测标题',
  `appId` varchar(50) DEFAULT NULL COMMENT '应用服务',
  `developer` varchar(255) DEFAULT NULL COMMENT '提测RD',
  `tester` varchar(255) DEFAULT NULL COMMENT '测试QA',
  `CcMail` varchar(500) DEFAULT NULL COMMENT '关系人',
  `version` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '提测版本',
  `type` tinyint(1) DEFAULT NULL COMMENT '提测类型 1.功能 2.性能 3.安全',
  `scope` text COMMENT '测试说明',
  `gitCode` varchar(200) DEFAULT NULL COMMENT '项目代码',
  `wiki` varchar(200) DEFAULT NULL COMMENT '产品文档',
  `more` text COMMENT '是否发送邮件，0未操作，1成功，2失败',
  `status` tinyint(1) DEFAULT NULL COMMENT '测试状态 1-已提测 2-测试中 3-通过 4-失败 9-废弃',
  `sendEmail` tinyint(1) DEFAULT NULL COMMENT '是否发送消息，0未操作，1成功，2失败',
  `isDel` tinyint(1) DEFAULT '0' COMMENT '状态0正常1删除',
  `createUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '创建人',
  `createDate` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '修改人',
  `updateDate` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `test_desc` varchar(2000) DEFAULT '' COMMENT '结论描述',
  `test_risks` varchar(2000) DEFAULT '' COMMENT '风险提示',
  `test_cases` varchar(2000) DEFAULT '' COMMENT '测试用例描述',
  `test_bugs` varchar(1000) DEFAULT '' COMMENT '缺陷列表',
  `test_file` varchar(255) DEFAULT '' COMMENT '附件文件地址',
  `test_note` varchar(1000) DEFAULT '' COMMENT '报告备注',
  `test_email` tinyint(1) DEFAULT '0' COMMENT '是否发送消息，0未操作，1成功，2失败',
    """
    id = db.Column(db.INTEGER, autoincrement=True, nullable=False, unique=True, primary_key=True, comment='自增id')
    title = db.Column(db.String(200), unique=True, nullable=False, comment='提测标题')
    appId = db.Column(db.INTEGER, db.ForeignKey('apps.id'), comment='应用服务')
    developer=db.Column(db.String(500),default=None,comment='提测rd')
    tester=db.Column(db.String(500),default=None,comment='qa')
    CcMail=db.Column(db.String(500),default=None,comment='关系人')
    test_version=db.Column(db.String(500),default=None,comment='提测版本')
    type=db.Column(db.INTEGER,nullable=False,comment='提测类型 1.功能 2.性能 3.安全')
    scope=db.Column(db.String(1000),default=None,comment='测试说明')
    gitCode=db.Column(db.String(500),default=None,comment='项目代码')
    wiki=db.Column(db.String(500),default=None,comment='产品文档')
    more=db.Column(db.TEXT,default=None,comment='更多')
    status=db.Column(db.INTEGER,default=0,comment='测试状态 1-已提测 2-测试中 3-通过 4-失败 9-废弃')
    sendEmail=db.Column(db.INTEGER,default=None,comment='是否发送消息，0未操作，1成功，2失败')
    isDel=db.Column(db.INTEGER,default=0,comment='状态0正常1删除')
    createUser=db.Column(db.String(500),nullable=False,comment='创建人')
    createDate=db.Column(db.DateTime,default=datetime.now,comment='创建时间')
    updateUser=db.Column(db.String(500),nullable=False,comment='更新人')
    updateDate=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment='更新时间')
    test_desc=db.Column(db.String(500),default=None,comment='结论描述')
    test_risks=db.Column(db.String(500),default=None,comment='风险提示')
    test_cases=db.Column(db.String(500),default=None,comment='测试用例描述')
    test_bugs=db.Column(db.String(500),default=None,comment='缺陷列表')
    test_file=db.Column(db.String(500),default=None,comment='附件文件地址')
    test_note=db.Column(db.String(500),default=None,comment='报告备注')
    test_email=db.Column(db.String(500),default=0,comment='是否发送消息，0未操作，1成功，2失败')
    version=db.Column(db.INTEGER,default=0,comment="数据版本")
    app=db.relationship("Apps", backref="submitTestInfo")

    # def __init__(self,title,appId,developer,tester,CcMail,version,type,scope,gitCode,wiki,more,
    #              status,sendEmail,isDel,createUser,createDate,updateUser,updateDate,test_desc,test_risks,test_cases,
    #              test_bugs,test_file,test_note,test_email):
    #     self.title=title
    #     self.appId=appId
    #     self.developer=developer
    #     self.tester=tester
    #     self.CcMail=CcMail
    #     self.version=version
    #     self.type=type
    #     self.scope=scope
    #     self.gitCode=gitCode
    #     self.wiki=wiki
    #     self.more=more
    #     self.status=status
    #     self.sendEmail=sendEmail
    #     self.isDel=isDel
    #     self.createUser=createUser
    #     self.createDate=createDate
    #     self.updateUser=updateUser
    #     self.updateDate=updateDate
    #     self.test_desc=test_desc
    #     self.test_risks=test_risks
    #     self.test_cases=test_cases
    #     self.test_bugs=test_bugs
    #     self.test_file=test_file
    #     self.test_note=test_note
    #     self.test_email=test_email