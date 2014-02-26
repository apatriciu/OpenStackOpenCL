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
import binascii
from nova.OpenCL import OpenCLKernelsAPI
import sys
from webob import exc

LOG = logging.getLogger(__name__)

# OpenCLKernels controller
# XML Builder for kernels.index(...)
class KernelsIndexResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ListKernels')
        element = xmlutil.SubTemplateElement(root, 'Kernels')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for kernels.show(...) resp
class KernelsShowResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('KernelsShowResp')
        element = xmlutil.SubTemplateElement(root, 'Kernel')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        subelement = xmlutil.SubTemplateElement(element, 'KernelFunctionName')
        subelement = xmlutil.SubTemplateElement(element, 'KernelNumArgs')
        subelement = xmlutil.SubTemplateElement(element, 'Context')
        subelement = xmlutil.SubTemplateElement(element, 'Device')
        subelement = xmlutil.SubTemplateElement(element, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

class OpenCLKernels(object):
    def __init__(self):
        self.opencl_kernels_api = OpenCLKernelsAPI.API()
        super(OpenCLKernels, self).__init__()

#handle for index command; returns all programs
    @wsgi.serializers(xml=KernelsIndexResp)
    def index(self, req):
        KernelsList = []
        nErr = 0
        try:
            KList = self.opencl_kernels_api.ListKernels()
            nErr = 0
            for oc_kernel in KList:
                KernelsList.append({'id': oc_kernel})
        except:
            LOG.debug(_("Exception caught in OpenCLKernels.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'Kernels': KernelsList}

#handle for the create command; returns the URI of the new program
    @wsgi.serializers(xml=openclinterfaceutils.CreateResp)
    def create(self, req, body):
        newKernel = 0
        nErr = 0
        try:
            program = int(body['Program'])
            kernelName = str(body['KernelName'])
            newKernel, nErr = self.opencl_kernels_api.CreateKernel(program, kernelName)
        except:
            LOG.debug(_("Exception caught in OpenCLKernels.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'CreateResp': {'id': newKernel, 'CL_ERROR_CODE': nErr}}

#handle for show request
    @wsgi.serializers(xml=KernelsShowResp)
    def show(self, req, id):
        KernelInfo = {}
        KernelInfo['id'] = int(id)
        nErr = 0
        try:
            KernelInfoDict, nErr = self.opencl_kernels_api.GetKernelProperties(int(id))
            KernelInfo['KernelFunctionName'] = KernelInfoDict['KernelFunctionName']
            KernelInfo['KernelNumArgs'] = 1 # not implemented yet
            KernelInfo['Context'] = KernelInfoDict['Context']
            KernelInfo['Device'] = 0 # not implemented yet
            KernelInfo['CL_ERR_CODE'] = nErr
            KernelInfo['Program'] = KernelInfoDict['Program']
        except:
            LOG.debug(_("Exception caught in OpenCLKernels.show method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'Kernel': KernelInfo}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def retain(self, req, id, body):
        '''
        Retain the kernel
        '''
        nErr = 0
        try:
            nErr = self.opencl_kernels_api.RetainKernel(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLKernels.RetainKernel method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def release(self, req, id, body):
        '''
        Release the kernel
        '''
        nErr = 0
        try:
            nErr = self.opencl_kernels_api.ReleaseKernel(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLKernels.ReleaseKernel method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def setkernelarg(self, req, id, body):
        '''
        Set the argument of a kernel
        '''
        nErr = 0
        try:
            paramIndex = int(body['ArgIndex'])
            paramDict = {}
            if body.has_key('LocalMemory'):
                paramDict = {'LocalMemory': int(body['LocalMemory'])}
            if body.has_key('DeviceMemoryObject'):
                paramDict = {'DeviceMemoryObject': int(body['DeviceMemoryObject'])}
            if body.has_key('HostValue'):
                paramDict = {'HostValue': str(body['HostValue'])}
            self.opencl_kernels_api.KernelSetArgument(int(id), paramIndex, paramDict)
        except:
            LOG.debug(_("Exception caught in OpenCLKernels.setkernelarg method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}


