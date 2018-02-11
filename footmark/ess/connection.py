# encoding: utf-8
"""
Represents a connection to the ECS service.
"""

import warnings
import time
import json
import base64
import logging
from footmark.ess.config import *
from footmark.connection import ACSQueryConnection
from footmark.exception import ECSResponseError
from footmark.resultset import ResultSet
from footmark.ess.configuration import ScalingConfiguration
from footmark.ess.group import ScalingGroup
from footmark.ess.instance import ScalingInstance
from footmark.ess.rule import ScalingRule
from footmark.ess.scheduled_task import ScheduledTask
# from aliyunsdkess.request.v20140828.DescribeScalingRulesRequest import


class ESSConnection(ACSQueryConnection):
    SDKVersion = '2014-08-28'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    ResponseError = ECSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None):
        """
        Init method to create a new connection to ECS.
        """
        if not region:
            region = self.DefaultRegionId
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.ESSSDK = 'aliyunsdkess.request.v' + self.SDKVersion.replace('-', '')

        super(ESSConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            region=self.region, product=self.ESSSDK,
                                            security_token=security_token, user_agent=user_agent)

    def build_filter_params(self, params, filters):
        if not isinstance(filters, dict):
            return

        flag = 1
        for key, value in filters.items():
            acs_key = key
            if acs_key.startswith('tag:'):
                while ('set_Tag%dKey' % flag) in params:
                    flag += 1
                if flag < 6:
                    params['set_Tag%dKey' % flag] = acs_key[4:]
                    params['set_Tag%dValue' % flag] = filters[acs_key]
                flag += 1
                continue
            if key == 'group_id':
                if not value.startswith('sg-') or len(value) != 12:
                    warnings.warn("The group-id filter now requires a security group "
                                  "identifier (sg-*) instead of a security group ID. "
                                  "The group-id " + value + "may be invalid.",
                                  UserWarning)
                params['set_SecurityGroupId'] = value
                continue
            if not isinstance(value, dict):
                acs_key = ''.join(s.capitalize() for s in acs_key.split('_'))
                params['set_' + acs_key] = value
                continue

            self.build_filters_params(params, value)

    def build_tags_params(self, params, tags, max_tag_number=None):
        tag_no = 1
        if tags:
            for key, value in tags.items():
                if tag_no < max_tag_number and key:
                    self.build_list_params(params, key, 'Tag' + bytes(tag_no+1) + 'Key')
                    self.build_list_params(params, value, 'Tag' + bytes(tag_no+1) + 'Value')
                    tag_no += 1

    def create_configuration(self, scaling_group_id, image_id, instance_type, security_group_id, name=None,
                             internet_charge_type=None, max_bandwidth_in=None, max_bandwidth_out=None,
                             system_disk_category='cloud_efficiency', system_disk_size=40, data_disks=None,
                             tags=None, key_pair_name=None, ram_role_name=None, user_data=None):
        """
        create an scaling configuration in ess

        :type str
        :param scaling_group_id: ID of the scaling group of a scaling configuration.
        :type str
        :param image_id: ID of an ECS instance image, indicating an image selected
        :type str
        :param instance_type: Resource type of an ECS instance.
        :type str
        :param security_group_id: ID of the security group to which a newly created instance belongs.
        :type str
        :param name: Name shown for the scheduled task. 
            The name must contain 2-40 English or Chinese characters, and start with a number, 
            a letter in upper or lower case or a Chinese character. 
            The name can contain numbers, “_“, “-“ or “.”. 
            The account name in the same scaling group is unique in the same region. 
            If this parameter value is not specified, the default value is ScalingConfigurationId.
        :type str
        :param internet_charge_type: Network billing type, Values: PayByBandwidth or PayByTraffic. Default to PayByBandwidth.
        :type str
        :param max_bandwidth_out: Maximum outgoing bandwidth from the public network, measured in Mbps (Mega bit per second). Default to 0.
        :type str
        :param max_bandwidth_in: Maximum incoming bandwidth from the public network, measured in Mbps (Mega bit per second). Default to 200.
        :type str
        :param system_disk_category: Category of the system disk. Values: cloud_efficiency or cloud_ssd. Default to cloud_efficiency.
        :type int
        :param system_disk_size: Size of the system disk. Values: 40~500. Default to 40.
        :type list
        :param data_disks: A list of hash/dictionaries of data disks. A maximum of four values can be entered.
            '[{size:"value", category:"value", snapshot_id:"value", delete_with_instance:"value"}]',
            size: Size of data disk. Values: 20 ~ 32768.
            category: Category of the data disk. Values: cloud_efficiency or cloud_ssd. Default to cloud_efficiency.
            snapshot_id: Snapshot used for creating the data disk. If it is specified, the size parameter is neglected, and the size of the created disk is the size of the snapshot.
            delete_with_instance: Whether the data disk will be released along with the instance. Default to true.
        :type list
        :param tags: A list of hash/dictionaries of instance
            tags, '[{tag_key:"value", tag_value:"value"}]', tag_key
            must be not null when tag_value isn't null
        :type str
        :param key_pair_name: Key pair name.
        :type str
        :param ram_role_name: The name of the instance RAM role.
        :type str
        :param user_data: The user-defined data of the instance. 
        
        :rtype: object
        :return: Returns a <footmark.ess.Configuration> object.

        """

        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')
        self.build_list_params(params, image_id, 'ImageId')
        self.build_list_params(params, instance_type, 'InstanceType')
        self.build_list_params(params, security_group_id, 'SecurityGroupId')

        if name:
            self.build_list_params(params, name, 'ScalingConfigurationName')
        if internet_charge_type:
            self.build_list_params(params, internet_charge_type, 'InternetChargeType')
        if max_bandwidth_in:
            self.build_list_params(params, max_bandwidth_in, 'InternetMaxBandwidthIn')
        if max_bandwidth_out:
            self.build_list_params(params, max_bandwidth_out, 'InternetMaxBandwidthOut')

        if system_disk_category:
            self.build_list_params(params, system_disk_category, 'SystemDisk.Category')
        if system_disk_size:
            self.build_list_params(params, system_disk_size, 'SystemDisk.Size')

        # Disks Details
        if data_disks:
            for i in range(len(data_disks)):
                if i > 3:
                    break
                disk = data_disks[i]
                if disk:
                    if 'size' in disk:
                        self.build_list_params(params, disk['size'], 'DataDisk' + bytes(i+1) + 'Size')
                    if 'category' in disk:
                        self.build_list_params(params, disk['category'], 'DataDisk' + bytes(i+1) + 'Category')
                    if 'snapshot_id' in disk:
                        self.build_list_params(params, disk['snapshot_id'], 'DataDisk' + bytes(i+1) + 'SnapshotId')
                    if 'delete_with_instance' in disk:
                        self.build_list_params(params, disk['delete_with_instance'],
                                               'DataDisk' + bytes(i+1) + 'DeleteWithInstance')

        self.build_tags_params(params, tags, max_tag_number=5)

        if key_pair_name:
            self.build_list_params(params, key_pair_name, 'KeyPairName')

        if user_data:
            self.build_list_params(params, base64.b64encode(user_data), 'UserData')

        if ram_role_name:
            self.build_list_params(params, ram_role_name, 'RamRoleName')
        instances = []

        result = self.get_object('CreateScalingConfiguration', params, ResultSet)
        return self.describe_configurations(scaling_group_id=scaling_group_id, scaling_configuration_ids=[result.scaling_configuration_id])[0]

    def describe_configurations(self, scaling_group_id=None, scaling_configuration_ids=None, scaling_configuration_names=None,
                                pagenumber=None, pagesize=50):
        """
        Retrieve all the scaling configurations 
        :type str
        :parameter scaling_group_id: ID of the scaling group of a scaling configuration.
        :type list
        :parameter scaling_configuration_ids: List ID of a scaling configurations.
        :type list
        :parameter scaling_configuration_names: List name of a scaling configurations.
        :type int
        :parameter pagenumber: Page number of the scaling configuration list. The initial value and default value are both 1.
        :type int
        :parameter pagesize: When querying by page, this parameter indicates the number of lines per page. Maximum value: 50; default value: 10.
        
        :rtype: list
        :return: A list of  :class:`footmark.ess.configuration`

        """

        cfgs = []
        params = {}
        if scaling_group_id:
            self.build_list_params(params, scaling_group_id, 'ScalingGroupId')
        if scaling_configuration_ids and len(scaling_configuration_ids) > 0:
            for i in range(len(scaling_configuration_ids)):
                if i < 10 and scaling_configuration_ids[i]:
                    self.build_list_params(params, scaling_configuration_ids[i], 'ScalingConfigurationId'+ bytes(i+1))
        if scaling_configuration_names:
            for i in range(len(scaling_configuration_names)):
                if i < 10 and scaling_configuration_names[i]:
                    self.build_list_params(params, scaling_configuration_names[i], 'ScalingConfigurationName'+ bytes(i+1))

        self.build_list_params(params, pagesize, 'PageSize')

        pNum = pagenumber
        if not pNum:
            pNum = 1
        while True:
            self.build_list_params(params, pNum, 'PageNumber')
            cfg_list = self.get_list('DescribeScalingConfigurations', params, ['ScalingConfigurations', ScalingConfiguration])

            for cfg in cfg_list:
                cfgs.append(cfg)
            if pagenumber or len(cfg_list) < pagesize:
                break
            pNum += 1

        return cfgs

    def terminate_configuration(self, scaling_configuration_id):
        """
        Deletes a specified scaling configuration.
        
        An active scaling configuration in a scaling group cannot be deleted.
        If any ECS instance created according to a scaling configuration is still in the scaling group, the scaling configuration cannot be deleted.

        :type str
        :param scaling_configuration_id: ID of a scaling configuration.

        :rtype: bool
        :return: The result of deleting scaling configuration.
        """
        params = {}

        self.build_list_params(params, scaling_configuration_id, 'ScalingConfigurationId')

        return self.get_status('DeleteScalingConfiguration', params)

    def create_group(self, max_size, min_size, name=None, default_cooldown=None, removal_policies=None,
                     load_balancer_ids=None, db_instance_ids=None, vswitch_ids=None):
        """
        A scaling group is a collection of ECS instances with the same application scenarios.
        It defines the maximum and minimum numbers of ECS instances in the group, 
        and their associated Server Load Balancer instances, RDS instances, and other attributes.

        :type int
        :param max_size: Maximum number of ECS instances in the scaling group. Value range: [0, 100].
        :type int
        :param min_size: Minimum number of ECS instances in the scaling group. Value range: [0, 100].
        :type str
        :param name: Name shown for the scaling group, which must contain 2-40 characters (English or Chinese).
            The name must begin with a number, an upper/lower-case letter or a Chinese character and may contain numbers, “_“, “-“ or “.”. 
            The account name is unique in the same region.
            If this parameter is not specified, the default value is its ID.
        :type int
        :param default_cooldown: Default cool-down time (in seconds) of the scaling group. Value range: [0, 86400]. Default to is 300.
        :type list
        :param removal_policies: Policy for removing ECS instances from the scaling group.
            Optional values:
                OldestInstance: removes the first ECS instance attached to the scaling group.
                NewestInstance: removes the first ECS instance attached to the scaling group.
                OldestScalingConfiguration: removes the ECS instance with the oldest scaling configuration.
            Default values: OldestScalingConfiguration and OldestInstance.
            At most 2 policies can be entered.
        :type list
        :param load_balancer_ids: ID list of a Server Load Balancer instance.
        :type list
        :param db_instance_ids: ID list of an RDS instance.
        :type list
        :param vswitch_ids: ID list of a VSwitch. It is used to create instance in multiple zones.
            At most 5 VSwitches in a VPC can be specified.
            The priority of VSwitches descends from 1 to 5, and 1 indicates the highest priority.
            When you fail to create an instance in the zone to which a specified VSwitch belongs, 
            another VSwitch with less priority replaces the specified one automatically. 
        
        :rtype: object
        :return: Returns a <footmark.ess.Group> object.

        """

        params = {}

        self.build_list_params(params, max_size, 'MaxSize')
        if min_size > max_size:
            self.build_list_params(params, max_size, 'MinSize')
        else:
            self.build_list_params(params, min_size, 'MinSize')

        if name:
            self.build_list_params(params, name, 'ScalingGroupName')
        if default_cooldown:
            self.build_list_params(params, default_cooldown, 'DefaultCooldown')
        if removal_policies:
            for i in range(len(removal_policies)):
                if i < 2 and removal_policies[i]:
                    self.build_list_params(params, removal_policies[i], 'RemovalPolicy' + bytes(i + 1));
        if load_balancer_ids:
            self.build_list_params(params, json.dumps(load_balancer_ids), 'LoadBalancerIds')

        if db_instance_ids:
            self.build_list_params(params, json.dumps(db_instance_ids), 'DBInstanceIds')

        if vswitch_ids:
            self.build_list_params(params, vswitch_ids, 'VSwitchIds')

        result = self.get_object('CreateScalingGroup', params, ResultSet)
        return self.describe_groups(scaling_group_ids=[result.scaling_group_id])[0]

    def describe_groups(self, scaling_group_ids=None, scaling_group_names=None, pagenumber=None, pagesize=50):
        """
        Query the information of a scaling group. Scaling groups have the following life cycle states:

            Active: In this state, the scaling group can receive scaling rule execution requests and trigger scaling activities.
            Inactive: In this state, the scaling group does not receive scaling rule execution requests.
            Deleting: The scaling group is being deleted and does not receive scaling rule execution requests. 
        
        :type list
        :param scaling_group_ids: List ID of a scaling groups.
            At most 20 IDs can be entered.
            Invalid scaling group IDs are not displayed in query results, and no error is reported.
        :type list
        :param scaling_group_names: List name of a scaling groups.
            At most 20 IDs can be entered.
            Invalid scaling group IDs are not displayed in query results, and no error is reported.
        :type int
        :param pagenumber: Page number of the scaling group list. The initial value and default value are both 1.
        :type int
        :param pagesize: When querying by page, this parameter indicates the number of lines per page. Maximum value: 50; default value: 10.
        
        :rtype: list
        :return: A list of :class:`footmark.ess.group`

        """

        cfgs = []
        params = {}
        if scaling_group_ids:
            for i in range(len(scaling_group_ids)):
                if i < 20 and scaling_group_ids[i]:
                    self.build_list_params(params, scaling_group_ids[i], 'ScalingGroupId' + bytes(i + 1))
        if scaling_group_names:
            for i in range(len(scaling_group_names)):
                if i < 20 and scaling_group_names[i]:
                    self.build_list_params(params, scaling_group_names[i], 'ScalingGroupName' + bytes(i + 1))

        self.build_list_params(params, pagesize, 'PageSize')

        pNum = pagenumber
        if not pNum:
            pNum = 1
        while True:
            self.build_list_params(params, pNum, 'PageNumber')
            cfg_list = self.get_list('DescribeScalingGroups', params, ['ScalingGroups', ScalingGroup])
            for cfg in cfg_list:
                cfgs.append(cfg)
            if pagenumber or len(cfg_list) < pagesize:
                break
            pNum += 1

        return cfgs

    def enable_group(self, scaling_group_id, scaling_configuration_id=None, instance_ids=None):
        """
        Enables the specified scaling group.
        After the scaling group is successfully enabled (the group is active), the ECS instances specified by the interface are attached to the group.

        ForceDelete indicates whether to forcibly delete a scaling group and remove and release ECS instances if the scaling group has ECS instances or scaling activities are in progress.

        Restrictions on attaching ECS instances:
        
            1. The attached ECS instance and the scaling group must be in the same region.
            2. The attached ECS instance and the instance with active scaling configurations must be of the same type.
            3. The attached ECS instance must in the running state.
            4. The attached ECS instance has not been attached to other scaling groups.
            5. The attached ECS instance supports Subscription and Pay-As-You-Go payment methods.
            6. If the VswitchID is specified for a scaling group, you cannot attach Classic ECS instances or ECS instances on other VPCs to the scaling group.
            7. If the VswitchID is not specified for the scaling group, ECS instances of the VPC type cannot be attached to the scaling group
        
        :type str
        :param scaling_group_id: ID of a scaling group.
        :type str
        :param scaling_configuration_id: ID of a active scaling configuration.
        :type list
        :param instance_ids: ID of the ECS instance to be attached to the scaling group after it is enabled.
            At most 20 IDs can be entered.

        :rtype: bool
        :return: The result of enabling scaling group.
        """
        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')

        if scaling_configuration_id:
            self.build_list_params(params, scaling_configuration_id, 'ActiveScalingConfigurationId')

        if instance_ids:
            for i in range(len(instance_ids)):
                if i < 20 and instance_ids[i]:
                    self.build_list_params(params, instance_ids[i], 'InstanceId' + bytes(i + 1))

        return self.get_status('EnableScalingGroup', params)

    def disable_group(self, scaling_group_id):
        """
        Disable a specified scaling group.

        The scaling activities in progress before the scaling group is disabled are continued until completion, 
        whereas scaling activities triggered after the scaling group is disabled are rejected.
        
        :type str
        :param scaling_group_id: ID of a scaling group.
        :type str
        
        :rtype: bool
        :return: The result of disabling scaling group.
        """
        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')

        return self.get_status('DisableScalingGroup', params)

    def modify_group(self, scaling_group_id, max_size=None, min_size=None, name=None, default_cooldown=None,
                     removal_policies=None, scaling_configuration_id=None):

        """
        Modifies the attributes of a scaling group.
        
        The interface can be called only when the scaling group is active or inactive.

        When the scaling configuration specified for the scaling group needs to be modified,
        the instance type attribute of the modified scaling configuration must be consistent with that of the active scaling configuration.

        After a new scaling configuration is added to the scaling group, the running ECS instances which are created based on the previous scaling configuration remain unchanged.
        When the number (total capacity) of ECS instances in the scaling group does not meet the modified MaxSize or MinSize specification,
        the Auto Scaling service automatically attaches or removes ECS instances to/from the group to make odds even.
    
        
        :type str
        :param scaling_group_id: ID of a scaling group.
        :type int
        :param max_size: Maximum number of ECS instances in the scaling group. Value range: [0, 100].
        :type int
        :param min_size: Minimum number of ECS instances in the scaling group. Value range: [0, 100].
        :type str
        :param name: Name shown for the scaling group, which must contain 2-40 characters (English or Chinese).
            The name must begin with a number, an upper/lower-case letter or a Chinese character and may contain numbers, “_“, “-“ or “.”. 
            The account name is unique in the same region.
            If this parameter is not specified, the default value is its ID.
        :type int
        :param default_cooldown: Default cool-down time (in seconds) of the scaling group. Value range: [0, 86400]. Default to is 300.
        :type list
        :param removal_policies: Policy for removing ECS instances from the scaling group.
            Optional values:
                OldestInstance: removes the first ECS instance attached to the scaling group.
                NewestInstance: removes the first ECS instance attached to the scaling group.
                OldestScalingConfiguration: removes the ECS instance with the oldest scaling configuration.
            Default values: OldestScalingConfiguration and OldestInstance.
            At most 2 policies can be entered.
        :type str
        :param scaling_configuration_id: ID of a active scaling configuration.
        
        :rtype: object
        :return: Returns a <footmark.ess.Group> object.
    
        """

        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')

        if max_size is not None:
            self.build_list_params(params, max_size, 'MaxSize')
        if min_size is not None:
            self.build_list_params(params, min_size, 'MinSize')
        if name:
            self.build_list_params(params, name, 'ScalingGroupName')
        if default_cooldown:
            self.build_list_params(params, default_cooldown, 'DefaultCooldown')
        if removal_policies:
            for i in range(len(removal_policies)):
                if i < 2 and removal_policies[i]:
                    self.build_list_params(params, removal_policies[i], 'RemovalPolicy' + bytes(i + 1));
        if scaling_configuration_id:
            self.build_list_params(params, scaling_configuration_id, 'ActiveScalingConfigurationId')

        return self.get_status('ModifyScalingGroup', params)

    def terminate_group(self, scaling_group_id, force=False):
        """
        Delete a specified scaling group.

        ForceDelete indicates whether to forcibly delete a scaling group and remove and release ECS instances if the scaling group has ECS instances or scaling activities are in progress.

        When ForceDelete is set to false, the scaling group can be deleted only when the following conditions are met:

            Condition 1: No scaling activities are in progress in the scaling group.
            Condition 2: The current number (total capacity) of ECS instances in the scaling group is 0.
        When the two conditions are met, the scaling group is disabled and then deleted.

        When ForceDelete is set to true, the scaling group is disabled to reject new scaling activity requests. 
        When the existing scaling activity is completed, all ECS instances are removed from the scaling group and the group is then deleted (manually attached ECS instances are removed from the scaling group, whereas ECS instances automatically created by the Auto Scaling service are deleted).
        Deleting a scaling group also deletes scaling configurations, rules, activities, and requests.
        
        :type str
        :param scaling_group_id: ID of a scaling group.
        :type bool
        :param force: Indicates whether to forcibly delete a scaling group and remove and release ECS instances if the scaling group has ECS instances or scaling activities are in progress.
            Default to False.

        :rtype: bool
        :return: The result of deleting scaling group.
        """
        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')

        if force:
            self.build_list_params(params, force, 'ForceDelete')

        return self.get_status('DeleteScalingGroup', params)

    def attach_instances(self, scaling_group_id, instance_ids):
        """
        Attaches an ECS instance to a specified scaling group. Restrictions on the attached ECS instance:

        The attached ECS instance and the scaling group must be in the same region.
        The attached ECS instance must in the running state.
        The attached ECS instance has not been attached to other scaling groups.
        The attached ECS instance supports Subscription and Pay-As-You-Go payment methods.
        If the VswitchID is specified for a scaling group, you cannot attach Classic ECS instances or ECS instances on other VPCs to the scaling group.
        If the VswitchID is not specified for the scaling group, ECS instances of the VPC type cannot be attached to the scaling group.
        
        :type str
        :param scaling_group_id: ID of a scaling group.
        :type list
        :param instance_ids: ID of the ECS instance to be attached to the scaling group after it is enabled.
            At most 20 IDs can be entered.

        :rtype: bool
        :return: The result of deleting scaling group.
        """
        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')

        for i in range(len(instance_ids)):
                if i < 20 and instance_ids[i]:
                    self.build_list_params(params, instance_ids[i], 'InstanceId' + bytes(i + 1))

        result = self.get_object('AttachInstances', params, ResultSet)
        return self.wait_for_instances_status(scaling_group_id, instance_ids, InService, activity_id=result.scaling_activity_id,
                                              delay=DefaultWaitForInterval, timeout=DefaultTimeOut)

    def remove_instances(self, scaling_group_id, instance_ids):
        """
        Removes an ECS instance from a specified scaling group.

        When the ECS instance automatically created by the Auto Scaling service is removed from the scaling group, the ECS instance is disabled and released.
        When the manually attached ECS instance is removed from the scaling group, the ECS instance is neither disabled nor released.
        The interface can be called only when the scaling group is active.
        The interface can be called only when no scaling activity in the scaling group is in progress.
        When no scaling activity in the scaling group is in progress, the interface can be directly executed without cooldown.
        Successfully calling this interface only means that the Auto Scaling service has accepted the call request, and the scaling activity can be executed, but does not necessarily mean that the scaling activity can be successfully executed. You can use the returned ScalingActivityId to check the status of the scaling activity.
        When the total capacity of instances of the scaling group minus instances specified by this interface is smaller than than MinSize, the call fails.

        :type str
        :param scaling_group_id: ID of a scaling group.
        :type list
        :param instance_ids: ID of the ECS instance to be attached to the scaling group after it is enabled.
            At most 20 IDs can be entered.

        :rtype: bool
        :return: The result of deleting scaling group.
        """
        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')

        for i in range(len(instance_ids)):
            if i < 20 and instance_ids[i]:
                self.build_list_params(params, instance_ids[i], 'InstanceId' + bytes(i + 1))

        result = self.get_object('RemoveInstances', params, ResultSet)

        timeout = DefaultTimeOut
        while True:
            instances = self.describe_instances(scaling_group_id=scaling_group_id, instance_ids=instance_ids)
            if not instances:
                return True

            timeout -= 5

            if timeout <= 0:
                raise Exception("Timeout Error: Waiting for removing instances, time-consuming {0} seconds."
                                " Scaling activity ID: {1}.".format(DefaultTimeOut, result.scaling_activity_id))

            time.sleep(5)

        return False

    def describe_instances(self, scaling_group_id=None, scaling_configuration_id=None, instance_ids=None,
                           health_status=None, lifecycle_state=None, creation_type=None, pagenumber=None, pagesize=50):
        """
        Queries the list of ECS instances in a scaling group. 
        You can query by scaling group ID, scaling configuration ID, health status, lifecycle status, and creation type.
        
        :type str
        :param scaling_group_id: ID of a scaling group.
        :type str
        :param scaling_configuration_id: ID of a scaling configuration
        :type list
        :param instance_ids: ID of the ECS instance to be attached to the scaling group after it is enabled.
            At most 20 IDs can be entered.
        :type str
        :param health_status: Health status of an ECS instance in the scaling group. Options: Healthy and Unhealthy.
        :type str
        :param lifecycle_state: Lifecycle status of an ECS instance in the scaling group. Options: 
            - InService: the ECS instance has been added to the scaling group and runs properly. 
            - Pending: the ECS instance is being attached to the scaling group with relevant configurations not completed.
            - Removing: the ECS instance is being removed from the scaling group.
        :type str
        :param creation_type: ECS instance creation type. Options: 
            - AutoCreated: the ECS instance is automatically created by the Auto Scaling service in the scaling group.
            - Attached: the ECS instance is created outside the Auto Scaling service and manually attached to the scaling group.
        :type int
        :param pagenumber: Page number of the scaling group list. The initial value and default value are both 1.
        :type int
        :param pagesize: When querying by page, this parameter indicates the number of lines per page. Maximum value: 50; default value: 10.
        
        :rtype: list
        :return: A list of :class:`footmark.ess.instance`

        """

        instances = []
        params = {}
        if scaling_group_id:
            self.build_list_params(params, scaling_group_id, 'ScalingGroupId')
        if scaling_configuration_id:
            self.build_list_params(params, scaling_configuration_id, 'ScalingConfigurationId')
        if instance_ids:
            for i in range(len(instance_ids)):
                if i < 20 and instance_ids[i]:
                    self.build_list_params(params, instance_ids[i], 'InstanceId' + bytes(i + 1))
        if health_status:
            self.build_list_params(params, health_status, 'HealthStatus')
        if lifecycle_state:
            self.build_list_params(params, lifecycle_state, 'LifecycleState')
        if creation_type:
            self.build_list_params(params, creation_type, 'CreationType')

        self.build_list_params(params, pagesize, 'PageSize')

        pNum = pagenumber
        if not pNum:
            pNum = 1
        while True:
            self.build_list_params(params, pNum, 'PageNumber')
            cfg_list = self.get_list('DescribeScalingInstances', params, ['ScalingInstances', ScalingInstance])
            for cfg in cfg_list:
                instances.append(cfg)
            if pagenumber or len(cfg_list) < pagesize:
                break
            pNum += 1

        return instances

    def create_rule(self, scaling_group_id, adjustment_type, adjustment_value, name=None, cooldown=None):
        """
        A scaling rule defines specific scaling actions, for example, adding or removing n ECS instances.

        If the execution of a scaling rule results in a number of ECS instances in the scaling group that is less than the MinSize or greater than the MaxSize,
        Auto Scaling automatically adjusts the number of ECS instances to be added or removed by executing the “Adjust scaling group instance quantity to MinSize” 
        or “Adjust scaling group instance quantity to MaxSize” rule.

        Example 1: If a scaling group has a MaxSize of 3, the current number of instances (Total Capacity) is 2, 
                   and a scaling rule instructs the system to “add 3 ECS instances”, this operation actually only adds one ECS instance.
                  (The values in the scaling rule are not changed.)
        Example 2: If a scaling group has a MinSize of 2, the current number of instances (Total Capacity) is 3,
                   and a scaling rule instructs the system to “remove 5 ECS instances”, this operation actually only removes one ECS instance.
                   (The values in the scaling rule are not changed.)

        :type str
        :param scaling_group_id: ID of the scaling group of a scaling rule.
        :type str
        :param adjustment_type: Adjustment mode of a scaling rule. Optional values:
            - QuantityChangeInCapacity: It is used to increase or decrease a specified number of ECS instances.
            - PercentChangeInCapacity: It is used to increase or decrease a specified proportion of ECS instances.
            - TotalCapacity: It is used to adjust the quantity of ECS instances in the current scaling group to a specified value.
        :type int
        :param adjustment_value: Adjusted value of a scaling rule. Value range:
            - QuantityChangeInCapacity: (0, 100] U (-100, 0]
            - PercentChangeInCapacity: [0, 10000] U [-10000, 0]
            - TotalCapacity: [0, 100]
        :type str
        :param name: Name shown for the scaling rule, which is a string containing 2 to 40 English or Chinese characters.
                It must begin with a number, a letter (case-insensitive) or a Chinese character and can contain numbers, “_”, “-“ or “.”.
                The account name in the same scaling group is unique in the same region.
                If this parameter value is not specified, the default value is ScalingRuleId.
        :type int
        :param cooldown: Cool-down time of a scaling rule. Value range: [0, 86,400], in seconds. The default value is empty.
        
        :rtype: object
        :return: Returns a <footmark.ess.Rule> object.

        """

        params = {}

        self.build_list_params(params, scaling_group_id, 'ScalingGroupId')
        self.build_list_params(params, adjustment_type, 'AdjustmentType')
        self.build_list_params(params, adjustment_value, 'AdjustmentValue')

        if name:
            self.build_list_params(params, name, 'ScalingRuleName')
        if cooldown is not None:
            self.build_list_params(params, cooldown, 'Cooldown')

        result = self.get_object('CreateScalingRule', params, ResultSet)
        return self.describe_rules(scaling_group_id=scaling_group_id, scaling_rule_ids=[result.scaling_rule_id])[0]

    def describe_rules(self, scaling_group_id=None, scaling_rule_ids=None, scaling_rule_names=None, scaling_rule_aris=None,
                       pagenumber=None, pagesize=50):
        """
        Queries information of a scaling rule. You can query all scaling rules in a scaling group by specifying the scaling group ID.
        
        :type str
        :param scaling_group_id: ID of the scaling group of a scaling configuration.
        :type list
        :param scaling_rule_ids: List ID of a scaling configurations. A maximum of 10 values can be entered.
        :type list
        :param scaling_rule_names: List name of a scaling configurations. A maximum of 10 values can be entered.
        :type list
        :param scaling_rule_aris: Unique identifier of a scaling rule. A maximum of 10 values can be entered.
        :type int
        :param pagenumber: Page number of the scaling rule list. The initial value and default value are both 1.
        :type int
        :param pagesize: When querying by page, this parameter indicates the number of lines per page. Maximum value: 50;
            default value: 50.
        
        :rtype: list
        :return: A list of  :class:`footmark.ess.rule`
    
        """

        rules = []
        params = {}
        if scaling_group_id:
            self.build_list_params(params, scaling_group_id, 'ScalingGroupId')
        if scaling_rule_ids:
            for i in range(len(scaling_rule_ids)):
                if i < 10 and scaling_rule_ids[i]:
                    self.build_list_params(params, scaling_rule_ids[i], 'ScalingRuleId'+ bytes(i+1))
        if scaling_rule_names:
            for i in range(len(scaling_rule_names)):
                if i < 10 and scaling_rule_names[i]:
                    self.build_list_params(params, scaling_rule_names[i], 'ScalingRuleName'+bytes(i+1))
        if scaling_rule_aris:
            for i in range(len(scaling_rule_aris)):
                if i < 10 and scaling_rule_aris[i]:
                    self.build_list_params(params, scaling_rule_aris[i], 'ScalingRuleAri'+bytes(i+1))

        self.build_list_params(params, pagesize, 'PageSize')

        pNum = pagenumber
        if not pNum:
            pNum = 1
        while True:
            self.build_list_params(params, pNum, 'PageNumber')
            rule_list = self.get_list('DescribeScalingRules', params, ['ScalingRules', ScalingRule])
            # API DescribeScalingRules has not 'ScalingRules' when there is no any rule.
            if not isinstance(rule_list, list):
                return rules

            for rule in rule_list:
                rules.append(rule)
            if pagenumber or len(rule_list) < pagesize:
                break
            pNum += 1

        return rules

    def modify_rule(self, scaling_rule_id, adjustment_type=None, adjustment_value=None, name=None, cooldown=None):
        """
        Modifies the attributes of a scaling rule.

        :type str
        :param scaling_rule_id: ID of a scaling rule.
        :type str
        :param adjustment_type: Adjustment mode of a scaling rule. Optional values:
            - QuantityChangeInCapacity: It is used to increase or decrease a specified number of ECS instances.
            - PercentChangeInCapacity: It is used to increase or decrease a specified proportion of ECS instances.
            - TotalCapacity: It is used to adjust the quantity of ECS instances in the current scaling group to a specified value.
        :type int
        :param adjustment_value: Adjusted value of a scaling rule. Value range:
            - QuantityChangeInCapacity: (0, 100] U (-100, 0]
            - PercentChangeInCapacity: [0, 10000] U [-10000, 0]
            - TotalCapacity: [0, 100]
        :type str
        :param name: Name shown for the scaling rule, which is a string containing 2 to 40 English or Chinese characters.
                It must begin with a number, a letter (case-insensitive) or a Chinese character and can contain numbers, “_”, “-“ or “.”.
                The account name in the same scaling group is unique in the same region.
                If this parameter value is not specified, the default value is ScalingRuleId.
        :type int
        :param cooldown: Cool-down time of a scaling rule. Value range: [0, 86,400], in seconds. The default value is empty.
        
        :rtype: bool
        :return: The result of modifying.

        """

        params = {}

        self.build_list_params(params, scaling_rule_id, 'ScalingRuleId')

        if adjustment_type:
            self.build_list_params(params, adjustment_type, 'AdjustmentType')

        if adjustment_value is not None:
            self.build_list_params(params, adjustment_value, 'AdjustmentValue')

        if name:
            self.build_list_params(params, name, 'ScalingRuleName')
        if cooldown is not None:
            self.build_list_params(params, cooldown, 'Cooldown')

        return self.get_status('ModifyScalingRule', params)

    def terminate_rule(self, scaling_rule_id):
        """
        Deletes a specified scaling rule.

        :type str
        :param scaling_rule_id: ID of a scaling rule.
        
        :rtype: bool
        :return: The result of deleting.

        """

        params = {}

        self.build_list_params(params, scaling_rule_id, 'ScalingRuleId')

        return self.get_status('DeleteScalingRule', params)

    def create_scheduled_task(self, scaling_rule_ari, launch_time, name=None, description=None, launch_expiration_time=None,
                              recurrence_type=None, recurrence_value=None, recurrence_end_time=None, task_enabled=None):
        """
        This operation creates a scheduled task according to input parameters.

        You can create up to 20 scheduled tasks.
        
        When the trigger of a scheduled task fails because a scaling activity in a scaling group is in progress or the scaling group is disabled, 
        the scheduled task is automatically retried within the LaunchExpirationTime; otherwise, the scheduled trigger task is abandoned.
        
        If multiple tasks are scheduled at similar times to execute the rule of the same group, the earliest task triggers the scaling activity first, 
        and other tasks make attempts to execute the rule within their Launch Expiration Time because a scaling group executes only one scaling activity at a time. 
        If another scheduled task is still making triggering attempts within its Launch Expiration Time after the scaling activity is finished, 
        the scaling rule is executed and the corresponding scaling activity is triggered.

        :type str
        :param scaling_rule_ari: The unique identifier of the scaling rule.
        :type str
        :param launch_time: Time point at which the scheduled task is triggered.
            The date format follows the ISO8601 standard and uses UTC time. It is in the format of YYYY-MM-DDThh:mmZ.
            If RecurrenceType is specified, the time point specified by this attribute is the default time point at which the circle is executed. 
            If RecurrenceType is not specified, the task is executed once on the designated date and time.
            A time point 90 days after creation or modification cannot be entered.
        :type str
        :param name: Display name of the scheduled task, which must be 2-40 characters (English or Chinese) long. 
            It must begin with a number, an upper/lower-case letter or a Chinese character and may contain numbers, “_”, “-“ or “.”.
            The account name is unique in the same region.
            If this parameter is not specified, the default value ScheduledScalingTaskId is used.
        :type str
        :param description: Description of the scheduled task, which is 2-200 characters (English or Chinese) long.
        :type int
        :param launch_expiration_time: Time period within which the failed scheduled task is retried. The default value is 600s. Value range: [0, 21600]
        :type str
        :param recurrence_type: Type of the scheduled task to be repeated. Optional values:
            - Daily: Recurrence interval by day for a scheduled task.
            - Weekly: Recurrence interval by week for a scheduled task.
            - Monthly: Recurrence interval by month for a scheduled task.
            RecurrenceType, RecurrenceValue and RecurrenceEndTime must be specified at the same time.
        :type str
        :param recurrence_value: Value of the scheduled task to be repeated.
            - Daily: Only one value in the range [1,31] can be filled.
            - Weekly: Multiple values can be filled. The values of Sunday to Saturday are 0 to 6 in sequence. Multiple values shall be separated by a comma “,”.
            - Monthly: In the format of A-B. The value range of A and B is 1 to 31, and the B value must be greater than the A value.
            RecurrenceType, RecurrenceValue and RecurrenceEndTime must be specified at the same tiem.
        :type str
        :param recurrence_end_time: End time of the scheduled task to be repeated.
            The date format follows the ISO8601 standard and uses UTC time. It is in the format of YYYY-MM-DDThh:mmZ.
            A time point 90 days after creation or modification cannot be entered.
            RecurrenceType, RecurrenceValue and RecurrenceEndTime must be specified at the same time.
        :type bool
        :param task_enabled: Whether to enable the scheduled task.
            - When the parameter is set to true, the task is enabled.
            - When the parameter is set to false, the task is disabled.
            The default value is true.
        
        :rtype: object
        :return: Returns a <footmark.ess.ScheduledTask> object.

        """

        params = {}

        self.build_list_params(params, scaling_rule_ari, 'ScheduledAction')
        self.build_list_params(params, launch_time, 'LaunchTime')

        if name:
            self.build_list_params(params, name, 'ScheduledTaskName')
        if description:
            self.build_list_params(params, description, 'Description')
        if launch_expiration_time is not None:
            self.build_list_params(params, launch_expiration_time, 'LaunchExpirationTime')
        if recurrence_type:
            self.build_list_params(params, recurrence_type, 'RecurrenceType')
        if recurrence_value:
            self.build_list_params(params, recurrence_value, 'RecurrenceValue')
        if recurrence_end_time:
            self.build_list_params(params, recurrence_end_time, 'RecurrenceEndTime')
        if task_enabled is True or task_enabled is None:
            self.build_list_params(params, True, 'TaskEnabled')

        result = self.get_object('CreateScheduledTask', params, ResultSet)
        return self.describe_scheduled_tasks(scheduled_task_ids=[result.scheduled_task_id])[0]

    def describe_scheduled_tasks(self, scheduled_task_ids=None, scheduled_task_names=None, scaling_rule_aris=None,
                                 pagenumber=None, pagesize=50):
        """
        Queries information of a scheduled task.

        You can use the Scaling Rule Ari to query the relevant scheduled task.
        
        :type list
        :parameter scheduled_task_ids: ID of the scheduled task. You can enter at most 20 IDs.
        :type list
        :parameter scheduled_task_names: Display name of the schedules task. You can enter at most 20 display names.
        :type list
        :parameter scaling_rule_aris: Unique identifier of a scaling rule. A maximum of 20 values can be entered.
        :type int
        :parameter pagenumber: Page number of the scaling scheduled task list. The initial value and default value are both 1.
        :type int
        :parameter pagesize: When querying by page, this parameter indicates the number of lines per page. Maximum value: 50; default value: 50.
        
        :rtype: list
        :return: A list of  :class:`footmark.ess.ScheduledTask`
    
        """

        tasks = []
        params = {}

        if scheduled_task_ids:
            for i in range(len(scheduled_task_ids)):
                if i < 20 and scheduled_task_ids[i]:
                    self.build_list_params(params, scheduled_task_ids[i], 'ScheduledTaskId'+ bytes(i+1))
        if scheduled_task_names:
            for i in range(len(scheduled_task_names)):
                if i < 20 and scheduled_task_names[i]:
                    self.build_list_params(params, scheduled_task_names[i], 'ScheduledTaskName'+ bytes(i+1))
        if scaling_rule_aris:
            for i in range(len(scaling_rule_aris)):
                if i < 10 and scaling_rule_aris[i]:
                    self.build_list_params(params, scaling_rule_aris[i], 'ScheduledAction'+ bytes(i+1))

        self.build_list_params(params, pagesize, 'PageSize')

        pNum = pagenumber
        if not pNum:
            pNum = 1
        while True:
            self.build_list_params(params, pNum, 'PageNumber')
            task_list = self.get_list('DescribeScheduledTasks', params, ['ScheduledTasks', ScheduledTask])

            for rule in task_list:
                tasks.append(rule)
            if pagenumber or len(task_list) < pagesize:
                break
            pNum += 1

        return tasks

    def modify_scheduled_task(self, scheduled_task_id, scaling_rule_ari=None, launch_time=None, name=None, description=None,
                              launch_expiration_time=None, recurrence_type=None, recurrence_value=None, recurrence_end_time=None, task_enabled=None):
        """
        Modifies the attributes of a scheduled task.

        :type str
        :param scheduled_task_id: ID of the scheduled task.
        :type str
        :param scaling_rule_ari: The unique identifier of the scaling rule.
        :type str
        :param launch_time: Time point at which the scheduled task is triggered.
            The date format follows the ISO8601 standard and uses UTC time. It is in the format of YYYY-MM-DDThh:mmZ.
            If RecurrenceType is specified, the time point specified by this attribute is the default time point at which the circle is executed. 
            If RecurrenceType is not specified, the task is executed once on the designated date and time.
            A time point 90 days after creation or modification cannot be entered.
        :type str
        :param name: Display name of the scheduled task, which must be 2-40 characters (English or Chinese) long. 
            It must begin with a number, an upper/lower-case letter or a Chinese character and may contain numbers, “_”, “-“ or “.”.
            The account name is unique in the same region.
            If this parameter is not specified, the default value ScheduledScalingTaskId is used.
        :type str
        :param description: Description of the scheduled task, which is 2-200 characters (English or Chinese) long.
        :type int
        :param launch_expiration_time: Time period within which the failed scheduled task is retried. The default value is 600s. Value range: [0, 21600]
        :type str
        :param recurrence_type: Type of the scheduled task to be repeated. Optional values:
            - Daily: Recurrence interval by day for a scheduled task.
            - Weekly: Recurrence interval by week for a scheduled task.
            - Monthly: Recurrence interval by month for a scheduled task.
            RecurrenceType, RecurrenceValue and RecurrenceEndTime must be specified at the same time.
        :type str
        :param recurrence_value: Value of the scheduled task to be repeated.
            - Daily: Only one value in the range [1,31] can be filled.
            - Weekly: Multiple values can be filled. The values of Sunday to Saturday are 0 to 6 in sequence. Multiple values shall be separated by a comma “,”.
            - Monthly: In the format of A-B. The value range of A and B is 1 to 31, and the B value must be greater than the A value.
            RecurrenceType, RecurrenceValue and RecurrenceEndTime must be specified at the same tiem.
        :type str
        :param recurrence_end_time: End time of the scheduled task to be repeated.
            The date format follows the ISO8601 standard and uses UTC time. It is in the format of YYYY-MM-DDThh:mmZ.
            A time point 90 days after creation or modification cannot be entered.
            RecurrenceType, RecurrenceValue and RecurrenceEndTime must be specified at the same time.
        :type bool
        :param task_enabled: Whether to enable the scheduled task.
            - When the parameter is set to true, the task is enabled.
            - When the parameter is set to false, the task is disabled.
            The default value is true.
        
        :rtype: object
        :return: Returns a <footmark.ess.ScheduledTask> object.

        """

        params = {}

        self.build_list_params(params, scheduled_task_id, 'ScheduledTaskId')
        if scaling_rule_ari:
            self.build_list_params(params, scaling_rule_ari, 'ScalingRuleAri')
        if launch_time:
            self.build_list_params(params, launch_time, 'LaunchTime')
        if name:
            self.build_list_params(params, name, 'ScheduledTaskName')
        if description:
            self.build_list_params(params, description, 'Description')
        if launch_expiration_time is not None:
            self.build_list_params(params, launch_expiration_time, 'LaunchExpirationTime')
        if recurrence_type:
            self.build_list_params(params, recurrence_type, 'RecurrenceType')
        if recurrence_value:
            self.build_list_params(params, recurrence_value, 'RecurrenceValue')
        if recurrence_end_time:
            self.build_list_params(params, recurrence_end_time, 'RecurrenceEndTime')
        if task_enabled is True or task_enabled is None:
            self.build_list_params(params, True, 'TaskEnabled')

        return self.get_status('ModifyScheduledTask', params)

    def terminate_scheduled_task(self, scheduled_task_id):
        """
        Deletes a specified scheduled task.

        :type str
        :param scheduled_task_id: ID of the scheduled task.
        
        :rtype: bool
        :return: The result of deleting.

        """

        params = {}

        self.build_list_params(params, scheduled_task_id, 'ScheduledTaskId')

        return self.get_status('DeleteScheduledTask', params)

    def wait_for_instances_status(self, scaling_group_id, instance_ids, status, activity_id=None, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        """
        To verify instances status has become expected after attaching or detaching instances
        """
        tm = timeout
        try:
            while True:
                instances = self.describe_instances(scaling_group_id=scaling_group_id, instance_ids=instance_ids)
                success = 0
                for inst in instances:
                    if str(inst.status).lower() == str.lower(status):
                        success += 1

                if success == len(instance_ids):
                    return True

                tm -= delay

                if tm <= 0:
                    raise Exception("Timeout Error: Waiting for scaling instances status is %s, time-consuming {0} seconds."
                                    " Scaling activity ID: {1}.".format(DefaultTimeOut, activity_id))

                time.sleep(delay)

            return False
        except Exception as e:
            raise e