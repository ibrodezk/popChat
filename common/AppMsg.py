import uuid
from asyncio import Lock

from common.timeUtils import getCurrentMili


class AppMsg:
    msg = ""
    score = 0
    invalid = 0
    id = 0
    userId = 0
    likeList = []
    # lock = Lock()
    def __init__(self, msg, score, userId):
        self.msg = msg
        self.score = score
        self.id = str(uuid.uuid4())
        self.userId = userId
        self.likeList.append(userId)
        self.time = getCurrentMili()

    def validate(self):
        return not self.invalid

    def setScore(self, score):
        self.score = score

    def incScore(self, userId):
        # self.lock.acquire(True)
        if(userId not in self.likeList):
            self.score += 1
            self.likeList.append(self.userId)
        # self.lock.release(False)

    def setMsg(self, msg):
        self.msg = str(msg)

    def getUniqueId(self):
        return self.id

    def getScore(self):
        return self.score

    def getMsg(self):
        return self.msg

    def getUserId(self):
        return self.userId

    def prepareEncode(self):
        return {
            'msg': self.msg,
            'score': self.score,
            'id': self.id,
            'time': self.time,
            'user_id': self.userId,
            '__class__': 'AppMsg'
        }

    def _decodeJson(self, jsonDict):
        if jsonDict['__class__'] != 'AppMsg':
            self.invalid = 1
        self.msg = jsonDict['msg']
        self.score = jsonDict['score']
        self.id = jsonDict['id']
        self.time = jsonDict['time']
        self.userId = jsonDict['user_id']