# -*- coding:utf-8 -*-


from flask import Blueprint,current_app

from STPService.comment.format import JsonResponse
from flask import request
import pymysql.cursors
import json
from sqlalchemy import func,and_
from STPService.comment.models.submit_test_info import SubmitTestInfo
from STPService.comment.models.apps import Apps
from STPService.comment.models import db


test_dashboard = Blueprint("test_dashboard", __name__)

@test_dashboard.route("/api/dashboard/stacked", methods=['POST'])
def get_request_stacked():
    current_app.logger.info('66666')
    # logger.add(current_app.config.get('LOG_PATH'))
    table_data=db.session.query(func.date_format(SubmitTestInfo.createDate,"%Y%u").label("weeks"),Apps.note,func.count(Apps.id)).\
        join(Apps,SubmitTestInfo.appId==Apps.id).\
        group_by("weeks",Apps.note).all()
    # print(table_data)
    # 第一次循环过滤生成week和notes，并生成做临时关键词储备数据，
    # 用户第二次循环生成 series 需要数据
    weeks = []
    notes = []
    key_value = {}
    for row in table_data:
        week = row[0]
        note = row[1]
        if not week in weeks:
            weeks.append(week)
        if not note in notes:
            notes.append(note)
        key_value[week+note] = row[2]
    # 做一个排序 小到大
    weeks.sort()
    # 做对应日期下应用数据列表生成，没有数据的week用0填充，保证顺序长度一致
    series = {}
    for note in notes:
        series[note] = []
        for week in weeks:
            if week+note in key_value:
                series[note].append(key_value[week+note])
            else:
                series[note].append(0)
    resp_data = {
        'weeks': weeks,
        'note': notes,
        'series': series
    }
    return JsonResponse.success(data=resp_data).to_dict()


@test_dashboard.route("/api/dashboard/metadata", methods=['POST'])
def get_request_stacked_metadata():
    body = request.get_json()
    resp_data = []
    current_app.logger.info("request：{}".format(body))
    if 'date' in body and body['date'] is not None and len(body['date']) > 0:
        start_date = body['date'][0]
        end_date = body['date'][1]
        data_model = db.session.query(func.date_format(SubmitTestInfo.createDate,"%Y%u").label("weeks"),Apps.note,func.count(Apps.id)).filter(and_(SubmitTestInfo.createDate>start_date,SubmitTestInfo.createDate<end_date)).join(Apps,SubmitTestInfo.appId==Apps.id).group_by("weeks",Apps.note).all()
    else:
        data_model = db.session.query(func.date_format(SubmitTestInfo.createDate,"%Y%u").label("weeks"),Apps.note,func.count(Apps.id)).join(Apps,SubmitTestInfo.appId==Apps.id).group_by("weeks",Apps.note).all()
    for data in data_model:
        resp_data.append({
            "weeks":data[0],
            "note":data[1],
            "counts":data[2]
        })
    return JsonResponse.success(data=resp_data).to_dict()

