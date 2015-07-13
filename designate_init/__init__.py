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

import copy
import json
import re

# from designateclient.v1 import domains
# from designateclient.v1 import records
from oslo_config import cfg
import requests
import six

from designate_init.clients import designate as designate_client
from designate_init.clients import keystone as keystone_client
from designate_init.clients import nova as nova_client


CONF = cfg.CONF

IPV4_PATTERN = re.compile(r'\d{0,3}\.\d{0,3}\.\d{0,3}')

_DESIGNATE_URL = None


def get_designate_url():
    global _DESIGNATE_URL
    if _DESIGNATE_URL is None:
        _DESIGNATE_URL = CONF.os_auth_url.replace('5000/v2.0', '9001')

    return _DESIGNATE_URL


def get_ip_data(ip_addr):
    ip_data = {}
    # TODO(mrostecki): Add v6 support
    if not IPV4_PATTERN.search(ip_addr):
        return None
    ip_addr = ip_addr.split('.')
    for i in six.moves.xrange(4):
        ip_data['octet%d' % i] = ip_addr[i]

    return ip_data


# def get_ptr_domain(designate, ip_data):
#     domain_name = '%(octet1)s.%(octet0)s.in-addr.arpa.' % ip_data
#     ptr_domains = designate.domains.list()
#     filtered_domains = filter(lambda domain: domain.name == domain_name,
#                               ptr_domains)
#     if len(filtered_domains) == 1:
#         domain = filtered_domains[0]
#     elif len(filtered_domains) == 0:
#         domain = domains.Domain(name=domain_name, email=CONF.email)
#         designate.domains.create(domain)
#     else:
#         raise Exception()
#
#     return domain


def create_records(designate, keystone, server, ip):
    domain = designate.domains.get(CONF.domain_id)
    ip_data = get_ip_data(ip)

    if ip_data is None:
        return

    format_data = copy.deepcopy(server.__dict__)
    format_data.update({
        'domain': domain.name,
        'tenant_name': keystone.tenants.get(server.tenant_id).name
    })
    format_data.update(ip_data)

    record_name = CONF.format % format_data

    # record = records.Record(name=record_name,
    #                         type='A',
    #                         data=ip,
    #                         managed_resource_type="instance",
    #                         managed_resource_id=server.id)
    # designate.records.create(domain, record)
    r = {
        "name": record_name,
        "type": "A",
        "data": ip,
        "managed_resource_type": "instance",
        "managed_resource_id": server.id
    }
    requests.post(
        "{}/v1/domains/{}/records".format(get_designate_url(), domain.id),
        data=json.dumps(r),
        headers={
            'content-type': 'application/json'
        }
    )

    if CONF.create_wildcard:
        # wildcard_record = records.Record(name='*.{}'.format(record_name),
        #                                  type='A',
        #                                  data=ip,
        #                                  managed_resource_type="instance",
        #                                  managed_resource_id=server.id)
        # designate.records.create(domain, wildcard_record)
        r = {
            "name": "*." + record_name,
            "type": "A",
            "data": ip,
            "managed_resource_type": "instance",
            "managed_resource_id": server.id,
        }
        requests.post(
            "{}/v1/domains/{}/records".format(get_designate_url(), domain.id),
            data=json.dumps(r),
            headers={
                'content-type': 'application/json',
            },
        )

    if CONF.create_ptr:
        # ptr_domain = get_ptr_domain(ip_data)
        ptr_record_name = CONF.ptr_format % format_data
        # ptr_record = records.Record(name=ptr_record_name,
        #                             type='PTR',
        #                             data=record_name,
        #                             managed_resource_type="instance",
        #                             managed_resource_id=server.id)
        # designate.records.create(domain, ptr_record)
        r = {
            "name": ptr_record_name,
            "type": "PTR",
            "data": record_name,
            "managed_resource_type": "instance",
            "managed_resource_id": server.id,
        }
        requests.post(
            "{}/v1/domains/{}/records".format(get_designate_url(), domain.id),
            data=json.dumps(r),
            headers={
                'content-type': 'application/json',
            },
        )


def initialize_server(designate, keystone, server):
    for network, ips in six.iteritems(server.networks):
        if (CONF.filter_networks is not None and network in
                CONF.filter_networks) or CONF.filter_networks is None:
            for ip in ips:
                create_records(designate, keystone, server, ip)


def initialize():
    designate = designate_client.ClientV1()
    keystone = keystone_client.Client()
    nova = nova_client.Client()

    servers = nova.get_all_servers()

    for server in servers:
        initialize_server(designate, keystone, server)
