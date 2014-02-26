# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from novaclient.v1_1 import client
from novaclient.tests.v1_1 import fakes
import binascii

class FakeClient(fakes.FakeClient):
    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, 'username', 'password',
                               'project_id', 'auth_url',
                               extensions=kwargs.get('extensions'))
        self.client = FakeHTTPClient(**kwargs)


class FakeHTTPClient(fakes.FakeHTTPClient):
# opencldevices responses
    def get_os_opencldevices(self):
        return (200, {}, {'Devices': [{'id': 0}]})

    def get_os_opencldevices_0(self, **kw):
        return (200, {}, {'Device': {'id': 0, 'CL_DEVICE_TYPE': "CL_GPU", 'CL_DEVICE_MAX_COMPUTE_UNITS': 5, 
            'CL_ERROR_CODE': 0}})

# openclcontexts responses
    def get_os_openclcontexts(self):
        return (200, {}, {'Contexts': [{'id': 1}]})

    def get_os_openclcontexts_0(self, **kw):
        return (200, {}, {'Context': {'id': 1, 'CL_CONTEXT_NUM_DEVICES': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclcontexts(self, **kw):
        return (201, {}, {'CreateResp': {'id': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclcontexts_1_retain(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclcontexts_1_release(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

# openclqueues responses
    def get_os_openclqueues(self):
        return (200, {}, {'Queues': [{'id': 1}]})

    def get_os_openclqueues_0(self, **kw):
        return (200, {}, {'Queue': {'id': 1, 'Device': 1, 'Context': 1, 
            'CL_ERROR_CODE': 0}})

    def post_os_openclqueues(self, **kw):
        return (201, {}, {'CreateResp': {'id': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclqueues_1_retain(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_release(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_enqueuereadbuffer(self, **kw):
        b64Data = binascii.b2a_base64( '11111111' )
        return (202, {}, {'ReadBufferResp': {'CL_ERROR_CODE': 0, 'Data': b64Data}})

    def post_os_openclqueues_1_enqueuewritebuffer(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_enqueuecopybuffer(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_enqueuendrangekernel(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_enqueuetask(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_enqueuebarrier(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclqueues_1_finish(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

# openclbuffers responses
    def get_os_openclbuffers(self):
        return (200, {}, {'Buffers': [{'id': 1}]})

    def get_os_openclbuffers_0(self, **kw):
        return (200, {}, {'Buffer': {'id': 1, 'Context': 1, 'MEM_SIZE': 128, 
            'CL_ERROR_CODE': 0}})

    def post_os_openclbuffers(self, **kw):
        return (201, {}, {'CreateResp': {'id': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclbuffers_1_retain(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclbuffers_1_release(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

# openclprograms responses
    def get_os_openclprograms(self):
        return (200, {}, {'Programs': [{'id': 1}]})

    def get_os_openclprograms_0(self, **kw):
        return (200, {}, {'Program': {'id': 1, 'Context': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclprograms(self, **kw):
        return (201, {}, {'CreateResp': {'id': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclprograms_1_retain(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclprograms_1_release(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclprograms_1_build(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclprograms_1_buildinfo(self, **kw):
        return (202, {}, {'BuildInfoResp': {'CL_ERROR_CODE': 0, 'ParamData': 'CL_SUCCESS'}})

# openclkernels responses
    def get_os_openclkernels(self):
        return (200, {}, {'Kernels': [{'id': 1}]})

    def get_os_openclkernels_0(self, **kw):
        return (200, {}, {'Kernel': {'id': 1, 'Context': 1,
            'Program': 1,
            'KernelFunctionName': 'TestKernel',
            'KernelNumArgs': 2, 
            'CL_ERROR_CODE': 0}})

    def post_os_openclkernels(self, **kw):
        return (201, {}, {'CreateResp': {'id': 1, 'CL_ERROR_CODE': 0}})

    def post_os_openclkernels_1_retain(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclkernels_1_release(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

    def post_os_openclkernels_1_setkernelarg(self, **kw):
        return (202, {}, {'CL_ERROR_CODE': 0})

# tenant networks
    def get_os_tenant_networks(self):
        return (200, {}, {'networks': [{"label": "1", "cidr": "10.0.0.0/24",
                'project_id': '4ffc664c198e435e9853f2538fbcd7a7',
                'id': '1'}]})

    def get_os_tenant_networks_1(self, **kw):
        return (200, {}, {'network': {"label": "1", "cidr": "10.0.0.0/24",
                'project_id': '4ffc664c198e435e9853f2538fbcd7a7',
                'id': '1'}})

    def post_os_tenant_networks(self, **kw):
        return (201, {}, {'network': {"label": "1", "cidr": "10.0.0.0/24",
                'project_id': '4ffc664c198e435e9853f2538fbcd7a7',
                'id': '1'}})

    def delete_os_tenant_networks_1(self, **kw):
        return (204, {}, None)

    def get_os_baremetal_nodes(self, **kw):
        return (
            200, {}, {
                'nodes': [
                    {
                        "id": 1,
                        "instance_uuid": None,
                        "pm_address": "1.2.3.4",
                        "interfaces": [],
                        "cpus": 2,
                        "local_gb": 10,
                        "memory_mb": 5,
                        "pm_address": "2.3.4.5",
                        "pm_user": "pmuser",
                        "pm_password": "pmpass",
                        "prov_mac_address": "aa:bb:cc:dd:ee:ff",
                        "prov_vlan_id": 1,
                        "service_host": "somehost",
                        "terminal_port": 8080,
                    }
                ]
            }
        )

    def get_os_baremetal_nodes_1(self, **kw):
        return (
            200, {}, {
                'node': {
                    "id": 1,
                    "instance_uuid": None,
                    "pm_address": "1.2.3.4",
                    "interfaces": [],
                    "cpus": 2,
                    "local_gb": 10,
                    "memory_mb": 5,
                    "pm_user": "pmuser",
                    "pm_password": "pmpass",
                    "prov_mac_address": "aa:bb:cc:dd:ee:ff",
                    "prov_vlan_id": 1,
                    "service_host": "somehost",
                    "terminal_port": 8080,
                }
            }
        )

    def post_os_baremetal_nodes(self, **kw):
        return (
            200, {}, {
                'node': {
                    "id": 1,
                    "instance_uuid": None,
                    "cpus": 2,
                    "local_gb": 10,
                    "memory_mb": 5,
                    "pm_address": "2.3.4.5",
                    "pm_user": "pmuser",
                    "pm_password": "pmpass",
                    "prov_mac_address": "aa:bb:cc:dd:ee:ff",
                    "prov_vlan_id": 1,
                    "service_host": "somehost",
                    "terminal_port": 8080,
                }
            }
        )

    def delete_os_baremetal_nodes_1(self, **kw):
        return (202, {}, {})

    def post_os_baremetal_nodes_1_action(self, **kw):
        body = kw['body']
        action = list(body)[0]
        if action == "add_interface":
            return (
                200, {}, {
                    'interface': {
                        "id": 2,
                        "address": "bb:cc:dd:ee:ff:aa",
                        "datapath_id": 1,
                        "port_no": 2,
                    }
                }
            )
        elif action == "remove_interface":
            return (202, {}, {})
        else:
            return (500, {}, {})

    def post_os_assisted_volume_snapshots(self, **kw):
        return (202, {}, {'snapshot': {'id': 'blah', 'volumeId': '1'}})

    def delete_os_assisted_volume_snapshots_x(self, **kw):
        return (202, {}, {})
