
from flask import Flask,Blueprint,request
import datetime,time
from flask import current_app
from STPService.comment.format import JsonResponse
get_off_work = Blueprint('get_off_work',__name__)

@get_off_work.route('/api/getOffWorkTime',methods=['POST'])
def getOffWorkTime():
    body = request.json
    current_app.logger.info("request:{}".format(body))
    startTime = body['startWorkTime']
    restTime = body['restTime']
    dateTime_p = time.strptime(startTime,'%Y-%m-%d %H:%M:%S')
    startTime_sjc = int(time.mktime(dateTime_p))
    endTime_sjc = startTime_sjc+(8*60*60)+(restTime*60*60)
    time_local = time.localtime(endTime_sjc)
    getOffWorkTime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    current_app.logger.info("response:{}".format(getOffWorkTime))
    current_app.logger.info(JsonResponse.success(data=getOffWorkTime).to_dict())
    return JsonResponse.success(data=getOffWorkTime).to_dict()