# -*- coding:utf-8 -*-


from urllib.parse import quote
from flask import Blueprint
from STPService.comment.format import JsonResponse
from flask import request,current_app
from STPService.comment.modelToJson import serialize
import os
from flask import send_from_directory, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from STPService.comment.models.submit_test_info import SubmitTestInfo
from STPService.comment.models.apps import Apps
from STPService.comment.emailUtil import mail
from STPService.comment.models import db
from sqlalchemy import and_,func
from flask_mail import Message
from STPService.comment.forms import SubmitTestForm
from STPService.comment.forms import FileForm

test_manager = Blueprint("test_manager", __name__)

@test_manager.route("/api/test/search", methods=['POST'])
def searchBykey():
    body = request.get_json()
    current_app.logger.info(body)
    # 获取pageSize和
    pageSize = 10 if 'pageSize' not in body or body['pageSize'] is None else body['pageSize']
    currentPage = 1 if 'currentPage' not in body or body['currentPage'] is None else body['currentPage']
    res_data=[]
    search = and_(
        Apps.productId.like('%{}%'.format(body['productId'])),
        SubmitTestInfo.appId.like('%{}%'.format(body['appId'])),
        SubmitTestInfo.tester.like('%{}%'.format(body['tester'])),
        SubmitTestInfo.developer.like('%{}%'.format(body['developer'])),
        SubmitTestInfo.status.like('%{}%'.format(body['status']))
    )
    if 'pickTime' in body and body['pickTime'] != '' and body['pickTime']:
        search=and_(
            Apps.productId.like('%{}%'.format(body['productId'])),
            SubmitTestInfo.appId.like('%{}%'.format(body['appId'])),
            SubmitTestInfo.tester.like('%{}%'.format(body['tester'])),
            SubmitTestInfo.developer.like('%{}%'.format(body['developer'])),
            SubmitTestInfo.status.like('%{}%'.format(body['status'])),
            SubmitTestInfo.createDate >= body['pickTime'][0],
            SubmitTestInfo.createDate<=body['pickTime'][1]
        )
    total = db.session.query(func.count(SubmitTestInfo.id)).filter(and_(SubmitTestInfo.appId==Apps.id,SubmitTestInfo.isDel==0,search)).scalar()
    test_model = db.session.query(SubmitTestInfo,Apps.appId).filter(and_(SubmitTestInfo.appId==Apps.id,SubmitTestInfo.isDel==0,search)).order_by(SubmitTestInfo.updateDate.desc()).offset((currentPage - 1) * pageSize).limit(pageSize).all()
    for test in test_model:
        test_json = serialize(test[0])
        # 把appid 转换成app 表里的appId ，页面容易分辨
        test_json["appId"] = test[1]
        res_data.append(test_json)
    # logger.info(res_data)
    return JsonResponse.success(data=res_data,total=total).to_dict()


@test_manager.route("/api/test/create", methods=['POST'])
def createReqeust():
    # 获取传递的数据，并转换成JSON
    body = request.get_json()
    current_app.logger.info(body)
    if 'appId' not in body:
        err_msg = 'appId 提测应用不能为空'
        return JsonResponse.error(msg=err_msg).to_dict()
    elif 'tester' not in body:
        err_msg = 'tester 测试人员不能为空'
        return JsonResponse.error(msg=err_msg).to_dict()
    elif 'developer' not in body:
        err_msg ='developer 提测人不能为空'
        return JsonResponse.error(msg=err_msg).to_dict()
    elif 'title' not in body:
        err_msg = 'title提测标题不能为空'
        return JsonResponse.error(msg=err_msg).to_dict()
    elif 'type' not in body or body["type"] == '':
        err_msg = '提测类型不能是空'
        return JsonResponse.error(msg=err_msg).to_dict()
    # 新建成功发送Email
    if body['type'] == 1:
        rquest_type = '功能测试'
    elif body['type'] == 2:
        rquest_type = '性能测试'
    elif body['type'] == 3:
        rquest_type = '安全测试'
    try:
        submitTestInfo_model = SubmitTestInfo(title=body["title"], appId=body["appId"], developer=body["developer"],
                                              tester=body["tester"],
                                              CcMail=body["CcMail"], test_version=body["test_version"], type=body["type"],
                                              scope=body["scope"], gitCode=body["gitCode"], wiki=body["wiki"],
                                              more=body["more"], createUser=body["createUser"],
                                              updateUser=body["updateUser"], status=1)
        db.session.add(submitTestInfo_model)
        db.session.commit()
        receivers = body["tester"].split(',') + body["developer"].split(',')
        if not body["CcMail"] == '':
            receivers = receivers + body["CcMail"].split(',')
        if 'isEmail' in body and body['isEmail'] == 'true':
            subject = '【提测】' + body['title']
            msg = Message(subject=subject, recipients=receivers, html=
            '<strong>[提测人]</strong><br />'
            '{}<br />'
            '<strong>[提测版本]</strong><br />'
            '{}<br />'
            '<strong>[提测类型]</strong><br />'
            '{}<br />'
            '<strong>[测试内容]</strong><br />'
            '{}<br />'
            '<strong>[相关文档]</strong><br />'
            '{}<br />'
            '<strong>[补充信息]</strong>'.format(
                body['developer'],
                body['test_version'],
                rquest_type,
                body['scope'],
                body['wiki'],
                body['more']
            ))
            try:
                mail.send(msg)
                flag = 1
            except Exception as e:
                flag = 2
                current_app.logger.info('发送失败{}'.format(e))
            update_test_model = SubmitTestInfo.query.filter(
                and_(SubmitTestInfo.title == body["title"], SubmitTestInfo.appId == body["appId"])).first()
            update_test_model.sendEmail = flag
            db.session.commit()
        else:
            current_app.logger.info('不发送邮件')
        return JsonResponse.success().to_dict()
    except Exception as e:
        err_msg = '提测失败了:' + str(e)
        return JsonResponse.error(msg=err_msg).to_dict()


@test_manager.route("/api/test/info", methods=['GET'])
def getTestInfo():
    test_id = request.args.get('id')
    if not test_id:
        error_message = '提测ID不能为空'
        return JsonResponse.error(msg=error_message).to_dict()
    test_model=SubmitTestInfo.query.filter(SubmitTestInfo.id==test_id).first()
    test_info = serialize(test_model)
    appid = serialize(test_model)['appId']
    app_model = Apps.query.get(appid)
    app = serialize(app_model)
    test_info["appName"] = app["appId"]
    test_info["appId"] = app["id"]
    res_data = test_info
    return JsonResponse.success(data=res_data).to_dict()


@test_manager.route("/api/test/update", methods=['POST'])
def updateReqeust():
    form = SubmitTestForm(data=request.get_json())
    if form.validate():
        # 获取传递的数据，并转换成JSON
        body = request.get_json()
        current_app.logger.info(body)
        if 'appId' not in body:
            error_message = 'appId 提测应用不能为空'
            return JsonResponse.error(msg=error_message).to_dict()
        elif 'tester' not in body:
            error_message = 'tester 测试人员不能为空'
            return JsonResponse.error(msg=error_message).to_dict()
        elif 'developer' not in body:
            error_message = 'developer 提测人不能为空'
            return JsonResponse.error(msg=error_message).to_dict()
        elif 'title' not in body:
            error_message = 'title提测标题不能为空'
            return JsonResponse.error(msg=error_message).to_dict()

        check_test_model = db.session.query(SubmitTestInfo,Apps.appId).filter(and_(SubmitTestInfo.appId==Apps.id,SubmitTestInfo.isDel==0,Apps.isDel==0,SubmitTestInfo.id==body['id'])).all()
        if len(check_test_model) == 1:
            test_json = serialize(check_test_model[0][0])
            test_json["appName"] = check_test_model[0][1]
            old_test_info = test_json
        else:
            return JsonResponse.error(msg='原有数据请求查询异常！').to_dict()
        test_model = SubmitTestInfo.query.filter(SubmitTestInfo.id==body["id"]).first()
        test_model.title=body["title"]
        test_model.appId = body["appId"]
        test_model.developer=body["developer"]
        test_model.tester=body["tester"]
        test_model.CcMail=body["CcMail"]
        test_model.test_version=body["test_version"]
        test_model.type=body["type"]
        test_model.scope=body["scope"]
        test_model.gitCode=body["gitCode"]
        test_model.wiki = body["wiki"]
        test_model.more=body["more"]
        test_model.updateUser=body["updateUser"]
        test_model.version = (serialize(test_model)["version"]) + 1
        db.session.commit()
        if 'isEmail' in body and body['isEmail'] == 'true':
            # 新建成功发送Email
            if body['type'] == 1:
                rquest_type = '功能测试'
            elif body['type'] == 2:
                rquest_type = '性能测试'
            elif body['type'] == 3:
                rquest_type = '安全测试'
            receivers = body["tester"].split(',') + body["developer"].split(',')
            if not body["CcMail"] is None:
                receivers = receivers + body["CcMail"].split(',')
            subject = '【提测】' + body['title']
            contents = []
            contents.append('<strong>[提测应用]</strong><br />')

            if old_test_info and old_test_info['appName'] != body['appName']:
                contents.append(old_test_info['appName'] + '变更为:' + body['appName'])
            else:
                contents.append(body['appName'])

            contents.append('<br /><strong>[提测人]</strong><br />')
            if old_test_info and old_test_info['developer'] != body['developer']:
                contents.append(old_test_info['developer'] + '变更为:' + body['developer'])
            else:
                contents.append(body['developer'])

            contents.append('<br /><strong>[提测版本]</strong><br />')
            if old_test_info and old_test_info['test_version'] != body['test_version']:
                contents.append(old_test_info['test_version'] + '变更为:' + body['test_version'])
            else:
                contents.append(body['developer'])

            contents.append('<br /><strong>[测试内容]</strong><br />')
            if old_test_info and old_test_info['scope'] != body['scope']:
                contents.append(old_test_info['scope'] + '变更为:' + body['scope'])
            else:
                contents.append(body['scope'])
            contents.append('<br /><strong>[相关文档]</strong><br />')
            if old_test_info and old_test_info['wiki'] != body['wiki']:
                contents.append(old_test_info['wiki'] + '变更为:' + body['wiki'])
            else:
                contents.append(body['wiki'])

            contents.append('<br /><strong>[补充信息]</strong><br />')
            if old_test_info and old_test_info['more'] != body['more']:
                contents.append(old_test_info['more'] + '变更为:' + body['more'])
            else:
                contents.append(body['more'])
            neirong = ''
            for content in contents:
                neirong += content
            msg = Message(recipients=receivers, subject=subject, html=neirong)
            try:
                mail.send(msg)
                flag = 1
            except Exception as e:
                flag = 2
                current_app.logger.info('发送失败{}'.format(e))

            update_test_model = SubmitTestInfo.query.filter(SubmitTestInfo.id == body['id']).first()
            update_test_model.updateUser = body["updateUser"]
            update_test_model.sendEmail = flag
            db.session.commit()

        else:
            current_app.logger.info('不发送邮件！')
        return JsonResponse.success().to_dict()
    else:
        return JsonResponse.error(msg='数据版本不一致，请刷新页面重试！').to_dict()


@test_manager.route("/api/test/change", methods=['POST'])
def changeStatus():
    reqbody = request.get_json()
    current_app.logger.info('body:{}'.format(reqbody))
    if 'id' not in reqbody:
        error_msg = '提测ID不能为空'
        return JsonResponse.error(msg=error_msg).to_dict()
    elif 'status' not in reqbody:
        error_msg = '更改的状态不能为空'
        return JsonResponse.error(msg=error_msg).to_dict()
    test_info_model = SubmitTestInfo.query.filter(SubmitTestInfo.id == reqbody['id']).first()
    if reqbody['status'] == 'start':
        test_info_model.status = 2
        succ_msg = '状态流转成功，进入测试阶段。'
    elif reqbody['status'] == 'delete':
        test_info_model.isDel = 1
        succ_msg = '提测已被删除!'
    else:
        err_msg = '状态标记错误'
        return JsonResponse.error(msg=err_msg).to_dict()
    db.session.commit()
    return JsonResponse.success(msg=succ_msg).to_dict()


@test_manager.route("/api/report/upload", methods=['POST'])
def uploadFile():
    file_form = FileForm(CombinedMultiDict([request.form, request.files]))
    if file_form.validate():
        # 保存文件的相对路径
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('STPService')[0], 'STPService/static')
        current_app.logger.info(save_path)
        attfile = request.files.get('file')
        file_name = secure_filename(attfile.filename)
        current_app.logger.info('file_name:{}'.format(file_name))
        attfile.save(os.path.join(save_path, file_name))
        resp_data = {"fileName": file_name}
        current_app.logger.info(resp_data)
        return JsonResponse.success(data=resp_data).to_dict()
    else:
        return JsonResponse.error(msg='文件校验不通过！{}'.format(file_form.errors),code=40000).to_dict()


@test_manager.route("/api/file/download", methods=['GET'])
def downloadFile():

    fileName = request.args.get('name')
    current_app.logger.info('fileName:{}'.format(fileName))
    save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('STPService')[0], 'STPService/static')
    current_app.logger.info(save_path)
    response = make_response(send_from_directory(save_path, fileName.encode('utf-8').decode('utf-8'), as_attachment=True))
    current_app.logger.info(response)
    response.headers["Content-Disposition"] = "attachment; filename={0}; filename*=utf-8''{0}".format(quote(fileName))
    return response



@test_manager.route("/api/report/save", methods=['POST'])
def saveTestReport():
    # 获取传递的数据，并转换成JSON
    body = request.get_json()
    # 判断必填参数
    if 'id' not in body:
        message = 'id 提测ID不能为空'
        return JsonResponse.error(msg=message).to_dict()
    elif 'test_desc' not in body:
        message =  'test_desc 测试结论不能为空'
        return JsonResponse.error(msg=message).to_dict()

    try:
        test_info_model = SubmitTestInfo.query.filter(SubmitTestInfo.id==body['id']).first()
        current_app.logger.info(test_info_model)
        test_info_model.status = body["status"]
        test_info_model.test_desc = body["test_desc"]
        test_info_model.test_risks = body["test_risks"]
        test_info_model.test_cases = body['test_cases']
        test_info_model.test_bugs = body["test_bugs"]
        test_info_model.test_file = body["test_file"]
        test_info_model.test_note = body["test_note"]
        test_info_model.updateUser = body["updateUser"]
        db.session.commit()

        if 'isEmail' in body and body['isEmail'] == 'true':
            # with connection.cursor() as cursor:
            #     select_result = "select * from submit_test_info where id={}".format(body["id"])
            #     cursor.execute(select_result)
            #     reports = cursor.fetchall()
            #     connection.commit()
            test_model = SubmitTestInfo.query.filter(SubmitTestInfo.id==body['id']).first()

            if test_model:
                report = serialize(test_model)
                receivers = report["developer"].split(',') + report["tester"].split(',')
                if report["CcMail"] is not None:
                    receivers = receivers + report["CcMail"].split(',')

                subject = '【测试报告】' + report['title']
                contents = []
                contents.append('<strong>[测试结果]</strong>')
                if report["status"] == 3:
                    contents.append("测试通过")
                elif report["status"] == 4:
                    contents.append("测试失败")
                elif report["status"] == 9:
                    contents.append("测试废弃")

                if report['test_desc'] != "":
                    contents.append('<strong>[结论描述]</strong>')
                    contents.append(body['test_desc'])

                if report['test_risks'] != "":
                    contents.append('<strong>[风险提示]</strong>')
                    contents.append(body['test_risks'])

                if report['test_cases'] != "":
                    contents.append('<strong>[测试CASE]</strong>')
                    contents.append(body['test_cases'])

                if report['test_bugs'] != "":
                    contents.append('<strong>[缺陷列表]</strong>')
                    contents.append(body['test_bugs'])

                if report['test_note'] != "":
                    contents.append('<strong>[备 注]</strong>')
                    contents.append(body['test_note'])

                # 附件添加
                if report['test_file']:
                    path_file = os.path.abspath(os.path.join(os.getcwd())) + '/static/' + report['test_file']
                    attachments = [path_file]
                else:
                    current_app.logger.info('邮件没附件📎')
                neirong = ''
                for content in contents:
                    neirong += content

                msg = Message(recipients=receivers, subject=subject, html=neirong)
                try:
                    mail.send(msg)
                    sendOk = 1
                except Exception as e:
                    sendOk = 2
                    current_app.logger.info('发送失败{}'.format(e))
                test_model.test_email = sendOk
                test_model.updateUser = body["updateUser"]
                db.session.commit()
            else:
                message = '准备发送邮件，！'
                return JsonResponse.error(msg=message).to_dict()
        else:
            current_app.logger.info('不发邮件！')
        return JsonResponse.success().to_dict()
    except Exception as err:
        message = '提测失败了{}'.format(err)
        return JsonResponse.error(msg=message).to_dict()


@test_manager.route("/api/report/info", methods=['GET'])
def getTestReoprt():
    report_id = request.args.get('id')
    if not report_id:
        message = '提测 id 不能为空'
        return JsonResponse.error(msg=message).to_dict()
    test_info_model = SubmitTestInfo.query.filter(SubmitTestInfo.id==report_id).first()
    current_app.logger.info(serialize(test_info_model))
    res_data = serialize(test_info_model)
    return JsonResponse.success(res_data).to_dict()
