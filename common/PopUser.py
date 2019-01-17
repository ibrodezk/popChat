import uuid
from asyncio import Lock


class User:
    def __init__(self, user_name):
        self.user_name = user_name
        self.user_id = str(uuid.uuid4())
        self.invalid = 0
    def getUniqueId(self):
        return self.id

    def getUserName(self):
        return self.user_name

    def prepareEncode(self):
        return {
            'user_name': self.user_name,
            '__class__': 'User'
        }

    def _decodeJson(self, jsonDict):
        if jsonDict['__class__'] != 'User':
            self.invalid = 1
        self.user_name = self.user_name