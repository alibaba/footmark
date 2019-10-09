import json
import os

import footmark
from footmark.exception import FootmarkClientError


def load_endpoint_json(path):
    """
    Loads a given JSON file & returns it.

    :param path: The path to the JSON file
    :type path: string

    :returns: The loaded data
    """
    with open(path, 'r') as endpoints_file:
        return json.load(endpoints_file)


def merge_endpoints(defaults, additions):
    """
    Given an existing set of endpoint data, this will deep-update it with
    any similarly structured data in the additions.

    :param defaults: The existing endpoints data
    :type defaults: dict

    :param defaults: The additional endpoints data
    :type defaults: dict

    :returns: The modified endpoints data
    :rtype: dict
    """
    # We can't just do an ``defaults.update(...)`` here, as that could
    # *overwrite* regions if present in both.
    # We'll iterate instead, essentially doing a deeper merge.
    for service, region_info in list(additions.items()):
        # Set the default, if not present, to an empty dict.
        defaults.setdefault(service, {})
        defaults[service].update(region_info)

    return defaults


def load_regions():
    """
    Actually load the region/endpoint information from the JSON files.

    By default, this loads from the default included ``footmark/endpoints.json``
    file.

    Users can override/extend this by supplying either a ``FOOTMARK_ENDPOINTS``
    environment variable or a ``endpoints_path`` config variable, either of
    which should be an absolute path to the user's JSON file.

    :returns: The endpoints data
    :rtype: dict
    """
    # Load the defaults first.
    endpoints = load_endpoint_json(footmark.ENDPOINTS_PATH)
    additional_path = None

    # Try the ENV var. If not, check the config file.
    if os.environ.get('FOOTMARK_ENDPOINTS'):
        additional_path = os.environ['FOOTMARK_ENDPOINTS']
    elif footmark.config.get('Footmark', 'endpoints_path'):
        additional_path = footmark.config.get('Footmark', 'endpoints_path')

    # If there's a file provided, we'll load it & additively merge it into
    # the endpoints.
    if additional_path:
        additional = load_endpoint_json(additional_path)
        endpoints = merge_endpoints(endpoints, additional)

    return endpoints


def get_regions(service_name, region_cls=None, connection_cls=None):
    """
    Given a service name (like ``ecs``), returns a list of ``RegionInfo``
    objects for that service.

    This leverages the ``endpoints.json`` file (+ optional user overrides) to
    configure/construct all the objects.

    :param service_name: The name of the service to construct the ``RegionInfo``
        objects for. Ex: ``ecs``
    :type service_name: string

    :param region_cls: (Optional) The class to use when constructing. By
        default, this is ``RegionInfo``.
    :type region_cls: class

    :param connection_cls: (Optional) The connection class for the
        ``RegionInfo`` object. Providing this allows the ``connect`` method on
        the ``RegionInfo`` to work. Default is ``None`` (no connection).
    :type connection_cls: class

    :returns: A list of configured ``RegionInfo`` objects
    :rtype: list
    """
    endpoints = load_regions()

    if service_name not in endpoints:
        raise FootmarkClientError(
            "Service '%s' not found in endpoints." % service_name
        )

    if region_cls is None:
        region_cls = RegionInfo

    region_objs = []

    for region_name, endpoint in list(endpoints.get(service_name, {}).items()):
        region_objs.append(
            region_cls(
                name=region_name,
                endpoint=endpoint,
                connection_cls=connection_cls
            )
        )

    return region_objs


class RegionInfo(object):
    """
    Represents an Aliyun Region
    """
    def __init__(self, connection=None, region=None, local_name=None, connection_cls=None):
        self.connection = connection
        self.connection_cls = connection_cls
        self.region_id = region
        self.local_name = local_name

    def __repr__(self):
        return 'RegionInfo:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.region_id
        if name in ('name', 'region_name'):
            return self.local_name

        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def connect(self, **kw_params):
        """
        Connect to this Region's endpoint. Returns an connection
        object pointing to the endpoint associated with this region.
        You may pass any of the arguments accepted by the connection
        class's constructor as keyword arguments and they will be
        passed along to the connection object.

        :rtype: Connection object
        :return: The connection to this regions endpoint
        """
        if self.connection_cls:
            return self.connection_cls(region=self, **kw_params)
