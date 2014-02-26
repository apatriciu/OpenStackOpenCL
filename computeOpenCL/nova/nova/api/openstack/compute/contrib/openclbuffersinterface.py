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
import sys
from webob import exc
from nova.OpenCL import OpenCLBuffersAPI

LOG = logging.getLogger(__name__)

# OpenCLBuffers controller
# XML Builder for buffers.index(...)
class BuffersIndexResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ListBuffers')
        element = xmlutil.SubTemplateElement(root, 'Buffers')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        element = xmlutil.SubTemplateElement(root, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for buffers.show(...) resp
class BuffersShowResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('BuffersShowResp')
        element = xmlutil.SubTemplateElement(root, 'Buffer')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        subelement = xmlutil.SubTemplateElement(element, 'Context')
        subelement = xmlutil.SubTemplateElement(element, 'MEM_SIZE')
        subelement = xmlutil.SubTemplateElement(element, 'BufferProperties')
        ssubelement = xmlutil.SubTemplateElement(subelement, 'PropertyName')
        ssubelement = xmlutil.SubTemplateElement(subelement, 'PropertyValue')
        element = xmlutil.SubTemplateElement(element, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

class OpenCLBuffers(object):
    def __init__(self):
        self.opencl_api = OpenCLBuffersAPI.API()
        super(OpenCLBuffers, self).__init__()

#handle for index command; returns all Buffers
    @wsgi.serializers(xml=BuffersIndexResp)
    def index(self, req):
        try:
            BuffList = self.opencl_api.ListBuffers()
            BuffersList = []
            for oc_buffer in BuffList:
                BuffersList.append({'id': oc_buffer})
        except:
            LOG.debug(_("Exception caught in OpenCLBuffers.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'Buffers': BuffersList}

#handle for the create command; returns the URI of the new buffer
    @wsgi.serializers(xml=openclinterfaceutils.CreateResp)
    def create(self, req, body):
        try:
            bufferContext = body['Context']
            bufferSize = body['MEM_SIZE']
            bufferAttribs = body['BufferProperties']
            newBuffer, nErr = self.opencl_api.CreateBuffer(bufferContext, bufferSize, bufferAttribs)
        except:
            LOG.debug(_("Exception caught in OpenCLBuffers.create method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'CreateResp': {'id': newBuffer, 'CL_ERROR_CODE': nErr}}

#handle for show request
    @wsgi.serializers(xml=BuffersShowResp)
    def show(self, req, id):
        BufferInfo = {}
        try:
            bufInfo, nErr = self.opencl_api.GetBufferProperties(int(id))
            BufferInfo['id'] = bufInfo['id']
            BufferInfo['Context'] = bufInfo['Context']
            BufferInfo['MEM_SIZE'] = bufInfo['Size']
            BufferInfo['BufferProperties'] = []
            BufferInfo['CL_ERROR_CODE'] = nErr
        except:
            LOG.debug(_("Exception caught in OpenCLBuffers.show method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'Buffer': BufferInfo}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def retain(self, req, id, body):
        '''
        Retain the buffer
        '''
        try:
            nErr = self.opencl_api.RetainBuffer(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLBuffers.retain method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def release(self, req, id, body):
        '''
        Release the buffer
        '''
        try:
            nErr = self.opencl_api.ReleaseBuffer(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLBuffers.retain method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

