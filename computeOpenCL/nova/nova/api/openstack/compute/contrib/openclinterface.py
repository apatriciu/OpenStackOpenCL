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
from nova.OpenCL import OpenCLDevicesAPI
from nova.OpenCL import OpenCLContextsAPI
from nova.api.openstack.compute.contrib import openclbuffersinterface
from nova.api.openstack.compute.contrib import openclkernelsinterface
from nova.api.openstack.compute.contrib import openclprogramsinterface
from nova.api.openstack.compute.contrib import openclqueuesinterface

# opencl devices controller

LOG = logging.getLogger(__name__)

# XML Builder for devices.index(...)
class DevicesIndexResult(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('GPUDevicesList')
        element = xmlutil.SubTemplateElement(root, 'Devices')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for devices.show(...)
class DevicesShowResult(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('DevicesShowResult')
        elementDeviceProperties = xmlutil.SubTemplateElement(root, 'Device')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'id')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_TYPE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_MAX_COMPUTE_UNITS')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_MAX_WORK_ITEM_SIZES')
        subelement = xmlutil.SubTemplateElement(element, 'WORK_ITEM_SIZE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_MAX_WORKGROUP_SIZE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_GLOBAL_MEM_SIZE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_MAX_MEM_ALLOCATION_SIZE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_SINGLE_FP_CONFIG')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_LOCAL_MEM_TYPE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_LOCAL_MEM_SIZE')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_DEVICE_NAME')
        element = xmlutil.SubTemplateElement(elementDeviceProperties, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

#controller class
class OpenCLDevices(object):
    def __init__(self):
        self.opencl_api = OpenCLDevicesAPI.API()
        #self.ext_mgr = ext_mgr;
        super(OpenCLDevices, self).__init__()

#handle for index command this gets all OpenCL platforms available
    @wsgi.serializers(xml=DevicesIndexResult)
    def index(self, req):
        ctxt = req.environ['nova.context']
        DeviceList = []
        nErr = 0
        try:
            (GPUList, nErr) = self.opencl_api.ListDevices()
            for device in GPUList:
                DeviceList.append({'id': device})
        except:
            LOG.debug(_("Exception caught in OpenCLDevices.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'Devices': DeviceList}

#handle for index command this gets all OpenCL platforms available
    @wsgi.serializers(xml=DevicesShowResult)
    def show(self, req, id):
        nid = int(id)
        DeviceProperties = {'id', nid}
        nErr = 0
        try:
            DeviceProperties, nErr = self.opencl_api.GetDeviceProperties(nid)
            DeviceProperties['CL_ERROR_CODE'] = nErr
        except:
            LOG.debug(_("Exception caught in OpenCLDevices.show method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'Device': DeviceProperties}

# OpenCLContexts controller
# XML Builder for contexts.index(...)
class ContextsIndexResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ListContexts')
        element = xmlutil.SubTemplateElement(root, 'Contexts')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for contexts.show(...) resp
class ContextsShowResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ContextsShowResult')
        element = xmlutil.SubTemplateElement(root, 'Context')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        subelement = xmlutil.SubTemplateElement(element, 'CL_CONTEXT_NUM_DEVICES')
        subelement = xmlutil.SubTemplateElement(element, 'ListDevices')
        subsubelement = xmlutil.SubTemplateElement(subelement, 'Device')
        subelement = xmlutil.SubTemplateElement(element, 'ListContextProperties')
        ssubelement = xmlutil.SubTemplateElement(subelement, 'PropertyName')
        ssubelement = xmlutil.SubTemplateElement(subelement, 'PropertyValue')
        element = xmlutil.SubTemplateElement(element, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

class OpenCLContexts(object):
    def __init__(self):
        self.opencl_api = OpenCLContextsAPI.API()
        super(OpenCLContexts, self).__init__()

#handle for index command; returns all contexts
    @wsgi.serializers(xml=ContextsIndexResp)
    def index(self, req):
        try:
            nErr = 0
            CtxsList = self.opencl_api.ListContexts()
            ContextList = []
            for context in CtxsList:
                ContextList.append({'id': context})
            return {'Contexts': ContextList}
        except:
            LOG.debug(_("Exception caught in OpenCLContexts.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()

#handle for the create command; returns the URI of the new context
    @wsgi.serializers(xml=openclinterfaceutils.CreateResp)
    def create(self, req, body):
        try:
            listDevices = body['Devices']
            dictProperties = body['Properties']
            listDevicesIDs = []
            for dev in listDevices:
                LOG.debug(_("OpenCLContexts.create method Device : %i"), dev['Device'])
                listDevicesIDs.append(dev['Device'])
            newContext, nErr = self.opencl_api.CreateContext(listDevicesIDs, dictProperties)
            return {'CreateResp': {'id': newContext, 'CL_ERROR_CODE': nErr}}
        except:
            LOG.debug(_("Exception caught in OpenCLContexts.create method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()

#handle for index command this gets all OpenCL platforms available
    @wsgi.serializers(xml=ContextsShowResp)
    def show(self, req, id):
        try:
            nid = int(id)
            Context, nErr = self.opencl_api.GetContextProperties(nid)
            ContextInfo = {}
            ContextInfo['id'] = Context['id']
            ListContextDevices = Context['Devices']
            ContextInfo['CL_CONTEXT_NUM_DEVICES'] =  len(ListContextDevices)
            ListContextDevicesOut = []
            for dev in ListContextDevices:
                ListContextDevicesOut.append({'Device': dev})
            ContextInfo['ListDevices'] = ListContextDevicesOut
            ContextInfo['ListContextProperties'] =  []
            ContextInfo['CL_ERROR_CODE'] = nErr
            return {'Context': ContextInfo}
        except:
            LOG.debug(_("Exception caught in OpenCLContexts.show method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def retain(self, req, id, body):
        '''
        Retain the context
        '''
        try:
            nErr = self.opencl_api.RetainContext(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLContexts.retain method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=openclinterfaceutils.OpenCLErrorResp)
    def release(self, req, id, body):
        '''
        Release the context
        '''
        try:
            nErr = self.opencl_api.ReleaseContext(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLContexts.release method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

class Openclinterface(extensions.ExtensionDescriptor):
    """ OpenCL interface implementation as nova compute extension """
    name = "openclinterface"
    alias = "os-openclinterface"
    namespace = "http://docs.openstack.org/compute/ext/openclinterface/api/v1.1"
    updated = "2013-12-12T00:00:00+00:00"

    def get_resources(self):
    # register OpenCLDevices RESTful resource
        resources = []
        #initialize the OpenCLInterface if there are any errors do not register any resources

        res = extensions.ResourceExtension(
            'os-opencldevices', 
            controller = OpenCLDevices())
        resources.append(res)
        res = extensions.ResourceExtension(
            'os-openclcontexts',
            controller = OpenCLContexts(),
            member_actions = {"retain": "POST", 
                              "release": "POST", })
        resources.append(res)
        res = extensions.ResourceExtension(
            'os-openclqueues',
            controller = openclqueuesinterface.OpenCLQueues(),
            member_actions = {"retain": "POST", 
                              "release": "POST",
                              "enqueuereadbuffer": "POST", 
                              "enqueuewritebuffer": "POST", 
                              "enqueuecopybuffer": "POST", 
                              "enqueuendrangekernel": "POST", 
                              "enqueuetask": "POST", 
                              "enqueuebarrier": "POST",
                              "finish": "POST",})
        resources.append(res)
        res = extensions.ResourceExtension(
            'os-openclbuffers',
            controller = openclbuffersinterface.OpenCLBuffers(),
            member_actions = {"retain": "POST", 
                              "release": "POST", })
        resources.append(res)
        res = extensions.ResourceExtension(
            'os-openclprograms',
            controller = openclprogramsinterface.OpenCLPrograms(),
            member_actions = {"retain": "POST", 
                              "release": "POST", 
                              "build": "POST",
                              "buildinfo": "POST",})
        resources.append(res)
        res = extensions.ResourceExtension(
            'os-openclkernels',
            controller = openclkernelsinterface.OpenCLKernels(),
            member_actions = {"retain": "POST", 
                              "release": "POST", 
                              "setkernelarg": "POST",})
        resources.append(res)
        return resources

