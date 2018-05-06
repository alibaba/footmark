
from footmark.ram.ramobject import TaggedRAMObject


class User(TaggedRAMObject):
    def __init__(self, connection=None):
        super(User, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'User:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.user_id
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.user_id = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRAMObject, self).__setattr__(name, value)

    def delete(self):
        """
        delete user

        :type user_name: str
        :param user_name: The name of user

        """
        return self.connection.delete_user(self.user_name)
