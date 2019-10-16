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
        if name == 'id':
            return self.route_entry_id
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

    def modify(self, name=None):
        """
        Update route_entry's name
        """
        params = {}
        if name and self.route_entry_name != name:
            params['route_entry_name'] = name
        if params:
            params['route_entry_id'] = self.route_entry_id
            return self.connection.modify_route_entry(**params)
        return False

    def get(self):
        return self.connection.get_route_entry_attribute(route_table_id=self.route_table_id, destination_cidrblock=self.destination_cidrblock)

    def read(self):
        route_entry = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue
            route_entry[name] = value
        return route_entry


