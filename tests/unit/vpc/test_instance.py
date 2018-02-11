#!/usr/bin/env python
# import sys
# sys.path.append("../../..")
from footmark.vpc.connection import VPCConnection
from tests.unit import ACSMockServiceTestCase

CREATE_VSWITCH = '''
{ 
        "RequestId":  "DC68F397-85F6-48DE-8D00-3075E6BEC850", 
        "VSwitchId":  "vsw-rj9v3y42xzbvgagukas4o"
}
'''

DELETE_VSWITCH = '''
{
    "Vpcs": {
        "Vpc": [
            {
                "Status": "Available",
                "VRouterId": "vrt-wz9lxprdu3wathvzlpdt0",
                "Description": "System created default VPC.",
                "UserCidrs": {
                    "UserCidr": []
                },
                "RegionId": "cn-shenzhen",
                "CreationTime": "2016-12-16T09:13:52Z",
                "VSwitchIds": {
                    "VSwitchId": [
                        "vsw-wz9juivvg4zk7ezapsc8l"
                    ]
                },
                "VpcId": "vpc-wz9rxpux51xpj0dwafuoz",
                "VpcName": "",
                "CidrBlock": "172.18.0.0/16",
                "IsDefault": true
            }
        ]
    },
    "VSwitches": {
        "VSwitch": [
            {
                "Status": "Available",
                "VSwitchName": "Test",
                "VpcId": "vpc-wz9rxpux51xpj0dwafuoz",
                "Description": "",
                "AvailableIpAddressCount": 8188,
                "CreationTime": "2017-01-02T13:27:59Z",
                "ZoneId": "cn-shenzhen-a",
                "VSwitchId": "vsw-wz9juivvg4zk7ezapsc8l",
                "CidrBlock": "172.18.0.0/19",
                "IsDefault": false
            }
        ]
    },
    "TotalCount": 1,
    "PageNumber": 1,
    "RequestId": "6740CBF5-CED5-4B80-9511-A48213DD5560",
    "PageSize": 10,
    "Instances": {
        "Instance": [
            {
                "AutoReleaseTime": "",
                "RegionId": "us-west-1",
                "InstanceTypeFamily": "ecs.s2",
                "SerialNumber": "1e661cfa-8af4-42c1-870c-8e11f8006d16",
                "CreationTime": "2017-01-05T08:02Z",
                "ExpiredTime": "2999-09-08T16:00Z",
                "IoOptimized": true,
                "Memory": 4096,
                "InternetChargeType": "",
                "VpcAttributes": {
                    "VpcId": "vpc-rj9jvfp98y9n22aaqtm7m",
                    "VSwitchId": "vsw-rj9l1xrwcnptti4o1q2cf",
                    "PrivateIpAddress": {
                        "IpAddress": [
                            "192.168.69.23"
                        ]
                    },
                    "NatIpAddress": ""
                },
                "Status": "Stopped",
                "Description": "volume attribute",
                "InstanceId": "i-rj9be6tlwmae1995uq5t",
                "HostName": "hostcomes",
                "ClusterId": "",
                "ImageId": "win2012_64_datactr_r2_cn_40G_alibase_20160622.vhd",
                "SpotStrategy": "NoSpot",
                "InstanceNetworkType": "vpc",
                "InstanceType": "ecs.s2.large",
                "EipAddress": {
                    "InternetChargeType": "",
                    "IpAddress": "",
                    "AllocationId": ""
                },
                "InnerIpAddress": {
                    "IpAddress": []
                },
                "GPUAmount": 0,
                "OperationLocks": {
                    "LockReason": []
                },
                "InstanceChargeType": "PostPaid",
                "SecurityGroupIds": {
                    "SecurityGroupId": [
                        "sg-rj94i8agzbqdiy8n76jb"
                    ]
                },
                "InternetMaxBandwidthOut": 0,
                "ZoneId": "us-west-1b",
                "InstanceName": "Access",
                "Cpu": 2,
                "PublicIpAddress": {
                    "IpAddress": []
                },
                "InternetMaxBandwidthIn": -1,
                "VlanId": "",
                "GPUSpec": "",
                "DeviceAvailable": true
            }        ]
    }  
}
'''

QUERYING_VSWITCH = '''
{
    "PageNumber": 1,
    "VSwitches":
         {
             "VSwitch":
                 [{
                     "Status": "Available",
                     "VpcId": "vpc-2zewr6sjkz4gn8wvua2j1",
                     "Description": "",
                     "AvailableIpAddressCount": 2043,
                     "CreationTime": "2016-12-27T10:06:07Z",
                     "ZoneId": "cn-beijing-b",
                     "VSwitchId": "vsw-j6c1byawdpc2lbwy7s1q1",
                     "CidrBlock": "172.16.0.0/21",
                     "TotalCount": "1"
                 }]
         },
        "TotalCount": 9,
        "PageSize": 50,
        "RequestId": "5D464158-D291-4C69-AA9E-84839A669B9D"
}
'''

REQUESTING_EIP = '''
{
    "EipAddress": "47.89.8.143",
    "RequestId": "2F05A27D-A9FB-45A3-9F24-27A9C1E3FD94",
    "AllocationId": "eip-j6cgp0w5v77odiqeihs66"
}
''' 

BIND_EIP = '''
{
        "RequestId": "4A9941A3-608B-4F96-A23C-EBA9DADBBE99"
}
'''

UNBIND_EIP = '''
{
        "RequestId": "BA9495A5-6F4D-4399-ABA9-A1252C641D2C"
}
'''

DELETE_VPC = '''
{
    "Vpcs":
    {
        "Vpc":
        [
             {
                "VpcName": "VpcName",
                "Description": "VpcDescription",
                "VRouterId": "sg-123",
                "Status": "Available"
             }
        ]
    }
}
'''  

QUERY_VROUTER = '''
{
    "VRouters": {
        "VRouter": [
            {
                "VRouterId": "vrt-j6cdxdjgy5jrjtrzk4jp4",
                "Description": "",
                "RegionId": "cn-hongkong",
                "CreationTime": "2016-12-14T13:24:16Z",
                "VpcId": "vpc-j6c16byqnpb7a27pa6xfb",
                "VRouterName": "",
                "RouteTableIds": {
                    "RouteTableId": [
                        "vtb-j6cre8qyb0zu6rpcmmy7t"
                    ]
                }
            }
        ]
    }
}
'''

DELETE_CUSTOM_ROUTE = '''
{
    "RequestId": "24FFBEBA-E0FC-47C5-BDC9-01F08815FF81"
}
'''

RELEASE_EIP = '''
{
    "TotalCount": 2,
    "PageNumber": 1,
    "PageSize": 10,
    "EipAddresses": {
        "EipAddress": [
            {
                "Status": "Available",
                "AllocationTime": "2017-02-14T06:23:30Z",
                "OperationLocks": {
                    "LockReason": []
                },
                "InstanceId": "",
                "RegionId": "cn-hongkong",
                "InstanceType": "",
                "Bandwidth": "1",
                "ExpiredTime": "",
                "ChargeType": "PostPaid",
                "InternetChargeType": "PayByTraffic",
                "IpAddress": "47.89.16.106",
                "AllocationId": "eip-j6ch2ko27eyfaysyo10fk"
            },
            {
                "Status": "InUse",
                "AllocationTime": "2017-02-14T05:15:31Z",
                "OperationLocks": {
                    "LockReason": []
                },
                "InstanceId": "i-j6c7si86xwstnxfrassv",
                "RegionId": "cn-hongkong",
                "InstanceType": "EcsInstance",
                "Bandwidth": "3",
                "ExpiredTime": "",
                "ChargeType": "PostPaid",
                "InternetChargeType": "PayByTraffic",
                "IpAddress": "47.89.19.46",
                "AllocationId": "eip-j6coz1xup8gkik73qbd0j"
            }
        ]
    },
    "RequestId": "5C3360D0-A873-4E83-AB23-E784247228E9"
}
'''

MODIFYING_EIP = '''
{
    "RequestId": "0EE6639C-6C6E-4494-8DB4-6FE50E72108B"
}
'''

CREATE_VPC = '''
 {
    "RequestId": "5DDFE80A-D249-42B7-AC53-3764CF74DA28",
    "RouteTableId": "vtb-j6c52u98rcrpsksqmlsg0",
    "VRouterId": "vrt-j6cboevcz8ot5sxuqbepr",
    "VpcId": "vpc-j6cgc9h8wzjmjgauw2ibi",
    "VSwitchId": "vsw-2zem239ckasw2suua2ncn"
}
'''

CREATE_ROUTE_ENTRY = '''
{
        "RequestId": "601CB03C-7653-48D4-8A8E-BFCB987E34F3"
}
'''


class TestCreateVpc(ACSMockServiceTestCase):
    connection_class = VPCConnection

    cidr_block = "192.168.0.0/16"
    user_cidr = None
    vpc_name = "demovpc"
    description = "vpc description comes here"
    vswitches = [
        {
            "cidr": "192.168.1.0/24", "az": "cn-beijing-b", "name": "subnet1", "description": "description here"
        }
    ]
    route_tables = None

    def default_body(self):
        return CREATE_VPC

    def test_create_vpc(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_vpc(cidr_block=self.cidr_block, user_cidr=self.user_cidr,
                                                             vpc_name=self.vpc_name, description=self.description,
                                                             vswitches=self.vswitches)
        if changed:
            self.assertEqual(result[0][u'RequestId'], "5DDFE80A-D249-42B7-AC53-3764CF74DA28")
            self.assertEqual(result[0][u'RouteTableId'], "vtb-j6c52u98rcrpsksqmlsg0")
            self.assertEqual(result[0][u'VRouterId'], "vrt-j6cboevcz8ot5sxuqbepr")
            self.assertEqual(result[0][u'VpcId'], "vpc-j6cgc9h8wzjmjgauw2ibi")
            self.assertEqual(result[0][u'VSwitchId'], "vsw-2zem239ckasw2suua2ncn")


class TestCreateRouteEntry(ACSMockServiceTestCase):
    connection_class = VPCConnection
    vpc_id = None
    route_tables = [
                        {
                            "route_table_id": "vtb-j6ca2jgv7ilh2b68450js",
                            "dest": "192.168.2.0/24",
                            "next_hop_id": "i-j6c3jeox1zi7x7jdwzym"
                        },
                        {
                            "route_table_id": "vtb-j6ca2jgv7ilh2b68450js",
                            "dest": "192.168.3.0/24",
                            "next_hop_id": "i-j6c3jeox1zi7x7jdwzym"
                        }              
                    ]

    def default_body(self):
        return CREATE_ROUTE_ENTRY
   
    def test_create_route_entry(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_route_entry(route_tables=self.route_tables, vpc_id=self.vpc_id)
        if changed:
            self.assertEqual(result[0][u'RequestId'], u'601CB03C-7653-48D4-8A8E-BFCB987E34F3')


# region Unit test method for create vswitch
class TestCreateVswitch(ACSMockServiceTestCase):
    connection_class = VPCConnection
    
    region = "cn-hongkong"
    region_id = "cn-hongkong"
    vpc_id = "vpc-j6cen1rrgdu53nywh7eh2" 
    vswitches = [
                    {
                        "zone_id": "cn-hongkong-b",
                        "cidr_block": "192.168.10.0/24",
                        "vswitch_name": "Rohit_VSwitch2",
                        "description": "Demo"
                    },
                    {
                        "zone_id": "cn-hongkong-b",
                        "cidr_block": "192.168.11.0/24",
                        "vswitch_name": "Rohit_VSwitch3",
                        "description": "Demo"
                    }
                
                ]
        
    def default_body(self):
        return CREATE_VSWITCH
    
    def test_create_vswitch(self):
        self.set_http_response(status_code=200)
        changed, result, vswitchId = self.service_connection.create_vswitch(vpc_id=self.vpc_id, vswitches=self.vswitches)
        vswitches = result[0] 
        self.assertEqual(vswitches[u'VSwitchId'], "vsw-rj9v3y42xzbvgagukas4o")
# endregion


# region Unit test method for delete vswitch
class TestDeleteVswitch(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region = 'cn-shenzhen'
    vpc_id = ""
    purge_vswitches = ['vsw-wz9juivvg4zk7ezapsc8l']
    
    def default_body(self):
        return DELETE_VSWITCH
    
    def test_delete_vswitch(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_vswitch(purge_vswitches=self.purge_vswitches, vpc_id=self.vpc_id)
        vswitch = result[0]
        self.assertEqual(vswitch[u'status'], 'vsw-wz9juivvg4zk7ezapsc8l deleted')
# endregion


# region Unit test method for requesting eip
class TestRequestingEIP(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region = 'cn-hongkong'
    bandwidth = ''
    internet_charge_type = 'PayByTraffic'  
    
    def default_body(self):
        return REQUESTING_EIP
    
    def test_requesting_eip_addresses(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.requesting_eip_addresses(
            bandwidth=self.bandwidth, internet_charge_type=self.internet_charge_type)
        self.assertEqual(result[u'RequestId'], '2F05A27D-A9FB-45A3-9F24-27A9C1E3FD94')
# endregion


# region Unit test method for querying vswitch list
class TestQueryingVswitch(ACSMockServiceTestCase):
    connection_class = VPCConnection
          
    pagenumber = 1
    pagesize = 50
    vpc_id = "vpc-2zewr6sjkz4gn8wvua2j1"
    
    
    def default_body(self):
        return QUERYING_VSWITCH
    
    def test_get_vswitch_status(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.get_vswitch_status(vpc_id=self.vpc_id, zone_id=None, vswitch_id=None,
                                                            pagenumber=self.pagenumber, pagesize=self.pagesize)
        if self.pagenumber:
            self.assertEqual(result[1][u'PageNumber'], self.pagenumber)

        if self.pagenumber:
            self.assertEqual(result[1][u'PageSize'], self.pagesize)
        
        if len(result[1][u'VSwitches']) > 0:
            self.assertEqual(result[1][u'VSwitches'][u'VSwitch'][0][u'VpcId'], self.vpc_id)           
        
# endregion


# region Unit test method for bind eip
class TestBindEip(ACSMockServiceTestCase):
    connection_class = VPCConnection

    region = 'cn-hongkong'
    allocation_id = 'eip-j6cn6n9fks0atkt9obhz4',
    instance_id = 'i-j6c6377q7u5t1j0vicgg',
    state = 'join'    

    def default_body(self):
        return BIND_EIP
    
    def test_bind_eip(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.bind_eip(allocation_id=self.allocation_id, instance_id=self.instance_id)

        self.assertEqual(result[u'RequestId'], "4A9941A3-608B-4F96-A23C-EBA9DADBBE99")


# region Unit test code for Unbind Eip
class TestUnbindEip(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region = 'cn-hongkong'
    allocation_id = 'eip-j6cdylcs5ui0wqnew1p1k',
    instance_id = 'i-j6c7si86xwstnxfrassv'
    
    def default_body(self):
        return UNBIND_EIP
    
    def test_unbind_eip(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.unbind_eip(allocation_id=self.allocation_id, instance_id=self.instance_id)
        if changed:
            self.assertEqual(result[u'RequestId'], "BA9495A5-6F4D-4399-ABA9-A1252C641D2C")
# endregion


# region Unit test code for Unbind Eip
class TestModifyingEip(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region = 'us-west-1'
    allocation_id = 'eip-j6cn6n9fks0atkt9obhz4',
    bandwidth = 2
    
    def default_body(self):
        return MODIFYING_EIP
    
    def test_modifying_eip_attributes(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.modifying_eip_attributes(allocation_id=self.allocation_id,
                                                                           bandwidth=self.bandwidth)
        self.assertEqual(result[u'RequestId'], "0EE6639C-6C6E-4494-8DB4-6FE50E72108B")
# endregion


# region Unit test code for Delete VPC
class TestDeleteVpc(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region_id = "cn-hangzhou"
    vpc_id = "vpc-bp18wb8vqlpf1ls1cc71g"

    def default_body(self):
        return DELETE_VPC

    def test_delete_vpc(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_vpc(vpc_id=self.vpc_id)
        self.assertEqual(result[0], 'Vpc with Id vpc-bp18wb8vqlpf1ls1cc71g successfully deleted.')
# endregion


# region Unit test code for get_all_vrouters
class TestQueryVRouterList(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region_id = "cn-hongkong"
    vrouter_id = ['vrt-j6cmpheaf94gehm4jw3x8']
    

    def default_body(self):
        return QUERY_VROUTER

    def test_query_vrouter_list(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.get_all_vrouters(vrouter_id=self.vrouter_id)
        if len(result) > 0:
            #id = result[0][0].vpc_id
            id = result[1][u'VRouters'][u'VRouter'][0][u'VpcId']
            self.assertTrue(len(id)>0)
# endregion


# region Unit test code for delete_custom_route
class TestDeleteRoute(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region_id = 'cn-hongkong'
    purge_routes = {
        "route_table_id": "vtb-j6c2tf8y4uxycfmqoyf0o",
        "destination_cidr_block": "192.168.0.1/32",
        "next_hop_id": "i-j6c3nt8kraa5uotd4j79"
    }

    def default_body(self):
        return DELETE_CUSTOM_ROUTE

    def test_delete_custom_route(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.delete_custom_route(purge_routes=self.purge_routes)
        if len(result) > 0 and 'RequestId' in result:
            self.assertTrue(len(result) == 1)
# endregion


# region Unit test code for ReleaseEip
class TestReleaseEip(ACSMockServiceTestCase):
    connection_class = VPCConnection
    region_id = 'cn-hongkong'
    allocation_id = "eip-j6ch2ko27eyfaysyo10fk"

    def default_body(self):
        return RELEASE_EIP

    def test_release_eip(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.releasing_eip(allocation_id=self.allocation_id)
        self.assertEqual(result[u'RequestId'], "5C3360D0-A873-4E83-AB23-E784247228E9")
# endregion
