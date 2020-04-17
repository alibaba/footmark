from footmark.ros.connection import ROSConnection


def connect_to_region(region_id, **kw_params):
    """
    Given a valid region name, return a
    :class:`footmark.ros.connection.ROSConnection`.
    Any additional parameters after the region_name are passed on to
    the connect method of the region object.

    :type: str
    :param region_id: The ID of the region to connect to.

    :rtype: :class:`footmark.ros.connection.ROSConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
             name is given
    """
    return ROSConnection(region=region_id, **kw_params)
