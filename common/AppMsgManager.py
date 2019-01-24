from threading import Lock

from common.AppMsg import AppMsg


class AppMsgManager:
    msgDict = {}
    # lock = Lock()

    def __init__(self):
        pass



    def addMsg(self, msg):
        # self.lock.acquire(True)
        self.msgDict[msg.getUniqueId()] = msg
        # self.lock.release()

    def delMsg(self, msg):
        # self.lock.acquire(True)
        del self.msgDict[msg.getUniqueId()]
        # self.lock.release()

    def upvoteMsg(self, id, userId):
        self.msgDict[id].incScore(userId)

    def debugPrint(self):
        for val in self.msgDict.values():
            print("score:" + str(val.getScore()))
            print("  id:" + str(val.getUniqueId()))
            print("  msg:" + str(val.getMsg()))

    def prepareEncode(self):
        return {
            'msgs': [y.prepareEncode() for y in self.msgDict.values()],
            '__class__': 'AppMsgManager'
        }

    def _decodeJson(self, jsonDict):
        if jsonDict['__class__'] != 'AppMsgManager':
            self.invalid = 1
        jsonMsgs = jsonDict['msgs']
        msgs = [AppMsg(msg) for msg in jsonMsgs]
        self.msgDict = {msg.id: msg for msg in msgs}