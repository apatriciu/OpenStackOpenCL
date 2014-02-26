# vim: tabstop=4 shiftwidth=4 softtabstop=4

# OpenCL interface for OpenStack
# This is a server component that will receive
# OpenCL requests

from nova.api.openstack import extensions
from nova.api.openstack import xmlutil
from nova.api.openstack import wsgi
from nova import compute
from nova.openstack.common.gettextutils import _
from nova.openstack.common import log as logging
from nova.OpenCL import openclinterfaceutils
from webob import exc
from nova.OpenCL import OpenCLProgramsAPI

import sys

LOG = logging.getLogger(__name__)

# OpenCLPrograms controller
# XML Builder for programs.index(...)
class ProgramsIndexResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ListPrograms')
        element = xmlutil.SubTemplateElement(root, 'Programs')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for programs.show(...) resp
class ProgramsShowResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ProgramsShowResp')
        element = xmlutil.SubTemplateElement(root, 'Program')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        subelement = xmlutil.SubTemplateElement(element, 'Context')
        subelement = xmlutil.SubTemplateElement(element, 'ListDevices')
        subsubelement = xmlutil.SubTemplateElement(element, 'Device')
        element = xmlutil.SubTemplateElement(element, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for programs.buildinfo(...) resp
class ProgramsBuildInfoResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ProgramsBuildInfo')
        sroot = xmlutil.SubTemplateElement('BuildInfoResp')
        element = xmlutil.SubTemplateElement(sroot, 'ParamData')
        element = xmlutil.SubTemplateElement(sroot, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

class OpenCLPrograms(object):
    def __init__(self):
        self.opencl_api = OpenCLProgramsAPI.API()
        super(OpenCLPrograms, self).__init__()

#handle for index command; returns all programs
    @wsgi.serializers(xml=ProgramsIndexResp)
    def index(self, req):
        ProgramsList = []
        try:
            ProgList = self.opencl_api.ListPrograms()
            for oc_program in ProgList:
                ProgramsList.append({'id': oc_program})
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'Programs': ProgramsList}

#handle for the create command; returns the URI of the new program
    @wsgi.serializers(xml=openclinterfaceutils.CreateResp)
    def create(self, req, body):
        newProgram = 0
        nErr = 0
        try:
            contextID = int(body['Context'])
            ProgramStrings = []
            for PSD in body['ListProgramStrings']:
                ProgramStrings.append(str(PSD['ProgramString']))
            newProgram, nErr = self.opencl_api.CreateProgram(contextID, ProgramStrings)
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'CreateResp': {'id': newProgram, 'CL_ERROR_CODE': nErr}}

#handle for show request
    @wsgi.serializers(xml=ProgramsShowResp)
    def show(self, req, id):
        ProgramInfo = {}
        ProgramInfo['id'] = int(id)
        nErr = 0
        try:
            ProgInfo, nErr = self.opencl_api.GetProgramProperties(int(id))
            ProgramInfo['Context'] = ProgInfo['Context']
            lstDev = []
            for dev in ProgInfo['Devices']:
                lstDev.append({'Device': dev})
            ProgramInfo['ListDevices'] = lstDev
            ProgramInfo['CL_ERROR_CODE'] = nErr
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.show method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'Program': ProgramInfo}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def retain(self, req, id, body):
        '''
        Retain the program
        '''
        try:
            nErr = self.opencl_api.RetainProgram(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.retain method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def release(self, req, id, body):
        '''
        Release the program
        '''
        try:
            nErr = self.opencl_api.ReleaseProgram(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.release method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def build(self, req, id, body):
        '''
        Builds the program
        '''
        nErr = 0
        try:
            listDevicesIDs = []
            for dev_dict_pair in body['ListDevices']:
                listDevicesIDs.append( dev_dict_pair['Device'] )
            buildOptions = "" #body['CompileOptions']
            nErr = self.opencl_api.BuildProgram(int(id), listDevicesIDs, buildOptions)
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.build method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=ProgramsBuildInfoResp)
    def buildinfo(self, req, id, body):
        '''
        Returns build info
        '''
        nErr = 0
        BuildInfoParam = ""
        try:
            device = int(body['Device'])
            buildInfo = str(body['ParamName'])
            dictRespBuildInfoData, nErr = self.opencl_api.GetProgramBuildInfo(int(id), device, buildInfo)
            BuildInfoParam = dictRespBuildInfoData[ buildInfo ]
        except:
            LOG.debug(_("Exception caught in OpenCLPrograms.buildinfo method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'BuildInfoResp': {'CL_ERROR_CODE': nErr, 'ParamData': BuildInfoParam}}

