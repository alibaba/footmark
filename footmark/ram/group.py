
from footmark.ram.ramobject import TaggedRAMObject


class Group(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Group, self).__init__(connection)
        self.tags = {}

    def __getattr__(self, name):
        if name == 'name':
            return self.group_name
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'name':
            self.group_name = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRAMObject, self).__setattr__(name, value)

    def delete(self):
        """
        delete the ram group
        """
        return self.connection.delete_group(self.group_name)
