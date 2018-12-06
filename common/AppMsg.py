import uuid
class AppMsg:
    msg = ""
    score = 0
    invalid = 0
    id = 0
    def __init__(self):
        Exception('invalid constructor appMsg')
    def __init__(self, jsonDict):
        self._decodeJson(jsonDict)

    def __init__(self, msg, score):
        self.msg = msg
        self.score = score
        self.id = str(uuid.uuid4()) + msg

    def validate(self):
        return not self.invalid

    def getUniqueId(self):
        return self.id

    def setScore(self, score):
        self.score = score

    def incScore(self):
        self.score += 1

    def setMsg(self, msg):
        self.msg = str(msg)

    def getScore(self):
        return self.score

    def getMsg(self):
        return self.msg

    def prepareEncode(self):
        return {
            'msg': self.msg,
            'score': self.score,
            '__class__': 'appMsg'

        }

    def _decodeJson(self, jsonDict):
        if jsonDict['__class__'] != 'appMsg':
            self.invalid = 1
        self.msg = jsonDict['msg']
        self.score = jsonDict['score']