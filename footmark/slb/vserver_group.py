"""
Represents an SLB
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
    
    def set(self, backend_servers=None, vserver_group_name=None):
        '''
        set attribute
        '''
        changed = False
        if backend_servers and self.backend_servers['backend_server']:
            set = []
            for old in self.backend_servers['backend_server']:
                for new in backend_servers:
                    if new['server_id'] == old['server_id']:
                        for key in list(old.keys()):
                            if key in new and str(old[key]) != str(new[key]):
                                set.append(new)
            if set:
                params = {'vserver_group_id': self.vserver_group_id}
                for index in range(0, len(set), 20):
                    params['backend_servers'] = self.format_backend_servers(set[index:index+20])
                    if self.connection.set_vserver_group_attribute(**params):
                        changed = True
        return changed
    
    def add(self, backend_servers):
        '''
        add backend servers
        '''
        add = []
        changed = False
        if backend_servers:
            if not self.backend_servers['backend_server']:
                add = backend_servers
            else:
                old = []
                for o in self.backend_servers['backend_server']:
                    old.append(o['server_id'])
                for new in backend_servers:
                    if new not in old:
                        add.append(new)
        if add:
            params = {'vserver_group_id': self.vserver_group_id}
            for index in range(0, len(add), 20):
                params['backend_servers'] = self.format_backend_servers(add[index:index+20])
                if self.connection.add_vserver_group_backend_servers(**params):
                    changed = True
        return changed
    
    def remove(self, backend_servers):
        '''
        remove backend servers
        '''
        removed = []
        changed = False
        if backend_servers:
            if not self.backend_servers['backend_server']:
                return False
            else:
                old = []
                for o in self.backend_servers['backend_server']:
                    old.append(o['server_id'])
                for new in backend_servers:
                    if new['server_id'] in old:
                        removed.append(new)
        if removed:
            params = {'vserver_group_id': self.vserver_group_id}
            for index in range(0, len(removed), 20):
                params['backend_servers'] = self.format_backend_servers(removed[index:index+20])
                if self.connection.remove_vserver_group_backend_servers(**params):
                    changed = True
        return changed

    def modify(self, backend_servers):
        '''
        modify backend servers
        '''
        changed = False
        old = []
        new = []
        if backend_servers and self.backend_servers['backend_server']:
            for o in self.backend_servers['backend_server']:
                for n in backend_servers:
                    if o['server_id'] == n['server_id']:
                        for key in list(o.keys()):
                            if key in n and str(o[key]) != str(n[key]):
                                old.append(o)
                                new.append(n)
                                break
        if old and new:
            params = {'vserver_group_id': self.vserver_group_id}
            for index in range(0, len(old), 20):
                params['old_backend_servers'] = self.format_backend_servers(old[index:index+20])
                params['new_backend_servers'] = self.format_backend_servers(new[index:index+20])
                if self.connection.modify_vserver_group_backend_servers(**params):
                    changed = True
        return changed

    def delete(self):
        '''
        delete vserver group 
        '''
        return self.connection.delete_vserver_group(**{'vserver_group_id':self.vserver_group_id})
    
    def get(self):
        '''
        describe vserver group attribute 
        '''
        return self.connection.describe_vserver_group_attribute(**{'vserver_group_id':self.vserver_group_id})

    def read(self):
        group = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region", "request_id"]:
                continue
            if name == "backend_servers":
                if value and value['backend_server']:
                    value = value['backend_server']
                else:
                    value = []

            if name == "vserver_group_id":
                group['id'] = value

            if name == "vserver_group_name":
                group['name'] = value

            group[name] = value
        return group

    def format_backend_servers(self, servers):
        backend_servers = []
        for s in servers:
            server = {}
            for key, value in list(s.items()):
                split = []
                for k in str(key).split("_"):
                    split.append(str.upper(k[0])+k[1:])
                server["".join(split)] = value
            backend_servers.append(server)
        return backend_servers
