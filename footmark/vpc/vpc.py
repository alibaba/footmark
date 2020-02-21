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
                v[tag.get('key')] = tag.get('value', None)
            value = v
        super(TaggedVPCObject, self).__setattr__(name, value)

    def modify(self, vpc_name=None, description=None):
        """
        Update vpc's attribute
        """
        params = {}
        if vpc_name and self.name != vpc_name:
            params['vpc_name'] = vpc_name
        if description and self.description != description:
            params['description'] = description
        if params:
            params['vpc_id'] = self.vpc_id
            return self.connection.modify_vpc_attribute(**params)
        return False

    def get(self):
        return self.connection.describe_vpc_attribute(vpc_id=self.id)

    def read(self):
        vpc = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue

            if name == 'vpc_id':
                vpc['id'] = value

            if name == 'status':
                name = 'state'
                value = str(value).lower()

            if name == 'user_cidrs':
                value = value['user_cidr']

            if name == 'vswitch_ids':
                value = value['vswitch_id']

            vpc[name] = value
        return vpc

    def delete(self):
        """
        Terminate the vpc
        """
        return self.connection.delete_vpc(vpc_id=self.id)

    # def add_tags(self, tags):
    #     """
    #     Add tags
    #     """
    #     remain = {}
    #     if tags:
    #         for key, value in list(tags.items()):
    #             if key in list(self.tags.keys()) and value == self.tags[key]:
    #                 continue
    #             remain[key] = value
    #     if remain:
    #         return self.connection.tag_resources(resource_ids=[self.id], resource_type="vpc", tags=remain)
    #     return False
    #
    # def remove_tags(self, tags):
    #     """
    #     remove tags
    #     """
    #     remain = []
    #     if tags:
    #         for key, value in list(tags.items()):
    #             if key not in list(self.tags.keys()):
    #                 continue
    #             remain.append(key)
    #     if remain:
    #         return self.connection.un_tag_resources(resource_ids=[self.id], resource_type="vpc", tag_keys=remain)
    #     return False

    def add_tags(self, tags):
        """
        Add tags
        """
        return self.connection.tag_resources(resource_ids=[self.id], tags=tags, resource_type='VPC')

    def remove_tags(self, tags):
        """
        remove tags
        """
        return self.connection.un_tag_resources(resource_ids=[self.id], tags=tags, resource_type='VPC')
