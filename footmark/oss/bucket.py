# encoding: utf-8
"""
Represents a connection to the OSS service.
"""

from footmark.oss.connection import OSSConnection
import oss2
import yaml

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


class Bucket(OSSConnection): 
    """ 
    Object Storage Services
    """

    def __init__(self, acs_access_key_id, acs_secret_access_key,
                 region, bucket_name, user_agent=None):
        """
        Init method to create a new bucket object.
        """
        super(Bucket, self).__init__(acs_access_key_id, acs_secret_access_key, region, bucket_name)
        self.bucket_name = bucket_name
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
        # self.grant = self.bucket.get_bucket_acl()

    def __getattr__(self, name):
        if name in ('id', 'name'):
            return self.bucket_name
        if name in ('permission', 'acl', 'grant'):
            return self.bucket.get_bucket_acl().acl
        if name == 'location':
            return self.bucket.get_bucket_location().location
        raise AttributeError

    def __setattr__(self, name, value):
        if name in ('id', 'name'):
            self.bucket_name = value
        if name in ('permission', 'acl'):
            self.grant = value
        super(OSSConnection, self).__setattr__(name, value)

    def create(self, permission):
        """
        Create a New Bucket
        :type permission: str
        :param permission: This option lets the user set the canned permissions on the bucket that are created
        :return: Details of newly created bucket
        """
        if self.is_exist():
            raise Exception("Error, Bucket with same name already exist.")

        self.bucket.create_bucket(permission=permission).headers

        return self

    def is_exist(self):
        """
        Verify bucket is exist
        :return: boolean value representing bucket existence
        """
        return self.is_bucket_exist(self.bucket_name)

    def delete(self):
        """
        Delete a Bucket
        :return: Returns status of operation
        """
        return self.bucket.delete_bucket()

    def put_acl(self, permission):
        """
        Update bucket acl
        :type permission: str
        :param permission: New bucket acl
        :rtype: class
        :return: Return the current bucket
        """
        self.bucket.put_bucket_acl(permission)
        setattr(self, 'grant', permission)
        return self

    def put_object(self, key, data, overwrite=False, headers=None, progress_callback=None):
        """
        Upload data to an object
        :type key: str
        :param key: Object name in bucket
        :type headers: dict
        :param headers: Custom headers for GET operation 
        :type data: str
        :param data: The content will be uploaded
        :type overwrite: bool
        :param overwrite: Whether overwrite existing object content. 
        If it is false and the specified object type is Appendable Object, the operation will append new content to it.
        :type progress_callback: str
        :param progress_callback: The callback function of upload progress
        :rtype class
        :return: `PutObjectResult <oss2.models.PutObjectResult>`
        """
        if headers and not isinstance(headers, dict):
            headers = yaml.load(headers)

        if not overwrite:
            position = 0
            if self.is_object_exist(key):
                obj = self.get_object_info(key)
                if obj.type != 'Appendable':
                    raise Exception('The specified object {0} is not Appendable. If you want to append it,'
                                    ' please remove it or put a new Appendable Object.'.format(key))
                position = obj.size
            return self.bucket.append_object(key, position, data, headers=headers, progress_callback=progress_callback)

        return self.bucket.put_object(key=key, data=data, headers=headers, progress_callback=progress_callback).headers

    def put_object_from_file(self, key, filename, overwrite=False, headers=None, progress_callback=None):
        """
        Upload a local file to an object
        :type key: str
        :param key: Object name in bucket
        :type headers: dict
        :param headers: Custom headers for GET operation 
        :type filename: str
        :param filename: The name of file used to upload
        :type overwrite: bool
        :param overwrite: Whether overwrite existing object content. 
        If it is false and the specified object type is Appendable Object, the operation will append new content to it.
        :type progress_callback: str
        :param progress_callback: The callback function of upload progress
        :rtype class
        :return: `PutObjectResult <oss2.models.PutObjectResult>`
        """
        if headers and not isinstance(headers, dict):
            headers = yaml.load(headers)

        if not overwrite:
            position = 0
            if self.is_object_exist(key):
                obj = self.get_object_info(key)
                if obj.type != 'Appendable':
                    raise Exception('The specified object {0} is not Appendable. If you want to append it,'
                                    ' please remove it and put a new Appendable Object.'.format(key))
                position = obj.size
            return self.bucket.append_object(key, position, open(filename).read(), headers=headers, progress_callback=progress_callback)

        return self.bucket.put_object_from_file(key, filename, headers=headers, progress_callback=progress_callback)

    def put_object_acl(self, key, permission):
        """
        Update object acl
        :type permission: str
        :param permission: New object acl
        :rtype: class
        :return: `RequestResult <oss2.models.RequestResult>`
        """
        return self.bucket.put_object_acl(key, permission)

    def is_object_exist(self, key):
        """
        Verify if object exists in Bucket
        :type key: str
        :param key: object key to verify for existence
        :rtype: bool
        :return: boolean value representing object existence
        """
        return self.bucket.object_exists(key)

    def update_object_headers(self, key, headers):
        """
        Upload a object's headers info
        :type key: str
        :param key: Object name in bucket
        :type headers: dict
        :param headers: Custom headers for GET operation 
        :rtype class
        :return: `RequestResult <oss2.models.RequestResults>`
        """
        if headers and not isinstance(headers, dict):
            headers = yaml.load(headers)
        return self.bucket.update_object_meta(key, headers)

    def get_object(self, key, byte_range=None, headers=None, progress_callback=None):
        """
        Download a object's content
        :type key: str
        :param key: Object name to download in bucket
        :type headers: dict
        :param headers: Custom headers for GET operation 
        :type byte_range: str
        :param byte_range: The range of content that would be download.
        Its format like 1-100 that indicates range from one to hundred bytes of object.
        :type progress_callback: str
        :param progress_callback: The callback function of download progress
        :rtype str
        :return: Download Object content
        """
        if headers and not isinstance(headers, dict):
            headers = yaml.load(headers)
        return self.bucket.get_object(key, byte_range=byte_range, headers=headers,
                                      progress_callback=progress_callback)

    def get_object_to_file(self, key, filename, byte_range=None, headers=None, progress_callback=None):
        """
        Download a object to a specified file
        :type key: str
        :param key: Object name to download in bucket
        :type headers: dict
        :param headers: Custom headers for GET operation 
        :type filename: str
        :param filename: The name of file used to store object content
        :type byte_range: str
        :param byte_range: The range of content that would be download.
        Its format like 1-100 that indicates range from one to hundred bytes of object.
        :type progress_callback: str
        :param progress_callback: The callback function of download progress
        :rtype object
        :return: Download Object file
        """
        if headers and not isinstance(headers, dict):
            headers = yaml.load(headers)

        if byte_range:
            byte_range=str.split(byte_range, '-')

        return self.bucket.get_object_to_file(key, filename, byte_range=byte_range, headers=headers,
                                              progress_callback=progress_callback)

    def get_object_info(self, key):
        """
        Get an specified Bucket Object Info
        :type key: str
        :param key: object name to retrieve in bucket.
        :rtype class: <oss2.models.SimplifiedObjectInfo>
        :return one specified object info
        """
        max_keys = 500

        while True:
            objects = self.list_objects(prefix=key, max_keys=max_keys)
            for obj in objects:
                if key == obj.key:
                    return obj
            if len(objects) < max_keys:
                return None

    def list_objects(self, prefix='', marker="", max_keys=100):
        """
        Lists Bucket Objects Info
        :type str
        :param prefix: retrieving all objects that have one specified prefix
        :type marker: str
        :param marker: the key to start with when using list mode. Object keys are returned in alphabetical order, 
         starting with key after the marker in order.
        :type max_keys: int
        :param max_keys: Max number of results to return in list mode
        :rtype List class: <oss2.models.SimplifiedObjectInfo>
        :return list of retrieved objects
        """

        return self.bucket.list_objects(prefix=prefix, marker=marker, max_keys=max_keys).object_list

    def delete_object(self, key):
        """
        Delete Object in Bucket
        :type key: str
        :param key: Object name to delete in bucket
        :rtype: bool
        :return: Whether delete object successfully
        """

        return self.bucket.delete_object(key)

    def delete_objects(self, keys):
        """
        Delete Objects in Bucket
        :type keys: list
        :param keys: objects to delete in bucket
        :rtype: bool
        :return: whether delete objects successfully
        """

        return self.bucket.batch_delete_objects(keys)

