#!/usr/bin/env python
# import sys
# sys.path.append("../../..")
from footmark.slb.connection import SLBConnection
from tests.unit import ACSMockServiceTestCase
import json


CREATE_LOAD_BALANCER = '''
{
    "Address": "60.205.131.32",
    "LoadBalancerId": "lb-2ze9vjx6o2hnmte7s71d6",
    "LoadBalancerName": "my_slb",
    "NetworkType": "classic",
    "RequestId": "3C97A537-4D50-4079-93BE-26E3B5C8B527",
    "VSwitchId": "",
    "VpcId": "",
    "http_listener_result": {"RequestId":"2ACD0300-FB78-48A5-8AAD-0DA08FC4B4D7"}
} 
'''

DELETE_LOAD_BALANCER = '''
{
     "RequestId": "60E461E9-C213-4C69-ADC8-2CBEB0256780"
    
}
'''
SET_LOAD_BALANCER_STATUS = '''
{        
      
      "RequestId": "74761D21-286D-4B1A-804F-E3B64D4B7A7E"  
              
}
'''
SET_LOAD_BALANCER_NAME = '''
{
    "RequestId": "5649FFC2-4058-4165-8805-503F31015601"
}
'''

CREATE_VSERVER_GROUP = '''
{
"BackendServers":
       {
        "BackendServer":[{"ServerId":"i-j6c8vsfdfz8b759n8ojz","Port":80,"Weight":30}]
       },
        "VServerGroupId":"rsp-3ns7xf2u9a9rf"
}
'''
SET_VSERVER_GROUP_ATTRIBUTE = '''
 {
            "BackendServers": {
                "BackendServer": [
                    {
                        "Port": 25,
                        "ServerId": "i-j6c3tdy2mgw1ameoetzt",
                        "Weight": 30
                    }
                ]
            },
            "VServerGroupId": "rsp-3ns1daa6i1fkh",
            "VServerGroupName": "Test_playbook"
        }
'''
ADD_VSERVER_GROUP_BACKEND_SERVER = '''
 {
            "BackendServers": {
                "BackendServer": [
                    {
                        "Port": 25,
                        "ServerId": "i-j6c3tdy2mgw1ameoetzt",
                        "Weight": 30
                    }
                ]
            },
            "VServerGroupId": "rsp-3ns1daa6i1fkh"
            
        }
'''
REMOVE_VSERVER_GROUP_BACKEND_SERVER = '''
 {
            "BackendServers": {
                "BackendServer": [
                    {
                        "Port": 25,
                        "ServerId": "i-j6c3tdy2mgw1ameoetzt",
                        "Weight": 30
                    }
                ]
            },
            "VServerGroupId": "rsp-3ns7xf2u9a9rf"
            
        }
'''

DELETE_VSERVER_GROUP = '''
{
    "VServerGroups":
    {
        "VServerGroup":
        [
            {
                "VServerGroupId":"rsp-3nsk5wfpx6lt8",
                "VServerGroupName":"VserverGroupRohit"
            },
            {
                "VServerGroupId":"rsp-3ns4pyvudkcyh",
                "VServerGroupName":"VserverGroupRohit2"
            },
            {
                "VServerGroupId":"rsp-3nsfioqojdael",
                "VServerGroupName":"VserverGroupRohit3"
            }
        ]
    }
}
'''

MODIFY_LOAD_BALANCER_INTERNET_SPEC = '''
{
    "RequestId":"80A96F3E-FD71-43ED-9E7B-EFA159CF55E1"
}
'''

REMOVE_VSERVER_GROUP = '''
 {
            "BackendServers": {
                "BackendServer": [
                    {
                        "Port": 80,
                        "ServerId": "i-j6ci04oi33i9pv2hnafk",
                        "Weight": 50
                    }
                ]
            },
            "VServerGroupId": "rsp-3nsmpxzq8p6mi"
 }
'''

ADD_BACKEND_SERVERS = '''
{
    "BackendServers":
    {
        "BackendServer":
        [
            {
                "ServerId": "i-t4n73vl5oaxuxmigat9x",
                "Weight": 100
            },
            {
                "ServerId": "i-t4njdk51ejf1a3xm9s2n",
                "Weight": 40
            }
        ]

    }
}
'''

REMOVE_BACKEND_SERVERS = '''
{
    "BackendServers":
    {
        "BackendServer":
        [
            {
                "ServerId": "i-t4n73vl5oaxuxmigat9",
                "Weight": 100
            }
        ]

    }
}
'''

SET_BACKEND_SERVERS = '''
{
    "BackendServers":
    {
        "BackendServer":
        [
            {
                "ServerId": "i-t4n73vl5oaxuxmigat9x",
                "Weight": 100
            },
            {
                "ServerId": "i-t4njdk51ejf1a3xm9s2n",
                "Weight": 40
            }
        ]

    }
}
'''

DESCRIBE_BACKEND_SERVERS_HEALTH = '''
{
    "BackendServers":
    {
        "BackendServer":
        [
            {
                "ListenerPort" : 80,
                "ServerId": "i-t4n73vl5oaxuxmigat9x",
                "Weight": 100
            },
            {
                "ListenerPort" : 80,
                "ServerId": "i-t4njdk51ejf1a3xm9s2n",
                "Weight": 40
            }
        ]

    }
}
'''

MODIFY_VSERVER_GROUP = '''
 {
            "BackendServers": {
                "BackendServer": [
                    {
                        "Port": 656,
                        "ServerId": "i-2zec953dxl686o8p4vq1",
                        "Weight": 100
                    },
                    {
                        "Port": 656,
                        "ServerId": "i-2zehfxz81ar5kvptw8b1",
                        "Weight": 100
                    }
                ]
            },
            "VServerGroupId": "rsp-dj1v1fcup9efj"
 }
'''


class TestCreateLoadBalancer(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region_id = "cn-beijing"
    listeners = [
        {
            "protocol": "http",
            "load_balancer_port": "80",
            "instance_port": "80",
            "bandwidth": "1"
        }
    ]
    helth_checkup = {
        "health_check": "on",
        "ping_port": "80",
        "ping_path": "/index.html",
        "response_timeout": "5",
        "interval": "30",
        "unhealthy_threshold": "2",
        "healthy_threshold": "10"
    }
    stickness = {
        "enabled": "on",
        "type": "insert",
        "cookie": "300",
        "cookie_timeout": "1"
    }
    load_balancer_name = "my_slb"
    address_type = None
    internet_charge_type = None
    bandwidth = None
    vswitch_id = None
    master_zone_id = "cn-beijing-b"
    slave_zone_id = "cn-beijing-a"
    instance_ids = None
    validate_cert = None
    tags = None
    wait = None
    wait_timeout = None

    def default_body(self):
        return CREATE_LOAD_BALANCER
                                                                    
    def test_create_load_balancer(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_load_balancer(load_balancer_name=self.load_balancer_name,
                                                                       address_type=self.address_type,
                                                                       vswitch_id=self.vswitch_id,
                                                                       internet_charge_type=self.internet_charge_type,
                                                                       master_zone_id=self.master_zone_id,
                                                                       slave_zone_id=self.slave_zone_id,
                                                                       bandwidth=self.bandwidth,
                                                                       listeners=self.listeners,
                                                                       instance_ids=self.instance_ids,
                                                                       validate_cert=self.validate_cert, tags=self.tags,
                                                                       wait=self.wait, wait_timeout=self.wait_timeout)

        if changed:
            self.assertEqual(result[u'LoadBalancerId'],  u'lb-2ze9vjx6o2hnmte7s71d6')


class TestDeleteLoadBalancer(ACSMockServiceTestCase):
    connection_class = SLBConnection
 
    slb_id = "lb-2ze55q82qcl77v5y2lxia"

    def default_body(self):
        return DELETE_LOAD_BALANCER
                                                                    
    def test_delete_load_balancer(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_load_balancer(slb_id=self.slb_id)        
        
        self.assertEqual(result[u'RequestId'], "60E461E9-C213-4C69-ADC8-2CBEB0256780")


class TestSetLoadBalancerStatus(ACSMockServiceTestCase):
    connection_class = SLBConnection
   
    slb_ids = ["lb-2evkmagsr7apth28stns1"]   
    status = "active"

    def default_body(self):
        return SET_LOAD_BALANCER_STATUS
                                                                    
    def test_set_load_balancer_status(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.set_load_balancer_status(slb_ids=self.slb_ids, status=self.status)     
        self.assertEqual(result[0][u'RequestId'], "74761D21-286D-4B1A-804F-E3B64D4B7A7E")        
        

class TestSetLoadBalancerName(ACSMockServiceTestCase):
    connection_class = SLBConnection

    load_balancer_id = "lb-dj1j7uy78htxtj75rckqo"
    load_balancer_name = "new_slb"

    def default_body(self):
        return SET_LOAD_BALANCER_NAME
                                                                    
    def test_set_load_balancer_name(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.set_load_balancer_name(load_balancer_id=self.load_balancer_id,
                                                                         load_balancer_name=self.load_balancer_name)
        if changed:
            self.assertEqual(result[0]['RequestId'], "5649FFC2-4058-4165-8805-503F31015601")
                   
                       
class TestCreateVServerGroup(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = 'cn-hongkong'
    loadbalancerid = 'lb-3nsspc0zn9wntvlyoe3tw'
    vservergroupname = 'Test2'
    backendservers = [
                       {'server_id': 'i-j6c8vsfdfz8b759n8ojz', 'port': 80, 'weight': 30},
                      ]
    
    def default_body(self):
        return CREATE_VSERVER_GROUP
    
    def test_create_vserver_group(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_vserver_group(load_balancer_id=self.loadbalancerid,
                                                                       vserver_group_name=self.vservergroupname,
                                                                       backend_servers=self.backendservers)
        self.assertEqual(result[u'VServerGroupId'], 'rsp-3ns7xf2u9a9rf')


class TestRemoveVServerGroupBackendServer(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = 'cn-hongkong'
    vserver_group_id = 'rsp-3ns7xf2u9a9rf'   
    purge_backend_servers = [
                       {'server_id': 'i-j6c8vsfdfz8b759n8ojz', 'port': 80, 'weight': 30},
                      ]
    
    def default_body(self):
        return REMOVE_VSERVER_GROUP_BACKEND_SERVER
    
    def test_remove_vserver_group_backend_server(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.remove_vserver_group_backend_server(
            vserver_group_id=self.vserver_group_id, purge_backend_servers=self.purge_backend_servers)
        self.assertEqual(result[u'VServerGroupId'], 'rsp-3ns7xf2u9a9rf')


class TestAddVServerGroupBackEndServer(ACSMockServiceTestCase):
    connection_class = SLBConnection
    
    region = 'cn-hongkong'
    vserver_group_id = 'lb-3nsspc0zn9wntvlyoe3tw'
    backendservers =[
                  {'server_id': 'i-j6c8vsfdfz8b759n8ojz', 'port': 80, 'weight': 30},
                 ]
    
    def default_body(self):
        return ADD_VSERVER_GROUP_BACKEND_SERVER
    
    def test_add_vserver_group_backend_server(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.add_vservergroup_backend_server(
            vserver_group_id=self.vserver_group_id, backend_servers=self.backendservers)
        self.assertEqual(result[u'VServerGroupId'], 'rsp-3ns1daa6i1fkh')


class TestSetVServerGroupAttribute(ACSMockServiceTestCase):
    connection_class = SLBConnection
    
    region = 'cn-hongkong'
    vserver_group_id = 'lb-3nsspc0zn9wntvlyoe3tw'
    vservergroupname = 'Test2'
    backendservers =[
                  {'server_id': 'i-j6c8vsfdfz8b759n8ojz', 'port': 80, 'weight': 30},
                 ]
    
    def default_body(self):
        return SET_VSERVER_GROUP_ATTRIBUTE
    
    def test_set_vserver_group_attribute(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.set_vservergroup_attribute(vserver_group_id=self.vserver_group_id,
                                                                             vserver_group_name=self.vservergroupname,
                                                                             backend_servers=self.backendservers)
        self.assertEqual(result[u'VServerGroupId'], 'rsp-3ns1daa6i1fkh')


class TestDeleteVServerGroup(ACSMockServiceTestCase):
    connection_class = SLBConnection

    vserver_group_id = 'rsp-3ns4pyvudkcyh'
    load_balancer_id = 'lb-3nsu8xgxs2eyp8arntiyq'
        
    def default_body(self):
        return DELETE_VSERVER_GROUP
    
    def test_delete_vserver_group(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_vserver_group(load_balancer_id=self.load_balancer_id,
                                                                       vserver_group_id=self.vserver_group_id)
        if changed is True:
            self.assertEqual(result[0]['Success Message'], 'VServer Group Deleted Successfully')
        if changed is False:
            self.assertEqual(result[0]['Error Message'], 'Server Group Not Exist')


class TestModifyLoadBalancerInternetSpec(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region_id = "cn-beijing"
    load_balancer_id = "lb-dj1j7uy78htxtj75rckqo"
    bandwidth = 5
    internet_charge_type = "paybytraffic"

    def default_body(self):
        return MODIFY_LOAD_BALANCER_INTERNET_SPEC

    def test_modify_load_balancer_internet_spec(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.modify_slb_internet_spec(
            load_balancer_id=self.load_balancer_id, internet_charge_type=self.internet_charge_type,
            bandwidth=self.bandwidth)
        if changed:
            self.assertEqual(result[0]['RequestId'], "80A96F3E-FD71-43ED-9E7B-EFA159CF55E1")


class TestRemoveVServerGroup(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = 'cn-hongkong'
    slb_id = 'lb-3nsspc0zn9wntvlyoe3tw'
    vserver_group_id = 'rsp-3nsmpxzq8p6mi'
    backend_servers = [
                       {'ServerId': 'i-j6ci04oi33i9pv2hnafk', 'Port': 80}
                      ]
    
    def default_body(self):
        return REMOVE_VSERVER_GROUP
    
    def test_remove_vserver_group(self):
        self.set_http_response(status_code=200)
        result = self.service_connection.remove_vserver_group(slb_id=self.slb_id,
                                                              vserver_group_id=self.vserver_group_id,
                                                              backend_servers=self.backend_servers)
        self.assertEqual(result[u'VServerGroupId'], "rsp-3nsmpxzq8p6mi")


class TestAddBackendServers(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = "ap-southeast-1"
    loadbalancerid = 'lb-gs5s110nqe1gnijldgl39'
    backendservers = \
        [
            {'server_id': 'i-t4n73vl5oaxuxmigat9x', 'weight': 100},
            {'server_id': 'i-t4njdk51ejf1a3xm9s2n', 'weight': 40},
        ]

    def default_body(self):
        return ADD_BACKEND_SERVERS

    def test_add_backend_servers(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.add_backend_servers(load_balancer_id = self.loadbalancerid,
                                                                      backend_servers = self.backendservers)
        self.assertEqual(result[0], {u'ServerId': u'i-t4n73vl5oaxuxmigat9x', u'Weight': 100})
        self.assertEqual(result[1], {u'ServerId': u'i-t4njdk51ejf1a3xm9s2n', u'Weight': 40})


class TestRemoveBackendServers(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = "ap-southeast-1"
    loadbalancerid = 'lb-gs5s110nqe1gnijldgl39'
    backendservers = \
        [
           'i-t4n73vl5oaxuxmigat9x',
           'i-t4njdk51ejf1a3xm9s2n'
        ]

    def default_body(self):
        return REMOVE_BACKEND_SERVERS

    def test_remove_backend_servers(self):
        self.set_http_response(status_code=200)
        changed, current_backend_servers, result = self.service_connection.remove_backend_servers(
            load_balancer_id=self.loadbalancerid, backend_server_ids=self.backendservers)
        self.assertEqual(current_backend_servers[0], {u'ServerId': u'i-t4n73vl5oaxuxmigat9', u'Weight': 100})


class TestSetBackendServers(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = "ap-southeast-1"
    loadbalancerid = 'lb-gs5s110nqe1gnijldgl39'
    backendservers = \
        [
            {'server_id': 'i-t4n73vl5oaxuxmigat9x', 'weight': 100},
            {'server_id': 'i-t4njdk51ejf1a3xm9s2n', 'weight': 40},
        ]

    def default_body(self):
        return SET_BACKEND_SERVERS

    def test_set_backend_servers(self):
        self.set_http_response(status_code=200)
        changed, current_backend_servers, result = self.service_connection.set_backend_servers(
            load_balancer_id = self.loadbalancerid, backend_servers = self.backendservers)
        self.assertEqual(current_backend_servers[0], {u'ServerId': u'i-t4n73vl5oaxuxmigat9x', u'Weight': 100})
        self.assertEqual(current_backend_servers[1], {u'ServerId': u'i-t4njdk51ejf1a3xm9s2n', u'Weight': 40})


class TestDescribeBackendServersHealth(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = "ap-southeast-1"
    loadbalancerid = 'lb-gs5s110nqe1gnijldgl39'
    ports = [80]

    def default_body(self):
        return DESCRIBE_BACKEND_SERVERS_HEALTH

    def test_describe_backend_servers_health(self):
        self.set_http_response(status_code=200)
        backend_servers_health_status, result = self.service_connection.describe_backend_servers_health_status(
            load_balancer_id = self.loadbalancerid, listener_ports = self.ports)
        self.assertEqual(backend_servers_health_status[0],
                         {u'ServerId': u'i-t4n73vl5oaxuxmigat9x', u'ListenerPort': 80, u'Weight': 100})
        self.assertEqual(backend_servers_health_status[1],
                         {u'ServerId': u'i-t4njdk51ejf1a3xm9s2n', u'ListenerPort': 80, u'Weight': 40})


class TestModifyVServerGroup(ACSMockServiceTestCase):
    connection_class = SLBConnection

    region = 'cn-beijing'    
    vserver_group_id = 'rsp-dj1v1fcup9efj'
    purge_backend_servers = [
                       {'server_id': 'i-2zec953dxl686o8p4vq1', 'port': 323},
                      ]
    backend_servers = [
                       {'server_id': 'i-2zehfxz81ar5kvptw8b1', 'port': 656, 'weight': '100'},
                      ]
    
    def default_body(self):
        return MODIFY_VSERVER_GROUP
    
    def test_modify_vserver_group(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.modify_vserver_group_backend_server(
            vserver_group_id=self.vserver_group_id, purge_backend_servers=self.purge_backend_servers,
            backend_servers=self.backend_servers)
        self.assertEqual(result[u'VServerGroupId'], 'rsp-dj1v1fcup9efj')
