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

from designateclient import v1 as designate_client_v1
from oslo_config import cfg


CONF = cfg.CONF


class ClientV1(designate_client_v1.Client):

    def __init__(self):
        super(ClientV1, self).__init__(
            endpoint=CONF.os_dns_endpoint,
            username=CONF.os_username,
            user_id=CONF.os_user_id,
            user_domain_id=CONF.os_user_domain_id,
            user_domain_name=CONF.os_user_domain_name,
            password=CONF.os_password,
            tenant_name=CONF.os_tenant_name,
            tenant_id=CONF.os_tenant_id,
            domain_name=CONF.os_domain_name,
            domain_id=CONF.os_domain_id,
            project_name=CONF.os_project_name,
            project_id=CONF.os_project_id,
            project_domain_name=CONF.os_project_domain_name,
            project_domain_id=CONF.os_project_domain_id,
            auth_url=CONF.os_auth_url,
            token=CONF.os_token,
            endpoint_type=CONF.os_dns_endpoint_type,
            region_name=CONF.os_region_name,
            service_type=CONF.os_dns_service_type,
            insecure=CONF.insecure,
            cacert=CONF.os_cacert
        )
