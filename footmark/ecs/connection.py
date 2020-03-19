# encoding: utf-8
"""
Represents a connection to the ECS service.
"""

import warnings

import six
import time
import json
import base64
from footmark.ecs.config import *
from footmark.connection import ACSQueryConnection
from footmark.ecs.zone import Zone
from footmark.ecs.instance_type import InstanceType, InstanceTypeFamily
from footmark.ecs.regioninfo import RegionInfo
from footmark.ecs.instance import Instance
from footmark.ecs.image import Image
from footmark.ecs.securitygroup import SecurityGroup
from footmark.ecs.volume import Disk
from footmark.ecs.networkinterface import NetworkInterfaceSet
from footmark.exception import ECSResponseError
from footmark.resultset import ResultSet
from aliyunsdkcore.acs_exception.exceptions import ServerException
# from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import Request import
# from aliyunsdkcore.auth.composer.rpc_signature_composer import ServerException


class ECSConnection(ACSQueryConnection):
    SDKVersion = '2014-05-26'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = ECSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, ecs_role_name=None, user_agent=None):
        """
        Init method to create a new connection to ECS.
        """
        if not region:
            # region = RegionInfo(self, self.DefaultRegionName,
            #                     self.DefaultRegionId)
            region = self.DefaultRegionId
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.ECSSDK = 'aliyunsdkecs.request.v' + self.SDKVersion.replace('-', '')

        super(ECSConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            region=self.region, product=self.ECSSDK,
                                            security_token=security_token, user_agent=user_agent,
                                            ecs_role_name=ecs_role_name)

    def build_filter_params(self, params, filters):
        if not isinstance(filters, dict):
            return

        flag = 1
        for key, value in list(filters.items()):
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
            for key, value in list(tags.items()):
                if tag_no > max_tag_number:
                    break
                if key:
                    self.build_list_params(params, key, 'Tag' + str(tag_no) + 'Key')
                    self.build_list_params(params, value, 'Tag' + str(tag_no) + 'Value')
                    tag_no += 1

    def create_instances(self, **kwargs):
        """
        create an instance in ecs

        :type image_id: string
        :param image_id: ID of an image file, indicating an image selected
            when an instance is started

        :type instance_type: string
        :param instance_type: Type of the instance

        :type group_id: string
        :param group_id: ID of the security group to which a newly created
            instance belongs

        :type zone_id: string
        :param zone_id: ID of a zone to which an instance belongs. If it is
            null, a zone is selected by the system

        :type instance_name: string
        :param instance_name: Display name of the instance, which is a string
            of 2 to 128 Chinese or English characters. It must begin with an
            uppercase/lowercase letter or a Chinese character and can contain
            numerals, “.”, “_“, or “-“.

        :type description: string
        :param description: Description of the instance, which is a string of
            2 to 256 characters.

        :type internet_data: list
        :param internet_data: It includes Internet charge type which can be
            PayByTraffic or PayByBandwidth, max_bandwidth_in and max_bandwidth_out

        :type host_name: string
        :param host_name: Host name of the ECS, which is a string of at least
            two characters. “hostname” cannot start or end with “.” or “-“.
            In addition, two or more consecutive “.” or “-“ symbols are not
            allowed.

        :type password: string
        :param password: Password to an instance is a string of 8 to 30
            characters

        :type io_optimized: string
        :param io_optimized: values are (1) none: none I/O Optimized
            (2) optimized: I/O Optimized

        :type system_disk: list
        :param system_disk: It includes disk_category, disk_size,
            disk_name and disk_description

        :type disks: list
        :param disks: It includes device_category, device_size,
            device_name, device_description, delete_on_termination
            and snapshot

        :type vswitch_id: string
        :param vswitch_id: When launching an instance in VPC, the
            virtual switch ID must be specified

        :type private_ip: string
        :param private_ip: Private IP address of the instance, which cannot be specified separately.

        :type count: integer
        :param count: Create No. of Instances

        :type allocate_public_ip: bool
        :param allocate_public_ip: Allocate Public IP Address to Instance

        :type bind_eip: string
        :param bind_eip: Bind Elastic IP Address

        :type instance_charge_type: string
        :param instance_charge_type: instance charge type

        :type: period: integer
        :param period: The time that you have bought the resource,
            in month. Only valid when InstanceChargeType is set as
            PrePaid. Value range: 1 to 12

        :type: auto_renew: bool
        :param auto_renew: Whether automatic renewal is supported.
            Only valid when InstanceChargeType is set PrePaid. Value
            range True: indicates to automatically renew
                  False，indicates not to automatically renew
            Default value: False.

        :type: auto_renew_period: int
        :param auto_renew_period: The period of each automatic renewal. Required when AutoRenew is True.
        The value must be the same as the period of the created instance.

        :type: ids: list
        :param ids: A list of identifier for this instance or set of
            instances, so that the module will be idempotent with
            respect to ECS instances.

        :type instance_tags: list
        :param instance_tags: A list of hash/dictionaries of instance
            tags, '[{tag_key:"value", tag_value:"value"}]', tag_key
            must be not null when tag_value isn't null

        :type wait: string
        :param wait: after execution of method whether it has to wait for some time interval

        :type wait_timeout: int
        :param wait_timeout: time interval of waiting

        :rtype: dict
        :return: Returns a dictionary of instance information about
            the instances started/stopped. If the instance was not
            able to change state, "changed" will be set to False.
            Note that if instance_ids and instance_tags are both non-
            empty, this method will process the intersection of the two

        """

        instance_ids = []
        count = kwargs["count"]
        kwargs = self.format_request_kwargs(**kwargs)
        if not count:
            count = 1
        for i in range(count):
            # CreateInstance method call, returns newly created instanceId
            client_token = kwargs["client_token"]
            if count > 1:
                client_token = "{0}-{1}".format(i, client_token)
            if len(client_token) > 64:
                client_token = client_token[0:64]
            kwargs["client_token"] = client_token
            instance_ids.append(self.get_object_new(self.build_request_params(kwargs), ResultSet).instance_id)

        transition = [].extend(instance_ids)
        while transition:
            for inst in self.describe_instances(instance_ids=transition, page_size=100):
                if str(inst.status).lower() == 'stopped':
                    transition.remove(inst.id)
        # There need sleep 10s to wait instance to finish initiated.
        if instance_ids:
            time.sleep(10)

        return self.describe_instances(instance_ids=instance_ids, page_size=100)

    def run_instances(self, **kwargs):
        kwargs = self.format_request_kwargs(**kwargs)
        client_token = kwargs["client_token"]
        if len(client_token) > 64:
            client_token = client_token[0:64]
        kwargs["client_token"] = client_token
        instance_ids = self.get_object_new(self.build_request_params(kwargs), ResultSet).instance_id_sets['instance_id_set']
        if instance_ids:
            time.sleep(10)

        transition = [].extend(instance_ids)
        while transition:
            for inst in self.describe_instances(instance_ids=transition, page_size=100):
                if str(inst.status).lower() == 'running':
                    transition.remove(inst.id)

        return self.describe_instances(instance_ids=instance_ids, page_size=100)

    # Instance methods
    def get_all_instances(self, **kwargs):
    # def get_all_instances(self, zone_id=None, instance_ids=None, instance_name=None, instance_tags=None,
    #                       vpc_id=None, vswitch_id=None, instance_type=None, instance_type_family=None,
    #                       instance_network_type=None, private_ip_addresses=None, inner_ip_addresses=None,
    #                       public_ip_addresses=None, security_group_id=None, instance_charge_type=None,
    #                       spot_strategy=None, internet_charge_type=None, image_id=None, status=None,
    #                       io_optimized=None, pagenumber=None, pagesize=100):
        """
        Retrieve all the instance associated with your account. 

        :rtype: list
        :return: A list of  :class:`footmark.ecs.instance`

        """
        instances = []
        params = {}
        for key, value in list(kwargs.items()):
            if key == "instance_ids":
                value = "[" + str(",").join(value) + "]"
                kwargs[key] = value
            if key == "tags":
                tags = []
                if isinstance(value, dict):
                    for k, v in list(value.items()):
                        tags.append({"Key": k, "Value": v})
                kwargs[key] = value
            kwargs['Action'] = 'DescribeInstances'
            for inst in self.get_list_new(self.build_request_params(filters), ['Instances', Instance]):
                filters = {}
                filters['instance_id'] = inst.id
                volumes = self.get_all_volumes(filters)
                setattr(inst, 'block_device_mapping', volumes)
                # if inst.security_group_ids:
                #     group_ids = []
                #     security_groups = []
                #     for sg_id in inst.security_group_ids['security_group_id']:
                #         group_ids.append(str(sg_id))
                #         security_groups.append(self.get_security_group_attribute(sg_id))
                #     setattr(inst, 'security_groups', security_groups)
                instances.append(inst)
        return instances

    def describe_instances(self, **kwargs):
        """
        Retrieve all the instance associated with your account.

        :rtype: list
        :return: A list of  :class:`footmark.ecs.instance`

        """
        pagenumber = 1
        instances = []
        page_size = kwargs['page_size'] if 'page_size' in kwargs else 10

        while True:
            kwargs['pagenumber'] = pagenumber
            inst_list = self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Instances', Instance])
            for inst in inst_list:
                instances.append(inst)
            if len(inst_list) < page_size:
                break
            pagenumber += 1
        return instances

    def start_instances(self, **kwargs):
        """
        Start the instances specified

        :type instance_ids: list
        :param instance_ids: A list of strings of the Instance IDs to start

        :rtype: list
        :return: A list of the instances started
        """
        instance_ids = kwargs["instance_ids"]
        kwargs = self.format_request_kwargs(**kwargs)
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                kwargs["instance_id"] = instance_id
                try:
                    self.get_status_new(self.build_request_params(kwargs))
                except ServerException as e:
                    if e.error_code == "IncorrectInstanceStatus":
                        target = self.describe_instances(instance_ids=[instance_id])
                        if target and str(target[0].status).lower() == "running":
                            continue
                    raise e
            while instance_ids:
                for inst in self.describe_instances(instance_ids=instance_ids, page_size=100):
                    if str(inst.status).lower() == "running":
                        instance_ids.remove(inst.id)
            return True
        return False

    def stop_instances(self, **kwargs):
        """
        Stop the instances specified

        :type instance_ids: list
        :param instance_ids: A list of strings of the Instance IDs to stop

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: list
        :return: A list of the instances stopped
        """
        instance_ids = kwargs["instance_ids"]
        kwargs = self.format_request_kwargs(**kwargs)
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                kwargs["instance_id"]= instance_id
                try:
                    self.get_status_new(self.build_request_params(kwargs))
                except ServerException as e:
                    if e.error_code == "IncorrectInstanceStatus":
                        target = self.describe_instances(instance_ids=[instance_id])
                        if target and str(target[0].status).lower() == "stopped":
                            continue
                    raise e
            while instance_ids:
                for inst in self.describe_instances(instance_ids=instance_ids, page_size=100):
                    if str(inst.status).lower() == "stopped":
                        instance_ids.remove(inst.id)
            return True
        return False

    def reboot_instances(self, **kwargs):
        """
        Reboot the specified instances.

        :type instance_ids: list
        :param instance_ids: The instances to terminate and reboot

        :type force: bool
        :param force: Forces the instance to stop

        """
        instance_ids = kwargs["instance_ids"]
        kwargs = self.format_request_kwargs(**kwargs)
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                kwargs["instance_id"]= instance_id
                try:
                    self.get_status_new(self.build_request_params(kwargs))
                except ServerException as e:
                    if e.error_code == "IncorrectInstanceStatus":
                        target = self.describe_instances(instance_ids=[instance_id])
                        if target and str(target[0].status).lower() == "stopped":
                            self.start_instances(instance_ids=[instance_id])
                    raise e
            while instance_ids:
                for inst in self.describe_instances(instance_ids=instance_ids, page_size=100):
                    status = str(inst.status).lower()
                    if status == "running":
                        instance_ids.remove(inst.id)
                    if status == "stopped":
                        self.start_instances(instance_ids=[inst.id])
            return True
        return False

    def delete_instances(self, **kwargs):
        """
        Delete the instances specified

        :type instance_ids: list
        :param instance_ids: A list of strings of the Instance IDs to terminate

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: list
        :return: A list of the instance_ids terminated
        """
        instance_ids = kwargs["instance_ids"]
        kwargs = self.format_request_kwargs(**kwargs)
        if instance_ids:
            if isinstance(instance_ids, six.string_types):
                instance_ids = [instance_ids]
            for instance_id in instance_ids:
                kwargs["instance_id"]= instance_id
                self.get_status_new(self.build_request_params(kwargs))
            while instance_ids:
                if self.describe_instances(instance_ids=instance_ids):
                    continue
                break
            return True
        return False

    def allocate_public_ip_address(self, **kwargs):
        timeout = 30
        while timeout:
            try:
                return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
            except ServerException as e:
                if e.error_code == "IncorrectInstanceStatus":
                    time.sleep(3)
                    timeout -= 3
        return False

    def describe_instance_types(self, instance_type_family=None):
        """
        Retrieve all the instance types associated with your account.

        :type instance_type_family: str
        :param instance_type_family: Family name of instance type

        :rtype: list
        :return: A list of  :class:`footmark.ecs.instance_type`

        """
        params = {}

        if instance_type_family:
            self.build_list_params(params, instance_type_family, 'InstanceTypeFamily')
        return self.get_list('DescribeInstanceTypes', params, ['InstanceTypes', InstanceType])

    def describe_zones(self, zone_id=None):
        """
            Retrieve all zones in the region.

            :type zone_id: str
            :param zone_id: Filter the zone which id is equal to zone_id

            :rtype: list
            :return: A list of  :class:`footmark.ecs.zone`

        """
        params = {}
        self.build_list_params(params, self.region, 'RegionId')
        zones = self.get_list('DescribeZones', params, ['Zones', Zone])
        if zone_id:
            zones = [zone for zone in zones if zone.id == zone_id]
        return zones

    def describe_instance_type_families(self, generation=None):
        """
            Retrieve all the instance type families associated with your account.

            :type generation: str
            :param generation: Filter the families by generation

            :rtype: list
            :return: A list of  :class:`footmark.ecs.instance_type_family`

        """
        params = {}
        self.build_list_params(params, self.region, 'RegionId')
        if generation:
            self.build_list_params(params, generation, "Generation")
        return self.get_list('DescribeInstanceTypeFamilies', params, ['InstanceTypeFamilies', InstanceTypeFamily])

    def describe_disks(self, **kwargs):
        pagenumber = 1
        disks = []
        page_size = kwargs['page_size'] if 'page_size' in kwargs else 10

        while True:
            kwargs['page_number'] = pagenumber
            disk_list = self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Disks', Disk])
            for inst in disk_list:
                disks.append(inst)
            if len(disk_list) < page_size:
                break
            pagenumber += 1
        return disks

    def get_all_volumes(self, zone_id=None, volume_ids=None, volume_name=None, filters=None):
        """
        Get all Volumes associated with the current credentials.

        :type volume_ids: list
        :param volume_ids: Optional list of volume ids.  If this list
                           is present, only the volumes associated with
                           these volume ids will be returned.

        :type filters: dict
        :param filters: Optional filters that can be used to limit
                        the results returned.  Filters are provided
                        in the form of a dictionary consisting of
                        filter names as the key and filter values
                        as the value.  The set of allowable filter
                        names/values is dependent on the request
                        being performed.  Check the ECS API guide
                        for details.

        :type dry_run: bool
        :param dry_run: Set to True if the operation should not actually run.

        :rtype: list of Volume
        :return: The requested Volume objects
        """
        params = {}
        if zone_id:
            self.build_list_params(params, zone_id, 'ZoneId')
        if volume_ids:
            ids = "["
            for id in volume_ids:
                ids += "\"" + str(id) + "\""
            ids += "]"
            self.build_list_params(params, ids, 'DiskIds')
        if volume_name:
            self.build_list_params(params, volume_name, 'DiskName')
        if filters:
            self.build_filter_params(params, filters)
        return self.get_list('DescribeDisks', params, ['Disks', Disk])

    def attach_key_pair(self, **kwargs):
        """
        Attach a key pair to a ecs instance

        :type instance_ids: list
        :param instance_ids: List of the instance ids

        :type key_pair_name: str
        :param key_pair_name: Name of Key Pair which is used to attach

        :return:
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def detach_key_pair(self, **kwargs):
        """
        Attach a key pair to a ecs instance

        :type instance_ids: list
        :param instance_ids: List of the instance ids

        :type key_pair_name: str
        :param key_pair_name: Name of Key Pair which is used to be detached

        :return:
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def modify_instance_charge_type(self, **kwargs):
        delay = 300
        timeout = DefaultTimeOut

        while True:
            try:
                return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
            except ServerException as e:
                if e.error_code == "Throttling":
                    time.sleep(delay)
                    timeout -= delay
                else:
                    raise e
            if timeout <= 0:
                raise Exception("Retry time out when error_code is 'Throttling' ")

    def modify_instance_attribute(self, **kwargs):
        """
        modify the instance attributes such as name, description, password and host_name

        :type instance_ids: list
        :param instance_ids: The list of Instance ID
        :type name: str
        :param name: Instance Name
        :type description: str
        :param description: Instance Description
        :type host_name: str
        :param host_name: Instance Host Name
        :type password: str
        :param password: Instance Password
        :return: A list of the instance_ids modified
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def get_instance_status(self, zone_id=None, pagenumber=None, pagesize=None):
        """
        Get status of instance

        :type zone_id: string
        :param zone_id: Optional parameter. ID of the zone to which an instance belongs

        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1

        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10

        :rtype: json
        :return: The result of passed instances
        """

        params = {}
        results = []

        if zone_id:
            self.build_list_params(params, zone_id, 'ZoneId')
        if pagenumber:
            self.build_list_params(params, pagenumber, 'PageNumber')
        if pagesize:
            self.build_list_params(params, pagesize, 'PageSize')

        try:
            results = self.get_object('DescribeInstanceStatus', params, ResultSet)
        except ServerException as e:
            results.append({"Error Code": e.error_code, "Error Message": e.message,
                            "RequestId": e.request_id, "Http Status": e.http_status})
        except Exception as e:
            results.append({"Error": e})

        return False, results

    def join_security_group(self, **kwargs):
        """
        Assign an existing instance to a pre existing security group

        :type instance_id: str
        :param instance_id: The instance id which are to be assigned to the security group

        :type group_id: dict
        :param group_id: ID of the security group to which a instance is to be added

        :return: Success message, confirming joining security group or error message if any
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def leave_security_group(self, **kwargs):
        """
        Remove an existing instance from given security group

        :type instance_id: str
        :param instance_id: The instance id which are to be assigned to the security group

        :type group_id: dict
        :param group_id: ID of the security group to which a instance is to be added

        :return: Success message, confirming joining security group or error message if any
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    # def create_security_group(self, **kwargs):
    def create_security_group(self, **kwargs):
        """
        create and authorize security group in ecs

        :type group_name: string
        :param group_name: Name of the security group

        :type description: string
        :param description: Description of the security group

        :type group_tags: list
        :param group_tags: A list of hash/dictionaries of disk
            tags, '[{tag_key:"value", tag_value:"value"}]', tag_key
            must be not null when tag_value isn't null

        :type vpc_id: string
        :param vpc_id: The ID of the VPC to which the security group belongs

        :rtype: dict
        :return: Returns a dictionary of group information about
            the the group created/authorized. If the group was not
            created and authorized, "changed" will be set to False.
        """
        response = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet)
        if response:
            return self.describe_security_group_attribute(security_group_id=response.security_group_id)

        return None

    def modify_security_group_attribute(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def authorize_security_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def authorize_security_group_egress(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def revoke_security_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def revoke_security_group_egress(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def describe_security_group_attribute(self, **kwargs):
        """
        Querying Security Group List returns the basic information about all
              user-defined security groups.

        :type  group_id: String
        :param group_id: ID of security groups id

        :type nic_type: String
        :param nic_type: Network type of security group. The choice value is 'internet' or 'intranet'.

        :type direction: String
        :param direction: The direction of security group rule. The choice value is 'egress', 'ingress' or 'all', and 'all' is default.

        :rtype: dict
        :return: Returns a dictionary of security group information

        """
        try:
            return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), SecurityGroup)
        except ServerException as e:
            if str(e.error_code) == "InvalidSecurityGroupId.NotFound":
                return None
            raise e

    def describe_security_groups(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['SecurityGroups', SecurityGroup])


    def delete_security_group(self, **kwargs):
        """
        Delete Security Group , delete security group inside particular region.

        :type  group_id: str
        :param group_id: The Security Group ID

        :rtype: bool
        :return: A method return result of after successfully deletion of security group
        """
        # Call DescribeSecurityGroups method to get response for all running instances
        kwargs = self.format_request_kwargs(**kwargs)
        delay = 5
        timeout = DefaultTimeOut
        while True:
            try:
                self.get_status_new(self.build_request_params(kwargs))
                group = self.describe_security_group_attribute(**kwargs)
                if not group or not group.id:
                    return True
            except ServerException as e:
                if str(e.error_code) == "InvalidSecurityGroupId.NotFound":
                    return True
                elif str(e.error_code) == "DependencyViolation":
                    pass

            time.sleep(delay)
            timeout -= delay
            if timeout <= 0:
                raise Exception("Timeout: Waiting for deleting Security Group {0}, time-consuming {1} seconds. "
                                "Error: {2}".format(kwargs["security_group_id"], DefaultTimeOut-timeout, e))

    def create_disk(self, **kwargs):
        """
        create an disk in ecs

        :type zone_id: string
        :param zone_id: ID of a zone to which an instance belongs.

        :type disk_name: string
        :param disk_name: Display name of the disk, which is a string
            of 2 to 128 Chinese or English characters.

        :type description: string
        :param description: Description of the disk, which is a string of
            2 to 256 characters.

        :type disk_category: string
        :param disk_category: Displays category of the data disk
                Optional values are:
                Cloud - general cloud disk
                cloud_efficiency - efficiency cloud disk
                cloud_ssd - cloud SSD
                Default value:cloud

        :type size: integer
        :param size: Size of the system disk, in GB, values range:
                Cloud - 5 ~ 2000
                cloud_efficiency - 20 ~ 2048
                cloud_ssd - 20 ~ 2048
                The value should be equal to or greater than the size of the specific SnapshotId.

        :type disk_tags: list
        :param disk_tags: A list of hash/dictionaries of instance
            tags, '[{tag_key:"value", tag_value:"value"}]', tag_key
            must be not null when tag_value isn't null        

        :type snapshot_id: integer
        :param snapshot_id: Snapshots are used to create the data disk
            After this parameter is specified, Size is ignored.

        :rtype: dict
        :return: Returns a dictionary of disk information
        """
        return self.describe_disk_attribute(disk_id=self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet).disk_id)

    def describe_disk_attribute(self, disk_id):
        disks = self.describe_disks(disk_ids=[disk_id])
        if disks:
            return disks[0]
        return None

    def attach_disk(self, **kwargs):
        """
        Method to attach a disk to instance

        :type instance_id: string
        :param instance_id: The instance's ID

        :type disk_id: string
        :param disk_id: The disk ID in the cloud

        :type delete_with_instance: string
        :param delete_with_instance: value depicting should disk be deleted with instance.

        :return: A list of the total number of security groups, region ID of the security group,
                 the ID of the VPC to which the security group belongs
        """
        delay = 3
        timeout = DefaultTimeOut

        while True:
            try:
                res = self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
                if res:
                    return self.wait_for_disk_status(disk_id=kwargs["disk_id"], status="in_use", delay=5, timeout=120)
                return False
            except ServerException as e:
                if e.error_code == "IncorrectInstanceStatus":
                    pass
            time.sleep(delay)
            timeout -= delay
            if timeout <= 0:
                raise Exception("Timeout: Waiting for instance {0} status to be correct , time-consuming {1} seconds. "
                                "Error: {2}".format(kwargs["instance_id"], timeout, e))

    def detach_disk(self, **kwargs):
        """
        Method to detach a disk to instance

        :type disk_id: dict
        :param disk_id: ID of Disk for attaching detaching disk

        :return: Return status of Operation
        """
        self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        return self.wait_for_disk_status(disk_id=kwargs["disk_id"], status="available", delay=5, timeout=120)

    def delete_disk(self, **kwargs):
        """
        Method to delete a disk

        :type disk_id: dict
        :param disk_id: ID of Disk for attaching detaching disk

        :return: Return status of Operation
        """
        kwargs = self.format_request_kwargs(**kwargs)

        delay = 3
        timeout = DefaultTimeOut

        while True:
            try:
                self.get_status_new(self.build_request_params(kwargs))
                volume = self.describe_disk_attribute(disk_id=kwargs["disk_id"])
                if volume is None or not volume.id:
                    return True
            except ServerException as e:
                if str(e.error_code) == "InvalidDiskId.NotFound":
                    return True
                elif str(e.error_code) == "IncorrectInstanceStatus.Initializing":
                    pass
            time.sleep(delay)
            timeout -= delay
            if timeout <= 0:
                raise Exception("Timeout: Waiting for deleting volume {0}, time-consuming {1} seconds. "
                                "Error: {2}".format(kwargs["disk_id"], DefaultTimeOut, e))

    def modify_disk_attribute(self, **kwargs):
        """
        Method to delete a disk

        :type disk_id: dict
        :param disk_id: ID of Disk for attaching detaching disk

        :return: Return status of Operation
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def create_image(self, snapshot_id=None, image_name=None, image_version=None, description=None,
                     instance_id=None, disk_mapping=None, client_token=None, wait=None,
                     wait_timeout=None):
        """
        Create a user-defined image with snapshots of system disks.
        The created image can be used to create a new ECS instance.

        :type snapshot_id: string
        :param snapshot_id: A user-defined image is created from the specified snapshot.

        :type image_name: string
        :param image_name: image name which is to be created

        :type image_version: string
        :param image_version: version of image

        :type description: string
        :param description: description of the image

        :type instance_id: string
        :param instance_id: the specified instance_id

        :type disk_mapping: list
        :param disk_mapping: An optional list of device hashes/dictionaries with custom configurations
      
        :type client_token: string
        :param client_token: An optional list of device hashes/dictionaries with custom configurations

        :type wait: string
        :param wait: An optional bool value indicating wait for instance to be running before running

        :type wait_timeout: int
        :param wait_timeout: An optional int value indicating how long to wait, default 300

        :return: Image id
        """
        params = {}
        results = []
        changed = False
        image_id = ''
        request_id = ''

        # the snapshot id for creating image
        if snapshot_id:
            # Verifying progress of snapshot_id, snapshot_id should be 100% completed
            snapshot_results, snapshot_progress, snapshot_changed = self.get_snapshot_image(snapshot_id)

            if snapshot_results:
                if 'error code' in str(snapshot_results).lower():
                    results = snapshot_results
                    return changed, image_id, results, request_id

            if not snapshot_changed:
                results.append({"Error Code": "Snapshot.NotReady", "Error Message": "snapshot is not ready"})
                return changed, image_id, results, request_id

        if snapshot_id:
            self.build_list_params(params, snapshot_id, 'SnapshotId')

        # set the image name
        if image_name:
            self.build_list_params(params, image_name, 'ImageName')

        # set the image version
        if image_version:
            self.build_list_params(params, image_version, 'ImageVersion')

        # set the description
        if description:
            self.build_list_params(params, description, 'Description')

        # set the client token
        if client_token:
            self.build_list_params(params, client_token, 'ClientToken')

        # specify the instance id
        if instance_id:
            self.build_list_params(params, instance_id, 'InstanceId')

        # specify the disk device mapping, An optional list of device hashes/dictionaries with custom configurations
        if disk_mapping:
            mapping_no = 1
            for mapping in disk_mapping:
                if mapping:
                    if 'disk_size' in mapping:
                        self.build_list_params(params, mapping[
                            'disk_size'], 'DiskDeviceMapping.' + str(mapping_no) + '.Size')
                    if 'snapshot_id' in mapping:
                        self.build_list_params(params, mapping[
                            'snapshot_id'], 'DiskDeviceMapping.' + str(mapping_no) + '.SnapshotId')
                        snapshot_map_results, snapshot_map_progress, snapshot_map_changed \
                            = self.get_snapshot_image(mapping['snapshot_id'])
                        if snapshot_map_results:
                            if 'error code' in str(snapshot_map_results).lower():
                                results = snapshot_map_results
                                return changed, image_id, results, request_id

                        if not snapshot_map_changed:
                            results.append(
                                {"Error Code": "Snapshot.NotReady", "Error Message": "snapshot is not ready"})
                            return changed, image_id, results, request_id

                    mapping_no += 1

        try:
            response = self.get_object('CreateImage', params, ResultSet)

            if response:
                image_id = response.image_id
                request_id = response.request_id

            if wait:
                if not wait_timeout:
                    wait_timeout = 300
                time.sleep(wait_timeout)

            results.append("Image creation successful")
            changed = True
         
        except ServerException as e:
            results.append({"Error Code": e.error_code, "Error Message": e.message,
                            "RequestId": e.request_id, "Http Status": e.http_status})
        except Exception as e:
            results.append({"Error:": e})

        return changed, image_id, results, request_id

    def delete_image(self, image_id):
        """
        Delete image , delete image inside particular region.
        :type image_id: dict
        :param image_id: ID of an Image        
        :rtype: Return status of Operation
        """
        params = {}
        results = []
        changed = False

        self.build_list_params(params, image_id, 'ImageId')

        try:
            response = self.get_object('DescribeImages', params, ResultSet)
            if response:
                json_obj = response
                total_instance = response.total_count
                if total_instance > 0:
                    for items in response.images['image']:
                        if image_id == items['image_id']:
                            response = self.get_status('DeleteImage', params)
                            results.append(response)
                            changed = True
                else:
                    results.append({"Error Code": "Image does not exist", "Error Message": "Image does not exist"})
        except ServerException as e:
            results.append({"Error Code": e.error_code, "Error Message": e.message,
                            "RequestId": e.request_id, "Http Status": e.http_status})
            changed = False
        except Exception as e:
            results.append({"Error:": e})
            changed = False

        return changed

    def get_all_images(self, image_id=None, image_name=None, 
                           snapshot_id=None, filters=None):
            """
            Get all Volumes associated with the current credentials.

            :type image_id: dict
            :param image_id: Optional  image id.  If this is present,
                             only the image associated with these
                             image id will be returned.
        
            :type image_name: dict
            :param image_name: Optional image name.  If this is present,
                               only the image associated with these 
                               image name will be returned.

            :type snapshot_id: list
            :param snapshot_id: Optional snapshot id.  If this list is
                                present, only the image associated with
                                these snapshot id will be returned.

            :type filters: dict
            :param filters: Optional filters that can be used to limit
                            the results returned.  Filters are provided
                            in the form of a dictionary consisting of
                            filter names as the key and filter values
                            as the value.  The set of allowable filter
                            names/values is dependent on the request
                            being performed.  Check the ECS API guide
                            for details.

            :rtype: list of Volume
            :return: The requested Volume objects
            """
            params = {}
            result = []
            changed = False
            if image_id:
                self.build_list_params(params, image_id, 'ImageId')
            if image_name:
                self.build_list_params(params, image_name, 'ImageName')
            if snapshot_id:
                self.build_list_params(params, snapshot_id, 'SnapshotId')
            if filters:
                self.build_filter_params(params, filters)
            result = self.get_list('DescribeImages', params, ['Images', Image])
            if result:
                changed = True;
            else:
                while changed == False:
                    time.sleep(20);
                    result = self.get_list('DescribeImages', params, ['Images', Image])
                    if result:
                        changed = True;
                        break                
                    
            return result;

    def describe_images(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Images', Image])

    def get_snapshot_image(self, snapshot_id):
        params = {}
        results = []
        progress = ''
        changed = False
        counter = 0
        try:
            while changed == False:
                self.build_list_params(params, [snapshot_id], 'SnapshotIds')

                if counter > 20:
                    break
                obtained_results = self.get_object('DescribeSnapshots', params, ResultSet)
                counter += 1
                if obtained_results and len(obtained_results.snapshots['snapshot']) > 0:
                    status = str(obtained_results.snapshots['snapshot'][0]['status'])
                    progress = str(obtained_results.snapshots['snapshot'][0]['progress'])

                    if not '100%' in progress:
                        time.sleep(60)
                    else:
                        changed = True
                        progress = '100'
                        break
                else:
                    results.append({"Error Code": "Invalid.SnapshotId", "Error Message": "The snapshot id not found"})
                    break
        except ServerException as e:
            results.append({"Error Code": e.error_code, "Error Message": e.message,
                            "RequestId": e.request_id, "Http Status": e.http_status})
        except Exception as e:
            results.append({"Error:": e})

        return results, progress, changed

    def get_instance_details(self, instance_id):
        """
        Get details of an Instance
        :param instance_id: Id of an Instance
        :return: Return info about instance
        """
        params = {}

        self.build_list_params(params, instance_id, 'InstanceId')

        return self.get_object('DescribeInstanceAttribute', params, Instance)

    def wait_for_instance_status(self, instance_id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        """
        To verify instance status has become expected
        """
        tm = timeout
        try:
            while True:
                instance = self.get_instance_details(instance_id)
                if instance and str(instance.status).lower() in [status, str(status).lower()]:
                    return True

                tm -= delay

                if tm <= 0:
                    raise Exception("Timeout Error: Waiting for Disk status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
            return False
        except Exception as e:
            raise e

    def wait_for_disk_status(self, disk_id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        """
        To verify disk status has become expected after attaching or detaching disk
        """
        tm = timeout
        try:
            while True:
                volume = self.describe_disk_attribute(disk_id)
                if volume and str(volume.status).lower() in [status, str(status).lower()]:
                    return True

                tm -= delay

                if tm <= 0:
                    raise Exception("Timeout Error: Waiting for Disk status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
            return False
        except Exception as e:
            raise e

    def delete_instance_retry(self, action, params, instance_id, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        while True:
            try:
                self.get_status(action, params)
                instance = self.get_instance_details(instance_id)
                if instance is None or not instance.id:
                    return True
            except ServerException as e:
                if str(e.error_code) == "InvalidInstanceId.NotFound":
                    return True

            time.sleep(delay)
            timeout -= delay
            if timeout <= 0:
                raise Exception("Timeout Error: Waiting for deleting instance {0}, time-consuming {1} seconds. "
                                "Error: {2}".format(instance_id, DefaultTimeOut, e))

    def verify_join_remove_securitygrp(self, instance_id, group_id, mode, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        """
        To verify join & remove operations got performed in security group
        """
        done = False
        count = 0
        id_of_instance = [instance_id]
        tm = timeout
        try:
            while not done:
                time.sleep(delay)
                instance_list = self.get_all_instances(id_of_instance, None, None)
                if len(instance_list) > 0:
                    if mode.lower() == 'join':
                        for inst in instance_list:
                            if len(inst.security_group_ids['security_group_id']) > 0:
                                for grp in inst.security_group_ids['security_group_id']:
                                    if str(grp) == group_id:
                                        done = True
                                        break

                    elif mode.lower() == 'remove':
                        for inst in instance_list:
                            if len(inst.security_group_ids['security_group_id']) > 0:
                                for grp in inst.security_group_ids['security_group_id']:
                                    if str(grp) == group_id:
                                        count = count + 1
                                if count == 0:
                                    done = True
                                    break
                tm -= delay
                if tm <= 0:
                    raise Exception("Timeout Error: Waiting for joining or removing security group, time-consuming %d seconds." % timeout)

        except Exception as ex:
            raise ex

        return done

    def get_all_regions(self):
        all_regions = self.get_list('DescribeRegions', None, ['Regions', RegionInfo])
        return all_regions

    def describe_regions(self):
        all_regions = self.get_list_new(self.build_request_params(self.format_request_kwargs()), ['Regions', RegionInfo])
        return all_regions

    def create_network_interface(self, **kwargs):
        res = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet)
        if not self.wait_for_network_interface(res.network_interface_id, "Available"):
            raise Exception("Waitting Network Interface {0} Failed.".format("Available"))
        return self.describe_network_interfaces(network_interface_ids=[res.network_interface_id])[0]

    def describe_network_interfaces(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['NetworkInterfaceSets', NetworkInterfaceSet])

    def attach_network_interface(self, **kwargs):
        changed = self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        if not self.wait_for_network_interface(kwargs["network_interface_id"], "InUse"):
            raise Exception("Waitting Network Interface {0} Failed.".format("InUse"))
        return changed

    def detach_network_interface(self, **kwargs):
        changed = self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        if not self.wait_for_network_interface(kwargs["network_interface_id"], "Available"):
            raise Exception("Waitting Network Interface {0} Failed.".format("Available"))
        return changed

    def modify_network_interface_attribute(self, **kwargs):
        if self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs))):
            time.sleep(10)
            return True
        return False

    def delete_network_interface(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def wait_for_network_interface(self, id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        """
        To verify network interface status has become expected
        """
        tm = timeout
        while True:
            result = self.describe_network_interfaces(network_interface_ids=[id])
            if result and str(result[0].status).lower() in [status, str(status).lower()]:
                return True

            tm -= delay

            if tm < 0:
                raise Exception("Timeout Error: Waiting for network interface {0} {1}, time-consuming {2} seconds.".format(id, status, timeout))

            time.sleep(delay)
        return False

    def describe_user_data(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet)

    def list_tag_resources(self, **kwargs):
        res = {}
        tags = self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['TagResources', Instance])
        for tag in tags:
            res[tag.tag_key] = tag.tag_value
        return res

    def tag_resources(self, **kwargs):
        tmp = {}
        if kwargs['tags']:
            for key, value in list(kwargs['tags'].items()):
                if key in list(self.list_tag_resources(**kwargs).keys()) and value == self.list_tag_resources(**kwargs)[key]:
                    continue
                tmp[key] = value
        if tmp:
            kwargs['tags'] = tmp
            return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        return False

    def untag_resources(self, **kwargs):
        tmp = []
        if kwargs['tags']:
            for key, value in list(kwargs['tags'].items()):
                if key not in list(self.list_tag_resources(**kwargs).keys()):
                    continue
                tmp.append(key)
        if tmp:
            kwargs['tag_keys'] = tmp
            return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        return False

