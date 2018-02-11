"""
This module provides an interface to the Elastic Compute Service (ECS) service from Alicloud.
"""
from footmark.vpc.connection import VPCConnection
from footmark.regioninfo import get_regions


def regions(**kw_params):
    """
    Get all available regions for the ECS service.
    You may pass any of the arguments accepted by the ECSConnection
    object's constructor as keyword arguments and they will be
    passed along to the ECSConnection object.

    :rtype: list
    :return: A list of :class:`footmark.ecs.regioninfo.RegionInfo`
    """
    return get_regions('ecs', connection_cls=VPCConnection)


def connect_to_region(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.ecs.connection.ECSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.ecs.connection.ECSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return VPCConnection(region=region_id, **kw_params)


def get_region(region_id, **kw_params):
    """
    Find and return a :class:`footmark.ecs.regioninfo.RegionInfo` object
    given a region name.

    :type: str
    :param: The name of the region.

    :rtype: :class:`footmark.ecs.regioninfo.RegionInfo`
    :return: The RegionInfo object for the given region or None if
             an invalid region name is provided.
    """
    for region in regions(**kw_params):
        if region.id == region_id:
            return region
    return None
