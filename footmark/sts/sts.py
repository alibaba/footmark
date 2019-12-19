"""
Represents an VPC Security Group
"""
from footmark.sts.stsobject import TaggedSTSObject


class Sts(TaggedSTSObject):
    def __init__(self, connection=None):
        super(Sts, self).__init__(connection)

    def __repr__(self):
        return 'Ram:%s' % self.id

    def __getattr__(self, name):
        if name == 'AccessKeyId':
            return self.access_key_id
        if name == 'AccessKeySecret':
            return self.access_key_secret
        if name == 'SecurityToken':
            return self.security_token

    def __setattr__(self, name, value):
        super(TaggedSTSObject, self).__setattr__(name, value)

    def read(self):
        ram = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name in ['credentials', 'assumed_role_user']:
                for key, value in value.items():
                    ram[key] = value
            ram[name] = value
        return ram

