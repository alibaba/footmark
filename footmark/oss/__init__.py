"""
This module provides an interface to the Object Storage Service (OSS) service from Alicloud.
"""
from footmark.oss.connection import OSSConnection
from footmark.regioninfo import get_regions
from footmark.oss.bucket import Bucket


def regions(**kw_params):
    """
    Get all available regions for the OSS service.
    You may pass any of the arguments accepted by the OSSConnection
    object's constructor as keyword arguments and they will be
    passed along to the OSSConnection object.

    :rtype: list
    :return: A list of :class:`footmark.oss.regioninfo.RegionInfo`
    """
    return get_regions('oss', connection_cls=OSSConnection)


def connect_to_region(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.oss.connection.OSSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.oss.connection.OSSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return OSSConnection(region=region_id, **kw_params)    


def get_region(region_id, **kw_params):
    """
    Find and return a :class:`footmark.oss.regioninfo.RegionInfo` object
    given a region name.

    :type: str
    :param: The name of the region.

    :rtype: :class:`footmark.oss.regioninfo.RegionInfo`
    :return: The RegionInfo object for the given region or None if
             an invalid region name is provided.
    """
    for region in regions(**kw_params):
        if region.id == region_id:
            return region
    return None


def connect_to_oss(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.oss.connection.OSSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.oss.connection.OSSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return OSSConnection(region=region_id, **kw_params)


def connect_to_bucket(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.oss.connection.OSSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.oss.connection.OSSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return Bucket(region=region_id, **kw_params)
