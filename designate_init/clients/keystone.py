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

from keystoneclient.v2_0 import client as keystone_client
from oslo_config import cfg


CONF = cfg.CONF


class Client(keystone_client.Client):

    def __init__(self):
        super(Client, self).__init__(
            username=CONF.os_username,
            password=CONF.os_password,
            token=CONF.os_token,
            tenant_id=CONF.os_tenant_id,
            tenant_name=CONF.os_tenant_name,
            auth_url=CONF.os_auth_url,
            region_name=CONF.os_region_name
        )
