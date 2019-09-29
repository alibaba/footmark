"""
Represents an ECS Network Interface
"""
from footmark.ecs.ecsobject import TaggedECSObject


class NetworkInterfaceSet(TaggedECSObject):
    """
    Represents an network interface.
    """

    def __init__(self, connection=None):
        super(NetworkInterfaceSet, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'NetworkInterface:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.network_interface_id
        if name == 'name':
            return getattr(self, "network_interface_name", "")
        if name == 'state':
            return self.status
        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def __setattr__(self, name, value):
        if name == 'id':
            self.network_interface_id = value
        if name == 'name':
            self.network_interface_name = value
        if name == 'status':
            value = value.lower()
        if name == 'state':
            self.status = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                if tag.get('tag_key'):
                    v[tag.get('tag_key')] = tag.get('tag_value', None)
            value = v
        super(TaggedECSObject, self).__setattr__(name, value)

    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False):
        """
        Update the network interface's state information by making a call to fetch
        the current interface attributes from the service.
        """
        rs = self.connection.describe_network_interfaces(network_interface_ids=[self.id])
        if rs:
            self._update(rs)
        elif validate:
            raise ValueError('%s is not a valid Network Interface ID' % self.id)
        return self.state

    def get(self):
        """
        Attach the network interface with an instance.
        """
        res = self.connection.describe_network_interfaces(network_interface_ids=[self.id])
        if res:
            return res[0]
        return None

    def attach(self, instance_id):
        """
        Attach the network interface with an instance.
        """
        if instance_id and not self.instance_id:
            return self.connection.attach_network_interface(network_interface_id=self.id, instance_id=instance_id)
        return False

    def detach(self, instance_id):
        """
        Detach the network interface from an instance.
        """
        if self.instance_id and self.instance_id == instance_id:
            return self.connection.detach_network_interface(network_interface_id=self.id, instance_id=instance_id)
        return False

    def modify(self, security_group_ids=None, name=None, description=None):
        """
        Modify the network interface.
        """
        params = {}
        if security_group_ids and sorted(security_group_ids) != sorted(self.security_group_ids["security_group_id"]):
            params['security_group_ids'] = security_group_ids
        if name and name != self.name:
            params['network_interface_name'] = name
        if description and description != self.description:
            params['description'] = description
        if params:
            params['network_interface_id'] = self.id
            return self.connection.modify_network_interface_attribute(**params)
        return False

    def delete(self):
        """
        Terminate the network interface
        """
        return self.connection.delete_network_interface(network_interface_id=self.id)

    def add_tags(self, tags):
        """
        Add tags
        """
        if tags:
            remain = {}
            for key, value in list(tags.items()):
                if key in list(self.tags.keys()) and value == self.tags[key]:
                    continue
                remain[key] = value
            if remain:
                return self.connection.add_tags(resource_id=self.id, resource_type="eni", tags=remain)
        return False

    def remove_tags(self, tags):
        """
        remove tags
        """
        if tags:
            remain = {}
            for key, value in list(tags.items()):
                if key not in list(self.tags.keys()):
                    continue
                remain[key] = value
            if remain:
                return self.connection.remove_tags(resource_id=self.id, resource_type="eni", tags=tags)
        return False

    def read(self):
        eni = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue

            if name == "network_interface_id":
                eni['id'] = value

            if name == 'private_ip_sets':
                temp = []
                for ip in value["private_ip_set"]:
                    temp.append({
                        'private_ip_address': ip["private_ip_address"],
                        'primary_address': ip["primary"]
                    })
                name = "private_ip_addresses"
                value = temp

            if name == "security_group_ids":
                name = "security_groups"
                value = value['security_group_id']

            if name == 'network_interface_name':
                name = 'name'

            if name == 'status':
                name = 'state'
                value = str(value).lower()

            eni[name] = value
        return eni
