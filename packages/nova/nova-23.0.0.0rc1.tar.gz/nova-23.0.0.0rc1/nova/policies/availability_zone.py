# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
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

from oslo_policy import policy

from nova.policies import base


POLICY_ROOT = 'os_compute_api:os-availability-zone:%s'


availability_zone_policies = [
    policy.DocumentedRuleDefault(
        name=POLICY_ROOT % 'list',
        check_str=base.RULE_ANY,
        description="List availability zone information without host "
        "information",
        operations=[
            {
                'method': 'GET',
                'path': '/os-availability-zone'
            }
        ],
        scope_types=['system', 'project']),
    policy.DocumentedRuleDefault(
        name=POLICY_ROOT % 'detail',
        check_str=base.SYSTEM_READER,
        description="List detailed availability zone information with host "
        "information",
        operations=[
            {
                'method': 'GET',
                'path': '/os-availability-zone/detail'
            }
        ],
        scope_types=['system'])
]


def list_rules():
    return availability_zone_policies
