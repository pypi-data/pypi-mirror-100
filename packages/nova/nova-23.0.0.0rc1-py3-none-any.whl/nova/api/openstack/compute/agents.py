# Copyright 2012 IBM Corp.
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


from webob import exc

from nova.api.openstack import wsgi


class AgentController(wsgi.Controller):
    """(Removed) Controller for agent resources.

    This was removed during the Victoria release along with the XenAPI driver.
    """
    @wsgi.expected_errors(410)
    def index(self, req):
        raise exc.HTTPGone()

    @wsgi.expected_errors(410)
    def update(self, req, id, body):
        raise exc.HTTPGone()

    @wsgi.expected_errors(410)
    def delete(self, req, id):
        raise exc.HTTPGone()

    @wsgi.expected_errors(410)
    def create(self, req, body):
        raise exc.HTTPGone()
