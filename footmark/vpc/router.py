"""
Represents an VPC Security Group
"""
from footmark.vpc.vpcobject import TaggedVPCObject


class RouteTable(TaggedVPCObject):
    def __init__(self, connection=None, ):
        super(RouteTable, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'RouteTable:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.route_table_id
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.route_table_id = value
        super(TaggedVPCObject, self).__setattr__(name, value)


class RouteEntry(TaggedVPCObject):
    def __init__(self, connection=None, ):
        super(RouteEntry, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'RouteEntry:%s' % self.destination_cidrblock

    def __getattr__(self, name):
        if name == 'destination_cidrblock':
            return self.destination_cidr_block
        if name == 'next_hop_id':
            return self.instance_id
        if name.startswith('nexthop_'):
            return getattr(self, 'next_hop' + name[7:])
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'destination_cidrblock':
            self.destination_cidr_block = value
        if name == 'next_hop_id':
            self.instance_id = value
        if name.startswith('nexthop_'):
            setattr(self, 'next_hop' + name[7:], value)
        super(TaggedVPCObject, self).__setattr__(name, value)
