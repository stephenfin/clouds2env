#!/usr/bin/env python3

import argparse
import os
import os.path
import shlex
import sys

import yaml


def _load_clouds_yaml() -> str:
    # Based on the openstacksdk docs
    # https://docs.openstack.org/openstacksdk/latest/user/config/configuration.html
    paths = [
        os.path.join(os.getcwd(), 'clouds.yaml'),
        os.path.expanduser('~/.config/openstack/clouds.yaml'),
        '/etc/openstack/clouds.yaml',
    ]

    if os.getenv('OS_CLIENT_CONFIG_FILE'):
        paths.insert(0, os.getenv('OS_CLIENT_CONFIG_FILE'))

    for path in paths:
        if os.path.exists(path) and os.path.isfile(path):
            break
    else:
        print('No clouds.yaml file was found.', file=sys.stderr)
        sys.exit(1)

    with open(path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(
                f'Error encountered loading YAML:\n\n{str(exc)}',
                file=sys.stderr,
            )
            sys.exit(1)

    if 'clouds' not in data:
        print(
            f"No 'clouds' key found in {path}; is this a valid clouds.yaml?",
            file=sys.stderr,
        )
        sys.exit(1)

    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "A tool to convert from an OpenStack 'clouds.yaml' file to "
            "'OS_'-prefixed environment variables suitable for use with "
            "legacy tooling like novaclient."
        ),
    )
    parser.add_argument(
        'cloud',
        nargs='?',
        help='the cloud to use',
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--set',
        action='store_true',
        dest='set',
        default=True,
        help='set environment variables (default)',
    )
    group.add_argument(
        '--unset',
        action='store_false',
        dest='set',
        default=True,
        help='unset environment variables',
    )
    args = parser.parse_args()

    cloud = args.cloud or os.getenv('OS_CLOUD')

    if not cloud:
        print(
            'no <cloud> argument provided and OS_CLOUD is unset',
            file=sys.stderr,
        )
        sys.exit(1)

    data = _load_clouds_yaml()
    if cloud not in data['clouds']:
        print(
            f"Could not find '{cloud}' in your clouds.yaml file",
            file=sys.stderr,
        )
        sys.exit(1)

    cloud_data = data['clouds'][cloud]

    for key, value in cloud_data.items():
        if key == 'auth':
            for key, value in cloud_data['auth'].items():
                if args.set:
                    print(f'export OS_{key.upper()}={shlex.quote(str(value))}')
                else:
                    print(f'unset OS_{key.upper()}')
            continue

        if key == 'regions':
            continue

        # handle list-style values
        if key in ('auth_methods',):
            value = ','.join(value)

        if args.set:
            print(f'export OS_{key.upper()}={shlex.quote(str(value))}')
        else:
            print(f'unset OS_{key.upper()}')


if __name__ == '__main__':
    main()
