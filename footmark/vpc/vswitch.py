"""
Represents an VPC Security Group
"""
from footmark.vpc.vpcobject import TaggedVPCObject


class VSwitch(TaggedVPCObject):
    def __init__(self, connection=None):
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
                v[tag.get('key')] = tag.get('value', None)
            value = v
        if name.startswith('subnet_'):
            setattr(self, 'vswitch' + name[6:], value)
        super(TaggedVPCObject, self).__setattr__(name, value)

    def modify(self, name=None, description=None):
        params = {}
        if name and self.vswitch_name != name:
            params['vswitch_name']=name
        if description and self.description != description:
            params['description'] = description
        if params:
            params['vswitch_id'] = self.vswitch_id
            return self.connection.modify_vswitch_attribute(**params)
        return False

    def get(self):
        return self.connection.describe_vswitch_attribute(vswitch_id=self.vswitch_id)

    def delete(self):
        return self.connection.delete_vswitch(vswitch_id=self.vswitch_id)

    def read(self):
        vswitch = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue

            if name == 'vswitch_id':
                vswitch['id'] = value
                vswitch['subnet_id'] = value

            if name == 'status':
                name = 'state'
                value = str(value).lower()

            vswitch[name] = value
        return vswitch

    def add_tags(self, tags):
        """
        Add tags
        """
        return self.connection.tag_resources(resource_ids=[self.id], tags=tags, resource_type='vswitch')

    def remove_tags(self, tags):
        """
        remove tags
        """
        return self.connection.un_tag_resources(resource_ids=[self.id], tags=tags, resource_type='vswitch')
