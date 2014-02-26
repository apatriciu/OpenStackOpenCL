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
openclbuffers interface
"""

from novaclient import base

class OpenCLBuffer(base.Resource):
    def __repr__(self):
        return "<OpenCL Buffer Id: %s>" % self.id

class OpenCLBufferId(base.Resource):
    def __repr__(self):
        return "<OpenCL Buffer: %s Id>" % self.id

class OpenCLBuffersManager(base.Manager):
    
    resource_class = OpenCLBuffer

    def list(self):
        """List all opencl buffers."""
        url = "/os-openclbuffers"
        resp = self._list(url, "Buffers", obj_class=OpenCLBufferId)
        bufferList = []
        for buf in resp:
            bufferList.append( buf.id )
        return bufferList

    def show(self, buffer_id):
        """show the parameters of buffer id"""
        url = "/os-openclbuffers/%d" % buffer_id
        return self._get(url, "Buffer")

    def create(self, Context, Size, listProperties):
        """
        Create a new buffer on context Context
        with properties listProperties
        """
        url = "/os-openclbuffers"
        body = {'Context': Context, 'MEM_SIZE': Size, 'BufferProperties': []}
        resp = self._create(url, body, 'CreateResp', return_raw=True)
        return (resp['id'], resp['CL_ERROR_CODE']) 

    def retain(self, buffer_id):
        """
        Retain a buffer
        """
        url = "/os-openclbuffers/%d/retain" % buffer_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def release(self, buffer_id):
        """
        Release a buffer
        """
        url = "/os-openclbuffers/%d/release" % buffer_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
        

