# -*- coding:utf-8 -*-
from flask import Blueprint
from STPService.comment.format import JsonResponse
from flask import request,current_app
import json
from STPService.comment.models.products import Products
from STPService.comment.modelToJson import serialize
from STPService.comment.models import db
from sqlalchemy import and_
from STPService.comment.forms import ProductForm


app_product = Blueprint("app_product", __name__)

# 搜索接口
@app_product.route("/api/product/search",methods=['GET'])
def product_search():
    data=[]
    # 获取title和keyCode
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')
    # 如果title不为空，拼接tilite的模糊查询
    current_app.logger.info("request:{}".format(request.args))
    try:
        product_models = Products.query.filter(and_(Products.title.like('%{}%'.format(title)),Products.keyCode.like('%{}%'.format(keyCode)))).all()
        for p in product_models:
            data.append(serialize(p))
        # 按返回模版格式进行json结果返回
    except Exception as e:
        return JsonResponse.error(msg=e).to_dict()
    # logger.info("response:{}".format(data))
    return JsonResponse.success(data=data)

@app_product.route("/api/product/searchPage",methods=['GET'])
def product_search_page():
    # 获取title和keyCode
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')
    current_app.logger.info("request:{}".format(request.args))
    data=[]
    # 新增页数和每页个数参数，空时候做默认处理，并注意前端传过来可能是字符串，需要做个强制转换
    pageSize = 10 if request.args.get('pageSize') is None else int(request.args.get('pageSize'))
    currentPage = 1 if request.args.get('currentPage') is None else int(request.args.get('currentPage'))
    try:
        if (title is None or title=='') and keyCode is None:

            product_models = Products.query.offset((currentPage - 1) * pageSize).limit(pageSize)
            all_product_models = Products.query.all()
            total = len(all_product_models)
            # product_models = Products.query.filter(and_(Products.title.like('%{}%'.format(title)),Products.keyCode.like('%{}%'.format(keyCode)))).offset((currentPage - 1) * pageSize).limit(pageSize)
            for p in product_models:
                data.append(serialize(p))
        else:

            if keyCode is None:
                keyCode = ''
            print(title,keyCode)
            all_product_models = Products.query.filter(and_(Products.title.like('%{}%'.format(title)),Products.keyCode.like('%{}%'.format(keyCode)))).all()
            total = len(all_product_models)
            product_models = Products.query.filter(and_(Products.title.like('%{}%'.format(title)),Products.keyCode.like('%{}%'.format(keyCode)))).offset((currentPage - 1) * pageSize).limit(pageSize)
            for p in product_models:
                data.append(serialize(p))
    except Exception as e:
        return JsonResponse.error(msg=e).to_dict()
    # logger.info("response:{}{}".format(data,total))
    return JsonResponse.success(data=data,total=total).to_dict()


@app_product.route("/api/product/list", methods=['GET'])
def product_list():
    data=[]
    product_models = Products.query.filter(Products.status==0).all()
    for p in product_models:
        data.append(serialize(p))
    # 按返回模版格式进行json结果返回
    # logger.info("response:{}".format(data))
    return JsonResponse.success(data=data).to_dict()


# [POST方法]实现新建数据的数据库插入
@app_product.route("/api/product/create",methods=['POST'])
def product_create():
    form = ProductForm(data=request.json)
    if form.validate():
        body = request.get_json()
        product_model = Products.query.filter(Products.keyCode == body['keyCode']).first()
        if product_model:
            err_msg = "唯一编码keyCode已存在"
            return JsonResponse.error(msg=err_msg).to_dict()
        else:
            new_product = Products(keyCode=body['keyCode'], title=body['title'], status=0, desc=body['desc'],
                                   operator=body['operator'], version=0)
            db.session.add(new_product)
            db.session.commit()
        return JsonResponse.success().to_dict()
    else:
        err_msg = form.errors
        return JsonResponse.error(msg=err_msg).to_dict()

# [POST方法]根据项目ID进行信息更新
@app_product.route("/api/product/update",methods=['POST'])
def product_update():
    # 获取请求传递json
    form = ProductForm(data=request.json)
    if form.validate():
        body = request.get_json()
        product = Products.query.filter(Products.id == body['id']).first()
        if product:
            if body["version"] == serialize(product)["version"]:
                product.keyCode = body["keyCode"]
                product.title = body["title"]
                product.desc = body["desc"]
                product.operator = body["operator"]
                product.version = (serialize(product)["version"]) + 1
                db.session.commit()
                return JsonResponse.success().to_dict()
            else:
                err_msg = "数据不是最新版本，请刷新后重试！"
                current_app.logger.error(err_msg)
                return JsonResponse.error(msg=err_msg).to_dict()
        else:
            err_msg = "更新失败，无此数据"
            return JsonResponse.error(msg=err_msg).to_dict()
    else:
        err_msg = form.errors
        current_app.logger.exception(err_msg)
        return JsonResponse.error(msg="数据不是最新版本，请刷新后重试!").to_dict()


# [DELETE方法]根据id实际删除项目信息
@app_product.route("/api/product/delete", methods=['DELETE'])
def product_delete():
    # 方式1：通过params 获取id
    ID = request.args.get('id')
    # 做个参数必填校验
    if ID is None:
        err_msg = "请求id参数为空"
        return JsonResponse.error(msg=err_msg).to_dict()
    try:
        product_model = Products.query.get(ID)
        db.session.delete(product_model)
        db.session.commit()
        return JsonResponse.success().to_dict()
    except Exception as e:
        return JsonResponse.error(msg=e).to_dict()


# [POST方法]根据id更新状态项目状态，做软删除
@app_product.route("/api/product/remove", methods=['POST'])
def product_remove():
    ID = request.args.get('id')
    # 做个参数必填校验
    if ID is None:
        err_msg = "请求id参数为空"
        return JsonResponse.error(msg=err_msg).to_dict()
    try:
        product_model = Products.query.get(ID)
        product_model.status = 1
        db.session.commit()
        return JsonResponse.success().to_dict()
    except Exception as e:
        return JsonResponse.error(msg=e).to_dict()

