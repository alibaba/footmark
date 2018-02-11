"""
This module provides an interface to the Server Load Balancer (SLB) service from Alicloud.
"""
from footmark.slb.connection import SLBConnection
from footmark.regioninfo import get_regions


def regions(**kw_params):
    """
    Get all available regions for the SLB service.
    You may pass any of the arguments accepted by the SLBConnection
    object's constructor as keyword arguments and they will be
    passed along to the SLBConnection object.

    :rtype: list
    :return: A list of :class:`footmark.slb.regioninfo.RegionInfo`
    """
    return get_regions('slb', connection_cls=SLBConnection)


def connect_to_region(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.slb.connection.SLBConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.slb.connection.SLBConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return SLBConnection(region=region_id, **kw_params)    


def get_region(region_id, **kw_params):
    """
    Find and return a :class:`footmark.slb.regioninfo.RegionInfo` object
    given a region name.

    :type: str
    :param: The name of the region.

    :rtype: :class:`footmark.slb.regioninfo.RegionInfo`
    :return: The RegionInfo object for the given region or None if
             an invalid region name is provided.
    """
    for region in regions(**kw_params):
        if region.id == region_id:
            return region
    return None
