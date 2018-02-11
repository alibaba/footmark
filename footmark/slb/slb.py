"""
Represents an SLB Security Group
"""
from footmark.slb.slbobject import TaggedSLBObject

class VServerGroup(TaggedSLBObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(VServerGroup, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'VServerGroup:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.vserver_group_id
        if name == 'name':
             return self.vserver_group_name

    def __setattr__(self, name, value):
        if name == 'id':
            self.vserver_group_id = value
        if name == 'name':
             self.vserver_group_name = value
        super(TaggedSLBObject, self).__setattr__(name, value)
    
    def set_attribute(self, vserver_group_name='', backend_servers = []):
        '''
        set attribute
        '''
        return self.connection.set_vserver_group_attribute(self.vserver_group_id, vserver_group_name, backend_servers)
    
    def add_backend_servers(self, backend_servers):
        '''
        add backend servers
        '''
        return self.connection.add_vserver_group_backend_servers(self.vserver_group_id, backend_servers)
    
    def remove_backend_servers(self, backend_servers):
        '''
        remove backend servers
        '''
        return self.connection.remove_vserver_group_backend_servers(self.vserver_group_id, backend_servers)
    
    def modify_backend_servers(self, old_backend_servers = [], new_backend_servers = []):
        '''
        modify backend servers
        '''
        return self.connection.modify_vserver_group_backend_servers(self.vserver_group_id, old_backend_servers, new_backend_servers)
    
    def delete(self):
        '''
        delete vserver group 
        '''
        return self.connection.delete_vserver_group(self.vserver_group_id)
    
    def describe_attribute(self):
        '''
        describe vserver group attribute 
        '''
        return self.connection.describe_vserver_group_attribute(self.vserver_group_id)

class LoadBalancerListener(TaggedSLBObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(LoadBalancerListener, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'LoadBalancerListener:%s' % self.port

    def __getattr__(self, name):
        if name == 'port':
            return self.listener_port
    
    def __setattr__(self, name, value):
        if name == 'port':
            self.listener_port = value
        super(TaggedSLBObject, self).__setattr__(name, value)
    
    def set_access_control_status(self, load_balancer_id, access_control_status):
        '''
        set listener access control status
        '''
        return self.connection.set_listener_access_control_status(load_balancer_id, self.listener_port, access_control_status)
    
    def add_white_list_item(self, load_balancer_id, source_items):
        '''
        add listener white list item
        '''
        return self.connection.add_listener_white_list_item(load_balancer_id, self.listener_port, source_items)
    
    def set_attribute(self, load_balancer_id='',\
                            bandwidth=None,\
                            sticky_session='',\
                            protocol='',\
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
                            master_slave_server_group=''):
        '''
        set listener attribute
        '''
        return self.connection.set_listener_attribute(load_balancer_id=load_balancer_id,\
                                    listener_port=self.listener_port,\
                                    bandwidth=bandwidth,\
                                    sticky_session=sticky_session,\
                                    protocol=protocol,\
                                    health_check=health_check,\
                                    scheduler=scheduler,\
                                    sticky_session_type=sticky_session_type,\
                                    cookie_timeout=cookie_timeout,\
                                    cookie=cookie,\
                                    health_check_domain=health_check_domain,\
                                    health_check_uri=health_check_uri,\
                                    health_check_connect_port=health_check_connect_port,\
                                    healthy_threshold=healthy_threshold,\
                                    unhealthy_threshold=unhealthy_threshold,\
                                    health_check_timeout=health_check_timeout,\
                                    health_check_interval=health_check_interval,\
                                    health_check_http_code=health_check_http_code,\
                                    vserver_group_id=vserver_group_id,\
                                    gzip=gzip,\
                                    server_certificate_id=server_certificate_id,\
                                    master_slave_server_group_id=master_slave_server_group_id,\
                                    persistence_timeout=persistence_timeout,\
                                    health_check_connect_timeout=health_check_connect_timeout,\
                                    ca_certificate_id=ca_certificate_id,\
                                    syn_proxy=syn_proxy,\
                                    health_check_type=health_check_type,\
                                    vserver_group=vserver_group,\
                                    master_slave_server_group=master_slave_server_group)
    
    def remove_white_list_item(self, load_balancer_id, source_items):
        '''
        remove listener white list item
        '''
        return self.connection.remove_listener_white_list_item(load_balancer_id, self.listener_port, source_items)
    
    def delete(self, load_balancer_id):
        '''
        delete load balance listener
        '''
        return self.connection.delete_load_balancer_listener(load_balancer_id, self.listener_port)
    
    def start(self, load_balancer_id):
        '''
        start load balancer listener
        '''
        return self.connection.start_load_balancer_listener(load_balancer_id, self.listener_port)
    
    def stop(self, load_balancer_id):
        '''
        stop load balancer listener
        '''
        return self.connection.stop_load_balancer_listener(load_balancer_id, self.listener_port)
    
    def describe_attribute(self, load_balancer_id, listener_type):
        '''
        describe load balance listener attribute
        '''
        return self.connection.describe_load_balancer_listener_attribute(load_balancer_id, self.listener_port, listener_type)
        
class LoadBalancer(TaggedSLBObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(LoadBalancer, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'LoadBalancer:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.load_balancer_id
        if name == 'name':
            return self.load_balancer_name

    def __setattr__(self, name, value):
        if name == 'id':
            self.load_balancer_id = value
        if name == 'name':
            self.load_balancer_name = value
        super(TaggedSLBObject, self).__setattr__(name, value)
    
    def set_status(self, load_balancer_status):
        '''
        set load balancer status
        '''
        return self.connection.set_load_balancer_status(self.load_balancer_id, load_balancer_status)
    
    def modify_name(self, new_name):
        '''
        modify load balancer name
        '''
        return self.connection.set_load_balancer_name(self.load_balancer_id, new_name)
    
    def modify_spec(self, internet_charge_type=None, bandwidth=None):
        '''
        modify load balancer name
        '''
        return self.connection.modify_slb_internet_spec(self.load_balancer_id, internet_charge_type=internet_charge_type, bandwidth=bandwidth)
    
    def delete(self):
        '''
        delete load balance 
        '''
        return self.connection.delete_load_balancer(self.load_balancer_id)
    
class BackendServer(TaggedSLBObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(BackendServer, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'BackendServer:%s' % self.id

    def __getattr__(self, name):
        if name in ['id', 'instance_id']:
            return self.server_id
        if name in ['status', 'health_status']:
            return self.server_health_status
        raise AttributeError('There is no ')

    def __setattr__(self, name, value):
        if name in ['id', 'instance_id']:
            self.server_id = value
        if name in ['status', 'health_status']:
            self.server_health_status = value
        super(TaggedSLBObject, self).__setattr__(name, value)
