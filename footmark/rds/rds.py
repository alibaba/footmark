from footmark.rds.rdsobject import TaggedRDSObject


class DbInstance(TaggedRDSObject):
    def __init__(self, connection=None):
        super(DbInstance, self).__init__(connection)

    def __repr__(self):
        return 'DbInstance:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.dbinstance_id
        if name == 'status':
            return self.dbinstance_status
        if name == 'type':
            return self.dbinstance_type
        if name == 'connection_string':
            return self.connection_string
        if name == 'name':
            return self.dbinstance_description

    def __setattr__(self, name, value):
        if name == 'dbinstance_id':
            self.id = value
        if name == 'dbinstance_status':
            self.status = value
        if name == 'dbinstance_type':
            self.type = value
        if name == 'dbinstance_description':
            self.name = value
        super(TaggedRDSObject, self).__setattr__(name, value)

    def get(self):
        return self.connection.describe_db_instance_attribute(db_instance_id=self.id)

    def read(self):
        ins = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "order_id"]:
                continue
            if name in ['dbinstance_class', 'dbinstance_description', 'dbinstance_id', 'dbinstance_net_type', 'dbinstance_status', 'dbinstance_type', 'dbinstance_class_type', 'dbinstance_cpu', 'dbinstance_memory', 'dbinstance_storage', 'dbinstance_storage_type', 'dbmax_quantity']:
                new_name = name.replace('db', 'db_')
                ins[new_name] = value
                continue
            ins[name] = value
        return ins

    def restart(self):
        return self.connection.restart_db_instance(db_instance_id=self.id)

    def delete(self):
        return self.connection.delete_db_instance(db_instance_id=self.id)

    def allocate_public_connection_string(self, connection_string_prefix=None, port=None):
        params = {}
        if connection_string_prefix and port:
            params['connection_string_prefix'] = connection_string_prefix
            params['port'] = port
            params['db_instance_id'] = self.id
            return self.connection.allocate_instance_public_connection(**params)

    def modify_db_instance_connection_string(self, connection_string_prefix=None, port=None, current_connection_string=None):
        info_obj_list = self.connection.describe_db_instance_net_info(dbinstance_id=self.id)
        res = ''
        for obj in info_obj_list:
            if obj.connection_string == current_connection_string and not obj.connection_string.startswith(connection_string_prefix):
                res = obj
        params = {}
        if res:
            params['connection_string_prefix'] = connection_string_prefix
            params['port'] = port
            params['current_connection_string'] = current_connection_string
            params['db_instance_id'] = self.id
            return self.connection.modify_db_instance_connection_string(**params)
        return False

    def modify_network_type(self, instance_network_type=None):
        params = {}
        if instance_network_type and self.instance_network_type != instance_network_type:
            params['instance_network_type'] = instance_network_type
            params['db_instance_id'] = self.id
            return self.connection.modify_db_instance_network_type(**params)
        return False

    def modify_description(self, db_instance_description=None):
        params = {}
        if db_instance_description and db_instance_description != self.name:
            params['db_instance_description'] = db_instance_description
            params['db_instance_id'] = self.id
            return self.connection.modify_db_instance_description(**params)
        return False

    def modify_instance_spec(self, db_instance_class=None, db_instance_storage=None):
        params = {}
        params['db_instance_id'] = self.id
        params['pay_type'] = self.pay_type
        if db_instance_class and self.db_instance_class != db_instance_class:
            params['db_instance_class'] = db_instance_class
        if db_instance_storage and self.db_instance_storage != db_instance_storage:
            params['db_instance_storage'] = db_instance_storage
        if params.get('db_instance_class') or params.get('db_instance_storage'):
            return self.connection.modify_db_instance_spec(**params)
        else:
            return False

    def list_tags(self):
        res = {}
        tags = self.connection.list_tag_resources(resource_ids=[self.id], resource_type='instance')
        for tag in tags:
            res[tag.tag_key] = tag.tag_value
        return res

    def add_tags(self, tags):
        """
        Add tags
        """
        tmp = {}
        if tags:
            for key, value in list(tags.items()):
                if key in list(self.list_tags().keys()) and value == self.list_tags()[key]:
                    continue
                tmp[key] = value
        if tmp:
            return self.connection.tag_resources(resource_ids=[self.id], tags=tmp, resource_type='instance')
        return False

    def remove_tags(self, tags):
        """
        remove tags
        """
        tmp = []
        if tags:
            for key, value in list(tags.items()):
                if key not in list(self.list_tags().keys()):
                    continue
                tmp.append(key)
        if tmp:
            return self.connection.untag_resources(resource_ids=[self.id], tag_keys=tmp, resource_type='instance')
        return False


class Database(TaggedRDSObject):
    def __init__(self, connection=None):
        super(Database, self).__init__(connection)

    def __repr__(self):
        return 'Database:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.dbinstance_id
        if name == 'status':
            return self.dbstatus
        if name == 'description':
            return self.dbdescription
        if name == 'name':
            return self.dbname

    def __setattr__(self, name, value):
        if name == 'dbinstance_id':
            self.id = value
        if name == 'dbname':
            self.name = value
        if name == 'dbdescription':
            self.description = value
        if name == 'dbstatus':
            self.status = value
        super(TaggedRDSObject, self).__setattr__(name, value)

    def get(self):
        return self.connection.describe_databases(db_instance_id=self.id)[0]

    def read(self):
        db = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue
            if name in ['dbdescription', 'dbinstance_id', 'dbname', 'dbstatus']:
                new_name = name.replace('db', 'db_')
                db[new_name] = value
                continue
            db[name] = value
        return db

    def delete(self):
        return self.connection.delete_database(db_instance_id=self.id, db_name=self.name)

    def modify_db_description(self, description=None):
        params = {}
        if description and self.description != description:
            params['DBDescription'] = description
            params['DBName'] = self.name
            params['DBInstanceId'] = self.id
            return self.connection.modify_db_description(**params)
        return False

    def copy_database_between_instances(self, **kwargs):
        target_instance_id = kwargs['target_db_instance_id']
        target_name = kwargs['target_db_name']
        target_instance_db = self.connection.describe_databases(db_instance_id=target_instance_id)
        for db in target_instance_db:
            if db.name == target_name:
                return False
        return self.connection.copy_database_between_instances(**kwargs)


class Account(TaggedRDSObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(Account, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Account:%s' % self.name

    def __getattr__(self, name):
        if name == 'name':
            return self.account_name
        if name == 'status':
            return self.account_status
        if name == 'description':
            return self.account_description
        if name == 'privileges':
            return self.database_privileges
        if name == 'type':
            return self.account_type
        if name == 'id':
            return self.dbinstance_id

    def __setattr__(self, name, value):
        if name == 'account_name':
            self.name = value
        if name == 'account_status':
            self.status = value
        if name == 'database_privileges':
            self.privileges = value
        if name == 'account_type':
            self.type = value
        super(TaggedRDSObject, self).__setattr__(name, value)

    def grant_privilege(self, db_names, account_privilege):
        '''
        grant privilege
        '''
        flag = False
        for db_name in db_names:
            flag = self.connection.grant_account_privilege(db_instance_id=self.id, account_name=self.name, db_name=db_name, account_privilege=account_privilege)
        return flag

    def revoke_privilege(self, db_names):
        '''
        revoke privilege
        '''
        flag = False
        for db_name in db_names:
            flag = self.connection.revoke_account_privilege(db_instance_id=self.id, account_name=self.name, db_name=db_name)
        return flag

    def modify_description(self, description=None):
        '''
        modify description
        '''
        params = {}
        if description:
            params['db_instance_id'] = self.id
            params['account_name'] = self.name
            params['account_description'] = description
        return self.connection.modify_account_description(**params)
    
    def delete(self):
        '''
        delete account 
        '''
        return self.connection.delete_account(db_instance_id=self.id, account_name=self.name)

    def reset(self, account_password):
        return self.connection.reset_account_password(account_password=account_password, db_instance_id=self.id, account_name=self.name)

    def read(self):
        account = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue
            if name == 'dbinstance_id':
                account['db_instance_id'] = value
                continue
            account[name] = value
        return account

    def get(self):
        return self.connection.describe_accounts(db_instance_id=self.id, account_name=self.name)[0]


class BackUp(TaggedRDSObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
        super(BackUp, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'BackUp:%s' % self.name

    def __getattr__(self, name):
        if name == 'id':
            return self.backup_id
        if name == 'instance_id':
            return self.dbinstance_id
        if name == 'status':
            return self.backup_status
        if name == 'mode':
            return self.backup_mode

    def __setattr__(self, name, value):
        if name == 'backup_id':
            self.id = value
        if name == 'dbinstance_id':
            self.instance_id = value
        if name == 'backup_status':
            self.status = value
        if name == 'backup_mode':
            self.mode = value
        super(TaggedRDSObject, self).__setattr__(name, value)

    def read(self):
        backup = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue
            if name == 'dbinstance_id':
                backup['db_instance_id'] = value
                continue
            backup[name] = value
        return backup

