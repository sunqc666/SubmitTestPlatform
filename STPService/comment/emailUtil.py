# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
#
# import yagmail
# import traceback
# from STPService.configs.config import Config
# from STPService.apps import app_config,app
# from flask_mail import Message
#
# '''
# receivers 收件人，字符数组['邮件地址']
# subject 邮件主题, 字符串
# contents 邮件内容，自定义 字符数组
# attachments 附件默认为空
# '''
# def sendEmail(subject,receivers, contents):
#
#
#     try:
#         # # 初始化服务对象直接根据参数给定，更多参考SMTP(）内部
#         # server = yagmail.SMTP(host=Config.MAIL_HOST, port=Config.MAIL_PORT,
#         #                       user=Config.MAIL_USER, password=Config.MAIL_PASSWORD)
#         # # 发送内容，设置接受人等信息，更多参考SMTP.send()内部
#         # server.send(to=receivers,
#         #             subject=subject,
#         #             contents=contents,
#         #             attachments=attachments)
#         # server.close()
#
#         msg = Message(subject,recipients=receivers)
#         msg.body=contents
#         print(msg)
#         app_config('').mail.send(msg)
#     except Exception:
#         print('traceback.format_exc(): {}'.format(traceback.format_exc()))
#         return False
#     # 无任何异常表示发送成功
#     return True
#
# def sendKim(botId):
#     pass
#
# if __name__ == "__main__":
#     # 测试发送服务
#     receivers = ['15630156711@163.com']
#     subject = 'DaQi工具类测试'
#     body = '简单的问题内容体'
#     sendEmail( subject, receivers, body)
from flask_mail import Mail
mail = Mail()