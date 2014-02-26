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
openclprograms interface
"""

from novaclient import base

class OpenCLProgram(base.Resource):
    def __repr__(self):
        return "<OpenCL Program: %d>" % self.id

class OpenCLProgramId(base.Resource):
    def __repr__(self):
        return "<OpenCL Program: %d>" % self.id

class OpenCLProgramsManager(base.Manager):
    
    resource_class = OpenCLProgram

    def list(self):
        """List all opencl programs."""
        url = "/os-openclprograms"
        resp = self._list(url, "Programs", obj_class=OpenCLProgramId)
        listPrograms = []
        for prog in resp:
            listPrograms.append(prog.id)
        return listPrograms

    def show(self, program_id):
        """show the parameters of program id"""
        url = "/os-openclprograms/%d" % program_id
        return self._get(url, "Program")

    def create(self, Context, ListProgramStrings):
        """
        Create a new program on context Context
        with ListProgramStrings code
        """
        url = "/os-openclprograms"
        Program = []
        for pstr in ListProgramStrings:
            Program.append({'ProgramString': pstr})
        body = {'Context': Context, 'ListProgramStrings': Program}
        resp = self._create(url, body, 'CreateResp', return_raw=True)
        return (resp['id'], resp['CL_ERROR_CODE']) 

    def retain(self, program_id):
        """
        Retain a program
        """
        url = "/os-openclprograms/%d/retain" % program_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def release(self, program_id):
        """
        Release a program
        """
        url = "/os-openclprograms/%d/release" % program_id
        body = None
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)
        
    def build(self, program_id, list_devices, build_options):
        """
        build a program
        """
        url = "/os-openclprograms/%d/build" % program_id
        list_devices_tagged = []
        for dev in list_devices:
            list_devices_tagged.append({'Device': dev})
        body = {'ListDevices': list_devices_tagged, 'CompileOptions': build_options}
        return self._create(url, body, "CL_ERROR_CODE", return_raw=True)

    def buildinfo(self, program_id, device, param_name):
        """
        Retrieves build info for a program
        """
        url = "/os-openclprograms/%d/buildinfo" % program_id
        body = {'Device': device, 'ParamName': param_name}
        resp = self._create(url, body, "BuildInfoResp", return_raw=True)
        return (resp['ParamData'], resp['CL_ERROR_CODE'])
        
