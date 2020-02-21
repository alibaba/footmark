# encoding: utf-8
import warnings
import time

from footmark.connection import ACSQueryConnection
from footmark.vpc.regioninfo import RegionInfo
from footmark.exception import VPCResponseError
from footmark.resultset import ResultSet
from footmark.vpc.vpc import Vpc
from footmark.vpc.eip import Eip
from footmark.vpc.vswitch import VSwitch
from footmark.vpc.router import RouteEntry, RouteTable
from footmark.vpc.config import *
from aliyunsdkcore.acs_exception.exceptions import ServerException
# from aliyunsdkvpc.request.v20160428.ModifyEipAddressAttributeRequest import


class VPCConnection(ACSQueryConnection):
    SDKVersion = '2016-04-28'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = VPCResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, ecs_role_name=None, user_agent=None):
        """
        Init method to create a new connection to ECS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.VPCSDK = 'aliyunsdkvpc.request.v' + self.SDKVersion.replace('-', '')

        super(VPCConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            region=self.region, product=self.VPCSDK,
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

    def format_vpc_request_kwargs(self, **kwargs):
        for key, value in list(kwargs.items()):

            # Format Vswitch to VSwitch
            if key == 'Action':
                if str(value).find("Vswitch"):
                    kwargs[key] = str(value).replace("Vswitch", "VSwitch")

            # Convert vpc user cidrs and vpc id
            if key in ['user_cidr', 'vpc_id']:
                if value:
                    if not isinstance(value, list):
                        value = [value]
                    kwargs[key] = str(",").join(value)

        return kwargs

    def create_vpc(self, **kwargs):
        vpc_id = self.get_object_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))), ResultSet).vpc_id
        self.wait_for_vpc_status(vpc_id, 'Available', 4, 120)
        return self.describe_vpc_attribute(vpc_id=vpc_id)

    def describe_vpc_attribute(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Vpc)

    def describe_vpcs(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))), ['Vpcs', Vpc])

    def modify_vpc_attribute(self, **kwargs):
        if self.get_status_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs)))):
            return self.wait_for_vpc_status(kwargs['vpc_id'], 'Available', 4, 60)
        return False

    def delete_vpc(self, **kwargs):
        retry = 5
        while retry:
            try:
                return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
            except ServerException as e:
                if str(e.error_code) == "Forbbiden" or str(e.error_code).find("Dependency"):
                    time.sleep(5)
                    retry -= 1
                    continue
                raise e
        return False

    def create_vswitch(self, **kwargs):
        vswitch_id = self.get_object_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))), ResultSet).vswitch_id
        self.wait_for_vswitch_status(vswitch_id, 'Available', 4, 120)
        return self.describe_vswitch_attribute(vswitch_id=vswitch_id)

    def describe_vswitches(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))), ['VSwitches', VSwitch])

    def describe_vswitch_attributes(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))), VSwitch)

    # In order to unify, add an extra method. It is equal to describe_vswitch_attributes
    def describe_vswitch_attribute(self, **kwargs):
        kwargs = self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))
        kwargs['Action'] = kwargs['Action'] + 's'
        return self.get_object_new(self.build_request_params(kwargs), VSwitch)

    def modify_vswitch_attribute(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))))

    def delete_vswitch(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))))

    def create_route_entry(self, **kwargs):
        """
        Create RouteEntry for VPC
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :type destination_cidrblock: str
        :param destination_cidrblock: The destination CIDR of route entry. It must be a legal CIDR or IP address, such as: 192.168.0.0/24 or 192.168.0.1
        :type nexthop_type: str
        :param nexthop_type: The type of next hop. Available value options: Instance, Tunnel, HaVip, RouterInterface. Default is Instance.
        :type next_hop_id: str
        :param next_hop_id: The ID of next hop.
        :type nexthop_list: str
        :param nexthop_list: The route item of next hop list.
        :rtype
        :return Return result of Creating RouteEntry.
        """
        status = self.get_status_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))))
        if status:
            return self.wait_for_route_entry_status(kwargs["route_table_id"], kwargs["destination_cidrblock"], 'Available', 4, 60)
        return None

    def modify_route_entry(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))))

    def get_route_entry_attribute(self, **kwargs):
        """
        Querying route entry attribute
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :type destination_cidrblock: str
        :param destination_cidrblock: The destination CIDR of route entry. It must be a legal CIDR or IP address, such as: 192.168.0.0/24 or 192.168.0.1
        :type nexthop_id: str
        :param nexthop_type: The ID of next hop.
        :rtype 
        :return: VRouters in json format
        """

        route_entries = self.get_all_route_entries(route_table_id=kwargs["route_table_id"])
        if route_entries:
            for entry in route_entries:
                if kwargs["destination_cidrblock"] == str(entry.destination_cidrblock):
                    return entry
        return None

    def get_all_route_entries(self, **kwargs):
        """
        Querying all route entries in the specified router or route_tables_id
        :type router_id: str
        :param router_id: The ID of router which is to be fetched.
        :type router_type str
        :param router_type: The type of router which is to be fetched.
        :type route_table_id: str
        :param route_table_id: ID of route table in one VPC
        :type pagenumber: integer
        :param pagenumber: Page number of the route table list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10 
        :rtype list<>
        :return: List of route entry.
        """
        route_tables = self.describe_route_tables(**kwargs)
        route_entries = []
        if route_tables:
            for table in route_tables:
                if table.route_entrys:
                    for entry in table.route_entrys['route_entry']:
                        route_entry = RouteEntry(self)
                        for k, v in list(entry.items()):
                            setattr(route_entry, k, v)
                        route_entries.append(route_entry)

        return route_entries

    def delete_route_entry(self, **kwargs):
        """
        Deletes the specified RouteEntry for the vpc
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :type destination_cidrblock: str
        :param destination_cidrblock: The destination CIDR of route entry. It must be a legal CIDR or IP address, such as: 192.168.0.0/24 or 192.168.0.1
        :type next_hop_id: str
        :param next_hop_id: The ID of next hop.
        :type nexthop_list: str
        :param nexthop_list: The route item of next hop list.
        :rtype bool
        :return Return result of deleting route entry.
        """
        return self.get_status_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))))

    def get_route_table_attribute(self, **kwargs):
        """
        Querying route table attribute
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :rtype dict
        :return: VRouters in json format
        """
        return self.describe_route_tables(route_table_id=kwargs["route_table_id"])

    def describe_route_tables(self, **kwargs):
        """
        Querying vrouter
        :type router_id: str
        :param router_id: The ID of router which is to be fetched.
        :type router_type str
        :param router_type: The type of router which is to be fetched.
        :type route_table_id: str
        :param route_table_id: ID of route table in one VPC
        :type pagenumber: integer
        :param pagenumber: Page number of the route entry list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10
        :rtype list<>
        :return: List of route entry.
        """
        return self.get_list_new(self.build_request_params(self.format_vpc_request_kwargs(**self.format_request_kwargs(**kwargs))), ['RouteTables', RouteTable])

    def get_instance_info(self):
        """
        method to get all Instances of particular region 
        :return: Return All Instances in the region
        """
        params = {}
        results = []

        try:
            v_ids = {}
            response = self.get_status('DescribeInstances', params)
            results.append(response)
            
        except Exception as ex:        
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return results

    def allocate_eip_address(self, **kwargs):
        """
        method to query eip addresses in the region
        :type int
        :param bandwidth : bandwidth of the eip address. Default to 5
        :type internet_charge_type : str
        :param internet_charge_type : paybytraffic or paybybandwidth types
        :return: Return the allocationId , requestId and EIP address
        """
                  
        id = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet).allocation_id
        self.wait_for_eip_status(allocation_id=id, status='Available', interval=3, timeout=60)
        eips = self.describe_eip_addresses(allocation_id=id)
        if eips:
            return eips[0]
        return None

    def get_all_eip_addresses(self, status=None, ip_address=None, allocation_id=None, associated_instance_type=None,
                              associated_instance_id=None, page_number=1, page_size=50):
        """
        Get EIP details for a region
        :param status: The EIP status includes Associating | Unassociating | InUse | Available
        :param ip_address: The EIP ip address
        :param allocation_id: ID of the allocated EIP
        :param associated_instance_type: The type of the associate device
        :param associated_instance_id: The ID of the associate device
        :param pagenumber: Page number. The start value is 1. The default value is 1
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50. Default to 50.
        :return:
        """
        params = {}

        if status:
            self.build_list_params(params, status, 'Status')
        if ip_address:
            self.build_list_params(params, ip_address, 'EipAddress')
        if allocation_id:
            self.build_list_params(params, allocation_id, 'AllocationId')
        if associated_instance_type:
            self.build_list_params(params, associated_instance_type, 'AssociatedInstanceType')
        if associated_instance_id:
            self.build_list_params(params, associated_instance_id, 'AssociatedInstanceId')

        self.build_list_params(params, page_number, 'PageNumber')
        self.build_list_params(params, page_size, 'PageSize')

        return self.get_list('DescribeEipAddresses', params, ['EipAddresses', Eip])

    def describe_eip_addresses(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['EipAddresses', Eip])

    def associate_eip_address(self, **kwargs):
        """
        :type allocation_id:string
        :param allocation_id:The instance ID of the EIP
        :type instance_id:string
        :param instance_id:The ID of an ECS instance
        :param client_token: Used to ensure the idempotence of the request
        :return:Returns the status of operation
        """
        self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        return self.wait_for_eip_status(allocation_id=kwargs['allocation_id'], status="InUse", interval=2, timeout=60)

    def unassociate_eip_address(self, **kwargs):
        """
        :type allocation_id:string
        :param allocation_id:The instance ID of the EIP
        :type instance_id:string
        :param instance_id:The ID of an ECS instance
        :return:Request Id
        """
        self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        return self.wait_for_eip_status(allocation_id=kwargs['allocation_id'], status="Available", interval=2, timeout=60)

    def modify_eip_address_attribute(self, **kwargs):
        """
        :type allocation_id:string
        :param allocation_id:The instance ID of the EIP
        :type bandwidth:int
        :param bandwidth:Bandwidth of the EIP instance
        :return:Request Id
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def release_eip_address(self, **kwargs):
        """
        To release Elastic Ip
        :type allocation_id: string
        :param allocation_id: To release the allocation ID,allocation ID uniquely identifies the EIP
        :return: Return status of operation
        """
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def get_all_vrouters(self, vrouter_id=None, pagenumber=None, pagesize=None):
        """
        Querying vrouter
        :param vrouter_id: VRouter_Id to be fetched
        :type vrouter_id: str
        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10
        :return: VRouters in json format
        """
        params = {}
        results = []

        try:
            if vrouter_id is not None:
                self.build_list_params(params, vrouter_id, 'VRouterId')

            if pagenumber is not None:
                self.build_list_params(params, pagenumber, 'PageNumber')

            if pagesize is not None:
                self.build_list_params(params, pagesize, 'PageSize')

            results = self.get_status('DescribeVRouters', params)
        except Exception as ex:
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return False, results

    def wait_for_eip_status(self, allocation_id, status, interval=DefaultWaitForInterval, timeout=DefaultTimeOut):
        """
        wait for bind ok
        :param eip_address:
        :param allocation_id:
        :param status:
        :return: 
        """
        try:
            tm = 0
            while tm < timeout:
                eips = self.describe_eip_addresses(allocation_id=allocation_id)
                if not eips or len(eips) < 1:
                    raise Exception("Not Found Error: The specified eip {0} is not found.".format(allocation_id))
                if str(status).lower() == str(eips[0].status).lower():
                    return True
                tm += interval
                if tm >= timeout:
                    raise Exception("Timeout Error: Waiting For EIP Status {0}, time-consuming {1} seconds.".format(status, timeout))
                time.sleep(interval)
            return None
        except Exception as e:
            raise Exception("Waiting For EIP Status {0} Error: {1}.".format(status, e))

    def get_vswitch_status(self, vpc_id, zone_id=None, vswitch_id=None, pagenumber=None, pagesize=None):
        """
        List VSwitches of VPC with their status
        :type vpc_id: string
        :param vpc_id: ID of Vpc from which VSwitch belongs
        :type zone_id: string
        :param zone_id: ID of the Zone
        :type vswitch_id: string
        :param vswitch_id: The ID of the VSwitch to be queried
        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: The number of lines per page set for paging query. The maximum value is 50 and default
        value is 10
        :return: Returns list of vswitches in VPC with their status
        """
        params = {}
        results = []

        self.build_list_params(params, vpc_id, 'VpcId')
        if zone_id:
            self.build_list_params(params, zone_id, 'ZoneId')
        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')
        if pagenumber:
            self.build_list_params(params, pagenumber, 'PageNumber')
        if pagesize:
            self.build_list_params(params, pagesize, 'PageSize')

        try:
            results = self.get_status('DescribeVSwitches', params)
        except Exception as ex:
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return False, results

    def wait_for_vpc_status(self, vpc_id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):

        try:
            while True:
                vpc = self.describe_vpc_attribute(vpc_id=vpc_id)
                if vpc and str(vpc.status) in [status, str(status).lower()]:
                    return True

                timeout -= delay

                if timeout <= 0:
                    raise Exception("Timeout Error: Waiting for VPC status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
        except Exception as e:
            raise e

    def wait_for_vswitch_status(self, vswitch_id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        try:
            while True:
                vsw = self.describe_vswitch_attribute(vswitch_id=vswitch_id)
                if vsw and str(vsw.status) in [status, str(status).lower()]:
                    return True

                timeout -= delay

                if timeout <= 0:
                    raise Exception("Timeout Error: Waiting for VSwitch status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
        except Exception as e:
            raise e

    def wait_for_route_entry_status(self, route_table_id, destination_cidrblock, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        try:
            tm = 0
            while tm < timeout:
                route_entry = self.get_route_entry_attribute(route_table_id=route_table_id, destination_cidrblock=destination_cidrblock)
                if route_entry and str.lower(route_entry.status) == str.lower(status):
                    return route_entry

                tm += delay

                if tm >= timeout:
                    raise Exception("Timeout Error: Waiting for route entry status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
            return None
        except Exception as e:
            raise Exception("Waiting For route entry Status {0} Error: {1}.".format(status, e))

    # def tag_resources(self, **kwargs):
    #     return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
    #
    # def un_tag_resources(self, **kwargs):
    #     return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def list_tag_resources(self, **kwargs):
        res = {}
        tags = self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['TagResources', Vpc])
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
        return None

    def un_tag_resources(self, **kwargs):
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

