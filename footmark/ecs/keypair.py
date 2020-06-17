"""
Represents an ECS key pair
"""
from footmark.ecs.ecsobject import TaggedECSObject


class KeyPair(TaggedECSObject):
    """
    Represents an ECS key pair.

    :ivar id: The unique ID of the key pair.
    :ivar name: The name of the key pair.
    :ivar create_time: The timestamp of when the key pair was created.
    :ivar finger_print: The finger print of the key pair, see RFC4716.
    :ivar private_key: The private key of key pair in format PEM PKCS#8.
    """

    def __init__(self, connection=None):
        super(KeyPair, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'KeyPair:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.key_pair_id
        if name == 'name':
            return self.key_pair_name
        if name == 'finger_print':
            return self.key_pair_finger_print
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.key_pair_id = value
        if name == 'name':
            self.key_pair_name = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedECSObject, self).__setattr__(name, value)

    def import_key(self, name=None, public_key_body=None):
        """
        Import a key pair
        """
        params = {}

        if name and self.key_pair_name != name:
            params['key_pair_name'] = name
        if public_key_body:
            params['public_key_body'] = public_key_body
        if params:
            return self.connection.import_key_pair(**params)

        return False

    def delete(self):
        return self.connection.delete_key_pair(key_pair_names=[self.name])

    def get(self):
        return self.connection.describe_key_pairs(key_pair_name=self.name)

    def read(self):
        key_pairs = {}

        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue
            if name == 'key_pair_id':
                key_pairs['id'] = value
            if name == 'key_pair_name':
                key_pairs['name'] = value
            if name == 'finger_print':
                key_pairs['finger_print'] = value
            key_pairs[name] = value
        return key_pairs
