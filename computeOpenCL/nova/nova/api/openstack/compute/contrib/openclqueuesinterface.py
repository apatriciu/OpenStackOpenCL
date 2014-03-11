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
from nova.OpenCL import openclinterfaceutils as os_openclutils
from nova.OpenCL import OpenCLCommandQueuesAPI
import sys
from webob import exc
import binascii

LOG = logging.getLogger(__name__)

# OpenCLQueues controller
# XML Builder for queues.index(...)
class QueuesIndexResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('ListQueues')
        element = xmlutil.SubTemplateElement(root, 'Queues')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        return xmlutil.MasterTemplate(root, 1)

#XML Builder for queues.show(...) resp
class QueuesShowResp(xmlutil.TemplateBuilder):
    def construct(self):
        root = xmlutil.TemplateElement('QueuesShowResp')
        element = xmlutil.SubTemplateElement(root, 'Queue')
        subelement = xmlutil.SubTemplateElement(element, 'id')
        subelement = xmlutil.SubTemplateElement(element, 'Device')
        subelement = xmlutil.SubTemplateElement(element, 'Context')
        subelement = xmlutil.SubTemplateElement(element, 'ListQueueProperties')
        ssubelement = xmlutil.SubTemplateElement(subelement, 'PropertyName')
        ssubelement = xmlutil.SubTemplateElement(subelement, 'PropertyValue')
        element = xmlutil.SubTemplateElement(root, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

#XML serializer for queues.enqueuereadbuffer() response
class QueueEnqueueReadBufferResp(xmlutil.TemplateBuilder):
    '''
    Serializer for EnqueueReadBuffer request
    '''
    def construct(self):
        root = xmlutil.TemplateElement('EnqueueReadBufferResp')
        sroot = xmlutil.SubTemplateElement(root, 'ReadBufferResp')
        element = xmlutil.SubTemplateElement(sroot, 'Data')
        element = xmlutil.SubTemplateElement(sroot, 'CL_ERROR_CODE')
        return xmlutil.MasterTemplate(root, 1)

class OpenCLQueues(object):
    def __init__(self):
        self.opencl_command_queues_api = OpenCLCommandQueuesAPI.API()
        super(OpenCLQueues, self).__init__()

#handle for index command; returns all contexts
    @wsgi.serializers(xml=QueuesIndexResp)
    def index(self, req):
        QueuesList = []
        try:
            QList = self.opencl_command_queues_api.ListQueues()
            for queue in QList:
                QueuesList.append({'id': queue})
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.index method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'Queues': QueuesList}

#handle for the create command; returns the URI of the new context
    @wsgi.serializers(xml=os_openclutils.CreateResp)
    def create(self, req, body):
        newQueue = 0
        nErr = 0
        try:
            context = int(body['Context'])
            device = int(body['Device'])
            createFlags = []
            newQueue, nErr = self.opencl_command_queues_api.CreateQueue(context, device, createFlags)
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.create method %s"), sys.exc_info()[0])
            raise exc.HTTPBadRequest()
        return {'CreateResp': {'id': newQueue, 'CL_ERROR_CODE': nErr}}

#handle for index command this gets all OpenCL platforms available
    @wsgi.serializers(xml=QueuesShowResp)
    def show(self, req, id):
        QueueInfo = {}
        QueueInfo['id'] = int(id)
        nErr = 0
        try:
            QueueInfoDict, nErr = self.opencl_command_queues_api.GetQueueProperties(int(id))
            QueueInfo['Device'] = QueueInfoDict['Device']
            QueueInfo['Context'] = QueueInfoDict['Context']
            QueueInfo['ListQueueProperties'] = []
            QueueInfo['CL_ERROR_CODE'] = nErr
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.show method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'Queue': QueueInfo}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def retain(self, req, id, body):
        '''
        Retain the queue
        '''
        nErr = 0
        try:
            nErr = self.opencl_command_queues_api.RetainQueue(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.retain method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def release(self, req, id, body):
        '''
        Release the context
        '''
        nErr = 0
        try:
            nErr = self.opencl_command_queues_api.ReleaseQueue(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.release method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=QueueEnqueueReadBufferResp)
    def enqueuereadbuffer(self, req, id, body):
        '''
        Enqueue a read buffer operation
        This should launch some hand-shaking algorithm for data transfer in the background.
        '''
        nErr = 0
        Data = ""
        try:
            Buffer = int(body['Buffer'])
            Offset = int(body['Offset'])
            ByteCount = int(body['ByteCount'])
            ContainerId = str(body['ContainerId'])
            SwiftContext = body['SwiftContext']
            Data, nErr = self.opencl_command_queues_api.EnqueueReadBuffer(int(id), 
                                               Buffer, ByteCount, Offset,
                                               ContainerId, SwiftContext)
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.enqueuereadbuffer method %s"), sys.exc_info()[0])
            print("Exception caught in OpenCLQueues.enqueuereadbuffer method %s" % sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'ReadBufferResp': {'CL_ERROR_CODE': nErr, 'DataObject': Data}}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def enqueuewritebuffer(self, req, id, body):
        '''
        Enqueue a write buffer operation
        This should launch some hand-shaking algorithm for data transfer in the background.
        '''
        nErr = 0
        RawData = bytearray()
        try:
            Buffer = int(body['Buffer'])
            Offset = int(body['Offset'])
            ByteCount = int(body['ByteCount'])
            DataObjectId = str(body['ObjectId'])
            ContainerId = str(body['ContainerId'])
            SwiftContext = body['SwiftContext']
            nErr = self.opencl_command_queues_api.EnqueueWriteBuffer(int(id), 
                                  Buffer, ByteCount, 
                                  Offset, DataObjectId,
                                  ContainerId, 
                                  SwiftContext)
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.enqueuewritebuffer method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def enqueuecopybuffer(self, req, id, body):
        '''
        Enqueue a copy buffer operation
        This should launch some hand-shaking algorithm for data transfer in the background.
        '''
        nErr = 0
        try:
            sourcebuffer = int(body['SourceBuffer'])
            destinationbuffer = int(body['DestinationBuffer'])
            sourceoffset = int(body['SourceOffset'])
            destinationoffset = int(body['DestinationOffset'])
            bytecount = int(body['ByteCount'])
            nErr = self.opencl_command_queues_api.EnqueueCopyBuffer(int(id), 
                                  sourcebuffer, destinationbuffer,
                                  sourceoffset, destinationoffset, bytecount)
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.enqueuewritebuffer method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def enqueuendrangekernel(self, req, id, body):
        '''
        Enqueue an nd range
        '''
        nErr = 0
        try:
            kernel = body['Kernel']
            gwo = []
            for dimPairItem in body['GlobalWorkOffset']:
                gwo.append( dimPairItem['Size']  )
            gws = []
            for dimPairItem in body['GlobalWorkSize']:
                gws.append( dimPairItem['Size'] )
            lws = []
            for dimPairItem in body['LocalWorkSize']:
                lws.append( dimPairItem['Size'] )
            nErr = self.opencl_command_queues_api.EnqueueNDRangeKernel(int(id), kernel, gwo, gws, lws)
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.enqueuendrangekernel method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def enqueuetask(self, req, id, body):
        '''
        Enqueue a task
        '''
        nErr = 0
        try:
            kernel = body['Kernel']
            nErr = self.opencl_command_queues_api.EnqueueTask(int(id), kernel)
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.enqueuetask method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def enqueuebarrier(self, req, id, body):
        '''
        Enqueue a barrier
        '''
        nErr = 0
        try:
            nErr = self.opencl_command_queues_api.EnqueueBarrier(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.enqueuebarrier method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

    @wsgi.response(202)
    @wsgi.serializers(xml=os_openclutils.OpenCLErrorResp)
    def finish(self, req, id, body):
        '''
        wait for all enqueued operations to finish
        '''
        nErr = 0
        try:
            nErr = self.opencl_command_queues_api.Finish(int(id))
        except:
            LOG.debug(_("Exception caught in OpenCLQueues.finish method %s"), sys.exc_info()[0])
            raise exc.HTTPNotFound()
        return {'CL_ERROR_CODE': nErr}

