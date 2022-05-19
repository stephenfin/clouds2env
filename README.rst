============
 clouds2env
============

A tool to convert from an OpenStack ``clouds.yaml`` file to environment
variables. This can be useful when all you have is a ``clouds.yaml`` file but
you need to work with a legacy tool like *novaclient*.

Like *openstacksdk*, *clouds2env* will look in the following location for
``clouds.yaml`` files:

* ``.`` (the current directory)
* ``$HOME/.config/openstack``
* ``/etc/openstack``

The first file found wins.

You can also set the environment variable ``OS_CLIENT_CONFIG_FILE`` to an
absolute path of a file to look for and that location will be inserted at the
front of the file search list.

You can specify the cloud to generate environment variables for by setting the
``OS_CLOUD`` environment variable. Alternatively, you may provide the cloud
name as an argument to tool.

Usage
-----

.. code-block:: shell

    $ python clouds2env --help
    usage: clouds2env [-h] [cloud]

    positional arguments:
      cloud       the cloud to use (defaults to $OS_CLOUD)

    options:
      -h, --help  show this help message and exit

Example
-------

.. code-block:: shell

    $ export OS_CLOUD=devstack-admin
    $ clouds2yaml
    export OS_AUTH_URL=http://10.0.108.84/identity
    export OS_PASSWORD=password
    export OS_PROJECT_DOMAIN_ID=default
    export OS_PROJECT_NAME=admin
    export OS_USER_DOMAIN_ID=default
    export OS_USERNAME=admin
    export OS_IDENTITY_API_VERSION=3
    export OS_REGION_NAME=RegionOne
    export OS_VOLUME_API_VERSION=3
