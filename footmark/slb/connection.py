# encoding: utf-8
"""
Represents a connection to the SLB service.
"""

import time
import json
from footmark.connection import ACSQueryConnection
from footmark.slb.regioninfo import RegionInfo
from footmark.exception import SLBResponseError
from footmark.slb.slb import LoadBalancer, BackendServer, VServerGroup, LoadBalancerListener


class SLBConnection(ACSQueryConnection):
    SDKVersion = '2014-05-15'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    ResponseError = SLBResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None):
        """
        Init method to create a new connection to SLB.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.SLBSDK = 'aliyunsdkslb.request.v' + self.SDKVersion.replace('-', '')

        super(SLBConnection, self).__init__(acs_access_key_id,
                                            acs_secret_access_key,
                                            self.region, self.SLBSDK, security_token, user_agent=user_agent)
    
    def describe_vserver_group_attribute(self, vserver_group_id):
        """
        describe vserver group
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :return: return the vserver group object
        """
        params = {}
        self.build_list_params(params, vserver_group_id, 'VServerGroupId')

        return self.get_object('DescribeVServerGroupAttribute', params, VServerGroup)
    
    def  describe_vserver_groups(self, load_balancer_id):
        """
        describe vserver group
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :return: return the vserver group object
        """
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        
        return self.get_object('DescribeVServerGroups', params, ['VServerGroups' ,VServerGroup])
    
    def create_vserver_group(self, load_balancer_id, vserver_group_name, backend_servers):
        """
        create vserver group
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :type load_balancer_id: string
        :param load_balancer_id: Unique identifier for load balancer
        :type backend_servers: list
        :param backend_servers:Backend server list
        :return: return the vserver group object
        """
        params = {}
        backend_serverlist = []
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, vserver_group_name, 'VServerGroupName')
        for servers in backend_servers:
            backend_serverlist.append({
                'ServerId': servers['instance_id'],
                'Port': servers['port'],
                'Weight': servers['weight']
            })
        self.build_list_params(params, backend_serverlist, 'BackendServers')
        
        return self.get_object('CreateVServerGroup', params, VServerGroup)
    
    def set_vserver_group_attribute(self, vserver_group_id, vserver_group_name = '', backend_servers = []):
        """
        set vserver group attribute
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :type load_balancer_id: string
        :param load_balancer_id: Unique identifier for load balancer
        :type backend_servers: list
        :param backend_servers:Backend server list
        :return: return the vserver group object
        """
        params = {}
        backend_serverlist = []
        self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        if vserver_group_name:
            self.build_list_params(params, vserver_group_name, 'VServerGroupName')
        if backend_servers:
            for servers in backend_servers:
                backend_serverlist.append({
                    'ServerId': servers['instance_id'],
                    'Port': servers['port'],
                    'Weight': servers['weight']
                })
            self.build_list_params(params, backend_serverlist, 'BackendServers')
        
        return self.get_object('SetVServerGroupAttribute', params, VServerGroup)
    
    def add_vserver_group_backend_servers(self, vserver_group_id, backend_servers):
        """
        add vserver group backend servers
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :type backend_servers: list
        :param backend_servers:Backend server list
        :return: return the vserver group object
        """
        params = {}
        backend_serverlist = []
        self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        self.build_list_params(params, backend_servers, 'BackendServers')
        for servers in backend_servers:
            backend_serverlist.append({
                'ServerId': servers['instance_id'],
                'Port': servers['port'],
                'Weight': servers['weight']
            })
        self.build_list_params(params, backend_serverlist, 'BackendServers')
        
        return self.get_object('AddVServerGroupBackendServers', params, VServerGroup)
    
    def remove_vserver_group_backend_servers(self, vserver_group_id, backend_servers):
        """
        remove vserver group backend servers
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :type backend_servers: list
        :param backend_servers:Backend server list
        :return: return the vserver group object
        """
        params = {}
        backend_serverlist = []
        self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        for servers in backend_servers:
            backend_serverlist.append({
                'ServerId': servers['instance_id'],
                'Port': servers['port']
            })
        self.build_list_params(params, backend_serverlist, 'BackendServers')
        
        return self.get_object('RemoveVServerGroupBackendServers', params, VServerGroup)
    
    def modify_vserver_group_backend_servers(self, vserver_group_id, old_backend_servers = [], new_backend_servers = []):
        """
        modify vserver group backend servers
        :type vserver_group_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :type old_backend_servers: list
        :param old_backend_servers:Old backend server list
        :type new_backend_servers: list
        :param new_backend_servers:new backend server list
        :return: return the vserver group object
        """
        params = {}
        old_backend_serverlist = []
        new_backend_serverlist = []
        self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        if old_backend_servers:
            for servers in old_backend_servers:
                old_backend_serverlist.append({
                    'ServerId': servers['instance_id'],
                    'Port': servers['port']
            })
            self.build_list_params(params, old_backend_serverlist, 'OldBackendServers')
        if new_backend_servers:
            for servers in new_backend_servers:
                new_backend_serverlist.append({
                    'ServerId': servers['instance_id'],
                    'Port': servers['port'],
                    'Weight': servers['weight']
            })
            self.build_list_params(params, new_backend_serverlist, 'NewBackendServers')
        
        return self.get_object('ModifyVServerGroupBackendServers', params, VServerGroup)
    
    def delete_vserver_group(self, vserver_group_id):
        """
        delete vserver group
        :type load_balancer_id: string
        :param vserver_group_id: Unique identifier for the virtual server group
        :return: return bool
        """
        params = {}
        self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        
        return self.get_status('DeleteVServerGroup', params)    

    def create_load_balancer(self, load_balancer_name=None, address_type=None, vswitch_id=None, client_token=None,
                             internet_charge_type=None, master_zone_id=None, slave_zone_id=None, bandwidth=None):
        """
        Creates a Server Load Balancer
        :type load_balancer_name: string
        :param load_balancer_name: Name to the server load balancer
        :type address_type: string
        :param address_type:  Address type. value: internet or intranet
        :type vswitch_id: string
        :param vswitch_id: The vswitch id of the VPC instance. This option is invalid if address_type parameter is
         provided as internet.
        :type internet_charge_type: string
        :param internet_charge_type: Charging mode for the public network instance
         Value: paybybandwidth or paybytraffic
        :type master_zone_id: string
        :param master_zone_id: Name of of availability zones to enable on this SLB
        :type slave_zone_id: string
        :param slave_zone_id: Name of of availability zones to enable on this SLB
        :type bandwidth: string
        :param bandwidth: Bandwidth peak of the public network instance charged per fixed bandwidth
        :return: return the created load balancer details
        """

        params = {}

        if load_balancer_name:
            self.build_list_params(params, load_balancer_name, 'LoadBalancerName')
        if address_type:
            self.build_list_params(params, address_type, 'AddressType')
        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')
        if internet_charge_type:
            self.build_list_params(params, internet_charge_type, 'InternetChargeType')
        if master_zone_id:
            self.build_list_params(params, master_zone_id, 'MasterZoneId')
        if slave_zone_id:
            self.build_list_params(params, slave_zone_id, 'SlaveZoneId')
        if bandwidth:
            self.build_list_params(params, bandwidth, 'Bandwidth')
        if client_token:
            self.build_list_params(params, client_token, 'ClientToken')
        slb = self.get_object('CreateLoadBalancer', params, LoadBalancer)
        return self.describe_load_balancer_attribute(slb.id)

    def add_listeners(self, load_balancer_id, purge_listener=None, listeners=None):
        """
        Add Listeners to existing ServerLoadBalancer
        :type load_balancer_id: str
        :param load_balancer_id: Id of ServerLoadBalancer
        :type purge_listener: bool
        :param purge_listener:  Whether to remove existing Listener or not
        :type listeners: dict
        :param listeners: List of ports/protocols for this SLB to listen on
        :return: returns RequestId id of request
        """
        params = {}
        results = []
        deleted_listener = []
        changed = False

        try:
            # find out all listeners of the load balancer
            self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
            slb_details = self.get_status('DescribeLoadBalancerAttribute', params)

            # if purge_listener is true then delete existing listeners
            if purge_listener:
                if slb_details:
                    if len(slb_details[u'ListenerPortsAndProtocal'][u'ListenerPortAndProtocal']) > 0:
                        for slb_listener in slb_details[u'ListenerPortsAndProtocal'][u'ListenerPortAndProtocal']:
                            params = {}
                            self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
                            self.build_list_params(params, slb_listener[u'ListenerPort'], 'ListenerPort')
                            response = self.get_status('DeleteLoadBalancerListener', params)
                            deleted_listener.append(response)
                            changed = True
                            
            # add listeners to load balancer
            if listeners:
                for listener in listeners:
                    if listener:
                        if 'protocol' in listener:
                            protocol = str(listener['protocol']).lower()
                            # Add HTTP Listener to Load Balancer
                            if protocol in ['http']:
                                listener_result = self.create_load_balancer_http_listener(load_balancer_id, listener)
                                if listener_result:                                    
                                    results.append({"http_listener_result": listener_result[1]})
                                    # modify changed param according to listener result
                                    if changed is False:
                                        changed = listener_result[0]

                            # Add HTTPS Listener to Load Balancer
                            elif protocol in ['https']:
                                listener_result = self.create_load_balancer_https_listener(load_balancer_id, listener)
                                if listener_result:
                                    results.append({"https_listener_result": listener_result[1]})
                                    # modify changed param according to listener result
                                    if changed is False:
                                        changed = listener_result[0]

                            # Add TCP Listener to Load Balancer
                            elif protocol in ['tcp']:
                                listener_result = self.create_load_balancer_tcp_listener(load_balancer_id, listener)
                                if listener_result:
                                    results.append({"tcp_listener_result": listener_result[1]})
                                    # modify changed param according to listener result
                                    if changed is False:
                                        changed = listener_result[0]

                            # Add UDP Listener to Load Balancer
                            elif protocol in ['udp']:
                                listener_result = self.create_load_balancer_udp_listener(load_balancer_id, listener)
                                if listener_result:
                                    results.append({"udp_listener_result": listener_result[1]})
                                    # modify changed param according to listener result
                                    if changed is False:
                                        changed = listener_result[0]
                            else:
                                results.append({"Error Message": "Invalid Listener Protocol " + listener['protocol']})

        except Exception as ex:
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def create_load_balancer_listener(self, load_balancer_id,\
                                            protocol,\
                                            listener_port,\
                                            backend_server_port,\
                                            bandwidth=None,\
                                            sticky_session='',\
                                            health_check='',\
                                            scheduler='',\
                                            sticky_session_type='',\
                                            cookie_timeout=None,\
                                            cookie='',\
                                            health_check_domain='',\
                                            health_check_uri='',\
                                            health_check_connect_port=None,\
                                            healthy_threshold=None,\
                                            unhealthy_threshold=None,\
                                            health_check_timeout=None,\
                                            health_check_interval=None,\
                                            health_check_http_code='',\
                                            vserver_group_id='',\
                                            gzip='',\
                                            server_certificate_id='',\
                                            master_slave_server_group_id='',\
                                            persistence_timeout=None,\
                                            health_check_connect_timeout=None,\
                                            xforwarded_for = 'on',\
                                            ca_certificate_id=''):
        """
        Create HTTP Listener; create Listeners based on the HTTP protocol for the Server Load Balancer instance,
        including policies and health check configurations based on the HTTP protocol
        :type load_balancer_id: string
        :param load_balancer_id: load balance id
        :type listener_port: int
        :param listener_port: Server Load Balancer instance frontend port. Value: 1-65535
        :type backend_server_port: int
        :param backend_server_port: Server Load Balancer instance backend port. Value: 1-65535
        :type bandwidth: int
        :param bandwidth: Listener bandwidth. Value: -1 / 1-1000 Mbps
        :type sticky_session: string
        :param sticky_session: Whether to open the Gzip compression
        :type protocol: string
        :param protocol: type of listener to create
        :type health_check: string
        :param health_check: Whether to enable health check
        :type health_check: string
        :param health_check: Whether to enable health check
        :type: scheduler: string
        :param: scheduler: Scheduling algorithm. Value: wrr / wlc / rr Default value: wrr
        :type: sticky_session_type: string
        :param: sticky_session_type: Mode for handling the cookie.
        :type: cookie_timeout: int
        :param: cookie_timeout: Cookie timeout.
        :type: cookie: string
        :param: cookie: The cookie configured on the server
        :type: health_check_domain: string
        :param: health_check_domain: Domain name used for health check.
        :type: health_check_uri: string
        :param: health_check_uri: URI used for health check
        :type: health_check_connect_port: int
        :param: health_check_connect_port: Port used for health check.
        :type: healthy_threshold: int
        :param: healthy_threshold: Threshold determining the result of the health check is success.
        :type: unhealthy_threshold: int
        :param: unhealthy_threshold: Threshold determining the result of the health check is fail. 
        :type: health_check_timeout: int
        :param: health_check_timeout: Maximum timeout of each health check response. 
        :type: health_check_http_code: string
        :param: health_check_http_code: Regular health check HTTP status code. Multiple codes are segmented by ",".
        :type: health_check_interval: int
        :param: health_check_interval: Time interval of health checks.
        :type: vserver_group_id: string
        :param: vserver_group_id: Virtual server group ID.
        :type: gzip: string
        :param: gzip: whether open Gzip compression
        :type: server_certificate_id: string
        :param: server_certificate_id: Server certificate ID.
        :type: master_slave_server_group_id: string
        :param: master_slave_server_group_id: Master standby server group ID
        :type: persistence_timeout: string
        :param: persistence_timeout: Timeout time for connection persistence.
        :type: health_check_connect_timeout: int
        :param: health_check_connect_timeout: Health check connection timeout.
        :type: xforwarded_for: int
        :param: xforwarded_for: Whether open access to the actual IP of visitors through X-Forwarded-For
        :type: ca_certificate_id: string
        :param: ca_certificate_id: CA certificate ID
        :return: returns request status
        """

        params = {}
        results = []
        changed = False
        listener_type_dic = dict(http="CreateLoadBalancerHTTPListener",\
                                 https= "CreateLoadBalancerHTTPSListener",\
                                 tcp="CreateLoadBalancerTCPListener",\
                                 udp="CreateLoadBalancerUDPListener")
        key = listener_type_dic.get(protocol, '')

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')
        self.build_list_params(params, backend_server_port, 'BackendServerPort')
        if bandwidth:
            self.build_list_params(params, bandwidth, 'Bandwidth')
        if sticky_session:
            self.build_list_params(params, sticky_session, 'StickySession')
        if health_check:
            self.build_list_params(params, health_check, 'HealthCheck')
        if scheduler:
            self.build_list_params(params, scheduler, 'Scheduler')
        if gzip:
            self.build_list_params(params, gzip, 'Gzip')
        if server_certificate_id:
            self.build_list_params(params, server_certificate_id, 'ServerCertificateId')
        if xforwarded_for:
            self.build_list_params(params, 'on', 'XForwardedFor')
        if sticky_session_type:
            self.build_list_params(params, sticky_session_type, 'StickySessionType')
        if cookie_timeout:
            self.build_list_params(params, cookie_timeout, 'CookieTimeout')
        if cookie:
            self.build_list_params(params, cookie, 'Cookie')
        if health_check_domain:
            self.build_list_params(params, health_check_domain, 'HealthCheckDomain')
        if health_check_uri:
            self.build_list_params(params, health_check_uri, 'HealthCheckURI')
        if health_check_connect_port:
            self.build_list_params(params, health_check_connect_port, 'HealthCheckConnectPort')
        if healthy_threshold:
            self.build_list_params(params, healthy_threshold, 'HealthyThreshold')
        if unhealthy_threshold:
            self.build_list_params(params, unhealthy_threshold, 'UnhealthyThreshold')
        if health_check_timeout:
            self.build_list_params(params, health_check_timeout, 'HealthCheckTimeout')
        if health_check_interval:
            self.build_list_params(params, health_check_interval, 'HealthCheckInterval')
        if health_check_http_code:
            self.build_list_params(params, health_check_http_code, 'HealthCheckHttpCode')
        if vserver_group_id:
            self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        if master_slave_server_group_id:
            self.build_list_params(params, master_slave_server_group_id, 'MasterSlaveServerGroupId')
        if persistence_timeout:
            self.build_list_params(params, persistence_timeout, 'PersistenceTimeout')
        if health_check_connect_timeout:
            self.build_list_params(params, health_check_connect_timeout, 'HealthCheckConnectTimeout')
        if ca_certificate_id:
            self.build_list_params(params, ca_certificate_id, 'CACertificateId')

        if self.get_status(key, params):
            return self.start_load_balancer_listener(load_balancer_id, listener_port)
        return False

    def set_listener_access_control_status(self, load_balancer_id, listener_port, access_control_status):
        """
        set listener access control status
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: int
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :type access_control_status: string
        :param load_balancer_id: Whether or not access control is enabled. open_white_list indicates the white list access control function is enabled.
        :return: returns bool
        """
        params = {}

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')
        self.build_list_params(params, access_control_status, 'AccessControlStatus')
        return self.get_status('SetListenerAccessControlStatus', params)

    def set_listener_attribute(self, load_balancer_id,\
                                    listener_port,\
                                    bandwidth,\
                                    protocol,\
                                    sticky_session='',\
                                    health_check='',\
                                    scheduler='',\
                                    sticky_session_type='',\
                                    cookie_timeout=None,\
                                    cookie='',\
                                    health_check_domain='',\
                                    health_check_uri='',\
                                    health_check_connect_port=None,\
                                    healthy_threshold=None,\
                                    unhealthy_threshold=None,\
                                    health_check_timeout=None,\
                                    health_check_interval=None,\
                                    health_check_http_code='',\
                                    vserver_group_id='',\
                                    gzip='',\
                                    server_certificate_id='',\
                                    master_slave_server_group_id='',\
                                    persistence_timeout=None,\
                                    health_check_connect_timeout=None,\
                                    ca_certificate_id='',\
                                    syn_proxy='',\
                                    health_check_type='',\
                                    vserver_group='',\
                                    master_slave_server_group='',
                                    xforwarded_for='on'):
        """
        set listener attribute
        :type load_balancer_id: string
        :param load_balancer_id: load balance id
        :type listener_port: int
        :param listener_port: Server Load Balancer instance frontend port. Value: 1-65535
        :type bandwidth: int
        :param bandwidth: Listener bandwidth. Value: -1 / 1-1000 Mbps
        :type sticky_session: string
        :param sticky_session: Whether to open the Gzip compression
        :type protocol: string
        :param protocol: type of listener to create
        :type health_check: string
        :param health_check: Whether to enable health check
        :type: scheduler: string
        :param: scheduler: Scheduling algorithm. Value: wrr / wlc / rr Default value: wrr
        :type: sticky_session_type: string
        :param: sticky_session_type: Mode for handling the cookie.
        :type: cookie_timeout: int
        :param: cookie_timeout: Cookie timeout.
        :type: cookie: string
        :param: cookie: The cookie configured on the server
        :type: health_check_domain: string
        :param: health_check_domain: Domain name used for health check.
        :type: health_check_uri: string
        :param: health_check_uri: URI used for health check
        :type: health_check_connect_port: int
        :param: health_check_connect_port: Port used for health check.
        :type: healthy_threshold: int
        :param: healthy_threshold: Threshold determining the result of the health check is success.
        :type: unhealthy_threshold: int
        :param: unhealthy_threshold: Threshold determining the result of the health check is fail.
        :type: health_check_timeout: int
        :param: health_check_timeout: Maximum timeout of each health check response.
        :type: health_check_http_code: string
        :param: health_check_http_code: Regular health check HTTP status code. Multiple codes are segmented by ",".
        :type: health_check_interval: int
        :param: health_check_interval: Time interval of health checks.
        :type: vserver_group_id: string
        :param: vserver_group_id: Virtual server group ID.
        :type: gzip: string
        :param: gzip: whether open Gzip compression
        :type: server_certificate_id: string
        :param: server_certificate_id: Server certificate ID.
        :type: master_slave_server_group_id: string
        :param: master_slave_server_group_id: Master standby server group ID
        :type: persistence_timeout: string
        :param: persistence_timeout: Timeout time for connection persistence.
        :type: health_check_connect_timeout: int
        :param: health_check_connect_timeout: Health check connection timeout.
        :type: xforwarded_for: int
        :param: xforwarded_for: Whether open access to the actual IP of visitors through X-Forwarded-For
        :type: ca_certificate_id: string
        :param: ca_certificate_id: CA certificate ID
        :type: syn_proxy: string
        :param: syn_proxy: CA certificate ID
        :type: health_check_type: string
        :param: health_check_type: health check type
        :type: vserver_group: string
        :param: vserver_group: Whether to use a virtual server group
        :type: master_slave_server_group: string
        :param: master_slave_server_group: Whether to use the primary and secondary server groups
        :return: returns request status
        """
        params = {}
        listener_type_dic = dict(http="SetLoadBalancerHTTPListenerAttribute",\
                                 https= "SetLoadBalancerHTTPSListenerAttribute",\
                                 tcp="SetLoadBalancerTCPListenerAttribute",\
                                 udp="SetLoadBalancerUDPListenerAttribute")
        key = listener_type_dic.get(protocol, '')

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')
        self.build_list_params(params, bandwidth, 'Bandwidth')
        if listener_port:
            self.build_list_params(params, listener_port, 'ListenerPort')
        if health_check:
            self.build_list_params(params, health_check, 'HealthCheck')
        if sticky_session:
            self.build_list_params(params, sticky_session, 'StickySession')
        if server_certificate_id:
            self.build_list_params(params, server_certificate_id, 'ServerCertificateId')
        if scheduler:
            self.build_list_params(params, scheduler, 'Scheduler')
        if xforwarded_for:
            self.build_list_params(params, 'on', 'XForwardedFor')
        if sticky_session_type:
            self.build_list_params(params, sticky_session_type, 'StickySessionType')
        if cookie_timeout:
            self.build_list_params(params, cookie_timeout, 'CookieTimeout')
        if cookie:
            self.build_list_params(params, cookie, 'Cookie')
        if health_check_domain:
            self.build_list_params(params, health_check_domain, 'HealthCheckDomain')
        if health_check_uri:
            self.build_list_params(params, health_check_uri, 'HealthCheckURI')
        if health_check_connect_port:
            self.build_list_params(params, health_check_connect_port, 'HealthCheckConnectPort')
        if healthy_threshold:
            self.build_list_params(params, healthy_threshold, 'HealthyThreshold')
        if unhealthy_threshold:
            self.build_list_params(params, unhealthy_threshold, 'UnhealthyThreshold')
        if health_check_timeout:
            self.build_list_params(params, health_check_timeout, 'HealthCheckTimeout')
        if health_check_interval:
            self.build_list_params(params, health_check_interval, 'HealthCheckInterval')
        if health_check_http_code:
            self.build_list_params(params, health_check_http_code, 'HealthCheckHttpCode')
        if vserver_group:
            self.build_list_params(params, vserver_group, 'VServerGroup')
        if vserver_group_id:
            self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        if master_slave_server_group_id:
            self.build_list_params(params, master_slave_server_group_id, 'MasterSlaveServerGroupId')
        if master_slave_server_group:
            self.build_list_params(params, master_slave_server_group, 'MasterSlaveServerGroup')
        if ca_certificate_id:
            self.build_list_params(params, ca_certificate_id, 'CACertificateId')
        if syn_proxy:
            self.build_list_params(params, syn_proxy, 'SynProxy')
        if health_check_type:
            self.build_list_params(params, health_check_type, 'HealthCheckType')
        if gzip:
            self.build_list_params(params, gzip, 'Gzip')
        if persistence_timeout:
            self.build_list_params(params, persistence_timeout, 'PersistenceTimeout')
        if health_check_connect_timeout:
            self.build_list_params(params, health_check_connect_timeout, 'HealthCheckConnectTimeout')

        return self.get_status(key, params)

    def delete_load_balancer_listener(self, load_balancer_id, listener_port):
        """
        delete load balance listener
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: string
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :return: returns bool
        """
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')

        return self.get_status('DeleteLoadBalancerListener', params)

    def start_load_balancer_listener(self, load_balancer_id, listener_port):
        """
        start load balance listener
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: string
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :return: returns bool
        """
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')

        return self.get_status('StartLoadBalancerListener', params)

    def stop_load_balancer_listener(self, load_balancer_id, listener_port):
        """
        stop load balance listener
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: string
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :return: returns bool
        """
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')

        return self.get_status('StopLoadBalancerListener', params)

    def add_listener_white_list_item(self, load_balancer_id, listener_port, source_items):
        """
        add load balance listener white list item
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: string
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :type source_items: string
        :param source_items: Access control list
        :return: returns bool
        """
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')
        self.build_list_params(params, source_items, 'SourceItems')

        return self.get_status('AddListenerWhiteListItem', params)

    def remove_listener_white_list_item(self, load_balancer_id, listener_port, source_items):
        """
        remove load balance listener white list item
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: string
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :type source_items: string
        :param source_items: Access control list
        :return: returns bool
        """
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')
        self.build_list_params(params, source_items, 'SourceItems')

        return self.get_status('RemoveListenerWhiteListItem', params)

    def describe_load_balancer_listener_attribute(self, load_balancer_id, listener_port, protocol):
        """
        describe load balancer listener attribute
        :type load_balancer_id: string
        :param load_balancer_id: Load balancer instance  id
        :type listener_port: string
        :param listener_port: Load balancer instance  frontend port. Value: 1-65535
        :return: obj: object of listener
        """
        action = "DescribeLoadBalancer"
        if protocol is None or len(str(protocol))<=0:
            lb = self.describe_load_balancer_attribute(load_balancer_id)
            if lb is None:
                return None
            for pp in lb.listener_ports_and_protocol.get("listener_port_and_protocol"):
                if pp.get("listener_port") == listener_port:
                    protocol = pp.get("listener_protocol")
                    break

        action += str.upper(protocol) + "ListenerAttribute"

        params = {}

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, listener_port, 'ListenerPort')
        try:
            obj = self.get_object(action, params, LoadBalancerListener)
        except Exception as e:
            obj = None
        return obj

    def add_backend_servers(self, load_balancer_id, backend_servers=None):
        """
        Add BackendServer to existing LoadBalancer
        :type load_balancer_id: str
        :param load_balancer_id: ID of server load balancer
        :type backend_servers: list
        :param backend_servers: list of dictionary containing server Id and weight of  backend server instance
        :return: return changed status, current_backend_servers and message with descriptive information
        """

        params = {}
        results = []
        current_backend_servers = []
        changed = False

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')

        backend_servers_list = []

        for backend_server in backend_servers:
            backend_servers_list.append({"ServerId": backend_server['server_id'],
                                         "Weight": str(backend_server['weight'])})

        backend_servers_json = json.dumps(backend_servers_list)
        self.build_list_params(params, backend_servers_json, 'BackendServers')

        return self.get_list('AddBackendServers', params, ["BackendServers", BackendServer])
    
    def purge_add_backend_server(self, load_balancer_id, instance_ids=None, purge_instance_ids=None):
        """
        Remove existing Instances or Backend Server and Add new instances or Backend Server to Load Balancer
        :type load_balancer_id: str
        :param load_balancer_id: Id of ServerLoadBalancer
        :type instance_ids:list
        :param instance_ids: Id of Instances or Backend Server
        :type purge_instance_ids: bool
        :param purge_instance_ids: Whether to remove existing Instances or Backend Servers
        :return: Returns Id of newly added Load Balancer
        """
        params = {}
        results = []
        instances = []
        changed = False

        try:
            # List all Backend Servers
            self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
            response = self.get_status('DescribeLoadBalancerAttribute', params)
            for instance in response[u'BackendServers'][u'BackendServer']:
                # append id of all Backend Servers to list
                instances.append(str(instance[u'ServerId']))

            # Remove instances only when purge_instance_ids is True
            if len(instances) > 0 and (purge_instance_ids is True):
                # Remove all Backend Servers
                response = self.remove_backend_servers(load_balancer_id=load_balancer_id, backend_server_ids=instances)
                if 'error' in (''.join(str(response))).lower():
                    results.append(response[2])
                else:
                    results.append(response[2][0])
                    changed = True

            # Add Backend Server to Load Balancer
            if instance_ids:
                if len(instance_ids) > 0:
                    backend_servers = []
                    for backend_server_id in instance_ids:
                        backend_servers.append({"server_id": backend_server_id, "weight": 100})

                    response = self.add_backend_servers(load_balancer_id, backend_servers)
                    if 'error' in (''.join(str(response))).lower():
                        results.append({"backend_server_result": response[2]})
                    else:
                        results.append({"backend_server_result": response[1][0]})
                        changed = True
        except Exception as ex:
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results    

    def remove_backend_servers(self, load_balancer_id=None, backend_server_ids=None):
        """
        :type load_balancer_id: str
        :param load_balancer_id: ID of server load balancer
        :type backend_server_ids: list
        :param backend_server_ids: list of IDs of backend server instance
        :return: return changed status, current_backend_servers and message with descriptive information
        """
        params = {}

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')

        backend_servers_json = json.dumps(backend_server_ids)

        self.build_list_params(params, backend_servers_json, 'BackendServers')

        return self.get_list('RemoveBackendServers', params, ["BackendServers", BackendServer])

    def set_backend_servers(self, load_balancer_id=None, backend_servers=None):
        """
        Set Backend Server to Load Balancer
        :type load_balancer_id: str
        :param load_balancer_id: ID of server load balancer
        :type backend_servers: list
        :param backend_servers: list of dictionary containing server Id and weight of  backend server instance
        :return: return changed status, current_backend_servers and message with descriptive information
        """

        params = {}
        results = []
        current_backend_servers = []
        changed = False

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')

        backend_servers_list = []

        for backend_server in backend_servers:
            backend_servers_list.append({"ServerId": backend_server['server_id'],
                                         "Weight": str(backend_server['weight'])})

        backend_servers_json = json.dumps(backend_servers_list)
        self.build_list_params(params, backend_servers_json, 'BackendServers')

        return self.get_list('SetBackendServers', params, ["BackendServers", BackendServer])

    def describe_backend_servers_health_status(self, load_balancer_id=None, port=None):
        """
        :type load_balancer_id: str
        :param load_balancer_id: ID of server load balancer
        :type port: list
        :param port: list of Ports used by the Server Load Balancer instance frontend for health check
        :return: return backend servers with health status and message with descriptive information
        """
        params = {}
        results = []
        backend_servers_health_status = []

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')

        if port:
            self.build_list_params(params, port, 'ListenerPort')

        return self.get_list('DescribeHealthStatus', params, ["BackendServers", BackendServer])

    def set_load_balancer_status(self, load_balancer_id, load_balancer_status):
        """
        Method added to Set Load Balancer Status
        :type load_balancer_id: List
        :param load_balancer_id: ID of server load balancer
        :type load_balancer_status: String
        :param load_balancer_status: Status of an Server Load Balancer instance
            Value: inactive | active
        :return: return name of the operating interface, which is
            specified in the system
        """
        params = {}
       
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')        
        self.build_list_params(params, load_balancer_status, 'LoadBalancerStatus')
        
        return self.get_status('SetLoadBalancerStatus', params)

    def set_load_balancer_name(self, load_balancer_id, load_balancer_name):
        """
        Set name or alias to the ServerLoadBalancer
        Method added to Set Load Balancer Name
        :type load_balancer_id: str
        :param load_balancer_id: ID of a Server Load Balancer instance
        :type load_balancer_id: str
        :param load_balancer_name: Displayed name of an Server Load Balancer instance. When the parameter is not
         specified, an instance name is allocated by the system by default.
        :return: returns the request_id of request
        """
        changed = False
        results = []
        params = {}
        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        self.build_list_params(params, load_balancer_name, 'LoadBalancerName')
        return self.get_status('SetLoadBalancerName', params)

    def delete_load_balancer(self, slb_id):
        """
        Method added to Delete Load Balancer
        :type slb_id: string
        :param slb_id: Id of the server load balancer
        :return: Return status of Operation
        """
        results = []
        params = {}

        self.build_list_params(params, slb_id, 'LoadBalancerId')
        return self.get_status('DeleteLoadBalancer', params)   
        
    def modify_slb_internet_spec(self, load_balancer_id, internet_charge_type=None, bandwidth=None):
        """
        Modify internet specifications of existing LoadBalancer, like internet_charge_type or bandwidth
        :type load_balancer_id: str
        :param load_balancer_id: The unique ID of an Server Load Balancer instance
        :type internet_charge_type: str
        :param internet_charge_type: Charging mode for the public network instance
        :type bandwidth: int
        :param bandwidth: Bandwidth peak of the public network instance charged per fixed bandwidth
        :return: returns the request_id of request
        """
        
        results = []
     
        params = {}  

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        if internet_charge_type:
            self.build_list_params(params, internet_charge_type, 'InternetChargeType')
        if bandwidth:
            self.build_list_params(params, bandwidth, 'Bandwidth')
        return self.get_status('ModifyLoadBalancerInternetSpec', params)
    

    def describe_load_balancer_attribute(self, load_balancer_id):
        """
        Describe attributes of Load Balancer
        :type load_balancer_id: string
        :param load_balancer_id: id of the load balancer
        :return: load balance attributes in dictionary format if found else None
        """

        params = {}

        self.build_list_params(params, load_balancer_id, 'LoadBalancerId')

        return self.get_object('DescribeLoadBalancerAttribute', params, LoadBalancer)
    
    def describe_load_balancers(self, load_balancer_id = None, load_balancer_name = None):
        """
        Describe Load Balancers
        :type load_balancer_id: string
        :param load_balancer_id: id of the load balancer
        :type load_balancer_name: string
        :param load_balancer_name: name of the load balancer
        :return: load balance in dictionary format if found else None
        """

        params = {}
        if load_balancer_id:
            self.build_list_params(params, load_balancer_id, 'LoadBalancerId')
        if load_balancer_name:
            self.build_list_params(params, load_balancer_name, 'LoadBalancerName')
        return self.get_list('DescribeLoadBalancers', params,  ['LoadBalancers', LoadBalancer])

    def add_vservergroup_backend_server(self, vserver_group_id, backend_servers):
        """
        Add a back-end server in a virtual server group, add a set of back-end servers to a specific virtual server
            group in the SLB,
        and return a list of back-end servers in that virtual server group.
        :type vserver_group_id: string
        :param vserver_group_id: The unique identifier for the virtual server group
        :param backend_servers:  - List of hash/dictionary of backend servers to add in
          - '[{"key":"value", "key":"value"}]', keys allowed:
            - server_id (required:true, description: Unique id of Instance to add)
            - port (required:true, description: The back-end server using the port, range: 1-65535)
            - weight (required:true; default: 100, description: Weight of the backend server, in the range of 1-100 )
        :return: VServerGroupId	String	The unique identifier for the virtual server group
                 BackendServers	List	Array format, returns the operation is successful,
                 the virtual server group all the back-end server list, the list of elements in the structure see
                 BackendServer
        """
        params = {}
        changed = False
        results = []
        backend_serverlist = []       
        if vserver_group_id:
            self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        if backend_servers:
            for servers in backend_servers:
                backend_serverlist.append({'ServerId': servers['server_id'],
                                           'Port': servers['port'],
                                           'Weight': servers['weight']})
                
            self.build_list_params(params, json.dumps(backend_serverlist), 'BackendServers')
        try:
            results = self.get_status('AddVServerGroupBackendServers', params)           
            changed = True
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append("Error Code:" + error_code + " ,Error Message:" + error_msg)

        return changed, results

    def remove_vserver_group_backend_server(self, vserver_group_id, purge_backend_servers):
        """        
        Method to Remove Vserver Group Backend server
        :type vserver_group_id: string
        :param vserver_group_id: Virtual server group Id
        :type purge_backend_servers:  List of hash/dictionary
        :param purge_backend_servers:
          - List of hash/dictionary of backend servers to remove
          - '[{"key":"value", "key":"value"}]', keys allowed:
            - server_id (required:true, description: Unique id of Instance to remove)
            - port (required:true, description: The back-end server using the port, range: 1-65535)          
                               
        :return: it return public parameters with ,VServerGroupId The unique identifier for the virtual server.
                 and BackendServers Array format, list of back-end servers in the virtual server group.
                 The structure of the elements in the list is detailed in BackendServer
        """
        
        params = {}
        results = []
        changed = False
        backend_serverlist = []
           
        if vserver_group_id:
            self.build_list_params(params, vserver_group_id, 'VServerGroupId')
        if purge_backend_servers:
            for servers in purge_backend_servers:
                backend_serverlist.append({'ServerId': servers['server_id'], 'Port': servers['port']})
            self.build_list_params(params, json.dumps(backend_serverlist), 'BackendServers')

        try: 
            results = self.get_status('RemoveVServerGroupBackendServers', params)
            changed = True 
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def modify_vserver_group_backend_server(self, vserver_group_id, purge_backend_servers, backend_servers):
        '''
        Modify VServer Group Backend Server
        :type vserver_group_id: string
        :param vserver_group_id:Virtual server group Id
        :type purge_backend_servers:  List of hash/dictionary
        :param purge_backend_servers:
          - List of hash/dictionary of backend servers to add in
          - '[{"key":"value", "key":"value"}]', keys allowed:
            - server_id (required:true, description: Unique id of Instance to add)
            - port (required:true, description: The back-end server using the port, range: 1-65535)
        :type backend_servers:  List of hash/dictionary
        :param backend_servers:
          - List of hash/dictionary of backend servers to add in
          - '[{"key":"value", "key":"value"}]', keys allowed:
            - server_id (required:true, description: Unique id of Instance to add)
            - port (required:true, description: The back-end server using the port, range: 1-65535)
            - weight (required:true; default: 100, description: Weight of the backend server, in the range of 1-100 )

        :return: Change the virtual back-end servers in the server group, in a particular SLB virtual server
                 group by adding / deleting the back-end server to replace the current server group, the group returned
                 to the virtual server back-end server list.
        '''
        params = {}
        results = []
        set_results = []
        add_results = []
        set_server_attribute = []
        add_backend_server = []
        delete_backend_servers = []
        delete_backend_servers_id = []
        filter_backend_servers_id = []
        final_backend_servers_id = []
        changed = False
        serverid_param = 'server_id'
        try: 

            self.build_list_params(params, vserver_group_id, 'VServerGroupId')
            result_all_backend_servers = self.get_status('DescribeVServerGroupAttribute', params)
            all_backend_servers = result_all_backend_servers['BackendServers']['BackendServer']
            if all_backend_servers:
                for purge_backend_server in purge_backend_servers:                    
                    for all_backend_server in all_backend_servers:
                        if purge_backend_server[serverid_param] in all_backend_server['ServerId']:
                            delete_backend_servers.append(purge_backend_server)
                            delete_backend_servers_id.append(purge_backend_server[serverid_param])
                            break
                
                for backend_server in backend_servers:
                    flag = False
                    for all_backend_server in all_backend_servers:
                        if backend_server[serverid_param] == all_backend_server['ServerId'] \
                                and backend_server[serverid_param] not in delete_backend_servers_id:
                            set_server_attribute.append(backend_server)
                            flag = True
                            break                       
                    if not flag:   
                        add_backend_server.append(backend_server)
            else:
                 add_backend_server.append(backend_servers[0])             
           
            if delete_backend_servers:
               changed, result = self.remove_vserver_group_backend_server(vserver_group_id, delete_backend_servers)
            
            if set_server_attribute:
                changed, set_results = self.set_vservergroup_attribute(vserver_group_id, vserver_group_name=None,
                                                                       backend_servers=set_server_attribute)
    
            if add_backend_server:
                changed, add_results = self.add_vservergroup_backend_server(vserver_group_id, add_backend_server)
            changed = True
            
            if set_results:
                results = set_results
                filter_backend_servers_id = set_results['BackendServers']['BackendServer']
            
            if add_results:
                results = add_results
                filter_backend_servers_id += add_results['BackendServers']['BackendServer']

            for backend_server in backend_servers:
                flag = False
                for filter_backend_servers in filter_backend_servers_id:
                    if filter_backend_servers["ServerId"] == backend_server[serverid_param] and\
                                    filter_backend_servers["Port"] == backend_server["port"] and not flag:
                        flag = True
                        final_backend_servers_id.append(filter_backend_servers)
            if final_backend_servers_id:
                results['BackendServers']['BackendServer'] = final_backend_servers_id
            if 'VServerGroupName' in results:
                del results['VServerGroupName']
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def describe_vservergroup_backendserver(self, vserver_group_id, backend_servers):
        """
        describe vserver group backend server      
        :type vserver_group_id: string
        :param vserver_group_id: The unique identifier for the virtual server group
        :type backend_servers:  List of hash/dictionary
        :param backend_servers:
          - List of hash/dictionary of backend servers to add in
          - '[{"key":"value", "key":"value"}]', keys allowed:
            - server_id (required:true, description: Unique id of Instance to add)
            - port (required:true, description: The back-end server using the port, range: 1-65535)
            - weight (required:true; default: 100, description: Weight of the backend server, in the range of 1-100 )
        :return: VServerGroupId	String	The unique identifier for the virtual server group
                 BackendServers	List	Array format, returns the operation is successful,
                 the virtual server group all the back-end server list, the list of elements in the structure
                 see BackendServer
        """
        changed_flag = True
        results = []   
        try:
            changed_vsg, result_vsgs = self.describe_vservergroup_attributes(vserver_group_id=vserver_group_id)
            if result_vsgs and changed_vsg:
                for backend_server in backend_servers:
                    final_check =False
                    for result_vsg in result_vsgs["BackendServers"]["BackendServer"]:
                        if backend_server["server_id"] == result_vsg["ServerId"] and backend_server["port"] \
                                == result_vsg["Port"]:
                            final_check = True  
                            break              
                    if not final_check: 
                        results.append(str(backend_server["server_id"])+" ECS with "
                                                                        "the port "+str(backend_server["port"])+" not "
                                                                        "match to perform operation")
                        changed_flag = False
            else:
                changed_flag = False
                results = result_vsgs
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append("Error Code:" + error_code + " ,Error Message:" + error_msg)

        return changed_flag, results

    def describe_vservergroup_backendserver_to_add(self, vserver_group_id, backend_servers):
        """
        describe vserver group backend server to add
        and return a list of back-end servers in that virtual server group.
        :type vserver_group_id: string
        :param vserver_group_id: The unique identifier for the virtual server group
        :type backend_servers:  List of hash/dictionary
        :param backend_servers:
          - List of hash/dictionary of backend servers to add in
          - '[{"key":"value", "key":"value"}]', keys allowed:
            - server_id (required:true, description: Unique id of Instance to add)
            - port (required:true, description: The back-end server using the port, range: 1-65535)
            - weight (required:true; default: 100, description: Weight of the backend server, in the range of 1-100 )
        :return: VServerGroupId	String	The unique identifier for the virtual server group
                 BackendServers	List	Array format, returns the operation is successful,
                 the virtual server group all the back-end server list, the list of elements in the structure
                 see BackendServer
        """
        changed_flag = True
        results = []   
        try:
            changed_vsg, result_vsgs = self.describe_vservergroup_attributes(vserver_group_id=vserver_group_id)
            if result_vsgs and changed_vsg:
                for backend_server in backend_servers:
                    changed_flag = True
                    for result_vsg in result_vsgs["BackendServers"]["BackendServer"]:
                        if (str(backend_server["server_id"]) == str(result_vsg["ServerId"])) \
                                and (str(backend_server["port"]) == str(result_vsg["Port"])):
                            changed_flag = False
                            break

                    if changed_flag is False:
                        results.append(str(backend_server["server_id"])+" "
                                                                        "ECS with port "+str(backend_server["port"])+" "
                                                                        "is already present")
            else:
                changed_flag =False
                results = result_vsgs
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append("Error Code:" + error_code + " ,Error Message:" + error_msg)

        return changed_flag, results

    # endregion



