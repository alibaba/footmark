# #!/usr/bin/env python
# # import sys
# # sys.path.append("../../..")
#
# from tests.unit import OSSMockServiceTestCase
# from footmark.oss.bucket import Bucket
# import json
#
# CREATE_FOLDER = '''
# '''
#
# class Key():
#     key = "myKey"
#
# class LIST_OBJECTS():
#     object_list=[Key()]
#
#
# DELETE_OBJECTS = '''
# '''
#
# CREATE_BUCKET = '''
# '''
#
# DELETE_BUCKET = '''
# '''
#
# SIMPLE_UPLOAD = '''
# '''
#
#
# class TestCreateBucket(OSSMockServiceTestCase):
#     connection_class = Bucket
#
#     permission = "private"
#
#     def default_body(self):
#         return CREATE_BUCKET
#
#     def test_create_bucket(self):
#         self.set_http_response(status_code=200)
#         changed, result = self.service_connection.create_bucket(permission=self.permission)
#         if changed is True:
#             self.assertEqual(result[0], 'Bucket Created Successfully')
#
#
# class TestDeleteBucket(OSSMockServiceTestCase):
#     connection_class = Bucket
#
#     def default_body(self):
#         return DELETE_BUCKET
#
#     def test_delete_bucket(self):
#         self.set_http_response(status_code=200)
#         changed, result = self.service_connection.delete_bucket()
#         if changed is True:
#             self.assertEqual(result[0], 'Bucket Deleted Successfully')
#
#
# class TestSimpleUpload(OSSMockServiceTestCase):
#     connection_class = Bucket
#
#     bucket_name = "tushar"
#     src = "D:\local_file.txt"
#     file_name = "remote.txt"
#     headers = {
#         "Content-Type": "text/html",
#         "Content-Encoding": "MD5"
#
#     }
#     metadata = {
#         "x-oss-meta-key": "value"
#     }
#     expiration = "30"
#     encrypt = None
#     overwrite = None
#
#     def default_body(self):
#         return SIMPLE_UPLOAD
#
#     def test_simple_upload(self):
#         self.set_http_response(status_code=200)
#         changed, result = self.service_connection.simple_upload(
#             expiration=self.expiration, headers=self.headers, encrypt=self.encrypt, metadata=self.metadata,
#             overwrite=self.overwrite, src=self.src, file_name=self.file_name)
#         if changed is True:
#             self.assertEqual(result[0], 'File uploaded Successfully')
#
#
# class TestCreateBucketFolder(OSSMockServiceTestCase):
#     connection_class = Bucket
#
#     folder_name = 'test/'
#
#     def default_body(self):
#         return CREATE_FOLDER
#
#     def test_create_folder(self):
#         self.set_http_response(status_code=200)
#         changed, result = self.service_connection.create_folder(self.folder_name)
#         self.assertEqual(changed, True)
#
#
# class TestListBucketObjects(OSSMockServiceTestCase):
#     connection_class = Bucket
#
#     marker = 'my'
#     max_keys = 100
#
#     def default_body(self):
#         return LIST_OBJECTS
#
#     def test_list_objects(self):
#         self.set_http_response(status_code=200)
#         keys, result = self.service_connection.list_bucket_objects(marker=self.marker, max_keys=self.max_keys)
#         self.assertEqual(result[0], 'Bucket objects retrieved successfully')
#
# class TestDeleteBucketObjects(OSSMockServiceTestCase):
#     connection_class = Bucket
#
#     objects_to_delete= ["myKey", "myDocs/"]
#
#     def default_body(self):
#         return DELETE_OBJECTS
#
#     def test_delete_objects(self):
#         self.set_http_response(status_code=200)
#         changed, results = self.service_connection.delete_bucket_objects(objects=self.objects_to_delete)
#         self.assertEqual(changed, True)
#
#
#
#
#
