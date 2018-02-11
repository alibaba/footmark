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

        return getattr(self, name, None)

    def __setattr__(self, name, value):
        if name in ('id', 'eip_id'):
            self.allocation_id = value
        if name in ('ip', 'eip', 'eip_address'):
            self.ip_address = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedVPCObject, self).__setattr__(name, value)
    
    def associate(self, instance_id):
        """
        bind eip
        """
        if self.status != 'Available':
            raise Exception('EIP {0} current status {1} does not support association.'.format(self.id, self.status))
        return self.connection.associate_eip(self.id, instance_id)

    def disassociate(self, instance_id):
        """
        unbind eip
        """
        return self.connection.disassociate_eip(self.id, instance_id)
    
    def release(self):
        """
        release eip
        """
        return self.connection.release_eip(self.id)
    
    def modify(self, bandwidth):
        """
        modify eip
        """
        if int(self.bandwidth) == int(bandwidth):
            return False
        return self.connection.modify_eip(self.id, bandwidth)
    
    
   
