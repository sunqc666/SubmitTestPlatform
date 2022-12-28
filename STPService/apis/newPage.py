# -*- coding:utf-8 -*-

from flask import Blueprint

import pymysql.cursors
from flask import request
import json
from STPService.configs import config

app_newpage = Blueprint('newpage',__name__,url_prefix='/testPage')

@app_newpage.route('/api/newpage/test')
def new_page():
    # print(request.url)
    data = [{
        "date": "2016-05-02",
        "name": "王小虎",
        "address": "上海市弄"
      },{
        "date": "2016-05-02",
        "name": "王小虎",
        "address": "上海市弄"
      }]

    resp_data = {
        "code": 20000,
        "data": data
    }
    return resp_data

@app_newpage.route('/api/newpage/commit',methods=['POST'])
def get_commit():
    print(request.url)
    # print(request.get_json())
    data = json.dumps(request.get_json())
    print(data)
    return {
        "code": 20000,
        "message": "success",
        "data": data
    }