
class JsonResponse(object):
    """
    统一的json返回格式
    """
    def __init__(self, data, code, message,total=0):
        self.data = data
        self.code = code
        self.message = message
        self.total = total

    @classmethod
    def success(cls, data=None, code=20000, msg='SUCCESS',total=0):
        return cls(data, code, msg,total)

    @classmethod
    def error(cls, data=None,msg="ERROR", code=-1):
        return cls(data, code, msg)

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data,
            "total":self.total
        }

if __name__=="__mail__":
    JsonResponse.success().to_dict()
