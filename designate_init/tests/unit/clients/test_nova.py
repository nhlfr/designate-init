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

import mock
import testtools

from designate_init.clients import nova as nova_client
from designate_init.tests import fakes


class TestNovaClient(testtools.TestCase):

    @mock.patch('novaclient.v2.servers.ServerManager.list')
    @mock.patch('designate_init.clients.nova.CONF')
    def test_get_all_servers(self, conf, servers_list):
        servers_list.side_effect = [
            [
                fakes.FakeServer(1, 'server_1'),
                fakes.FakeServer(2, 'server_2')
            ], [
                fakes.FakeServer(3, 'server_3'),
                fakes.FakeServer(4, 'server_4')
            ]
        ]

        client = nova_client.Client()

        servers = client.get_all_servers()

        first_server = next(servers)
        self.assertEqual(first_server.id, 1)
        self.assertEqual(first_server.name, 'server_1')
        second_server = next(servers)
        self.assertEqual(second_server.id, 2)
        self.assertEqual(second_server.name, 'server_2')
        third_server = next(servers)
        self.assertEqual(third_server.id, 3)
        self.assertEqual(third_server.name, 'server_3')
        fourth_server = next(servers)
        self.assertEqual(fourth_server.id, 4)
        self.assertEqual(fourth_server.name, 'server_4')

        self.assertRaises(StopIteration, next, servers)
