import serpy


class APIStatusCode():
    SUCCESS = 0
    ERROR = 500


class APIStatusMessage():
    SUCCESS = ''
    ERROR = '서버 에러가 발생하였습니다.'


class APIResult(object):

    def __init__(self):
        self.status = APIStatusCode.SUCCESS
        self.message = APIStatusMessage.SUCCESS

    def __dict__(self):
        return { 'status': self.status, 'message': self.message }


class APIResultSerializer(serpy.Serializer):
    status = serpy.IntField()
    message = serpy.StrField()
