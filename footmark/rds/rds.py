from footmark.rds.rdsobject import TaggedRDSObject

class DbInstance(TaggedRDSObject):
    def __init__(self, connection=None):
        super(DbInstance, self).__init__(connection)

    def __repr__(self):
        return 'DbInstance:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
             return self.id
        if name == 'status':
             return self.dbinstance_status
        if name == 'type':
             return self.dbinstance_type

    def __setattr__(self, name, value):
        if name == 'id':
             self.dbinstance_id=value
        if name == 'status':
             self.dbinstance_status=value
        if name == 'type':
             self.dbinstance_type=value
        super(TaggedRDSObject, self).__setattr__(name, value)


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

    def __setattr__(self, name, value):
        if name == 'name':
             self.account_name=value
        if name == 'status':
             self.account_status=value
        if name == 'description':
             self.account_description=value
        if name == 'privileges':
             self.database_privileges=value
        super(TaggedRDSObject, self).__setattr__(name, value)
    
    def reset(self, dbinstance_id, account_password):
        '''
        reset
        '''
        return self.connection.reset_account_password(dbinstance_id, self.account_name, account_password)
    
    def grant_privilege(self, dbinstance_id, db_name, account_privilege):
        '''
        grant privilege
        '''
        return self.connection.grant_account_privilege(dbinstance_id, self.account_name, db_name, account_privilege)
    
    def revoke_privilege(self, dbinstance_id, db_name):
        '''
        revoke privilege
        '''
        return self.connection.revoke_account_privilege(dbinstance_id, self.account_name, db_name)
    
    def modify_description(self, dbinstance_id, description):
        '''
        modify description
        '''
        return self.connection.modify_account_description(dbinstance_id, self.account_name, description)
    
    def delete(self, dbinstance_id):
        '''
        delete account 
        '''
        return self.connection.delete_account(dbinstance_id, self.account_name)
