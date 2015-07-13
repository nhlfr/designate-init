# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from oslo_config import cfg

import designate_init


def env(*vars, **kwargs):
    for v in vars:
        value = os.environ.get(v)
        if value:
            return value
    return kwargs.get('default', '')


opts = [
    # Designate init options
    cfg.StrOpt('domain-id',
               required=True,
               help='Domain ID for which A records will be created.'),
    cfg.StrOpt('format',
               default='%(name)s.%(tenant_name)s.%(domain)s',
               help='Format of record to create.'),
    cfg.MultiStrOpt('filter-networks',
                    help='Networks for which records or/and domains will be'
                         'created.'),
    cfg.BoolOpt('create-wildcard',
                default=False,
                help='Automatically create wildcard records.'),
    cfg.BoolOpt('create-ptr',
                default=False,
                help='Automatically create PTR domains and records.'),
    cfg.StrOpt('ptr-format',
               default='%(octet3)s.%(octet2)s.%(octet1)s.%(octet0)s.'
                       'in-addr.arpa.',
               help='Format of PTR record to create.'),
    cfg.StrOpt('email',
               help='E-mail addres for which PTR domains should be created.'),
    # OpenStack clients auth options
    cfg.StrOpt('os-username',
               default=env('OS_USERNAME'),
               help='Name used for authentication with the '
                    'OpenStack Identity service. '
                    'Defaults to env[OS_USERNAME].'),
    cfg.StrOpt('os-user-id',
               default=env('OS_USER_ID'),
               help='User ID used for authentication with the '
                    'OpenStack Identity service. '
                    'Defaults to env[OS_USER_ID].'),
    cfg.StrOpt('os-user-domain-id',
               default=env('OS_USER_DOMAIN_ID'),
               help='Defaults to env[OS_USER_DOMAIN_ID].'),
    cfg.StrOpt('os-user-domain-name',
               default=env('OS_USER_DOMAIN_NAME'),
               help='Defaults to env[OS_USER_DOMAIN_NAME].'),
    cfg.StrOpt('os-password',
               default=env('OS_PASSWORD'),
               help='Password used for authentication with the '
                    'OpenStack Identity service. '
                    'Defaults to env[OS_PASSWORD].'),
    cfg.StrOpt('os-tenant-name',
               default=env('OS_TENANT_NAME'),
               help='Tenant to request authorization on. '
                    'Defaults to env[OS_TENANT_NAME].'),
    cfg.StrOpt('os-tenant-id',
               default=env('OS_TENANT_ID'),
               help='Tenant to request authorization on. '
                    'Defaults to env[OS_TENANT_ID].'),
    cfg.StrOpt('os-project-name',
               default=env('OS_PROJECT_NAME'),
               help='Project to request authorization on. '
                    'Defaults to env[OS_PROJECT_NAME].'),
    cfg.StrOpt('os-domain-name',
               default=env('OS_DOMAIN_NAME'),
               help='Project to request authorization on. '
                    'Defaults to env[OS_DOMAIN_NAME].'),
    cfg.StrOpt('os-domain-id',
               default=env('OS_DOMAIN_ID'),
               help='Defaults to env[OS_DOMAIN_ID].'),
    cfg.StrOpt('os-project-id',
               default=env('OS_PROJECT_ID'),
               help='Project to request authorization on. '
                    'Defaults to env[OS_PROJECT_ID].'),
    cfg.StrOpt('os-project-domain-id',
               default=env('OS_PROJECT_DOMAIN_ID'),
               help='Defaults to env[OS_PROJECT_DOMAIN_ID].'),
    cfg.StrOpt('os-project-domain-name',
               default=env('OS_PROJECT_DOMAIN_NAME'),
               help='Defaults to env[OS_PROJECT_DOMAIN_NAME].'),
    cfg.StrOpt('os-auth-url',
               default=env('OS_AUTH_URL'),
               help='Specify the Identity endpoint to use for '
                    'authentication. '
                    'Defaults to env[OS_AUTH_URL].'),
    cfg.StrOpt('os-region-name',
               default=env('OS_REGION_NAME'),
               help='Specify the region to use. '
                    'Defaults to env[OS_REGION_NAME].'),
    cfg.StrOpt('os-token',
               default=env('OS_SERVICE_TOKEN'),
               help='Specify an existing token to use instead of '
                    'retrieving one via authentication (e.g. '
                    'with username & password). '
                    'Defaults to env[OS_SERVICE_TOKEN].'),
    cfg.StrOpt('os-compute-endpoint',
               default=env('OS_COMPUTE_ENDPOINT'),
               help='Specify an endpoint to use instead of '
                    'retrieving one from the service catalog '
                    '(via authentication). '
                    'Defaults to env[OS_COMPUTE_ENDPOINT].'),
    cfg.StrOpt('os-compute-endpoint-type',
               default=env('OS_COMPUTE_ENDPOINT_TYPE', 'publicURL'),
               help='Defaults to env[OS_COMPUTE_ENDPOINT_TYPE].'),
    cfg.StrOpt('os-compute-service-type',
               default=env('OS_COMPUTE_SERVICE_TYPE',
                           default='compute'),
               help="Defaults to env[OS_COMPUTE_SERVICE_TYPE], or "
                    "'dns'"),
    cfg.StrOpt('os-dns-endpoint',
               default=env('OS_DNS_ENDPOINT'),
               help='Specify an endpoint to use instead of '
                    'retrieving one from the service catalog '
                    '(via authentication). '
                    'Defaults to env[OS_DNS_ENDPOINT].'),
    cfg.StrOpt('os-dns-endpoint-type',
               default=env('OS_DNS_ENDPOINT_TYPE', 'publicURL'),
               help='Defaults to env[OS_DNS_ENDPOINT_TYPE].'),
    cfg.StrOpt('os-dns-service-type',
               default=env('OS_DNS_SERVICE_TYPE', default='dns'),
               help=("Defaults to env[OS_DNS_SERVICE_TYPE], or "
                     "'dns'")),
    cfg.StrOpt('os-cacert',
               default=env('OS_CACERT'),
               help=('CA certificate bundle file. Defaults to '
                     'env[OS_CACERT]')),
    cfg.BoolOpt('insecure', default=True,
                help="Explicitly allow 'insecure' SSL requests"),
    cfg.BoolOpt('all-tenants', default=True,
                help="Allows to list all domains from all tenants"),
    cfg.BoolOpt('edit-managed', default=True,
                help='Allows to edit records that are marked as '
                     'managed')
]

CONF = cfg.CONF
CONF.register_cli_opts(opts)


def main():
    CONF(sys.argv[1:], project='designate-init')
    designate_init.initialize()
