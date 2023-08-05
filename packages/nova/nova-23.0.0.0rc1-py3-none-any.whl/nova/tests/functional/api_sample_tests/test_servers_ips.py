# Copyright 2012 Nebula, Inc.
# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nova.tests import fixtures as nova_fixtures
from nova.tests.functional.api_sample_tests import test_servers


class ServersIpsJsonTest(test_servers.ServersSampleBase):
    sample_dir = 'server-ips'

    def test_get(self):
        # Test getting a server's IP information.
        uuid = self._post_server()
        response = self._do_get('servers/%s/ips' % uuid)
        self._verify_response('server-ips-resp', {}, response, 200)

    def test_get_by_network(self):
        # Test getting a server's IP information by network id.
        server_uuid = self._post_server()
        network_label = nova_fixtures.NeutronFixture.network_1['name']
        response = self._do_get('servers/%s/ips/%s' % (
            server_uuid, network_label))
        self._verify_response('server-ips-network-resp', {}, response, 200)
