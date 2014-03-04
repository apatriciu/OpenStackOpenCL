from queues import queue_opencl_devices
from queues import queue_opencl_contexts
from queues import queue_opencl_buffers
from queues import queue_opencl_programs
from queues import queue_opencl_kernels
from queues import queue_opencl_command_queues
from queues import queue_opencl_notify
import sys
from oslo.config import cfg
import PyOpenCLInterface
from kombu.mixins import ConsumerMixin
import binascii

def DispatchDevices(method, args):
    if method == 'ListDevices':
        nErr = 0
        try:
            result = PyOpenCLInterface.ListDevices()
        except:
            nErr = -128
        return result
    if method == 'GetDeviceProperties':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.GetDeviceProperties(nid)
        except:
            nErr = -128
            DeviceProperties = {}
            return (DeviceProperties, nErr)
        return result
    return -128

def DispatchContexts(method, args):
    if method == 'ListContexts':
        nErr = 0
        try:
            result = PyOpenCLInterface.ListContexts()
        except:
            nErr = -128
        return (result, nErr)
    if method == 'GetContextProperties':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.GetContextProperties(nid)
        except:
            nErr = -128
            ContextProperties = {}
            return (ContextProperties, nErr)
        return result
    if method == 'CreateContext':
        try:
            listDevices = args['Devices']
            properties = args['Properties']
            result = PyOpenCLInterface.CreateContext(listDevices, properties)
        except:
            return -128
        return result
    if method == 'ReleaseContext':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.ReleaseContext(nid)
        except:
            return -128
        return result
    if method == 'RetainContext':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.RetainContext(nid)
        except:
            return -128
        return result
    return -128

def DispatchBuffers(method, args):
    if method == 'ListBuffers':
        nErr = 0
        try:
            result = PyOpenCLInterface.ListBuffers()
        except:
            print "DISPATCHBUFFERS : Exception caught ListBuffers"
            nErr = -128
        return (result, nErr)
    if method == 'GetBufferProperties':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.GetBufferProperties(nid)
        except:
            nErr = -128
            BufferProperties = {}
            return (BufferProperties, nErr)
        return result
    if method == 'CreateBuffer':
        try:
            context = int(args['Context'])
            size = int(args['Size'])
            properties = args['Properties']
            result = PyOpenCLInterface.CreateBuffer(context, size, properties)
        except:
            print "DISPATCHBUFFERS.CreateBuffer Exception Caught : %s" % sys.exc_info()[0]
            return -128
        return result
    if method == 'ReleaseBuffer':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.ReleaseBuffer(nid)
        except:
            return -128
        return result
    if method == 'RetainBuffer':
        nid = int(args['id'])
        try:
            result = PyOpenCLInterface.RetainBuffer(nid)
        except:
            return -128
        return result
    print "DISPATCHBUFFERS : Unknown Method"
    return -128

def DispatchPrograms(method, args):
    if method == 'ListPrograms':
        nErr = 0
        try:
            result = PyOpenCLInterface.ListPrograms()
        except:
            nErr = -128
        return (result, nErr)
    if method == 'GetProgramProperties':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.GetProgramProperties(nid)
        except:
            print "Exception caught in DispatchPrograms.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            nErr = -128
            Properties = {}
            return (Properties, nErr)
        return result
    if method == 'CreateProgram':
        try:
            context = int(args['Context'])
            programStringsList = args['ProgramStrings']
            programStrings = []
            for stru in programStringsList:
                programStrings.append(str(stru))
            result = PyOpenCLInterface.CreateProgram(context, programStrings)
        except:
            print "Exception caught in DispatchPrograms.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'ReleaseProgram':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.ReleaseProgram(nid)
        except:
            print "Exception caught in DispatchPrograms.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'RetainProgram':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.RetainProgram(nid)
        except:
            print "Exception caught in DispatchPrograms.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'BuildProgram':
        try:
            nid = int(args['id'])
            listDevices = args['Devices']
            buildOptions = args['Options']
            result = PyOpenCLInterface.BuildProgram(nid, listDevices, buildOptions)
        except:
            print "Exception caught in DispatchPrograms.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'GetProgramBuildInfo':
        try:
            nid = int(args['id'])
            device = int(args['Device'])
            buildInfo = args['BuildInfo']
            result = PyOpenCLInterface.GetProgramBuildInfo(nid, device, buildInfo)
        except:
            print "Exception caught in DispatchPrograms.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    print "DISPATCHPROGRAMS : Unknown Method"
    return -128

def DispatchKernels(method, args):
    if method == 'ListKernels':
        nErr = 0
        try:
            result = PyOpenCLInterface.ListKernels()
        except:
            nErr = -128
        return (result, nErr)
    if method == 'GetKernelProperties':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.GetKernelProperties(nid)
        except:
            print "Exception caught in DispatchKernels.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            nErr = -128
            Properties = {}
            return (Properties, nErr)
        return result
    if method == 'CreateKernel':
        try:
            program = int(args['Program'])
            kernel_name = str(args['KernelName'])
            result = PyOpenCLInterface.CreateKernel(program, kernel_name)
        except:
            print "Exception caught in DispatchKernels.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'ReleaseKernel':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.ReleaseKernel(nid)
        except:
            print "Exception caught in DispatchKernels.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'RetainKernel':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.RetainKernel(nid)
        except:
            print "Exception caught in DispatchKernel.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'KernelSetArgument':
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
            print "Exception caught in DispatchKernels.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    print "DISPATCHPROGRAMS : Unknown Method"
    return -128

def DispatchCommandQueues(method, args):
    if method == 'ListCommandQueues':
        nErr = 0
        try:
            result = PyOpenCLInterface.ListQueues()
        except:
            nErr = -128
        return (result, nErr)
    if method == 'GetCommandQueueProperties':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.GetQueueProperties(nid)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            nErr = -128
            Properties = {}
            return (Properties, nErr)
        return result
    if method == 'CreateCommandQueue':
        try:
            context = int(args['Context'])
            device = int(args['Device'])
            createFlags = args['Properties']
            result = PyOpenCLInterface.CreateQueue(context, device, createFlags)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'ReleaseCommandQueue':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.ReleaseQueue(nid)
        except:
            print "Exception caught in DispatchQueue.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'RetainCommandQueue':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.RetainQueue(nid)
        except:
            print "Exception caught in DispatchQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'EnqueueReadBuffer':
        try:
            nid = int(args['id'])
            membuffer = int(args['MemBuffer'])
            bytecount = int(args['ByteCount'])
            offset = int(args['Offset'])
            RawData, RetErr = PyOpenCLInterface.EnqueueReadBuffer(nid, membuffer, bytecount, offset)
            # RawData is a byte array of length ByteCount; We have to divide 
            # RawData in 57 bytes slices and convert to base64
            Data = ""
            StartPosition = 0
            while StartPosition < bytecount:
                EndPosition = StartPosition + 57
                if EndPosition > bytecount:
                    EndPosition = bytecount
                Data2Convert = bytearray(RawData[StartPosition : EndPosition])
                StartPosition = EndPosition
                base64Data = binascii.b2a_base64(Data2Convert)
                Data = Data + base64Data
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return (Data, RetErr)
    if method == 'EnqueueWriteBuffer':
        try:
            nid = int(args['id'])
            membuffer = int(args['MemBuffer'])
            bytecount = int(args['ByteCount'])
            offset = int(args['Offset'])
            # unpack the data
            data = bytearray(binascii.a2b_base64( str(args['Data'] )))
            result = PyOpenCLInterface.EnqueueWriteBuffer(nid, membuffer, bytecount, offset, data)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'EnqueueCopyBuffer':
        try:
            nid = int(args['id'])
            sourcebuffer = int(args['SourceBuffer'])
            destinationbuffer = int(args['DestinationBuffer'])
            bytecount = int(args['ByteCount'])
            sourceoffset = int(args['SourceOffset'])
            destinationoffset = int(args['DestinationOffset'])
            result = PyOpenCLInterface.EnqueueCopyBuffer(nid, sourcebuffer, destinationbuffer,
                                  sourceoffset, destinationoffset, bytecount)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'EnqueueNDRangeKernel':
        try:
            nid = int(args['id'])
            kernel = int(args['Kernel'])
            gwo = args['GWO']
            gws = args['GWS']
            lws = args['LWS']
            result = PyOpenCLInterface.EnqueueNDRangeKernel(nid, kernel, gwo, gws, lws)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'EnqueueTask':
        try:
            nid = int(args['id'])
            kernel = int(args['Kernel'])
            result = PyOpenCLInterface.EnqueueTask(nid, kernel)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'EnqueueBarrier':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.EnqueueBarrier(nid)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    if method == 'Finish':
        try:
            nid = int(args['id'])
            result = PyOpenCLInterface.Finish(nid)
        except:
            print "Exception caught in DispatchCommandQueues.%s " % method
            print "Exception info %s " %  sys.exc_info()[0] 
            return -128
        return result
    print "DISPATCHPROGRAMS : Unknown Method"
    return -128

class C(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        return
    
    def get_consumers(self, Consumer, channel):
        return [Consumer( queue_opencl_devices, accept = ['json'], callbacks = [self.on_devices_message]),
                Consumer( queue_opencl_contexts, accept = ['json'], callbacks = [self.on_contexts_message]),
                Consumer( queue_opencl_programs, accept = ['json'], callbacks = [self.on_programs_message]),
                Consumer( queue_opencl_kernels, accept = ['json'], callbacks = [self.on_kernels_message]),
                Consumer( queue_opencl_buffers, accept = ['json'], callbacks = [self.on_buffers_message]),
                Consumer( queue_opencl_command_queues, accept = ['json'], callbacks = [self.on_command_queues_message]),
                Consumer( queue_opencl_notify, accept = ['json'], callbacks = [self.on_message])]

    def on_message(self, body, message):
        message.ack()
        return

    def on_command_queues_message(self, body, message):
        message.ack()
        print ("notify: RECEIVED COMMAND QUEUES MSG - body: %r" % (body,))
        print ("notify: RECEIVED COMMAND QUEUES MSG - message: %r" % (message,))
        try:
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
            payload = {"Result": DispatchCommandQueues(method, args)}
            resp_queue.put(payload, serializer='json')
            resp_queue.close()
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_devices_message(self, body, message):
        message.ack()
        print ("notify: RECEIVED DEVICES MSG - body: %r" % (body,))
        print ("notify: RECEIVED DEVICES MSG - message: %r" % (message,))
        try:
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
            payload = {"Result": DispatchDevices(method, args)}
            resp_queue.put(payload, serializer='json')
            resp_queue.close()
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_contexts_message(self, body, message):
        print ("notify: RECEIVED CONTEXTS MSG - body: %r" % (body,))
        print ("notify: RECEIVED CONTEXTS MSG - message: %r" % (message,))
        message.ack()
        try:
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
            payload = {"Result": DispatchContexts(method, args)}
            resp_queue.put(payload, serializer='json')
            resp_queue.close()
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_buffers_message(self, body, message):
        print ("notify: RECEIVED BUFFERS MSG - body: %r" % (body,))
        print ("notify: RECEIVED BUFFERS MSG - message: %r" % (message,))
        message.ack()
        try:
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
            payload = {"Result": DispatchBuffers(method, args)}
            resp_queue.put(payload, serializer='json')
            resp_queue.close()
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_programs_message(self, body, message):
        print ("notify: RECEIVED PROGRAMS MSG - body: %r" % (body,))
        print ("notify: RECEIVED PROGRAMS MSG - message: %r" % (message,))
        message.ack()
        try:
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
            payload = {"Result": DispatchPrograms(method, args)}
            resp_queue.put(payload, serializer='json')
            resp_queue.close()
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_kernels_message(self, body, message):
        print ("notify: RECEIVED KERNELS MSG - body: %r" % (body,))
        print ("notify: RECEIVED KERNELS MSG - message: %r" % (message,))
        message.ack()
        try:
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
            payload = {"Result": DispatchKernels(method, args)}
            resp_queue.put(payload, serializer='json')
            resp_queue.close()
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

if __name__ == "__main__":
    from kombu import BrokerConnection
    from kombu.utils.debug import setup_logging
    
    setup_logging(loglevel="DEBUG")

    configs = cfg.ConfigOpts()
    options = [ cfg.StrOpt('rabbit_host', default = 'localhost'),
                cfg.StrOpt('rabbit_password', required = 'true'),
                cfg.StrOpt('rabbit_user', default = 'guest')]
    configs.register_opts( options )
    configs(sys.argv[1:])

    rh = configs.rabbit_host
    rp = configs.rabbit_password
    ru = configs.rabbit_user

    strBroker = "amqp://" + ru + ":" + rp + "@" + rh + ":5672//"

    retErr = PyOpenCLInterface.Initialize("GPU")
    if retErr != 0:
        print "Error could not initialize OpenCL interface"
    else:
        with BrokerConnection(strBroker) as connection:
            try:
                C(connection).run()
            except KeyboardInterrupt:
                print("bye bye")
    print "Exiting..."

