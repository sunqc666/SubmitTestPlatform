# -*- coding:utf-8 -*-

from flask import request,current_app
import json
from STPService.comment.forms import LoginForm,AddUserForm
from flask import Blueprint
from STPService.comment.models.user import UserModel
from werkzeug.security import check_password_hash,generate_password_hash
from STPService.comment.models import db
from STPService.comment.format import JsonResponse


app_user = Blueprint("app_user", __name__)

@app_user.route("/api/user/login",methods=['POST'])
def login():
    form = LoginForm(data=request.json)
    username=form.username.data
    password=form.password.data
    if form.validate():
        user_model = UserModel.query.filter(UserModel.user_name==username).first()
        if user_model:
            if check_password_hash(user_model.password_md5,password):
                res_data={"token":"{}".format(username)}
                return JsonResponse.success(data=res_data).to_dict()
            else:
                error_message = "密码错误"
                return JsonResponse.error(msg=error_message).to_dict()
        else:
            error_message = "账号不存在"
            return JsonResponse.error(msg=error_message).to_dict()
    else:
        error_message ="账号密码错误"
        return JsonResponse.error(msg=error_message).to_dict()


@app_user.route("/api/user/info",methods=['GET'])
def info():
    # 获取GET中请求token参数值
    token = request.args.get('token')
    user_model=UserModel.query.filter(UserModel.user_name==token).first()
    if token == user_model.user_name:
        result_data={
                "roles":["admin"],
                "introduction":"",
                "avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                "name":"{}".format(token)}
        current_app.logger.info("登录用户：{}".format(token))
        return JsonResponse.success(data=result_data).to_dict()
    else:
        error_message= "用户信息获取错误"
        return JsonResponse.error(msg=error_message).to_dict()

@app_user.route("/api/user/logout",methods=['POST'])
def logout():
    return JsonResponse.success().to_dict()

@app_user.route("/api/user/user_list",methods=['POST'])
def user_list():
    user_models=UserModel.query.all()
    table_data=[]
    for user in user_models:
        table_data.append({"username":user.user_name,"mail":user.mail,"date":user.join_time})
    res_data = table_data
    return JsonResponse.success(data=res_data).to_dict()


@app_user.route("/api/user/add_user",methods=['POST'])
def add_user():
    form = AddUserForm(data=request.json)
    if form.validate():
        try:
            user_model=UserModel(user_name=form.username.data,password=form.password.data,
                                 password_md5=generate_password_hash(form.password.data),mail=form.mail.data)
            db.session.add(user_model)
            db.session.commit()
            return JsonResponse.success(data="添加成功").to_dict()
        except Exception as e:
            message = "{}".format(e)
            return JsonResponse.error(msg=message).to_dict()
    else:
        message="表单校验不通过，请检查"
        return JsonResponse.error(msg=message).to_dict()




