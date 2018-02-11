#!/usr/bin/env python
# import sys
# sys.path.append("../../..")
from footmark.rds.connection import RDSConnection
from tests.unit import ACSMockServiceTestCase
import json


CREATE_RDS_INSTANCE = '''
{
    "DBInstanceId": "rm-3nsuc8muqq2tgk6wk",
    "ConnectionString": "rm-dj14onij078sh6wwr.ppas.rds.aliyuncs.com",
    "Port": "3306",
    "RequestId": "E7329CB3-9DE3-4413-BDE5-C0C974A016D1",  
    "TotalRecordCount": 1,
    "PageRecordCount": 1,
    "PageNumber": 1,           
    "Items": {
        "DBInstance": [
            {
                "Engine": "SQLServer",
                "DBInstanceType": "Primary",
                "MutriORsignle": false,
                "DBInstanceDescription": "demo_created",
                "ConnectionMode": "Safe",
                "LockMode": "Unlock",
                "InsId": 1,
                "RegionId": "cn-hongkong",
                "DBInstanceId": "rm-3nsuc8muqq2tgk6wk",
                "PayType": "Postpaid",
                "ZoneId": "cn-hongkong-b",
                "ExpireTime": "",
                "DBInstanceNetType": "Internet",
                "ReadOnlyDBInstanceIds": {
                    "ReadOnlyDBInstanceId": []
                },
                "EngineVersion": "2008r2",
                "InstanceNetworkType": "Classic",
                "LockReason": "",
                "CreateTime": "2017-03-07T15:52Z",
                "DBInstanceStatus": "Running"
            }
        ]
    }
}
'''

MODIFY_RDS_INSTANCE = '''
{
    "TotalRecordCount": 1,
    "PageRecordCount": 1,
    "PageNumber": 1,
    "RequestId": "A9E8BA89-ED5A-4F94-A7D6-935E36CA35B6",
    "Items": {
        "DBInstance": [
            {
                "Engine": "SQLServer",
                "DBInstanceType": "Primary",
                "MutriORsignle": false,
                "DBInstanceDescription": "demo_created",
                "ConnectionMode": "Safe",
                "LockMode": "Unlock",
                "InsId": 1,
                "RegionId": "cn-hongkong",
                "DBInstanceId": "rm-dj14z88396ms4b8v8",
                "PayType": "Postpaid",
                "ZoneId": "cn-hongkong-b",
                "ExpireTime": "",
                "DBInstanceNetType": "Internet",
                "ReadOnlyDBInstanceIds": {
                    "ReadOnlyDBInstanceId": []
                },
                "EngineVersion": "2008r2",
                "InstanceNetworkType": "Classic",
                "LockReason": "",
                "CreateTime": "2017-03-07T15:52Z",
                "DBInstanceStatus": "Running"
            }
        ]
    }
}
'''

CHANGE_RDS_INSTANCE_TYPE = '''
{
     "RequestId": "CDB3C0B3-A51F-4B93-8ACD-AC10C4DE0625"
    
}
'''

CREATE_RDS_READ_ONLY_INSTANCE = '''
{
     "RequestId": "CDB3C0B3-A51F-4B93-8ACD-AC10C4DE0625"
    
}
'''

CREATE_DATABASE = '''
{
     "RequestId": "C4F94DFB-5D62-4399-A66A-2A48A6A30EBC"
    
}
'''

DELETE_DATABASE = '''
{
     "RequestId": "1B5EFC0C-07B3-4B0B-8600-73E35B30A3BF"
    
}
'''

CREATE_ACCOUNT = '''
{
     "RequestId": "A5094804-442F-4755-9FB8-1AB2586D3D23"
    
}
'''

RESET_INSTANCE_PASSWORD = '''
{
     "RequestId": "11D5681C-7090-435F-BB17-E4E19DA836F5"
    
}
'''

RESTART_RDS_INSTANCE = '''
{
     "RequestId": "81DDE6C8-C10F-401F-B758-80487483AB62"
    
}
'''

RELEASE_RDS_INSTANCE = '''
{
     "RequestId": "EC72C609-238F-42C8-9CF0-C2BC21D52DD3"
    
}
'''

SWITCH_BETWEEN_PRIMARY_AND_STANDBY_DATABASE = '''
{
     "Items": {
        "DBInstance": [
            {
                "Engine": "SQLServer",
                "DBInstanceType": "Primary",
                "MutriORsignle": true,
                "DBInstanceDescription": "DEMO_RDS",
                "ConnectionMode": "Safe",
                "LockMode": "Unlock",
                "InsId": 1,
                "RegionId": "cn-hongkong",
                "DBInstanceId": "rm-3nsyw635bgr40ft6d",
                "PayType": "Postpaid",
                "ZoneId": "cn-hongkong-MAZ1(b,c)",
                "ExpireTime": "",
                "DBInstanceNetType": "Intranet",
                "ReadOnlyDBInstanceIds": {
                    "ReadOnlyDBInstanceId": []
                },
                "EngineVersion": "2008r2",
                "InstanceNetworkType": "Classic",
                "LockReason": "",
                "CreateTime": "2017-03-07T20:28Z",
                "DBInstanceStatus": "Running"
            }
        ]
    },
    "TotalRecordCount": 1,
    "PageRecordCount": 1,
    "PageNumber": 1,
    "RequestId": "9DDF2575-7821-411D-AB2D-5AAF56860A3A",

    "DBInstanceId": "rm-3nsyw635bgr40ft6d",
    "RequestId": "B5894B87-F83A-4BA1-B83F-DADB0AB47164",
    "HostInstanceInfos": {
        "NodeInfo": [
            {
                "DataSyncTime": "",
                "LogSyncTime": "",
                "NodeType": "Slave",
                "NodeId": "2410959",
                "SyncStatus": "NotSupport"
            },
            {
                "DataSyncTime": "",
                "LogSyncTime": "",
                "NodeType": "Master",
                "NodeId": "2410961",
                "SyncStatus": "NotSupport"
            }
        ]
    }
    
}
'''

RESET_ACCOUNT = '''
{
     "RequestId": "0F630492-7754-405A-B631-9974F54D5728"
    
}
'''

DELETE_ACCOUNT = '''
{
     "RequestId": "662D4C5A-8469-4877-A2D8-3B8241EAF9DE"
    
}
'''

GRANT_ACCOUNT_PERMISSIONS = '''
{
     "RequestId": "4F479108-6C86-4AA0-BB88-9982A697C8DE"
    
}
'''

REVOKE_ACCOUNT_PERMISSIONS = '''
{
     "RequestId": "7EA5AEA2-869F-44CB-A5C3-401F9C03D81A"
    
}
'''


# C2C : Unit Test For Create RDS Instance Method
class TestCreateRDSInstance(ACSMockServiceTestCase):
    connection_class = RDSConnection    
    db_engine = "MySQL"
    engine_version = "5.6"
    db_instance_class = "rds.mysql.t1.small" 
    db_instance_storage = "5"
    instance_net_type = "Internet"
    security_ip_list = "192.168.0.0/24"
    pay_type = "Postpaid"
    connection_mode = "Safe "
    instance_network_type = "Classic"

    def default_body(self):
        return CREATE_RDS_INSTANCE
                                                                    
    def test_create_rds_instance(self):
        self.set_http_response(status_code=200)
        changed, result = \
            self.service_connection.create_rds_instance(self.db_engine, self.engine_version, self.db_instance_class,
                                                        self.db_instance_storage, self.instance_net_type,
                                                        self.security_ip_list,self. pay_type, period=None,zone=None,
                                                        instance_network_type=self.instance_network_type,
                                                        connection_mode=self.connection_mode, vpc_id=None,
                                                        vswitch_id=None, private_ip_address=None,
                                                        allocate_public_ip=None, connection_string_prefix=None,
                                                        public_port=None, db_name=None, db_description=None,
                                                        character_set_name=None, maint_window=None,
                                                        preferred_backup_time=None, preferred_backup_period=None,
                                                        backup_retention_period=None, db_tags=None, wait=None,
                                                        wait_timeout=None)
       
        self.assertEqual(str(result[0][u'DBInstanceId']), "rm-3nsuc8muqq2tgk6wk")

# C2C : Unit Test For Create RDS Read-Only Instance Method


class TestCreateReadOnlyRDSInstance(ACSMockServiceTestCase):
    connection_class = RDSConnection
    zone = ""
    instance_id = "rm-dj14z88396ms4b8v8"
    db_engine = "MySQL"
    engine_version = "5.6"
    db_instance_class = "rds.mysql.t1.small" 
    db_instance_storage = "5"
    instance_net_type = "Internet"
    security_ip_list = "192.168.0.0/24"
    pay_type = "Postpaid"
    connection_mode = "Intranet "
    instance_network_type = "Classic"
    instance_description = "test description"

    def default_body(self):
        return CREATE_RDS_READ_ONLY_INSTANCE
                                                                    
    def test_create_read_only_rds_instance(self):
        self.set_http_response(status_code=200)
        changed, result = \
            self.service_connection.create_rds_read_only_instance(source_instance=self.instance_id, zone=self.zone,
                                                                  engine_version=self.engine_version,
                                                                  db_instance_class=self.db_instance_class,
                                                                  db_instance_storage=self.db_instance_storage,
                                                                  instance_description=self.instance_description,
                                                                  pay_type=self.pay_type, instance_network_type=None,
                                                                  vpc_id=None, vswitch_id=None, private_ip_address=None)
       
        self.assertEqual(str(result[0][u'DBInstanceId']), "rm-3nsuc8muqq2tgk6wk")   

# C2C : Unit Test For Modify RDS Instance Method


class TestModifyRDSInstance(ACSMockServiceTestCase):
    connection_class = RDSConnection
    zone = ""
    instance_id = "rm-dj14z88396ms4b8v8"
    db_engine = "MySQL"
    engine_version = "5.6"
    db_instance_class = "rds.mysql.t1.small" 
    db_instance_storage = "5"
    instance_net_type = "Internet"
    security_ip_list = "192.168.0.0/24"
    pay_type = "Postpaid"
    instance_network_type = "Classic"
    connection_mode = "Safety"
    current_connection_string = "rm-dj14z88396ms4b8v8.mysql.rds.aliyuncs.com"
    connection_string_prefix = "new"
    port = "3306"

    def default_body(self):
        return MODIFY_RDS_INSTANCE
                                                                    
    def test_modify_rds_instance(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.modify_rds_instance(self.instance_id, self.current_connection_string,
                                                                      self.connection_string_prefix, self.port,
                                                                      self.connection_mode, self.db_instance_class,
                                                                      self.db_instance_storage, self.pay_type,
                                                                      instance_description=None,
                                                                      security_ip_list=None,
                                                                      instance_network_type=None, vpc_id=None,
                                                                      vswitch_id=None, maint_window=None,
                                                                      preferred_backup_time=None,
                                                                      preferred_backup_period=None,
                                                                      backup_retention_period=None)
        self.assertEqual(str(result[0][u'RequestId']), 'A9E8BA89-ED5A-4F94-A7D6-935E36CA35B6')       


# C2C : Unit Test For Change RDS Instance Type Method
class TestChangeRDSInstanceType(ACSMockServiceTestCase):
    connection_class = RDSConnection

    instance_id = "rm-3nst28462da58z43g"
    db_instance_class = "rds.mysql.t1.small"
    db_instance_storage = "10" 
    pay_type = "Postpaid"

    def default_body(self):
        return CHANGE_RDS_INSTANCE_TYPE 
                                                                    
    def test_change_rds_instance_type(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.change_rds_instance_type(self.instance_id, self.db_instance_class,
                                                                           self.db_instance_storage, self.pay_type)
        self.assertEqual(result[u'RequestId'], "CDB3C0B3-A51F-4B93-8ACD-AC10C4DE0625")        


# C2C : Unit Test For Create Database Method
class TestCreateDatabase(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    instance_id = "rm-3nst28462da58z43g"
    db_name = "demodtabase"
    db_description = "demo database" 
    character_set_name = "utf8"
    command = "create"

    def default_body(self):
        return CREATE_DATABASE 
                                                                    
    def test_create_database(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_database(instance_id=self.instance_id, db_name=self.db_name,
                                                                  db_description=self.db_description,
                                                                  character_set_name=self.character_set_name)
        self.assertEqual(result[0][u'RequestId'], "C4F94DFB-5D62-4399-A66A-2A48A6A30EBC")        


# C2C : Unit Test For Delete Database Method
class TestDeleteDatabase(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    instance_id = "rm-3nst28462da58z43g"
    db_name = "demo3"

    def default_body(self):
        return DELETE_DATABASE 
                                                                    
    def test_delete_database(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_database(instance_id=self.instance_id, db_name=self.db_name)     
        self.assertEqual(result[0][u'RequestId'], "1B5EFC0C-07B3-4B0B-8600-73E35B30A3BF")        
        

# C2C : Unit Test For Create Account Method
class TestCreateAccount(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    db_instance_id = "rm-3ns9392w5ezzo2270"
    account_name = "demo1235"
    account_password = "123456"
    description = "nq"
    account_type = "Normal"
    command = "create"

    def default_body(self):
        return CREATE_ACCOUNT 
                                                                    
    def test_create_account(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.create_account(db_instance_id=self.db_instance_id,
                                                                 account_name=self.account_name,
                                                                 account_password=self.account_password,
                                                                 description=self.description,
                                                                 account_type=self.account_type)
        self.assertEqual(result[0][u'RequestId'], "A5094804-442F-4755-9FB8-1AB2586D3D23")        


# C2C : Unit Test For Reset Instance Password Method
class TestResetInstancePassword(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    db_instance_id = "rm-3ns9392w5ezzo2270"
    account_name = "demo"
    account_password = "demo@123"
    command = "reset_password"

    def default_body(self):
        return RESET_INSTANCE_PASSWORD 
                                                                    
    def test_reset_instance_password(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.reset_instance_password(db_instance_id=self.db_instance_id,
                                                                          account_name=self.account_name,
                                                                          account_password=self.account_password)
        self.assertEqual(result[0][u'RequestId'], "11D5681C-7090-435F-BB17-E4E19DA836F5")        


# C2C : Unit Test For Restart Rds Instance Method
class TestRestartRdsInstance(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    instance_id = "rm-3ns9392w5ezzo2270"

    def default_body(self):
        return RESTART_RDS_INSTANCE 
                                                                    
    def test_restart_rds_instance(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.restart_rds_instance(instance_id=self.instance_id)
        self.assertEqual(result[0][u'RequestId'], "81DDE6C8-C10F-401F-B758-80487483AB62")        
        

# C2C : Unit Test For Release Rds Instance Method
class TestReleaseRdsInstance(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    instance_id = "rm-3ns9392w5ezzo2270"

    def default_body(self):
        return RELEASE_RDS_INSTANCE 
                                                                    
    def test_release_rds_instance(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.release_rds_instance(instance_id=self.instance_id)
        self.assertEqual(result[0][u'RequestId'], "EC72C609-238F-42C8-9CF0-C2BC21D52DD3")        
        

# C2C : Unit Test For Switch between primary and standby database Method
class TestSwitchBetweenPrimaryAndStandbyDatabase(ACSMockServiceTestCase):
    connection_class = RDSConnection   
    instance_id = "rm-3nsyw635bgr40ft6d"
    node_id = "2410959"
    force = "Yes"

    def default_body(self):
        return SWITCH_BETWEEN_PRIMARY_AND_STANDBY_DATABASE
                                                                    
    def test_switch_between_primary_standby_database(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.switch_between_primary_standby_database(instance_id=self.instance_id,
                                                                                          node_id=self.node_id,
                                                                                          force=self.force)
        self.assertEqual(result[0][u'RequestId'], "B5894B87-F83A-4BA1-B83F-DADB0AB47164")


# C2C : Unit Test For Reset Account Method
class TestResetAccount(ACSMockServiceTestCase):
    connection_class = RDSConnection
    db_instance_id = "rm-dj148mev98v237v42"
    account_name = "demo"
    account_password = "demo@123"

    def default_body(self):
        return RESET_ACCOUNT

    def test_reset_account(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.reset_account(db_instance_id=self.db_instance_id,
                                                                account_name=self.account_name,
                                                                account_password=self.account_password)
        self.assertEqual(result[0][u'RequestId'], "0F630492-7754-405A-B631-9974F54D5728")


# C2C : Unit Test For DeleteAccount Method
class TestDeleteAccount(ACSMockServiceTestCase):
    connection_class = RDSConnection
    db_instance_id = "rm-3nst28462da58z43g"
    account_name = "demo3"

    def default_body(self):
        return DELETE_ACCOUNT
                                                                    
    def test_delete_account(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.delete_account(db_instance_id=self.db_instance_id,
                                                                 account_name=self.account_name)
        self.assertEqual(result[u'RequestId'], "662D4C5A-8469-4877-A2D8-3B8241EAF9DE")    


# C2C : Unit Test For Grant Account Permissions Method
class TestGrantAccountPermission(ACSMockServiceTestCase):
    connection_class = RDSConnection
    db_instance_id = "rm-3nst28462da58z43g"
    account_name = "demo3"
    db_name = "demo_created"
    account_privilege = "ReadOnly"

    def default_body(self):
        return GRANT_ACCOUNT_PERMISSIONS
                                                                    
    def test_grant_account_permissions(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.grant_account_permissions(db_instance_id=self.db_instance_id,
                                                                            account_name=self.account_name,
                                                                            db_name=self.db_name,
                                                                            account_privilege=self.account_privilege)
        self.assertEqual(result[u'RequestId'], "4F479108-6C86-4AA0-BB88-9982A697C8DE")    


# C2C : Unit Test For Revoke Account Permissions Method
class TestRevokingAccountPermission(ACSMockServiceTestCase):
    connection_class = RDSConnection
    db_instance_id = "rm-3nst28462da58z43g"
    account_name = "demo3"
    db_name = "demo_created"

    def default_body(self):
        return REVOKE_ACCOUNT_PERMISSIONS
                                                                    
    def test_revoke_account_permissions(self):
        self.set_http_response(status_code=200)
        changed, result = self.service_connection.revoke_account_permissions(db_instance_id=self.db_instance_id,
                                                                             account_name=self.account_name,
                                                                             db_name=self.db_name)
        self.assertEqual(result[u'RequestId'], "7EA5AEA2-869F-44CB-A5C3-401F9C03D81A")    

