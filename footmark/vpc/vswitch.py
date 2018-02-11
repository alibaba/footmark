"""
Represents an VPC Security Group
"""
from footmark.vpc.vpcobject import TaggedVPCObject


class VSwitch(TaggedVPCObject):
    def __init__(self, connection=None, ):
        super(VSwitch, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'VSwitch:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.vswitch_id
        if name == 'subnet_id':
            return self.vswitch_id
        if name == 'name':
            return self.vswitch_name
        if name.startswith('subnet_'):
            return getattr(self, 'vswitch' + name[6:])
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.vswitch_id = value
        if name == 'name':
            self.vswitch_name = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        if name.startswith('subnet_'):
            setattr(self, 'vswitch' + name[6:], value)
        super(TaggedVPCObject, self).__setattr__(name, value)

    def update(self, name=None, description=None):
        """
        Update vswitch's attribute
        """
        return self.connection.modify_vswitch(self.id, vswitch_name=name, description=description)

    def delete(self):
        """
        Terminate the vswitch
        """
        return self.connection.delete_vswitch(self.id)
