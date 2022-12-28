# -*- coding:utf-8 -*-

from flask import request
from flask import Blueprint
import requests
import json
from STPService.comment.format import JsonResponse
from flask import current_app

app_updateEs = Blueprint("operateEs", __name__)
@app_updateEs.route("/api/operateEs",methods=['POST'])
def updateEs():
    try:
        data = request.get_json()
        current_app.logger.info("request:{}".format(data))
        url = "http://{}/{}/{}/{}/_update?pretty".format(data["host"],data["index"],data["type"],data["id"])
        body = {"doc": {}}
        for field in data["field"]:
            if field["type"] == "number":
                if '.' in field["value2"]:
                    field["value2"] = float(field["value2"])
                else:field["value2"] = int(field["value2"])
            if field["type"] == "bool":
                if field["value2"] == "true":
                    field["value2"] = True
                else: field["value2"] = False
            body["doc"][field["value1"]] = field["value2"]
        payload = json.dumps(
            body
        )
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res_data=json.loads(response.text)
        current_app.logger.info("response:{}".format(res_data))
        return JsonResponse.success(data=res_data).to_dict()
    except Exception as e:
        return JsonResponse.error(msg='更新失败，请检查参数').to_dict()