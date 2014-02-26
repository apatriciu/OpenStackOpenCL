# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 IBM Corp.
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

"""
openclcontexts interface
"""

from novaclient import base

class OpenCLContext(base.Resource):
    def __repr__(self):
        return "<Context: %d>" % self.id

class OpenCLContextId(base.Resource):
    def __repr__(self):
        return "<Context: %d>" % self.id

class OpenCLContextsManager(base.Manager):
    
    resource_class = OpenCLContext

    def list(self):
        """List all opencl contexts."""
        url = "/os-openclcontexts"
        resp = self._list(url, "Contexts", obj_class=OpenCLContextId)
        listContexts = []
        for con in resp:
            listContexts.append(con.id)
        return listContexts

    def show(self, context_id):
        """show the parameters of device id"""
        url = "/os-openclcontexts/%d" % context_id
        return self._get(url, "Context")

    def create(self, listDevices, listProperties):
        """
        Create a new context using the devices in the list
        with properties listProperties
        """
        url = "/os-openclcontexts"
        listTaggedDevices = []
        for dev in listDevices:
            listTaggedDevices.append({"Device": dev})
        body = {"Devices" : listTaggedDevices, "Properties" : []}
        resp = self._create(url, body, 'CreateResp', return_raw=True)
        return (resp['id'], resp['CL_ERROR_CODE']) 

    def retain(self, context_id):
        """
        Retain a context
        """
        url = "/os-openclcontexts/%d/retain" % context_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def release(self, context_id):
        """
        Release a context
        """
        url = "/os-openclcontexts/%d/release" % context_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
        
