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

from novaclient.v2 import client as nova_client
from oslo_config import cfg


CONF = cfg.CONF


class Client(nova_client.Client):

    def __init__(self):
        super(Client, self).__init__(
            username=CONF.os_username,
            api_key=CONF.os_password,
            project_id=CONF.os_tenant_name,
            auth_url=CONF.os_auth_url,
            # insecure=CONF.insecure,
            # region_name=CONF.os_region_name,
            # endpoint_type=CONF.os_compute_endpoint_type,
            # service_type=CONF.os_compute_service_type,
            # auth_token=CONF.os_token,
            # cacert=CONF.os_cacert,
            # tenant_id=CONF.os_tenant_id
        )

    def get_all_servers(self):
        """Get all servers without 1000 limit."""
        marker = None

        while True:
            servers = self.servers.list(search_opts={'all_tenants': True},
                                        limit=1000, marker=marker)

            try:
                marker = servers[-1].id
            except IndexError:
                raise StopIteration()

            for server in servers:
                yield server
