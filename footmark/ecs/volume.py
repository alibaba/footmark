"""
Represents an ECS Elastic Block Storage Volume
"""
from footmark.ecs.ecsobject import TaggedECSObject


class Disk(TaggedECSObject):
    """
    Represents an EBS volume.

    :ivar id: The unique ID of the volume.
    :ivar create_time: The timestamp of when the volume was created.
    :ivar status: The status of the volume.
    :ivar size: The size (in GB) of the volume.
    :ivar snapshot_id: The ID of the snapshot this volume was created
        from, if applicable.
    :ivar attach_data: An AttachmentSet object.
    :ivar zone: The availability zone this volume is in.
    :ivar type: The type of volume (standard or consistent-iops)
    :ivar iops: If this volume is of type consistent-iops, this is
        the number of IOPS provisioned (10-300).
    :ivar encrypted: True if this volume is encrypted.
    """

    def __init__(self, connection=None):
        super(Disk, self).__init__(connection)
        self.tag = {}

    def __repr__(self):
        return 'Disk:%s' % self.id

    def __getattr__(self, name):
        if name.startswith('volume'):
            return getattr(self, 'disk' + name[6:])
        if name == 'id':
            return self.disk_id
        if name == 'name':
            return self.disk_name
        if name == 'state':
            return self.status
        if name == 'delete_on_termination':
            return self.delete_with_instance
        raise AttributeError

    def __setattr__(self, name, value):
        if name.startswith('volume'):
            return setattr(self, 'disk' + name[6:])
        if name == 'id':
            self.disk_id = value
        if name == 'name':
            self.disk_name = value
        if name == 'status':
            value = value.lower()
        if name == 'state':
            self.status = value
        if name == 'delete_on_termination':
            self.delete_with_instance = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedECSObject, self).__setattr__(name, value)

    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False):
        """
        Update the data associated with this volume by querying ECS.

        :type validate: bool
        :param validate: By default, if ECS returns no data about the
                         volume the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from ECS.
        """
        # Check the resultset since Eucalyptus ignores the volumeId param
        unfiltered_rs = self.connection.get_all_volumes([self.id])
        rs = [x for x in unfiltered_rs if x.id == self.id]
        if len(rs) > 0:
            self._update(rs[0])
        # rs = self.connection.get_all_volumes([self.id])
        # if len(rs) > 0:
        #     for r in rs:
        #         if r.id == self.id:
        #             self._update(r)
        elif validate:
            raise ValueError('%s is not a valid Volume ID' % self.id)
        return self.status

    def attach(self, instance_id, delete_with_instance=None):
        """
        Attach disk to an instance.

        :type instance_id: str
        :param instance_id: The Id of instance.
        """
        return self.connection.attach_disk(self.id, instance_id, delete_with_instance=delete_with_instance)

    def detach(self, instance_id):
        """
        Attach disk to an instance.

        :type instance_id: str
        :param instance_id: The Id of instance.
        """
        return self.connection.detach_disk(self.id, instance_id)

    def delete(self):
        """
        Attach disk to an instance.

        :type instance_id: str
        :param instance_id: The Id of instance.
        """
        return self.connection.delete_disk(self.id)

    def modify(self, disk_name=None, description=None, delete_with_instance=None):
        """
        Attach disk to an instance.

        :type instance_id: str
        :param instance_id: The Id of instance.
        """
        return self.connection.modify_disk(self.id, disk_name=disk_name, description=description, delete_with_instance=delete_with_instance)
