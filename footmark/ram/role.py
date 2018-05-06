
from footmark.ram.ramobject import TaggedRAMObject


class Role(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Role, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Role:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.role_id
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.role_id = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRAMObject, self).__setattr__(name, value)

    def delete(self,role_name):
        """
        delete the role
        """
        return self.connection.delete_role(role_name)
