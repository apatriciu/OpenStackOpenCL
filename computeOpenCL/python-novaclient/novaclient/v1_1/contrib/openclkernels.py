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
openclkernels interface
"""

from novaclient import base
import binascii


class OpenCLKernel(base.Resource):
    def __repr__(self):
        return "<OpenCL Kernel: %d>" % self.id

class OpenCLKernelId(base.Resource):
    def __repr__(self):
        return "<OpenCL Kernel: %d>" % self.id

class OpenCLKernelsManager(base.Manager):
    
    resource_class = OpenCLKernel

    def list(self):
        """List all opencl kernels."""
        url = "/os-openclkernels"
        resp = self._list(url, "Kernels", obj_class=OpenCLKernelId)
        listKernels = []
        for kernel in resp:
            listKernels.append(kernel.id)
        return listKernels

    def show(self, kernel_id):
        """show the parameters of kernel id"""
        url = "/os-openclkernels/%d" % kernel_id
        return self._get(url, "Kernel")

    def create(self, Program, KernelName):
        """
        Create a new kernel on program
        """
        url = "/os-openclkernels"
        body = {'Program': Program, 'KernelName': KernelName}
        resp = self._create(url, body, 'CreateResp', return_raw=True)
        return (resp['id'], resp['CL_ERROR_CODE']) 

    def retain(self, kernel_id):
        """
        Retain a kernel
        """
        url = "/os-openclkernels/%d/retain" % kernel_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def release(self, kernel_id):
        """
        Release a kernel
        """
        url = "/os-openclkernels/%d/release" % kernel_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
        
    def setkernelarg(self, kernel_id, argindex, argtype, argvalue):
        """
        sets a kernel parameter
        """
        url = "/os-openclkernels/%d/setkernelarg" % kernel_id
        if argtype == "HostValue":
            bytearrayArgValue = bytearray( argvalue )
            argvalue = binascii.b2a_base64( bytearrayArgValue )
        body = {'ArgIndex': argindex, argtype: argvalue}
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
        
