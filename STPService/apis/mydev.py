# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request
import json
from STPService.comment.models import db
from STPService.comment.models.apps import Apps
from STPService.comment.models.submit_test_info import SubmitTestInfo
from sqlalchemy import func ,and_
from STPService.comment.modelToJson import serialize
from STPService.comment.format import JsonResponse


mydev = Blueprint("mydev", __name__)
@mydev.route('/api/mydev/search',methods=["POST"])
def search_mydev():
    body = request.get_json()
    # 获取pageSize和
    pageSize = 10 if 'pageSize' not in body or body['pageSize'] is None else body['pageSize']
    currentPage = 1 if 'currentPage' not in body or body['currentPage'] is None else body['currentPage']
    # response = format.resp_format_success
    # print(response)
    res_data = []
    search = and_(
        Apps.productId.like('%{}%'.format(body['productId'])),
        SubmitTestInfo.appId.like('%{}%'.format(body['appId'])),
        SubmitTestInfo.tester.like('%{}%'.format(body['tester'])),
        SubmitTestInfo.developer.like('%{}%'.format(body['developer'])),
        SubmitTestInfo.status.like('%{}%'.format(body['status']))
    )
    if 'pickTime' in body and body['pickTime'] != '' and body['pickTime']:
        search = and_(
            Apps.productId.like('%{}%'.format(body['productId'])),
            SubmitTestInfo.appId.like('%{}%'.format(body['appId'])),
            SubmitTestInfo.tester.like('%{}%'.format(body['tester'])),
            SubmitTestInfo.developer.like('%{}%'.format(body['developer'])),
            SubmitTestInfo.status.like('%{}%'.format(body['status'])),
            SubmitTestInfo.createDate >= body['pickTime'][0],
            SubmitTestInfo.createDate <= body['pickTime'][1]
        )
    # 排序和页数拼接
    total = db.session.query(func.count(SubmitTestInfo.id)).filter(
        and_(SubmitTestInfo.appId == Apps.id, SubmitTestInfo.isDel == 0, search)).scalar()
    test_model = SubmitTestInfo.query.filter(
        and_(SubmitTestInfo.appId == Apps.id, SubmitTestInfo.isDel == 0, search)).order_by(
        SubmitTestInfo.updateDate.desc()).offset((currentPage - 1) * pageSize).limit(pageSize).all()

    for test in test_model:
        test = serialize(test)
        developer_list = str(test['developer']).split(',')
        if body['op_user'] in developer_list:
            res_data.append(test)
    return JsonResponse.success(data=res_data,total=len(res_data)).to_dict()
