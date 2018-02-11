"""
Represents an VPC Security Group
"""
from footmark.vpc.vpcobject import TaggedVPCObject


class Vpc(TaggedVPCObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(Vpc, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Vpc:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.vpc_id
        if name == 'name':
            return self.vpc_name
        if name == 'router_id':
            return self.vrouter_id
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.vpc_id = value
        if name == 'name':
            self.vpc_name = value
        if name == 'router_id':
            self.vrouter_id = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedVPCObject, self).__setattr__(name, value)

    def update(self, name=None, description=None, user_cidr=None):
        """
        Update vpc's attribute
        """
        return self.connection.modify_vpc(self.id, vpc_name=name, description=description, user_cidr=user_cidr)

    def delete(self):
        """
        Terminate the vpc
        """
        return self.connection.delete_vpc(self.id)
