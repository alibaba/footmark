#!/usr/bin/env python
# import sys
# sys.path.append("../../..")
from footmark.ecs.connection import ECSConnection
from tests.unit import ACSMockServiceTestCase
import json

DESCRIBE_INSTANCE = '''
{
  "Instances": {
    "Instance": [
      {
        "CreationTime": "2016-06-20T21:37Z",
        "DeviceAvailable": true,
        "EipAddress": {},
        "ExpiredTime": "2016-10-22T16:00Z",
        "HostName": "xiaozhu_test",
        "ImageId": "centos6u5_64_40G_cloudinit_20160427.raw",
        "InnerIpAddress": {
          "IpAddress": [
            "10.170.106.80"
          ]
        },
        "InstanceChargeType": "PostPaid",
        "InstanceId": "i-94dehop6n",
        "InstanceNetworkType": "classic",
        "InstanceType": "ecs.s2.large",
        "InternetChargeType": "PayByTraffic",
        "InternetMaxBandwidthIn": -1,
        "InternetMaxBandwidthOut": 1,
        "IoOptimized": false,
        "OperationLocks": {
          "LockReason": []
        },
        "PublicIpAddress": {
          "IpAddress": [
            "120.25.13.106"
          ]
        },
        "RegionId": "cn-shenzhen",
        "SecurityGroupIds": {
          "SecurityGroupId": [
            "sg-94kd0cyg0"
          ]
        },
        "SerialNumber": "51d1353b-22bf-4567-a176-8b3e12e43135",
        "Status": "Running",
        "Tags":{
          "Tag":[
            {
              "TagValue":"1.20",
              "TagKey":"xz_test"
            },
            {
              "TagValue":"1.20",
              "TagKey":"xz_test_2"
            }
          ]
        },
        "VpcAttributes": {
          "PrivateIpAddress": {
            "IpAddress": []
          }
        },
        "ZoneId": "cn-shenzhen-a"
      }
    ]
  },
  "PageNumber": 1,
  "PageSize": 10,
  "RequestId": "14A07460-EBE7-47CA-9757-12CC4761D47A",
  "TotalCount": 1
}
'''

MANAGE_INSTANCE = '''
{
    "RequestId": "14A07460-EBE7-47CA-9757-12CC4761D47A",
}
'''

CREATE_INSTANCE = '''
{
    "InstanceId":"i-2zeg0900kzwn7dpo7zrb",
    "RequestId":"9206E7A7-BFD5-457F-9173-91CF4525DE21"
}
'''

MODIFY_INSTANCE = '''
{
       
        "changed": true,
        "instance_ids": ["i-rj97hhf9ue16ewoged75"],
        "result": [
            {
                "RequestId": "855267EE-BC10-49BB-847A-2A564B63178C"
            }
        ]
}
'''

GET_INSTANCE = '''
{
    "PageNumber": 1,
    "InstanceStatuses":
         {"InstanceStatus": [
            {"Status": "Running", "InstanceId": "i-2zehcagr3vt06iyir7hc"},
            {"Status": "Running", "InstanceId": "i-2zedup3d5p01daky1622"},
            {"Status": "Stopped", "InstanceId": "i-2zei2zq55lx87st85x2j"},
            {"Status": "Running", "InstanceId": "i-2zeaoq67u62vmkbo71o7"},
            {"Status": "Running", "InstanceId": "i-2ze5wl5aeq8kbblmjsx1"}
         ]},
        "TotalCount": 9,
        "PageSize": 5,
        "RequestId": "5D464158-D291-4C69-AA9E-84839A669B9D"
}
'''

JOIN_GROUP = '''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D"
}
'''

LEAVE_GROUP = '''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D"
}
'''

DETACH_DISK = '''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D",
    "TotalCount": 1,
    "Disks": {
        "Disk": [
            {
                "Category": "cloud_efficiency",
                "DeleteWithInstance": true,
                "AttachedTime": "2017-01-18T07:20:43Z",
                "CreationTime": "2017-01-18T07:20:42Z",
                "ExpiredTime": "2999-09-08T16:00Z",
                "EnableAutoSnapshot": true,
                "Type": "system",
                "DeleteAutoSnapshot": true,
                "Status": "In_use",
                "DiskName": "",
                "Description": "",
                "Tags": {
                    "Tag": []
                },
                "InstanceId": "i-2zehwdby6fkuv403fc6j",
                "RegionId": "cn-beijing",
                "ImageId": "m-256u3s01x",
                "SourceSnapshotId": "",
                "DiskId": "d-2ze9p2pzpwjqqx0burf5",
                "ProductCode": "jxsc000008",
                "AutoSnapshotPolicyId": "",
                "OperationLocks": {
                    "OperationLock": []
                },
                "ZoneId": "cn-beijing-b",
                "Device": "/dev/xvda",
                "EnableAutomatedSnapshotPolicy": false,
                "Portable": false,
                "DiskChargeType": "PostPaid",
                "DetachedTime": "",
                "Size": 40
            }
    ]
    }
}
'''

ATTACH_DISK = '''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D",
    "TotalCount": 1,
    "Disks": {        
        "Disk": [
            {
                "Category": "cloud_efficiency",
                "DeleteWithInstance": true,
                "AttachedTime": "2017-01-18T07:20:43Z",
                "CreationTime": "2017-01-18T07:20:42Z",
                "ExpiredTime": "2999-09-08T16:00Z",
                "EnableAutoSnapshot": true,
                "Type": "system",
                "DeleteAutoSnapshot": true,
                "Status": "available",
                "DiskName": "",
                "Description": "",
                "Tags": {
                    "Tag": []
                },
                "InstanceId": "i-2zehwdby6fkuv403fc6j",
                "RegionId": "cn-beijing",
                "ImageId": "m-256u3s01x",
                "SourceSnapshotId": "",
                "DiskId": "d-2ze9p2pzpwjqqx0burf5",
                "ProductCode": "jxsc000008",
                "AutoSnapshotPolicyId": "",
                "OperationLocks": {
                    "OperationLock": []
                },
                "ZoneId": "cn-beijing-b",
                "Device": "/dev/xvda",
                "EnableAutomatedSnapshotPolicy": false,
                "Portable": false,
                "DiskChargeType": "PostPaid",
                "DetachedTime": "",
                "Size": 40
            }
    ]
    }
}
'''

DELETE_DISK = '''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D"
} 
'''

Create_Security_Group ='''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D",
    "SecurityGroupId": "sg-2ze95f8a2ni6bb2wql3b"
}
'''

Authorize_Security_Group = '''
{
    "RequestId": "AF3991A3-5203-4F83-8FAD-FDC1253AF15D"
}
'''

DELETE_SECURITY_GROUP = '''
{
    "PageNumber":1,
    "TotalCount":1,
    "PageSize":10,
    "RequestId":"D8C42A44-7B92-40BC-9DAA-41B7EB733A6C",
    "RegionId":"us-west-1",
    "SecurityGroups":
    {
    "SecurityGroup":[
       {
         "CreationTime":"2016-12-15T06:48:05Z",
         "Tags":{"Tag":[]},
         "SecurityGroupId":"sg-rj9606ryhhy2c3t8ljtx",
         "Description":"",
         "SecurityGroupName":"est",
         "AvailableInstanceAmount":1000,
         "VpcId":""
         }]
    }
}
'''

GET_SECURITY_STATUS = '''
{
    "PageNumber": 1,
    "PageSize": 10,
    "RegionId": "cn-beijing",
    "RequestId": "2076C42F-7E15-4F69-926F-C404E6A2F0DD",
    "SecurityGroups": {
    "SecurityGroup": [
                    {
                        "AvailableInstanceAmount": 1000,
                        "CreationTime": "2016-12-19T04:54:38Z",
                        "Description": "",
                        "SecurityGroupId": "sg-2zegbxmrjvoz4ypz3kku",
                        "SecurityGroupName": "",
                        "Tags": {
                            "Tag": []
                        },
                        "VpcId": ""
                    },
                    {
                        "AvailableInstanceAmount": 1000,
                        "CreationTime": "2016-12-19T04:52:34Z",
                        "Description": "",
                        "SecurityGroupId": "sg-2zeaikpg8zhl7j5rrfnt",
                        "SecurityGroupName": "",
                        "Tags": {
                            "Tag": []
                        },
                        "VpcId": ""
                    },
                    {
                        "AvailableInstanceAmount": 1000,
                        "CreationTime": "2016-12-01T12:01:28Z",
                        "Description": "Allow inboud traffic for control nodes",
                        "SecurityGroupId": "sg-2ze80xuiw0b85tzbv7x9",
                        "SecurityGroupName": "hi-control",
                        "Tags": {
                            "Tag": []
                        },
                        "VpcId": "vpc-2zegy4zyl0nv0w5i1ay6j"
                    },
                    {
                        "AvailableInstanceAmount": 996,
                        "CreationTime": "2014-12-18T05:30:20Z",
                        "Description": "System created security group.",
                        "SecurityGroupId": "sg-25y6ag32b",
                        "SecurityGroupName": "sg-25y6ag32b",
                        "Tags": {
                            "Tag": []
                        },
                        "VpcId": ""
                    }
                ]
            },
    "TotalCount": 4
}

'''

CREATE_DISK = '''
{
     
    "changed": true,
    "DiskId": "d-rj91n5w6koukwqqkxsf8",
    "result": ["Disk Creation Successful"]
}
'''
  
DELETE_IMAGE = '''
{
    "PageSize": 10,
    "RegionId": "cn-hongkong",
    "TotalCount": 1,
    "PageNumber": 1,
    "RequestId": "EB62BD82-B468-4CDC-BF97-91C9A97996FA",
    "Images": {
        "Image": [
            {
                "Status": "Available",
                "ProductCode": "",
                "Platform": "CentOS",
                "Description": "",
                "IsCopied": false,
                "Tags": {
                    "Tag": []
                },
                "IsSubscribed": false,
                "IsSelfShared": "",
                "CreationTime": "2017-01-19T05:47:25Z",
                "OSName": "CentOS  7.2 64\u4f4d",
                "DiskDeviceMappings": {
                    "DiskDeviceMapping": [
                        {
                            "Format": "",
                            "ImportOSSBucket": "",
                            "Device": "/dev/xvda",
                            "SnapshotId": "s-62jsw4rba",
                            "ImportOSSObject": "",
                            "Size": "40"
                        }
                    ]
                },
                "ImageId": "m-j6chvbnmr7lr6tg9276s",
                "Usage": "none",
                "ImageName": "m-j6chvbnmr7lr6tg9276s",
                "Architecture": "x86_64",
                "ImageOwnerAlias": "self",
                "OSType": "linux",
                "Progress": "100%",
                "Size": 40,
                "ImageVersion": "",
                "IsSupportIoOptimized": true
            }
        ]
    }
}
'''

CREATE_IMAGE = '''
{
    "RequestId": "8ECE78F4-9E81-46CD-9340-0D69CFAAA315",
    "ImageId": "m-j6cb0rw4eso5jsc6927n",
    "PageSize": 10,
    "TotalCount": 1,
    "PageNumber": 1,
    "Snapshots": {
        "Snapshot": [{
            "Status": "accomplished",
            "ProductCode": "",
            "Description": "Created s-j6ccfgptbi05ha1csvw9 from i-j6c2tbw6nsau39ippm94",
            "Tags": {
                "Tag": []
            },
            "SnapshotName": "",
            "SourceDiskType": "system",
            "CreationTime": "2017-01-27T11:50:58Z",
            "SourceDiskId": "d-j6ccbroi7rj23c3de0s4",
            "SourceDiskSize": 40,
            "Progress": "100%",
            "Usage": "image",
            "SnapshotId": "s-j6ccfgptbi05ha1csvw9"
        }]
    }
}
'''


class TestDescribeInstances(ACSMockServiceTestCase):
    connection_class = ECSConnection

    def default_body(self):
        return DESCRIBE_INSTANCE

    def test_instance_attribute(self):
        self.set_http_response(status_code=200, body=DESCRIBE_INSTANCE)
        filters = {}
        instance_ids = ["i-94dehop6n"]
        tag_key = 'xz_test'
        tag_value = '1.20'
        filters['tag:' + tag_key] = tag_value
        instances = self.service_connection.get_all_instances(instance_ids=instance_ids, filters=filters)
        self.assertEqual(len(instances), 1)
        instance = instances[0]
        self.assertEqual(instance.id, 'i-94dehop6n')
        self.assertEqual(instance.group_id, 'sg-94kd0cyg0')
        self.assertEqual(instance.public_ip, '120.25.13.106')
        self.assertEqual(instance.tags, {"xz_test": "1.20", "xz_test_2": "1.20"})
        self.assertFalse(instance.io_optimized)
        self.assertEqual(instance.status, 'running')
        self.assertEqual(instance.image_id, 'centos6u5_64_40G_cloudinit_20160427.raw')
        return instances

    def test_manage_instances(self):
        self.set_http_response(status_code=200, body=MANAGE_INSTANCE)
        instances = self.test_instance_attribute()
        for inst in instances:
            if inst.state == 'running':
                inst.stop()
            elif inst.state == 'stopped':
                inst.start()
            else:
                inst.reboot()


class TestManageInstances(ACSMockServiceTestCase):
    connection_class = ECSConnection
    instance_ids = ['i-94dehop6n', 'i-95dertop6m']

    def default_body(self):
        return MANAGE_INSTANCE

    def test_start_instance(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.start_instances(instance_ids=self.instance_ids)
        self.assertEqual(len(result), len(self.instance_ids))
        self.assertIn(result[0], self.instance_ids)

    def test_stop_instance(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.stop_instances(instance_ids=self.instance_ids, force=True)
        self.assertEqual(len(result), len(self.instance_ids))
        self.assertIn(result[0], self.instance_ids)

    def test_reboot_instance(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.reboot_instances(instance_ids=self.instance_ids, force=True)
        self.assertEqual(len(result), len(self.instance_ids))
        self.assertIn(result[0], self.instance_ids)

    def test_terminate_instance(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.terminate_instances(instance_ids=self.instance_ids, force=True)
        self.assertEqual(len(result), len(self.instance_ids))
        self.assertIn(result[0], self.instance_ids)


class TestDeleteSecurityGroup(ACSMockServiceTestCase): 
    connection_class = ECSConnection
    group_ids = [
                  'sg-rj9606ryhhy2c3t8ljtx'
                 ]
    region = 'us-west-1'
    
    def default_body(self):
        return DELETE_SECURITY_GROUP
    
    def test_delete_security_grp(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_security_group(group_ids=self.group_ids)
        self.assertEqual(result[0][u'RequestId'], "D8C42A44-7B92-40BC-9DAA-41B7EB733A6C")


class TestGetSecurityStatus(ACSMockServiceTestCase):
    connection_class = ECSConnection
   
    region = 'cn-beijing'
    state = 'getinfo'

    def default_body(self):
        return GET_SECURITY_STATUS

    def test_get_security_status(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.get_security_status(vpc_id=None, group_ids=None)
        
        self.assertEqual(result[u'RequestId'], "2076C42F-7E15-4F69-926F-C404E6A2F0DD")


class TestCreateAuthorizeSecurityGroup(ACSMockServiceTestCase):
    connection_class = ECSConnection
    region_id = "cn-beijing"

    group_tags = [
        {
            "tag_key": "create_test_1",
            "tag_value": "0.01"
        },
        {
            "tag_key": "create_test_2",
            "tag_value": "0.02"
        }
    ]

    def default_body(self):
        return Create_Security_Group

    def test_create_security_grp(self):
        self.set_http_response(status_code=200)
        changed, security_group_id, result = self.service_connection.create_security_group(
            group_name="Blue123", group_description="TestDataforBlue", group_tags=self.group_tags)

        self.assertEqual(security_group_id, u'sg-2ze95f8a2ni6bb2wql3b')
        rs = result[0]
        self.assertEqual(rs, u'Security Group Creation Successful')


class TestAuthorizeSecurityGroup(ACSMockServiceTestCase):
    connection_class = ECSConnection
    region_id = "cn-beijing"
    security_group_id = 'sg-2ze95f8a2ni6bb2wql3b'

    inbound_rules = [
        {
            "ip_protocol": "all",
            "port_range": "-1/-1",
            "cidr_ip": "10.159.6.18/12",
        }
    ]

    outbound_rules = [
        {
            "ip_protocol": "tcp",
            "port_range": "2/100",
            "cidr_ip": "10.159.6.18/12",
        }
    ]

    def default_body(self):
        return Authorize_Security_Group

    def test_authorize_security_grp(self):
        self.set_http_response(status_code=200)
        changed, inbound_failed_rules, outbound_failed_rules, result = self.service_connection.authorize_security_group(
                                                                            security_group_id=self.security_group_id,
                                                                           inbound_rules=self.inbound_rules,
                                                                           outbound_rules=self.outbound_rules)
        rs = result[0]
        self.assertEqual(rs, u'inbound rule authorization successful for group id sg-2ze95f8a2ni6bb2wql3b')
        rs = result[1]
        self.assertEqual(rs, u'outbound rule authorization successful for group id sg-2ze95f8a2ni6bb2wql3b')


class TestCreateInstance(ACSMockServiceTestCase):
    connection_class = ECSConnection

    image_id = "win2012_64_datactr_r2_cn_40G_alibase_20160622.vhd"
    instance_type = "ecs.n1.small"
    group_id = "sg-2ze0ktjl4szwycum4q2b"
    zone_id = "cn-beijing-b"
    instance_name = "MyInstance"
    description = None
    internet_data = {
                        'charge_type': 'PayByTraffic',
                        'max_bandwidth_in': 200,
                        'max_bandwidth_out': 0
                    }

    host_name = None
    password = None
    io_optimized = True
    system_disk = {
        "disk_category": "cloud_efficiency",
        "disk_size": 50
    }
    disks = [
        {
            "disk_category": "cloud_efficiency",
            "disk_size": 20,
            "disk_name": "disk_1",
            "disk_description": "disk 1 description comes here"
        },
        {
            "disk_category": "cloud_efficiency",
            "disk_size": 20,
            "disk_name": "disk_2",
            "disk_description": "disk 2 description comes here"
        }
    ]

    vswitch_id = None
    private_ip = True
    allocate_public_ip = True
    bind_eip = False
    instance_charge_type = None
    period = None
    auto_renew = False
    auto_renew_period =None
    instance_tags = [
        {
            "tag_key": "create_test_1",
            "tag_value": "0.01"
        },
        {
            "tag_key": "create_test_2",
            "tag_value": "0.02"
        }
    ]
    ids = None
    count = 1
    wait = True
    wait_timeout = 60    
    
    def default_body(self):
        return CREATE_INSTANCE
                                                                    
    def test_create_instance(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_instance(image_id=self.image_id,
                                                                  instance_type=self.instance_type,
                                                                  group_id=self.group_id, zone_id=self.zone_id,
                                                                  instance_name=self.instance_name,
                                                                  description=self.description,
                                                                  internet_data=self.internet_data,
                                                                  host_name=self.host_name, password=self.password,
                                                                  io_optimized=self.io_optimized,
                                                                  system_disk=self.system_disk, disks=self.disks,
                                                                  vswitch_id=self.vswitch_id,
                                                                  private_ip=self.private_ip,
                                                                  count=self.count,
                                                                  allocate_public_ip=self.allocate_public_ip,
                                                                  bind_eip=self.bind_eip,
                                                                  instance_charge_type=self.instance_charge_type,
                                                                  period=self.period, auto_renew=self.auto_renew,
                                                                  auto_renew_period=self.auto_renew_period,
                                                                  instance_tags=self.instance_tags,
                                                                  ids=self.ids, wait=self.wait,
                                                                  wait_timeout=self.wait_timeout)
        if changed is True:
            self.assertEqual(len(result), self.count)
            self.assertEqual(result[0]['instance_id'], u'i-2zeg0900kzwn7dpo7zrb')


class TestModifyInstance(ACSMockServiceTestCase):
    connection_class = ECSConnection
    attributes = [
        {
            "description": "volume attribute",
            "host_name": "hostcomes",
            "id": "i-rj97hhf9ue16ewoged75",
            "name": "aspen",
            "password": "Pass@123"
        }
    ]

    def default_body(self):
        return MODIFY_INSTANCE

    def test_modify_instance(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.modify_instance(attributes=self.attributes)                  
        self.assertEqual(result[0]['instance_ids'], [u'i-rj97hhf9ue16ewoged75'])


class TestGetInstance(ACSMockServiceTestCase):
    connection_class = ECSConnection
   
    region_id = "cn-beijing"
    pagenumber = 1
    pagesize = 5

    def default_body(self):
        return GET_INSTANCE

    def test_get_instance(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.get_instance_status(zone_id=None, pagenumber=self.pagenumber,
                                                             pagesize=self.pagesize)
        
        self.assertEqual(result[1][u'PageNumber'], self.pagenumber)
        self.assertEqual(result[1][u'PageSize'], self.pagesize)


class TestJoinSecGrp(ACSMockServiceTestCase): 
    connection_class = ECSConnection
    instance_ids = ["i-2zehfxz81ar5kvptw8b1"]
    group_id = 'sg-2zeewmie535ht7d90cki'
    region = 'cn-beijing'
    state = 'join'
    changed = False

    def default_body(self):
        return JOIN_GROUP

    def test_join_grp(self):
        self.set_http_response(status_code=200)
        changed, result, success_instance_ids, failed_instance_ids = self.service_connection.join_security_group(
            instance_ids=self.instance_ids, group_id=self.group_id)
        res=''
        if len(result) == 1:
            res = "success"
        else:
            res = "fail"


class TestLeaveSecGrp(ACSMockServiceTestCase): 
    connection_class = ECSConnection
    instance_ids = ["i-j6c5txh3q0wivxt5m807"]
    group_id = 'sg-j6c34iujuqbw29zpd53u'
    region = 'cn-hongkong'
    state = 'remove'
    changed = False

    def default_body(self):
        return LEAVE_GROUP

    def test_leave_grp(self):
        self.set_http_response(status_code=200)
        changed, result, success_instance_ids, failed_instance_ids = self.service_connection.leave_security_group(
            instance_ids=self.instance_ids, group_id=self.group_id)
        res=''
        if len(result) == 1:
            res = "success"
        else:
            res = "fail"


class TestCreateDisk(ACSMockServiceTestCase):
    connection_class = ECSConnection
   
    region =  'us-west-1'  
    disk_category = 'cloud'
    zone_id = 'us-west-1a'
    disk_name = 'aspen'    
    size = 20
    state = 'present'

    def default_body(self):
        return CREATE_DISK

    def test_create_disk(self):
        self.set_http_response(status_code=200)
        changed, disk_id, result = self.service_connection.create_disk(zone_id=self.zone_id, disk_name=self.disk_name,
                                                                       description=None,
                                                                       disk_category=self.disk_category, size=self.size,
                                                                       disk_tags=None, snapshot_id=None)

        self.assertEqual(disk_id, u'd-rj91n5w6koukwqqkxsf8')
        rs = result[0]
        self.assertEqual(rs, u'Disk Creation Successful')    


class TestAttachDisk(ACSMockServiceTestCase): 
    connection_class = ECSConnection
    instance_ids = ["i-j6c5txh3q0wivxt5m807"]
    disk_id = 'd-j6cc9ssgxbkjdf55w8p7'
    region = 'cn-hongkong'
    device = None
    delete_with_instance = None
    state = 'present'
    
    def default_body(self):
        return ATTACH_DISK

    def test_attach_disk(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.attach_disk(disk_id=self.disk_id, instance_id=self.instance_ids,
                                                              device=self.device,
                                                              delete_with_instance=self.delete_with_instance)

        self.assertEqual(result[0]['RequestId'], "AF3991A3-5203-4F83-8FAD-FDC1253AF15D")


class TestDetachDisk(ACSMockServiceTestCase): 
    connection_class = ECSConnection
    region_id = "cn-beijing"           
    disk_id = "d-2zecexhwthhw5wyco3m2"
    
    def default_body(self):
        return DETACH_DISK

    def test_detach_disk(self):
        self.set_http_response(status_code=200)
        changed, result, instance_id = self.service_connection.detach_disk(disk_id=self.disk_id)
        if changed is True:
            self.assertEqual(result[0]['RequestId'], "AF3991A3-5203-4F83-8FAD-FDC1253AF15D")


class TestDeleteDisk(ACSMockServiceTestCase): 
    connection_class = ECSConnection
    disk_id = "d-2zecexhwthhw5wyco3m2"
    
    def default_body(self):
        return DELETE_DISK

    def test_delete_disk(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_disk(disk_id=self.disk_id)
        if changed is True:
            self.assertEqual(result[u'RequestId'], "AF3991A3-5203-4F83-8FAD-FDC1253AF15D")
        else:
            self.assertEqual(result[0], {'Error Code:': 'InvalidDiskId.NotFound', 'Error Message:': 'Disk not exist'})
                                                  
 
class TestCreateImage(ACSMockServiceTestCase):
    connection_class = ECSConnection
    region_id = 'cn-hongkong'
    snapshot_id = 's-j6cjdk51ejf0mtdnb7ba'
    image_name = 'testimage4'
    image_version = '2'
    description = 'test4'
    images_tags = [{"tag_key": "tag1key", "tag_value": "tag1value"}, {"tag_key": "tag2key", "tag_value": "tag2value"}]
    disk_mapping = None
    instance_id = None

    def default_body(self):
        return CREATE_IMAGE
   
    def test_create_image(self):
        self.set_http_response(status_code=200)
        changed, image_id, result, request_id = self.service_connection.create_image(snapshot_id=self.snapshot_id,
                                                                                     image_name=self.image_name,
                                                                                     image_version=self.image_version,
                                                                                     description=self.description,
                                                                                     images_tags=self.images_tags,
                                                                                     instance_id=self.instance_id,
                                                                                     disk_mapping=self.disk_mapping,
                                                                                     wait=None, wait_timeout=None)
        self.assertEqual(image_id, 'm-j6cb0rw4eso5jsc6927n')               


class TestDeleteImage(ACSMockServiceTestCase): 
    connection_class = ECSConnection

    image_id = 'm-j6chvbnmr7lr6tg9276s'
    region = 'cn-hongkong'
    state = 'absent'    

    def default_body(self):
        return DELETE_IMAGE

    def test_delete_image(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_image(image_id=self.image_id)
        self.assertEqual(result[0][u'RequestId'], "EB62BD82-B468-4CDC-BF97-91C9A97996FA")












