import uuid
from asyncio import Lock


class AppMsg:
    msg = ""
    score = 0
    invalid = 0
    id = 0
    # lock = Lock()

    def __init__(self):
        Exception('invalid constructor appMsg')

    def __init__(self, jsonDict):
        self._decodeJson(jsonDict)

    def __init__(self, msg, score):
        self.msg = msg
        self.score = score
        self.id = str(uuid.uuid4())

    def validate(self):
        return not self.invalid

    def setScore(self, score):
        # self.lock.acquire(True)
        self.score = score
        # self.lock.release(False)

    def incScore(self):
        # self.lock.acquire(True)
        self.score += 1
        # self.lock.release(False)

    def setMsg(self, msg):
        self.msg = str(msg)

    def getUniqueId(self):
        return self.id

    def getScore(self):
        return self.score

    def getMsg(self):
        return self.msg

    def prepareEncode(self):
        return {
            'msg': self.msg,
            'score': self.score,
            'id': self.id,
            '__class__': 'appMsg'
        }

    def _decodeJson(self, jsonDict):
        if jsonDict['__class__'] != 'appMsg':
            self.invalid = 1
        self.msg = jsonDict['msg']
        self.score = jsonDict['score']
        self.id = jsonDict['id']