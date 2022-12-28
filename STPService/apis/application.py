# -*- coding:utf-8 -*-


from flask import Blueprint
from STPService.comment.format import JsonResponse
from flask import request
import json
from STPService.comment.forms import AppsForm
from STPService.comment.models.apps import Apps
from STPService.comment.models.products import Products
from STPService.comment.models import db
from STPService.comment.modelToJson import serialize
from sqlalchemy import and_

app_application = Blueprint("app_application", __name__)


@app_application.route("/api/application/list", methods=['GET'])
def application_list():
    data = []
    app_models = Apps.query.filter(Apps.status == 0).all()
    for app in app_models:
        data.append(serialize(app))
    # 按返回模版格式进行json结果返回
    return JsonResponse.success(data=data).to_dict()


@app_application.route("/api/application/search", methods=['POST'])
def searchBykey():
    try:
        body = request.get_json()
        print(body)
        productId = body['productId']
        appId = body['appId']
        data = []
        pageSize = 10 if body['pageSize'] is None else body['pageSize']
        currentPage = 1 if body['currentPage'] is None else body['currentPage']
        if (productId is None or productId == '') and appId is None:
            app_models = Apps.query.filter(Apps.status == 0).offset((currentPage - 1) * pageSize).limit(pageSize)
            all_app_models = Apps.query.filter(Apps.status == 0).all()
            total = len(all_app_models)
            print(total)
            for p in app_models:
                data.append(serialize(p))
        else:
            all_product_models = Apps.query.filter(and_(Apps.status == 0, Apps.productId.like('%{}%'.format(productId)),
                                                        Apps.appId.like('%{}%'.format(appId)))).all()
            total = len(all_product_models)
            app_models = Apps.query.filter(and_(Apps.status == 0, Apps.productId.like('%{}%'.format(productId)),
                                                Apps.appId.like('%{}%'.format(appId)))).offset(
                (currentPage - 1) * pageSize).limit(pageSize)
            for app in app_models:
                product = app.product
                app_dick = serialize(app)
                app_dick["productTitle"] = product.title
                data.append(app_dick)
    except Exception as e:
        return JsonResponse.error(msg=str(e)).to_dict()
    # print(data)
    return JsonResponse.success(data=data,total=total).to_dict()


@app_application.route("/api/application/update", methods=['POST'])
def application_update():
    form = AppsForm(data=request.json)
    if form.validate():
        # 获取传递的数据，并转换成JSON
        body = request.get_json()
        # 判断必填参数
        if 'appId' not in body:
            error_message = '应用不能为空'
            return JsonResponse.error(msg=error_message).to_dict()
        elif 'tester' not in body:
            error_message = '测试负责人不能为空'
            return JsonResponse.error(msg=error_message).to_dict()
        elif 'developer' not in body:
            error_message = '测试负责人不能为空'
            return JsonResponse.error(msg=error_message).to_dict()
        elif 'producer' not in body:
            error_message = '产品负责人不能为空'
            return JsonResponse.error(msg=error_message).to_dict()

        if not body.get('note'):
            body['note'] = ''
        if not body.get('CcEmail'):
            body['CcEmail'] = ''
        if not body.get('gitCode'):
            body['gitCode'] = ''
        if not body.get('wiki'):
            body['wiki'] = ''
        if not body.get('more'):
            body['more'] = ''
        if not body.get('createUser'):
            body['createUser'] = ''
        if not body.get('updateUser'):
            body['updateUser'] = ''

        # 如果传的值有ID，那么进行修改操作，否则为新增数据
        if 'id' in body and body['id'] != '':
            app = Apps.query.get(body['id'])
            app.id = body['id']
            app.productId = body['productId']
            app.note = body["note"]
            app.tester = body["tester"]
            app.developer = body["developer"]
            app.producer = body['producer']
            app.CcEmail = body["CcEmail"]
            app.version = serialize(app)["version"]+1
            app.gitCode = body["gitCode"]
            app.wiki = body["wiki"]
            app.more = body["more"]
            app.updateUser = body["updateUser"]
            db.session.commit()
            return JsonResponse.success().to_dict()
        else:
            # 新增需要判断appId是否重复
            result = Apps.query.filter(Apps.appId == body['appId']).all()
            # 有数据说明存在相同值，封装提示直接返回
            if result:
                error_msg = "唯一编码keyCode已存在"
                return JsonResponse.error(msg=error_msg).to_dict()
            else:
                new_app_model = Apps(appId=body['appId'], productId=body['productId'], note=body["note"],
                                     tester=body["tester"],
                                     developer=body["developer"], producer=body['producer'], CcEmail=body["CcEmail"],
                                     gitCode=body["gitCode"],
                                     wiki=body["wiki"], more=body["more"], status=0, createUser=body["createUser"])
                db.session.add(new_app_model)
                db.session.commit()
                return JsonResponse.success().to_dict()
    else:
        return JsonResponse.error(msg='数据版本不一致，请刷新后重试！').to_dict()


@app_application.route("/api/application/product", methods=['GET'])
def getProduct():
    data=[]
    products = Products.query.order_by(Products.update.desc()).all()
    for p in products:
        product = serialize(p)
        data.append(product)
    return JsonResponse.success(data=data).to_dict()


@app_application.route("/api/application/options", methods=['GET'])
def getOptionsForSelected():
    value = request.args.get('value', '')
    data=[]
    dataByppId = Apps.query.filter(Apps.appId.like('%{}%'.format(value))).all()
    if len(dataByppId) > 0:
        for app in dataByppId:
            data.append(serialize(app))
    else:
        dataByppNote = Apps.query.filter(Apps.note.like('%{}%'.format(value))).all()
        for app in dataByppNote:
            data.append(serialize(app))
    return JsonResponse.success(data=data).to_dict()


@app_application.route("/api/application/delete", methods=['POST'])
def app_delete():
    try:
        body = request.get_json()
        id = body['id']
        print(id)
        app_model = Apps.query.filter(Apps.id == id).first()
        if app_model:
            db.session.delete(app_model)
            db.session.commit()
            return JsonResponse.success().to_dict()
        else:
            err_msg = "app不存在，请刷新页面"
            return JsonResponse.error(msg=err_msg).to_dict()
    except Exception as e:
        err_msg = e
        return JsonResponse.error(msg=err_msg).to_dict()


@app_application.route("/api/application/remove", methods=['POST'])
def app_remove():
    try:
        body = request.get_json()
        id = body['id']
        app_model = Apps.query.get(id)
        app_model.status = 1
        db.session.commit()
        return JsonResponse.success().to_dict()
    except Exception as e:
        return JsonResponse.error(msg=e).to_dict()
