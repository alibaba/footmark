# encoding: utf-8
"""
Represents a connection to the RDS service.
"""                    

import warnings

import six
import time
import json

from footmark.connection import ACSQueryConnection
from footmark.rds.regioninfo import RegionInfo
from footmark.rds.rds import Account, DbInstance
from footmark.resultset import ResultSet
from footmark.exception import RDSResponseError


class RDSConnection(ACSQueryConnection):
    SDKVersion = '2014-08-15'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    ResponseError = RDSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None):
        """
        Init method to create a new connection to RDS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.RDSSDK = 'aliyunsdkrds.request.v' + self.SDKVersion.replace('-', '')

        super(RDSConnection, self).__init__(acs_access_key_id,
                                            acs_secret_access_key,
                                            self.region, self.RDSSDK, security_token, user_agent=user_agent)

    def create_rds_instance(self, db_engine, engine_version, db_instance_class, db_instance_storage,
                            instance_net_type, security_ip_list, pay_type, period=None,zone=None,
                            instance_description=None, used_time=None, instance_network_type=None, connection_mode=None,
                            vpc_id=None, vswitch_id=None, private_ip_address=None, allocate_public_ip=False,
                            connection_string_prefix=None, public_port=None, db_name=None, db_description=None,
                            character_set_name=None, maint_window=None, preferred_backup_time=None,
                            preferred_backup_period=None, backup_retention_period=None, db_tags=None, wait=None,
                            wait_timeout=None, client_token=None):
        """
         Create RDS Instance

         :type zone: string
         :param zone:  ID of a zone to which an instance belongs
         :type db_engine: string
         :param db_engine: The type of database
         :type engine_version: string
         :param engine_version: Version number of the database engine to use
         :type db_instance_class: string
         :param db_instance_class: The instance type of the database.
         :type db_instance_storage: integer
         :param db_instance_storage: Size in gigabytes of the initial storage for the DB instance.
         :type instance_net_type: string
         :param instance_net_type: The net type of the DB instance
         :type instance_description: string
         :param instance_description: Instance description or remarks, no more than 256 bytes.
         :type security_ip_list: string
         :param security_ip_list: List of IP addresses allowed to access all databases of an instance.
         :type pay_type: string
         :param pay_type: The pay type of the DB instance.
         :type period: string
         :param period: Period of the instance if pay_type set to prepaid.
         :type used_time: integer
         :param used_time: This parameter specifies the duration for purchase.
         :type instance_network_type: string
         :param instance_network_type: The network type of the instance.
         :type connection_mode: string
         :param connection_mode: The connection mode of the instance
         :type vpc_id: string
         :param vpc_id: The ID of the VPC
         :type vswitch_id: string
         :param vswitch_id: ID of VSwitch
         :type private_ip_address: string
         :param private_ip_address: IP address of an VPC under VSwitchId.
         :type allocate_public_ip: string
         :param allocate_public_ip: Whether to allocate public IP
         :type connection_string_prefix: string
         :param connection_string_prefix: Prefix of an Internet connection string
         :type public_port: integer
         :param public_port: The public connection port.
         :type db_name: string
         :param db_name: Name of a database to create within the instance.
         :type db_description: string
         :param db_description: Description of a database to create within the instance.
         :type character_set_name: string
         :param character_set_name: Associate the DB instance with a specified character set.
         :type maint_window: string
         :param maint_window: Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.
         :type preferred_backup_time: string
         :param preferred_backup_time: Backup time, in the format of HH:mmZ- HH:mm Z.
         :type preferred_backup_period: string
         :param preferred_backup_period: Backup period.
         :type backup_retention_period: integer
         :param backup_retention_period: Retention days of the backup
         :type db_tags: dict
         :param db_tags: A list of hash/dictionaries of db tags
         :type db_engine: string
         :param wait: Wait for the RDS instance to be 'running' before returning.
         :type wait_timeout: integer
         :param wait_timeout: how long before wait gives up, in seconds
         :return:
             changed: If instance is created successfully the changed will be set
                 to True else False
             DBInstanceId: the newly created instance id
         """
        params = {}
        results = []
        flag = False
        changed = False

        if zone:
            self.build_list_params(params, zone, 'ZoneId')
        if db_engine:
            self.build_list_params(params, db_engine, 'Engine')
        if engine_version:
            self.build_list_params(params, engine_version, 'EngineVersion')
        if db_instance_class:
            self.build_list_params(params, db_instance_class, 'DBInstanceClass')
        if db_instance_storage:
            self.build_list_params(params, db_instance_storage, 'DBInstanceStorage')
        if instance_net_type:
            self.build_list_params(params, instance_net_type, 'DBInstanceNetType')
        if instance_description:
            self.build_list_params(params, instance_description, 'DBInstanceDescription')
        if security_ip_list:
            self.build_list_params(params, security_ip_list, 'SecurityIPList')
        if pay_type:
            self.build_list_params(params, pay_type, 'PayType')
        if period:
            self.build_list_params(params, period, 'Period')
        if used_time:
            self.build_list_params(params, used_time, 'UsedTime')
        if instance_network_type:
            self.build_list_params(params, instance_network_type, 'InstanceNetworkType')
        if connection_mode:
            self.build_list_params(params, connection_mode, 'ConnectionMode')
        if vpc_id:
            self.build_list_params(params, vpc_id, 'VPCId')
        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')
        if private_ip_address:
            self.build_list_params(params, private_ip_address, 'PrivateIpAddress')
        if client_token:
            self.build_list_params(params, client_token, 'ClientToken')
        try:
            results_instance = self.get_status('CreateDBInstance', params)
            if results_instance:
                results.append({"DBInstanceId": results_instance["DBInstanceId"]})
            changed = True
        except Exception as ex:
            custom_msg = [
                "The API is showing None error code and error message while creating rds instance",
                "Following error occur while creating rds instance: ",
                "Failed to create rds instance with error code "
            ]
            results = results + self.rds_error_handler(ex, custom_msg)

        else:          
            time.sleep(240)
            # Start newly created Instance
            # wait until instance status becomes running         
            if allocate_public_ip and self.check_instance_status(results_instance[u'DBInstanceId']):
                if connection_string_prefix and public_port:
                    if instance_net_type == "Intranet":
                        changed_conn_str, result_conn_str = \
                            self.create_instance_public_connection_string(results_instance[u'DBInstanceId'],
                                                                          connection_string_prefix, public_port)
                    elif instance_net_type == "Internet":
                        changed_conn_str, result_conn_str = \
                            self.modify_instance_public_connection(results_instance[u'DBInstanceId'], 
                                                                   results_instance[u'ConnectionString'],
                                                                   connection_string_prefix, public_port)
            
                    if 'error' in (''.join(str(result_conn_str))).lower():
                        results.append(result_conn_str)
                           
            if self.check_instance_status(results_instance[u'DBInstanceId']):
                if db_name or character_set_name: 
                    changed_create_db, result_create_db = self.create_database(results_instance[u'DBInstanceId'],
                                                                               db_name, db_description,
                                                                               character_set_name)
            
                    if 'error' in (''.join(str(result_create_db))).lower():
                        results.append(result_create_db)                      
              
            if maint_window and self.check_instance_status(results_instance[u'DBInstanceId']):
                changed_maint_window, result_maint_window = \
                    self.modify_db_instance_maint_time(results_instance[u'DBInstanceId']
                                                            , maint_window)
                if 'error' in (''.join(str(result_maint_window))).lower():
                    results.append(result_maint_window) 
            
            if preferred_backup_time and preferred_backup_period:               
                if self.check_instance_status(results_instance[u'DBInstanceId']):
                    changed_backup_policy, result_backup_policy = \
                        self.modify_backup_policy(results_instance[u'DBInstanceId'],
                                                  preferred_backup_time, preferred_backup_period,
                                                  backup_retention_period)
                    if 'error' in (''.join(str(result_backup_policy))).lower():
                        results.append(result_backup_policy) 
               
            if db_tags:
                changed_tags, result_db_tags = self.bind_tags(results_instance[u'DBInstanceId'], db_tags) 
                if 'error' in (''.join(str(result_db_tags))).lower():
                    results.append(result_db_tags)                                    

            if str(wait).lower() in ['yes', 'true'] and wait_timeout:
                time.sleep(wait_timeout)

        return changed, results

    def create_rds_read_only_instance(self, source_instance, zone, engine_version, db_instance_class,
                                      db_instance_storage, instance_description, pay_type, instance_network_type=None,
                                      vpc_id=None, vswitch_id=None, private_ip_address=None):
        """
        Create RDS Read-Only Instance

        :type source_instance: string
        :param source_instance: ID of the database to replicate.
        :type zone: string
        :param zone:  ID of a zone to which an instance belongs
        :type engine_version: string
        :param engine_version: Version number of the database engine to use
        :type db_instance_class: string
        :param db_instance_class: The instance type of the database.
        :type db_instance_storage: integer
        :param db_instance_storage: Size in gigabytes of the initial storage for the DB instance.
        :type instance_description: string
        :param instance_description: Instance description or remarks, no more than 256 bytes.
        :type pay_type: string
        :param pay_type: The pay type of the DB instance.
        :type instance_network_type: string
        :param instance_network_type: The network type of the instance.
        :type vpc_id: string
        :param vpc_id: The ID of the VPC
        :type vswitch_id: string
        :param vswitch_id: ID of VSwitch
        :type private_ip_address: string
        :param private_ip_address: IP address of an VPC under VSwitchId.
        :return:
            changed: If ready-only instance is created successfully the changed will be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False

        if zone:
            self.build_list_params(params, zone, 'ZoneId')
        if source_instance:
            self.build_list_params(params, source_instance, 'DBInstanceId')
        if engine_version:
            self.build_list_params(params, engine_version, 'EngineVersion')
        if db_instance_class:
            self.build_list_params(params, db_instance_class, 'DBInstanceClass')
        if db_instance_storage:
            self.build_list_params(params, db_instance_storage, 'DBInstanceStorage')
        if instance_description:
            self.build_list_params(params, instance_description, 'DBInstanceDescription')
        if pay_type:
            self.build_list_params(params, pay_type, 'PayType')
        if instance_network_type:
            self.build_list_params(params, instance_network_type, 'InstanceNetworkType')
        if vpc_id:
            self.build_list_params(params, vpc_id, 'VPCId')
        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')
        if private_ip_address:
            self.build_list_params(params, private_ip_address, 'PrivateIpAddress')
        try:
            results = self.get_status('CreateReadOnlyDBInstance', params)
            changed = True
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def get_rds_instances_info(self, instance_id):
        """
        Get RDS Instance Info
        :type instance_id: string
        :param instance_id: Id of instance
        :return:
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
             
        try:
            results = self.get_status('DescribeDBInstances', params)            
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def modify_rds_instance(self, instance_id, current_connection_string, connection_string_prefix, port,
                            connection_mode, db_instance_class, db_instance_storage, pay_type, instance_description,
                            security_ip_list, instance_network_type, vpc_id, vswitch_id, maint_window,
                            preferred_backup_time, preferred_backup_period, backup_retention_period):
        """
        Modify RDS Instance

        :type  instance_id: string
        :param instance_id: Id of the Instance to modify
        :type  current_connection_string: string
        :param current_connection_string: Current connection string of an instance.
        :type  connection_string_prefix: string
        :param connection_string_prefix: Target connection string
        :type  port: integer
        :param port: Target port
        :type  connection_mode: string
        :param connection_mode: Connection mode of the RDS Instance
        :type  db_instance_class: string
        :param db_instance_class: The instance type of the database
        :type  db_instance_storage: integer
        :param db_instance_storage: Size in gigabytes of the DB instance to change
        :type  pay_type: string
        :param pay_type: The pay type of the DB instance.
        :type  instance_description: string
        :param instance_description: Instance description or remarks, no more than 256 bytes
        :type  security_ip_list: string
        :param security_ip_list: List of IP addresses allowed to access all databases of an instance
        :type  instance_network_type: string
        :param instance_network_type: The network type of the instance.
        :type  vpc_id: string
        :param vpc_id: The ID of the VPC.
        :type  vswitch_id: string
        :param vswitch_id: ID of VSwitch
        :type  maint_window: string
        :param maint_window: Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.
        :type  preferred_backup_time: string
        :param preferred_backup_time: Backup time, in the format ofHH:mmZ- HH:mm Z.
        :type  preferred_backup_period: string
        :param preferred_backup_period: Backup period
        :type  backup_retention_period: integer
        :param backup_retention_period: Retention days of the backup
        :return:
            changed: If instance is modified successfully. the changed para will be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
        perform_flag = True               
        try:
            instance_status = "Stopped"
            while instance_status == "Stopped":
                try:
                    instance_info = self.get_rds_instances_info(instance_id)
                    if instance_info:
                        if int(instance_info[1][u'TotalRecordCount']) == 1:
                            instance_status = "Present"
                            break
                        else:
                            perform_flag = False
                            results.append({"Error Message": "Instance not found in specified region"})
                            break

                except Exception as ex:
                    instance_status = "Stopped" 
            if perform_flag:    
                if self.check_instance_status(instance_id):
                    changed_inst_type, result_inst_type = self.change_rds_instance_type(instance_id, db_instance_class,
                                                                                        db_instance_storage, pay_type)
                    if result_inst_type:
                        results.append(result_inst_type)
                    
                    if 'error' not in (''.join(str(result_inst_type))).lower():
                        changed = True
                    time.sleep(60)                                                                   

                if self.check_instance_status(instance_id):                                  
                    changed_security_ip, result_security_ip =\
                        self.modify_rds_instance_security_ip_list(instance_id, security_ip_list)

                    if 'error' in (''.join(str(result_security_ip))).lower():
                        results.append(result_security_ip)
                    else:
                        changed = True                      
                                 
                if preferred_backup_time and preferred_backup_period:
                    if self.check_instance_status(instance_id):        
                        changed_backup_policy, result_backup_policy = \
                            self.modify_backup_policy(instance_id, preferred_backup_time, preferred_backup_period,
                                                      backup_retention_period)
                        if 'error' in (''.join(str(result_backup_policy))).lower():
                            results.append(result_backup_policy)
                        else:
                            changed = True       
                                             
                if maint_window:
                    if self.check_instance_status(instance_id):     
                        changed_maint_time, result_maint_time = self.modify_db_instance_maint_time(instance_id,
                                                                                                   maint_window)
                        if 'error' in (''.join(str(result_maint_time))).lower():
                            results.append(result_maint_time)
                        else:
                            changed = True  
                                  
                if connection_mode:
                    if self.check_instance_status(instance_id):
                        changed_conn_mode, result_conn_mode = self.modify_rds_instance_access_mode(instance_id,
                                                                                                   connection_mode)
                    if 'error' in (''.join(str(result_conn_mode))).lower():
                        results.append(result_conn_mode)
                    else:
                        changed = True  
                    time.sleep(5)

                if instance_description:
                    if self.check_instance_status(instance_id):
                        changed_inst_desc, result_inst_desc = self.modify_rds_instance_description(instance_id,
                                                                                                   instance_description)
                        if 'error' in (''.join(str(result_inst_desc))).lower():
                            results.append(result_inst_desc)
                        else:
                            changed = True           
                              
                if current_connection_string:    
                    if self.check_instance_status(instance_id) and connection_string_prefix and port:                          
                        changed_public_conn, result_public_conn = \
                            self.modify_instance_public_connection(instance_id, current_connection_string,
                                                                   connection_string_prefix, port)
            
                        if 'error' in (''.join(str(result_public_conn))).lower():
                            results.append(result_public_conn)                          
                        else:
                            changed = True                       
                        time.sleep(5)    
                                       
                if instance_network_type and self.check_instance_status(instance_id):   
                    changed_net_type, result_net_type = self.modify_rds_instance_network_type(instance_id,
                                                                                              instance_network_type,
                                                                                              vpc_id, vswitch_id)
                    if 'error' in (''.join(str(result_net_type))).lower():
                        results.append(result_net_type)                        
                    else:
                        changed = True                      

        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def check_instance_status(self, instance_id):
        """
        Check RDS Instance Status
        
        :type  instance_id: string
        :param instance_id: Id of the Instance to modify
        :return: return true if instance status is running else false
        """
        status_flag = False
        instance_status = "Stopped"
        while instance_status == "Stopped":
            try:
                instance_info = self.get_rds_instances_info(instance_id)
                if instance_info:    
                    if instance_info[1][u'Items'][u'DBInstance'][0][u'DBInstanceStatus'] \
                            in ['running', 'Running']:
                        instance_status = instance_info[1][u'Items'][u'DBInstance'][0][u'DBInstanceStatus']
                        status_flag = True
                    else:
                        time.sleep(15)                           
            except Exception as ex:
                instance_status = "Stopped"           
        return status_flag

    def change_rds_instance_type(self, instance_id, db_instance_class, db_instance_storage, pay_type):
        """
        Change RDS Instance Type

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type db_instance_class: string
        :param db_instance_class: The instance type of the database
        :type db_instance_storage: integer
        :param db_instance_storage: Size in gigabytes to change of the DB instance.
        :type pay_type: string
        :param pay_type: The pay type of the DB instance.
        :return:
            changed: If instance is changed successfully. the changed para will be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False

        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if db_instance_class:
            self.build_list_params(params, db_instance_class, 'DBInstanceClass')
        if db_instance_storage:
            self.build_list_params(params, db_instance_storage, 'DBInstanceStorage')
        if pay_type:
            self.build_list_params(params, pay_type, 'PayType')
             
        try:
            results = self.get_status('ModifyDBInstanceSpec', params)  
            changed = True          
        except Exception as ex:
            custom_msg = [
                "The API is showing None error code and error message while changing rds instance type",
                "Following error occur while changing rds instance type: ",
                "Failed to change rds instance type with error code "
            ]
            results = results + self.rds_error_handler(ex, custom_msg)

        return changed, results
    
    def modify_rds_instance_access_mode(self, instance_id, connection_mode):
        """
        Modify RDS Instance Access Mode

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type  connection_mode: string
        :param connection_mode: Connection mode of the RDS Instance
        :return:
            changed: If access mode of instance changed successfully. the changed para will be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False  
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if connection_mode:
            self.build_list_params(params, connection_mode, 'ConnectionMode')                     
        try:

            results = self.get_status('ModifyDBInstanceConnectionMode', params)  
            changed = True          
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error "
                                                 "message while modifying instance access mode"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify instance access mode with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results
    
    def modify_rds_instance_network_type(self, instance_id, instance_network_type, vpc_id, vswitch_id,
                                         private_ip_address=None):
        """
        Modify RDS Instance Network Type

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type instance_network_type: string
        :param instance_network_type: The network type of the instance.
        :type vpc_id: string
        :param vpc_id: The ID of the VPC. Value depends on network_type.
        :type vswitch_id: string
        :param vswitch_id: ID of VSwitch
        :type private_ip_address: string
        :param private_ip_address: IP address of an VPC under VSwitchId.
        :return:
            changed: If network type of the instance modified successfully. the changed para will be set to True else
            False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False  
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if instance_network_type:
            self.build_list_params(params, instance_network_type, 'InstanceNetworkType')       
        if vpc_id:
            self.build_list_params(params, vpc_id, 'VPCId')
        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')   
        if private_ip_address:
            self.build_list_params(params, private_ip_address, 'PrivateIpAddress')
                                              
        try:

            results = self.get_status('ModifyDBInstanceNetworkType', params)  
            changed = True          
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error"
                                                 " message while modifying instance network type "})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify instance network type with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def modify_rds_instance_description(self, instance_id, instance_description):
        """
        Modify RDS Instance Description

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type instance_id: string
        :param instance_description: Instance description or remarks, no more than 256 bytes
        :return:
            changed: If rds instance description modified successfully. the changed para will be set to True else
            False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False  
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if instance_description:
            self.build_list_params(params, instance_description, 'DBInstanceDescription')       
                                              
        try:

            results = self.get_status('ModifyDBInstanceDescription', params)  
            changed = True          
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error "
                                                 "message while modifying instance description"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify instance description with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def modify_rds_instance_security_ip_list(self, instance_id, security_ip_list, db_instance_ip_array_name=None,
                                             db_instance_ip_array_attribute=None):
        """
        Modify RDS Instance Security Ip List

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type security_ip_list: list
        :param security_ip_list: List of IP addresses allowed to access all databases of an instance.
        :type db_instance_ip_array_name: string
        :param db_instance_ip_array_name: Name of an IP address white list array
        :type db_instance_ip_array_attribute: string
        :param db_instance_ip_array_attribute: This parameter differentiates attribute values
        :return:
            changed: If security ip list is modified successfully. the changed para will be set to True else
            False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False  
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if security_ip_list:
            self.build_list_params(params, security_ip_list, 'SecurityIps')       
        if db_instance_ip_array_name:
            self.build_list_params(params, db_instance_ip_array_name, 'DBInstanceIPArrayName')
        if db_instance_ip_array_attribute:
            self.build_list_params(params, db_instance_ip_array_attribute, 'DBInstanceIPArrayAttribute')   
                                              
        try:

            results = self.get_status('ModifySecurityIps', params)  
            changed = True          
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error "
                                                 "message modifying security ip list"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify security ip list with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def create_instance_public_connection_string(self, db_instance_id, public_connection_string_prefix, public_port):
        """
        Create Instance Public Connection String

        :type db_instance_id: string
        :param db_instance_id: Id of instances to change
        :type public_connection_string_prefix: string
        :param public_connection_string_prefix: Prefix of an Internet connection string
        :type public_port: integer
        :param public_port: The public connection port.
        :return:
            changed: If instance public connection string created successfully.The changed para will be set to True else
            False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
        
        if db_instance_id:
            self.build_list_params(params, db_instance_id, 'DBInstanceId')
        if public_connection_string_prefix:
            self.build_list_params(params, public_connection_string_prefix, 'ConnectionStringPrefix')
        if public_port:
            self.build_list_params(params, public_port, 'Port')
        try:
            results = self.get_status('AllocateInstancePublicConnection', params)
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error message"
                                                 " while creating public connection string "})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to create public connection string with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def modify_instance_public_connection(self, db_instance_id, current_connection_string,
                                          connection_string_prefix, port):
        """
        Modify Instance Public connection string

        :type db_instance_id: string
        :param db_instance_id: Id of instances to change
        :type current_connection_string: string
        :param current_connection_string: Current connection string of an instance.
        :type connection_string_prefix: string
        :param connection_string_prefix: Prefix of an Internet connection string
        :type port: integer
        :param port: The public connection port.
        :return:
            changed: If instance public connection string modified successfully.The changed para will
             be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
        
        if db_instance_id:
            self.build_list_params(params, db_instance_id, 'DBInstanceId')
        if current_connection_string:
            self.build_list_params(params, current_connection_string, 'CurrentConnectionString')
        if connection_string_prefix:
            self.build_list_params(params, connection_string_prefix, 'ConnectionStringPrefix')
        if port:
            self.build_list_params(params, port, 'Port')
        try:
            results = self.get_status('ModifyDBInstanceConnectionString', params)
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error message"
                                                 " while modifying public connection string "})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify public connection string with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def modify_db_instance_maint_time(self, instance_id, maint_window):
        """
        Modify Instance Maintenance Time
        :type instance_id: string
        :param instance_id: Id of instances to change
        :type maint_window: string
        :param maint_window: Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.
        :return:
            changed: If instance maintenance time is modified successfully.The changed para will
             be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
                
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if maint_window:
            self.build_list_params(params, maint_window, 'MaintainTime')
        try:
            results = self.get_status('ModifyDBInstanceMaintainTime', params)            
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error message"
                                                 " while modifying maintenance time"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify maintenance time with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def modify_backup_policy(self, instance_id, preferred_backup_time, preferred_backup_period,
                             backup_retention_period, backup_log=None):
        """
        Modify Backup Policy

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type preferred_backup_time: string
        :param preferred_backup_time: Backup time, in the format ofHH:mmZ- HH:mm Z.
        :type preferred_backup_period: string
        :param preferred_backup_period: Backup period
        :type backup_retention_period: integer
        :param backup_retention_period: Retention days of the backup (7 to 730 days
        :type backup_log: string
        :param backup_log: The default value is Enable. You can change it to Disabled
        :return:
            changed: If backup policy is modified successfully.The changed para will
             be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if preferred_backup_time:
            self.build_list_params(params, preferred_backup_time, 'PreferredBackupTime')
        if preferred_backup_period:
            self.build_list_params(params, preferred_backup_period, 'PreferredBackupPeriod')
        if backup_retention_period:
            self.build_list_params(params, backup_retention_period, 'BackupRetentionPeriod')
        if backup_log:
            self.build_list_params(params, backup_log, 'BackupLog')
        try:
            results = self.get_status('ModifyBackupPolicy', params)            
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error message "
                                                 "while modifying backup policy"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to modify backup policy with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def bind_tags(self, instance_id, db_tags):
        """
        Bind Tags to Instance

        :type instance_id: string
        :param instance_id: Id of instances to change
        :type instance_id: dict
        :param db_tags: A dictionaries of db tags
        :return:
            changed: If tags binded to instance successfully.The changed para will
             be set to True else False
            result: detailed server response
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if db_tags:
            db_tags_json = json.dumps(db_tags)
        if db_tags_json:
            self.build_list_params(params, db_tags_json, 'Tags')
        try:
            results = self.get_status('AddTagsToResource', params)            
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack") or ex.error_code is None:
                results.append({"Error Message": "The API is showing None error code and error message "
                                                 "while binding tags"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append("Failed to bind tags with error code " + error_code +
                               " and message: " + error_msg)

        return changed, results

    def create_database(self, instance_id, db_name, db_description, character_set_name):
        """
        Creates a new database in an instance
        :type instance_id: str
        :param instance_id: Id of instances
        :type db_name: str
        :param db_name: Name of a database to create within the instance.  If not specified, then no database is created
        :type db_description: str
        :param db_description: Description of a database to create within the instance.  If not specified,
        then no database is created.
        :type character_set_name: str
        :param character_set_name: Associate the DB instance with a specified character set.
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if db_name:
            self.build_list_params(params, db_name, 'DBName')
        if character_set_name:
            self.build_list_params(params, character_set_name, 'CharacterSetName')
        if db_description:
            self.build_list_params(params, db_description, 'DBDescription')
        
        try:
            response = self.get_status('CreateDatabase', params)
            results.append(response)
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack"):
                results.append({"Error Message": "The API is showing None error code and error message"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def delete_database(self, instance_id, db_name):
        """
        Delete database
        :type instance_id: str
        :param instance_id: Id of instances
        :type db_name: str
        :param db_name: Name of a database to delete within the instance. If not specified, then no database is deleted
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if db_name:
            self.build_list_params(params, db_name, 'DBName')
        try:
            response = self.get_status('DeleteDatabase', params)
            results.append(response)
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack"):
                results.append({"Error Message": "The API is showing None error code and error message"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results
    
    def reset_instance_password(self, db_instance_id, account_name, account_password):
        """
        Reset instance password
        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :type account_password: str
        :param account_password: A new password. It may consist of letters, numbers, or underlines,
        with a length of 6 to 32 characters
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False
        
        if db_instance_id:
            self.build_list_params(params, db_instance_id, 'DBInstanceId')

        if account_name:
            self.build_list_params(params, account_name, 'AccountName')

        if account_password:
            self.build_list_params(params, account_password, 'AccountPassword')
        
        try:
            response = self.get_status('ResetAccountPassword', params)
            results.append(response)
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack"):
                results.append({"Error Message": "The API is showing None error code and error message"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def restart_rds_instance(self, instance_id):
        """
        Restart rds instance
        :type instance_id: str
        :param instance_id: Id of instances to reboot
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        
        try:
            response = self.get_status('RestartDBInstance', params)
            results.append(response)
            changed = True
            time.sleep(120)
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack"):
                results.append({"Error Message": "The API is showing None error code and error message"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def release_rds_instance(self, instance_id):
        """
        Release rds instance
        :type instance_id: str
        :param instance_id: Id of instances to remove
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False
        
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        
        try:
            response = self.get_status('DeleteDBInstance', params)
            results.append(response)
            changed = True
        except Exception as ex:
            error_code = str(ex.error_code)
            error_msg = str(ex.message)
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results
    
    def create_account(self, db_instance_id, account_name, account_password, description=None, account_type=None):
        """
        Create account for database
        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Operation account requiring a uniqueness check. It may consist of lower case letters,
        numbers and underlines, and must start with a letter and have no more than 16 characters.
        :type account_password: str
        :param account_password: Operation password. It may consist of letters, digits, or underlines,
        with a length of 6 to 32 characters
        :type description: str
        :param description: Account remarks, which cannot exceed 256 characters. NOTE: It cannot begin with http://,
        https:// . It must start with a Chinese character or English letter. It can include Chinese and English
        characters/letters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters
        :type account_type: str
        :param account_type: Privilege type of account. Normal: Common privilege;Super: High privilege;
        Default value is Normal.This parameter is valid for MySQL 5.5/5.6 only.
        :return: Bool
        """
        params = {}
        account_obj = None
        
        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        self.build_list_params(params, account_name, 'AccountName')
        self.build_list_params(params, account_password, 'AccountPassword')
        if description:
            self.build_list_params(params, description, 'AccountDescription')
        if account_type:
            self.build_list_params(params, account_type, 'AccountType')
        self.get_object('CreateAccount', params, ResultSet)
        if self.wait_for_account_status(db_instance_id, account_name):
            account_obj = self.list_account(db_instance_id, account_name)[0]
        return account_obj
    
    def wait_for_account_status(self, db_instance_id, account_name, dely_time = 3, timeout = 60, state = "Available"):
        """
        Wait for account status
        :type dely_time: int
        :param dely_time: The request time interval
        :type timeout: int
        :param timeout: overtime time
        :type state: str
        :param state: Expected state
        :return: Bool
        """
        assert(dely_time < timeout)
        account_list = []
        runing_time = 0
        result = False
        while runing_time < timeout:
            account_list = self.list_account(db_instance_id, account_name)
            if len(account_list) != 1:
                time.sleep(dely_time)
                runing_time = runing_time + dely_time
                continue
            if account_list[0].account_status == state:
                result = True
                break
            runing_time = runing_time + dely_time
            time.sleep(dely_time)    
        return result
    
    def reset_account_password(self, db_instance_id, account_name, account_password):
        """
        Reset instance password
        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :type account_password: str
        :param account_password: A new password. It may consist of letters, numbers, or underlines,
        with a length of 6 to 32 characters
        :return: Bool
        """
        params = {}

        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        self.build_list_params(params, account_name, 'AccountName')
        self.build_list_params(params, account_password, 'AccountPassword')
        
        return self.get_status('ResetAccountPassword', params)

    def delete_account(self, db_instance_id, account_name):
        """
        Delete Account

        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :return: Bool
        """
        params = {}
        
        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        self.build_list_params(params, account_name, 'AccountName')
        return self.get_status('DeleteAccount', params)

    def modify_account_description(self, db_instance_id, account_name, description):
        """
        modify Account

        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :type description: str
        :param description: description of account
        :return: Bool
        """
        params = {}
        
        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        self.build_list_params(params, account_name, 'AccountName')
        self.build_list_params(params, description, 'AccountDescription')
        return self.get_status('ModifyAccountDescription', params)

    def grant_account_privilege(self, db_instance_id, account_name, db_name, account_privilege):
        """
        Grant Account Permissions

        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :type db_name: str
        :param db_name: Name of a database.
        :type account_privilege: str
        :param account_privilege: Account permissions
        :return: Bool
        """
        params = {}
        
        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        self.build_list_params(params, account_name, 'AccountName')
        self.build_list_params(params, db_name, 'DBName')
        self.build_list_params(params, account_privilege, 'AccountPrivilege')
        return self.get_status('GrantAccountPrivilege', params)

    def revoke_account_privilege(self, db_instance_id, account_name, db_name):
        """
        Revoke Account Permissions

        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :type db_name: str
        :param db_name: Name of a database.
        :return: Bool
        """
        params = {}
        results = []
        changed = False
        
        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        self.build_list_params(params, account_name, 'AccountName')
        self.build_list_params(params, db_name, 'DBName')
        return self.get_status('RevokeAccountPrivilege', params)

    def list_account(self, db_instance_id, account_name = None):
        """
        Reset account
        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :return: object list of accounts
        """
        params = {}
        self.build_list_params(params, db_instance_id, 'DBInstanceId')
        if account_name:
            self.build_list_params(params, account_name, 'AccountName')
        return self.get_list('DescribeAccounts', params, ['Accounts', Account])

    def switch_between_primary_standby_database(self, instance_id, node_id, force):
        """
        Switch between primary and standby databases in rds instance
        :type instance_id: str
        :param instance_id: Id of instances to modify
        :type node_id: str
        :param node_id: Unique ID of a node
        :type force: str
        :param force: Yes: forced; No: unforced; default value: unforced
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False       

        try:
            self.build_list_params(params, instance_id, 'DBInstanceId')
            describe_response = self.get_status('DescribeDBInstanceHAConfig', params)
            if describe_response:
                for describe_config in describe_response[u'HostInstanceInfos'][u'NodeInfo']:
                    if describe_config[u'NodeType'] == 'Slave':
                        node = describe_config[u'NodeId']
                        break
                if node == node_id:
                    if node_id:
                        self.build_list_params(params, node_id, 'NodeId')
                    if force:
                        self.build_list_params(params, force, 'Force')
        
                    response = self.get_status('SwitchDBInstanceHA', params)
                    results.append(response)
                    changed = True
                    time.sleep(7)
                else:
                    results.append({"Error Message": "The specified node_id is not found"})

        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack"):
                results.append({"Error Message": "The API is showing None error code and error message"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def reset_account(self, db_instance_id, account_name, account_password):
        """
        Reset account
        :type db_instance_id: str
        :param db_instance_id: Id of instance
        :type account_name: str
        :param account_name: Name of an account
        :type account_password: str
        :param account_password: Account password.
        :return: Result dict of operation
        """
        params = {}
        results = []
        changed = False

        if db_instance_id:
            self.build_list_params(params, db_instance_id, 'DBInstanceId')

        if account_name:
            self.build_list_params(params, account_name, 'AccountName')

        if account_password:
            self.build_list_params(params, account_password, 'AccountPassword')

        try:
            response = self.get_status('ResetAccountForPG', params)
            results.append(response)
            changed = True
        except Exception as ex:
            if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                    or (ex.message == "need more than 2 values to unpack"):
                results.append({"Error Message": "The API is showing None error code and error message"})
            else:
                error_code = ex.error_code
                error_msg = ex.message
                results.append({"Error Code": error_code, "Error Message": error_msg})

        return changed, results

    def rds_error_handler(self, ex, custom_msg):
        """    
        Generic method to handling errors
        :type ex: list
        :param ex: An exception object
        :type custom_msg: list
        :param custom_msg: List of custom error messages
        :return: retun error message
        """
        results = []
        error_code = ex.error_code
        error_msg = ex.message
        error_dict = {
            "FUWU_BIZ_COMMODITY_VERIFY_FAIL": "Provided db_engine, engine_version and"
                                              " db_instance_class is not valid or mismatch",
            "CreateOrder.Failed": "Provided db_engine, engine_version and"
                                  " db_instance_class is not valid or mismatch",
            "InvalidOrderTask.NotSupport": "Provided private_ip_address is not"
                                           " valid ip address for VPC under VSwitch"
        }

        if (ex.args is None) or (ex.args == "need more than 2 values to unpack") \
                or (error_msg == "need more than 2 values to unpack") or error_code is None:
            results.append({"Error Message": custom_msg[0]})
        elif error_code in error_dict:
            results.append(custom_msg[1] + str(error_dict[error_code]))
        else:
            results.append(custom_msg[2] + error_code +
                           " and message: " + error_msg)
        return results


    def get_rds_instances(self, instance_id=None, engine=None, dbinstance_type=None, instance_network_type=None,
                          connection_mode=None, tags=None):
        """
        Get RDS Instance Info

        :type instance_id: string
        :param instance_id: Id of instance
        :type engine: string
        :param engine: Type of the database
        :type dbinstance_type: string
        :param dbinstance_type: Instance type
        :type instance_network_type: string
        :param instance_network_type: Instance Network type
        :type connection_mode: string
        :param connection_mode: Instance connection mode
        :type db_tags: dict
        :param db_tags: Database tags
        :return:
            result: detailed server response
        """
        db_tags_json = []
        params = {}
        if instance_id:
            self.build_list_params(params, instance_id, 'DBInstanceId')
        if engine:
            self.build_list_params(params, engine, 'Engine')
        if dbinstance_type:
            self.build_list_params(params, dbinstance_type, 'DBInstanceType')
        if instance_network_type:
            self.build_list_params(params, instance_network_type, 'InstanceNetworkType')
        if connection_mode:
            self.build_list_params(params, connection_mode, 'ConnectionMode')
        if tags:
            db_tags_json = json.dumps(tags)
        if db_tags_json:
            self.build_list_params(params, db_tags_json, 'Tags')
        return self.get_list('DescribeDBInstances', params, ['Items', DbInstance])



