"""
Represents an SLB Instance
"""
from footmark.slb.slbobject import TaggedSLBObject


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
        if name == 'status':
            return self.load_balancer_status

    def __setattr__(self, name, value):
        if name == 'internet_charge_type':
            if value == 'paybybandwidth':
                value = 'PayByBandwidth'
            elif value == 'paybytraffic':
                value = 'PayByTraffic'
        if name == 'pay_type':
            if value == 'PayOnDemand':
                value == "PostPaid"
            elif value == 'PrePay':
                value == "PrePaid"
        super(TaggedSLBObject, self).__setattr__(name, value)

    def get(self):
        '''
        delete load balance 
        '''
        return self.connection.describe_load_balancers(**{'load_balancer_id': self.load_balancer_id})[0]

    def set_status(self, status):
        '''
        set load balancer status
        '''
        if str(status).lower() != str(self.status).lower():
            return self.connection.set_load_balancer_status(**{'load_balancer_id': self.load_balancer_id, 'load_balancer_status': status})
        return False
    
    def modify_name(self, new_name):
        '''
        modify load balancer name
        '''
        return self.connection.set_load_balancer_name(self.load_balancer_id, new_name)
    
    def modify_spec(self, internet_charge_type=None, bandwidth=None):
        '''
        modify load balancer name
        '''
        params = {}
        if internet_charge_type and str.lower(self.internet_charge_type) != str.lower(internet_charge_type):
            params['internet_charge_type'] = str.lower(internet_charge_type)
        if internet_charge_type and str(internet_charge_type).lower() == "paybybandwidth":
            if bandwidth and int(self.bandwidth) != int(bandwidth):
                params['bandwidth'] = bandwidth
        if params:
            params['load_balancer_id'] = self.load_balancer_id
            return self.connection.modify_load_balancer_internet_spec(**params)
        return False

    def delete(self):
        '''
        delete load balance 
        '''
        return self.connection.delete_load_balancer(self.load_balancer_id)

    def read(self):
        balancer = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "region_id_alias", "listener_ports", "create_time_stamp", "end_time_stamp",
                        "request_id", "has_reserved_info", 'listener_ports_and_protocal']:
                continue

            if name == 'load_balancer_id':
                balancer['id'] = value

            if name == 'load_balancer_name':
                balancer['name'] = value

            if name == 'listener_ports_and_protocol':
                name = "listeners"
                if value and value['listener_port_and_protocol']:
                    value = value['listener_port_and_protocol']
                else:
                    value = []

            if name == 'backend_servers':
                if value and value['backend_server']:
                    value = value['backend_server']
                else:
                    value = []

            balancer[name] = value
        return balancer

    def add_tags(self, tags):
        """
        Add tags
        """
        return self.connection.tag_resources(resource_ids=[self.id], tags=tags, resource_type='instance')

    def remove_tags(self, tags):
        """
        remove tags
        """
        return self.connection.untag_resources(resource_ids=[self.id], tags=tags, resource_type='instance')
