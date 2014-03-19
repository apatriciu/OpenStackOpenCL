from queues import task_exchange
from queues import queue_opencl_nodes
import sys
from oslo.config import cfg
import PyOpenCLInterface
from kombu import Exchange, Queue
from kombu.mixins import ConsumerMixin
from kombu.utils import uuid
from kombu.common import maybe_declare
from kombu.pools import producers
import binascii
from swiftclient import client as cs
from Dispatch import Dispatch

class DispatchDevices(Dispatch):
    def ListDevices(self, args):
        nErr = 0
        try:
            result = PyOpenCLInterface.ListDevices()
        except:
            nErr = -128
        return result
    def GetDeviceProperties(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.GetDeviceProperties(nid)
        except:
            nErr = -128
            DeviceProperties = {}
            return (DeviceProperties, nErr)
        return result

class DispatchContexts(Dispatch):
    def ListContexts(self, args):
        nErr = 0
        try:
            result = PyOpenCLInterface.ListContexts()
        except:
            result = []
            nErr = -128
        return (result, nErr)
    def GetContextProperties(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.GetContextProperties(nid)
        except:
            nErr = -128
            ContextProperties = {}
            return (ContextProperties, nErr)
        return result
    def CreateContext(self, args):
        try:
            listDevices = args['Devices']
            properties = args['Properties']
            result = PyOpenCLInterface.CreateContext(listDevices, properties)
        except:
            return -128
        return result
    def ReleaseContext(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.ReleaseContext(nid)
        except:
            return -128
        return result
    def RetainContext(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.RetainContext(nid)
        except:
            return -128
        return result

class DispatchBuffers(Dispatch):
    def ListBuffers(self, args):
        nErr = 0
        try:
            result = PyOpenCLInterface.ListBuffers()
        except:
            print "DISPATCHBUFFERS : Exception caught ListBuffers"
            nErr = -128
        return (result, nErr)
    def GetBufferProperties(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.GetBufferProperties(nid)
        except:
            nErr = -128
            BufferProperties = {}
            return (BufferProperties, nErr)
        return result
    def CreateBuffer(self, args):
        try:
            context = int(args['Context'])
            size = int(args['Size'])
            properties = args['Properties']
            result = PyOpenCLInterface.CreateBuffer(context, size, properties)
        except:
            print "DISPATCHBUFFERS.CreateBuffer Exception Caught : %s" % sys.exc_info()[0]
            return -128
        return result
    def ReleaseBuffer(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.ReleaseBuffer(nid)
        except:
            return -128
        return result
    def RetainBuffer(self, args):
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.RetainBuffer(nid)
        except:
            return -128
        return result

class DispatchPrograms(Dispatch):
    def ListPrograms(self, args):
        nErr = 0
        try:
            result = PyOpenCLInterface.ListPrograms()
        except:
            nErr = -128
        return (result, nErr)
    def GetProgramProperties(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.GetProgramProperties(nid)
        except:
            print "DispatchPrograms exception %s " %  sys.exc_info()[0] 
            nErr = -128
            Properties = {}
            return (Properties, nErr)
        return result
    def CreateProgram(self, args):
        try:
            context = int(args['Context'])
            programStringsList = args['ProgramStrings']
            programStrings = []
            for stru in programStringsList:
                programStrings.append(str(stru))
            result = PyOpenCLInterface.CreateProgram(context, programStrings)
        except:
            print "DispatchPrograms exception %s " %  sys.exc_info()[0] 
            return -128
        return result
    def ReleaseProgram(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.ReleaseProgram(nid)
        except:
            print "DispatchPrograms exception %s " %  sys.exc_info()[0] 
            return -128
        return result
    def RetainProgram(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.RetainProgram(nid)
        except:
            print "DispatchPrograms exception %s " %  sys.exc_info()[0] 
            return -128
        return result
    def BuildProgram(self, args):
        try:
            nid = int(args['id'])
            listDevices = args['Devices']
            buildOptions = args['Options']
            result = PyOpenCLInterface.BuildProgram(nid, listDevices, buildOptions)
        except:
            print "DispatchPrograms exception %s " %  sys.exc_info()[0] 
            return -128
        return result
    def GetProgramBuildInfo(self, args):
        try:
            nid = int(args['id'])
            device = int(args['Device'])
            buildInfo = args['BuildInfo']
            result = PyOpenCLInterface.GetProgramBuildInfo(nid, device, buildInfo)
        except:
            print "DispatchPrograms exception %s " %  sys.exc_info()[0] 
            return -128
        return result

class DispatchKernels(Dispatch):
    def ListKernels(self, args):
        nErr = 0
        try:
            result = PyOpenCLInterface.ListKernels()
        except:
            nErr = -128
        return (result, nErr)
    def GetKernelProperties(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.GetKernelProperties(nid)
        except:
            print "DispatchKernels exception : %s " %  sys.exc_info()[0] 
            nErr = -128
            Properties = {}
            return (Properties, nErr)
        return result
    def CreateKernel(self, args):
        try:
            program = int(args['Program'])
            kernel_name = str(args['KernelName'])
            result = PyOpenCLInterface.CreateKernel(program, kernel_name)
        except:
            print "DispatchKernels exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def ReleaseKernel(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.ReleaseKernel(nid)
        except:
            print "DispatchKernels exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def RetainKernel(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.RetainKernel(nid)
        except:
            print "DispatchKernels exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def KernelSetArgument(self, args):
        try:
            nid = int(args['id'])
            paramIndex = int(args['ParamIndex'])
            body = args['ParamDict']
            paramDict = {}
            if body.has_key('LocalMemory'):
                paramDict = {'LocalMemory': int(body['LocalMemory'])}
            if body.has_key('DeviceMemoryObject'):
                paramDict = {'DeviceMemoryObject': int(body['DeviceMemoryObject'])}
            if body.has_key('HostValue'):
                base64string = str(body['HostValue'])
                binArray = bytearray( binascii.a2b_base64(base64string) )
                paramDict = {'HostValue': binArray}
            result = PyOpenCLInterface.KernelSetArgument(nid, paramIndex, paramDict)
        except:
            print "DispatchKernels exception : %s " %  sys.exc_info()[0] 
            return -128
        return result

class DispatchCommandQueues(Dispatch):
    def ListCommandQueues(self, args):
        nErr = 0
        try:
            result = PyOpenCLInterface.ListQueues()
        except:
            nErr = -128
        return (result, nErr)
    def GetCommandQueueProperties(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.GetQueueProperties(nid)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            nErr = -128
            Properties = {}
            return (Properties, nErr)
        return result
    def CreateCommandQueue(self, args):
        try:
            context = int(args['Context'])
            device = int(args['Device'])
            createFlags = args['Properties']
            result = PyOpenCLInterface.CreateQueue(context, device, createFlags)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def ReleaseCommandQueue(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.ReleaseQueue(nid)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def RetainCommandQueue(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.RetainQueue(nid)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def EnqueueReadBuffer(self, args):
        try:
            nid = int(args['id'])
            membuffer = int(args['MemBuffer'])
            bytecount = int(args['ByteCount'])
            offset = int(args['Offset'])
            swift_container = args['ContainerId']
            swift_context = args['SwiftContext']
            url = str(swift_context['SwiftUrl'])
            token = str(swift_context['SwiftToken'])
            #url, token = cs.get_keystoneclient_2_0(auth_url, 
            #                                       swift_context['UserName'],
            #                                       swift_context['Password'],
            #                                       {'tenant_name': swift_context['TenantName']})
            RawData, RetErr = PyOpenCLInterface.EnqueueReadBuffer(nid, membuffer, bytecount, offset)
            # put data in the container
            data_length = len(RawData)
            DataObjectId = str(uuid())
            cs.put_object(url = url, token = token, container = swift_container, 
                          name = DataObjectId, contents = RawData, 
                          content_length = data_length)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return (DataObjectId, RetErr)
    def EnqueueWriteBuffer(self, args):
        try:
            nid = int(args['id'])
            membuffer = int(args['MemBuffer'])
            bytecount = int(args['ByteCount'])
            offset = int(args['Offset'])
            swift_container = args['ContainerId']
            swift_object = args['DataObjectId']
            swift_context = args['SwiftContext']
            # unpack the data
            url = str(swift_context['SwiftUrl'])
            token = str(swift_context['SwiftToken'])
            #url, token = cs.get_keystoneclient_2_0(auth_url,
            #                                       swift_context['UserName'],
            #                                       swift_context['Password'],
            #                                       {'tenant_name': swift_context['TenantName']})
            respDict, respObject = cs.get_object(url = url, token = token, container = swift_container,
                                                 name = swift_object)
            data = bytearray(respObject)
            result = PyOpenCLInterface.EnqueueWriteBuffer(nid, membuffer, bytecount, offset, data)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def EnqueueCopyBuffer(self, args):
        try:
            nid = int(args['id'])
            sourcebuffer = int(args['SourceBuffer'])
            destinationbuffer = int(args['DestinationBuffer'])
            bytecount = int(args['ByteCount'])
            sourceoffset = int(args['SourceOffset'])
            destinationoffset = int(args['DestinationOffset'])
            print args
            result = PyOpenCLInterface.EnqueueCopyBuffer(nid, sourcebuffer, destinationbuffer,
                                  bytecount, sourceoffset, destinationoffset)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def EnqueueNDRangeKernel(self, args):
        try:
            nid = int(args['id'])
            kernel = int(args['Kernel'])
            gwo = args['GWO']
            gws = args['GWS']
            lws = args['LWS']
            result = PyOpenCLInterface.EnqueueNDRangeKernel(nid, kernel, gwo, gws, lws)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def EnqueueTask(self, args):
        try:
            nid = int(args['id'])
            kernel = int(args['Kernel'])
            result = PyOpenCLInterface.EnqueueTask(nid, kernel)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def EnqueueBarrier(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.EnqueueBarrier(nid)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result
    def Finish(self, args):
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.Finish(nid)
        except:
            print "DispatchCommandQueues exception : %s " %  sys.exc_info()[0] 
            return -128
        return result

class C(ConsumerMixin):
    def __init__(self, connection, broker_url, OpenCLNodeID):
        try:
            # try to setup the upstream connection
            self.connection = connection
            # create the response channel
            respQueueName = "NewOpenCLComputeNode" + str(uuid())
            respQueue = connection.SimpleQueue(respQueueName,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
            with producers[connection].acquire(block=True) as producer:
                maybe_declare(task_exchange, producer.channel)
                payload = {"RespQueue": respQueueName, 
                           "Method": "NewNode",
                           "Source": broker_url,
                           "args": None}
                producer.publish(payload, exchange = "opencl", serializer="json", routing_key = "opencl.nodes")
            # wait for the response
            resp_message = respQueue.get(block=True, timeout=1)
            self.node_id = resp_message.payload['Result']['NodeId']
            OpenCLNodeID.NodeID = self.node_id
            self.proxyexchangename = "openclproxy" + self.node_id
            self.openclnodeproxy_exchange = Exchange(self.proxyexchangename, 
                                            type="topic", 
                                            delivery_mode = 1,
                                            durable = False)
            self.queue_opencl_devices = Queue(self.proxyexchangename + ".devices", 
                                              self.openclnodeproxy_exchange, 
                                              routing_key = self.proxyexchangename + '.devices',
                                              durable = False) #, auto_delete = True)
            self.queue_opencl_contexts = Queue(self.proxyexchangename + ".contexts", 
                                               self.openclnodeproxy_exchange, 
                                               routing_key = self.proxyexchangename + '.contexts',
                                               durable = False) #, auto_delete = True)
            self.queue_opencl_buffers = Queue(self.proxyexchangename + ".buffers", 
                                              self.openclnodeproxy_exchange, 
                                              routing_key = self.proxyexchangename + '.buffers',
                                              durable = False) #, auto_delete = True)
            self.queue_opencl_programs = Queue(self.proxyexchangename + ".programs", 
                                               self.openclnodeproxy_exchange, 
                                               routing_key = self.proxyexchangename + '.programs', 
                                               durable = False) #, auto_delete = True)
            self.queue_opencl_kernels = Queue(self.proxyexchangename + ".kernels", 
                                              self.openclnodeproxy_exchange, 
                                              routing_key = self.proxyexchangename + '.kernels',
                                              durable = False) #, auto_delete = True)
            self.queue_opencl_command_queues = Queue(self.proxyexchangename + ".commandqueues", 
                                              self.openclnodeproxy_exchange,
                                              routing_key = self.proxyexchangename + '.commandqueues',
                                              durable = False) #, auto_delete = True)
            self.queue_opencl_notify = Queue(self.proxyexchangename + "notify", 
                                              self.openclnodeproxy_exchange, 
                                              routing_key = self.proxyexchangename + '.#',
                                              durable = False) #, auto_delete = True)
            resp_message.ack()
            respQueue.close()
        except:
            print "Exception info %s " %  sys.exc_info()[0] 
            raise Exception('Could not connect to OpenCLProxy')

    def get_consumers(self, Consumer, channel):
        return [Consumer( self.queue_opencl_devices, accept = ['json'], callbacks = [self.on_devices_message]),
                Consumer( self.queue_opencl_contexts, accept = ['json'], callbacks = [self.on_contexts_message]),
                Consumer( self.queue_opencl_programs, accept = ['json'], callbacks = [self.on_programs_message]),
                Consumer( self.queue_opencl_kernels, accept = ['json'], callbacks = [self.on_kernels_message]),
                Consumer( self.queue_opencl_buffers, accept = ['json'], callbacks = [self.on_buffers_message]),
                Consumer( self.queue_opencl_command_queues, accept = ['json'], callbacks = [self.on_command_queues_message]),
                Consumer( self.queue_opencl_notify, accept = ['json'], callbacks = [self.on_message])]

    def CallDispatchAndReply(self, body, dispatchobject):
        respTarget = body['Source']
        respQueue = body['RespQueue']
        method = body['Method']
        args = body['args']
        # create the response connection
        resp_connection = BrokerConnection(respTarget)
        resp_queue = resp_connection.SimpleQueue(respQueue,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
        payload = {"Result": dispatchobject.dispatch(method, args)}
        resp_queue.put(payload, serializer='json')
        resp_queue.close()
 
    def on_message(self, body, message):
        message.ack()
        return

    def on_command_queues_message(self, body, message):
        message.ack()
        print ("notify: RECEIVED COMMAND QUEUES MSG - body: %r" % (body,))
        print ("notify: RECEIVED COMMAND QUEUES MSG - message: %r" % (message,))
        try:
            self.CallDispatchAndReply(body, DispatchCommandQueues())
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_devices_message(self, body, message):
        message.ack()
        print ("notify: RECEIVED DEVICES MSG - body: %r" % (body,))
        print ("notify: RECEIVED DEVICES MSG - message: %r" % (message,))
        try:
            self.CallDispatchAndReply(body, DispatchDevices())
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_contexts_message(self, body, message):
        print ("notify: RECEIVED CONTEXTS MSG - body: %r" % (body,))
        print ("notify: RECEIVED CONTEXTS MSG - message: %r" % (message,))
        message.ack()
        try:
            self.CallDispatchAndReply(body, DispatchContexts())
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_buffers_message(self, body, message):
        print ("notify: RECEIVED BUFFERS MSG - body: %r" % (body,))
        print ("notify: RECEIVED BUFFERS MSG - message: %r" % (message,))
        message.ack()
        try:
            self.CallDispatchAndReply(body, DispatchBuffers())
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_programs_message(self, body, message):
        print ("notify: RECEIVED PROGRAMS MSG - body: %r" % (body,))
        print ("notify: RECEIVED PROGRAMS MSG - message: %r" % (message,))
        message.ack()
        try:
            self.CallDispatchAndReply(body, DispatchPrograms())
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_kernels_message(self, body, message):
        print ("notify: RECEIVED KERNELS MSG - body: %r" % (body,))
        print ("notify: RECEIVED KERNELS MSG - message: %r" % (message,))
        message.ack()
        try:
            self.CallDispatchAndReply(body, DispatchKernels())
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

#global vars
auth_url = ""

class OpenCLNode(object):
    def __init__(self):
        self.NodeID = ""

if __name__ == "__main__":
    from kombu import BrokerConnection
    from kombu.utils.debug import setup_logging
    
    setup_logging(loglevel="DEBUG")

    configs = cfg.ConfigOpts()
    options = [ cfg.StrOpt('rabbit_host', default = 'localhost'),
                cfg.StrOpt('rabbit_password', required = 'true'),
                cfg.StrOpt('rabbit_user', default = 'guest')]
    configs.register_opts( options )
    configs.register_group( cfg.OptGroup('keystone_authtoken') )
    configs.register_opt( cfg.StrOpt('auth_host', default = 'localhost'),
                          group = 'keystone_authtoken' )
    configs.register_opt( cfg.StrOpt('auth_port', default = '5000'),
                          group = 'keystone_authtoken' )
    configs.register_opt( cfg.StrOpt('auth_protocol', default = 'http'),
                          group = 'keystone_authtoken' )
    
    configs(sys.argv[1:])

    rh = configs.rabbit_host
    rp = configs.rabbit_password
    ru = configs.rabbit_user
    auth_url = (configs.keystone_authtoken.auth_protocol + "://" + 
                configs.keystone_authtoken.auth_host + ":" + 
                configs.keystone_authtoken.auth_port + "/v2.0/")

    print auth_url

    strBroker = "amqp://" + ru + ":" + rp + "@" + rh + ":5672//"

    retErr = PyOpenCLInterface.Initialize("GPU")
    if retErr != 0:
        print "Error could not initialize OpenCL interface"
    else:
        oclnodeID = OpenCLNode()
        with BrokerConnection(strBroker) as connection:
            try:
                C(connection, strBroker, oclnodeID).run()
            except:
                print ("try to cleanup proxy resources for NodeId : " ,
                       oclnodeID.NodeID)
                if (oclnodeID.NodeID != ""): 
                    respQueueName = "DeleteOpenCLComputeNode" + str(uuid())
                    respQueue = connection.SimpleQueue(respQueueName,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
                    with producers[connection].acquire(block=True) as producer:
                        maybe_declare(task_exchange, producer.channel)
                        payload = {"RespQueue": respQueueName, 
                                   "Method": "DeleteNode",
                                   "Source": strBroker,
                                   "args": {'NodeId': oclnodeID.NodeID}}
                        producer.publish(payload, exchange = "opencl", serializer="json", routing_key = "opencl.nodes")
                    # wait for the response
                    resp_message = respQueue.get(block=True, timeout=1)
                    print resp_message.payload
                    resp_message.ack()
                    respQueue.close()
                print("bye bye")
    print "Exiting..."

