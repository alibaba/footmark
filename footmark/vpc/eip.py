"""
Represents an VPC Security Group
"""
from footmark.vpc.vpcobject import TaggedVPCObject


class Eip(TaggedVPCObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(Eip, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Eip:%s' % self.id

    def __getattr__(self, name):
        if name in ('id', 'eip_id'):
            return self.allocation_id
        if name in ('ip', 'eip', 'eip_address'):
            return self.ip_address

        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'status':
            value = str.lower(value)
        if name in ('ip', 'eip', 'eip_address'):
            self.ip_address = value
        if name == 'descritpion':
            name = 'description'
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('key')] = tag.get('value', None)
            value = v
        super(TaggedVPCObject, self).__setattr__(name, value)

    def get(self):
        return self.connection.describe_eip_addresses(allocation_id=self.id)[0]
    
    def associate(self, instance_id):
        """
        bind eip
        """
        if str(self.status).lower() == 'inuse':
            if self.instance_id == instance_id:
                return False
            raise Exception('EIP {0} current status {1} does not support association.'.format(self.id, self.status))
        instance_type = "EcsInstance"
        if str(instance_id).startswith("lb-"):
            instance_type = "SlbInstance"
        if str(instance_id).startswith("nat-"):
            instance_type = "Nat"
        if str(instance_id).startswith("havip-"):
            instance_type = "HaVip"
        if str(instance_id).startswith("eni-"):
            instance_type = "NetworkInterface"

        return self.connection.associate_eip_address(allocation_id=self.id, instance_id=instance_id, instance_type=instance_type)

    def unassociate(self, instance_id):
        """
        unbind eip
        """
        if str(self.status).lower() == 'available':
            return False
        return self.connection.unassociate_eip_address(allocation_id=self.id, instance_id=instance_id)
    
    def release(self):
        """
        release eip
        """
        return self.connection.release_eip_address(allocation_id=self.id)
    
    def modify(self, bandwidth=None, name=None, description=None):
        """
        modify eip
        """
        params = {}
        if bandwidth and int(self.bandwidth) != int(bandwidth):
            params['bandwidth'] = bandwidth
        if name and self.name != name:
            params['name'] = name
        if description and self.description != description:
            params['description'] = description
        if params:
            params['allocation_id'] = self.allocation_id
            return self.connection.modify_eip_address_attribute(**params)
        return False

    def read(self):
        eip = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "available_regions", "operation_locks", "resource_group_id",
                        "has_reservation_data", "hdmonitor_status", "isp"]:
                continue

            if name == 'allocation_id':
                eip['id'] = value

            eip[name] = value
        return eip

    def add_tags(self, tags):
        """
        Add tags
        """
        return self.connection.tag_resources(resource_ids=[self.id], tags=tags, resource_type='eip')

    def remove_tags(self, tags):
        """
        remove tags
        """
        return self.connection.un_tag_resources(resource_ids=[self.id], tags=tags, resource_type='eip')

