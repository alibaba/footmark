from footmark.oos.connection import OOSConnection


def connect_to_region(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.oos.connection.OOSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.oos.connection.OOSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return OOSConnection(region=region_id, **kw_params)
