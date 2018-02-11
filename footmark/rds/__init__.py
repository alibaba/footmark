"""
This module provides an interface to the Relational Database System (RDS) service from Alicloud.
"""
from footmark.rds.connection import RDSConnection
from footmark.regioninfo import get_regions


def regions(**kw_params):
    """
    Get all available regions for the RDS service.
    You may pass any of the arguments accepted by the RDSConnection
    object's constructor as keyword arguments and they will be
    passed along to the RDSConnection object.

    :rtype: list
    :return: A list of :class:`footmark.rds.regioninfo.RegionInfo`
    """
    return get_regions('rds', connection_cls=RDSConnection)


def connect_to_region(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.rds.connection.RDSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.rds.connection.RDSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return RDSConnection(region=region_id, **kw_params)    


def get_region(region_id, **kw_params):
    """
    Find and return a :class:`footmark.rds.regioninfo.RegionInfo` object
    given a region name.

    :type: str
    :param: The name of the region.

    :rtype: :class:`footmark.rds.regioninfo.RegionInfo`
    :return: The RegionInfo object for the given region or None if
             an invalid region name is provided.
    """
    for region in regions(**kw_params):
        if region.id == region_id:
            return region
    return None
