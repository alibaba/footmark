"""
Exception classes - Subclassing allows you to check for specific errors
"""

StandardError = Exception


class ResultSet(object):
    """
    General Footmark Client error (error accessing Aliyun)
    """

    def __repr__(self):
        return 'ResultSet:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.request_id
        raise AttributeError

    def __setattr__(self, name, value):
        super(object, self).__setattr__(name, value)
