
from footmark.ram.ramobject import TaggedRAMObject
class LoginProfile(TaggedRAMObject):
    def __init__(self, connection=None):
        super(LoginProfile, self).__init__(connection)
        self.tags = {}

    def __setattr__(self, name, value):
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRAMObject, self).__setattr__(name, value)

    def delete(self,user_name):
        """
        delete the login_profile
        """
        return self.connection.delete_login_profile(user_name)
