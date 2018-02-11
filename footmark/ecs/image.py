class image(object):
    """description of class"""

"""
Represents an ECS Image
"""
from footmark.ecs.ecsobject import TaggedECSObject


class Image(TaggedECSObject):
    def __init__(self, connection=None):
        super(Image, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Image:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.image_id
        if name == 'name':
            return self.image_name
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.image_id = value
        if name == 'name':
            self.image_name = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedECSObject, self).__setattr__(name, value)

    def delete(self):
        """
        Terminate the image
        """
        return self.connection.delete_image(self.id)



