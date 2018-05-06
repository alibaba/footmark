
from footmark.ram.ramobject import TaggedRAMObject
class AccessKey(TaggedRAMObject):
    def __init__(self, connection=None):
        super(AccessKey, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'AccessKey:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.access_key_id
        if name == 'secret':
            return self.access_key_secret
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.access_key_id = value
        if name == 'secret':
            self.secret = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRAMObject, self).__setattr__(name, value)

    def delete(self,user_name):
        """
        delete the access_key
        """
        return self.connection.delete_access_key(user_name,self.id)
