from queues import queue_opencl_devices
from queues import queue_opencl_contexts
from queues import queue_opencl_buffers
from queues import queue_opencl_programs
from queues import queue_opencl_kernels
from queues import queue_opencl_command_queues
from queues import queue_opencl_notify
from queues import queue_opencl_nodes
import sys
from oslo.config import cfg
from kombu.mixins import ConsumerMixin
from kombu.utils import uuid
from OpenCLNodesDispatch import OpenCLNodesManager
from OpenCLContextsDispatch import OpenCLContextsManager
from OpenCLDevicesDispatch import OpenCLDevicesManager
from OpenCLBuffersDispatch import OpenCLBuffersManager
from OpenCLProgramsDispatch import OpenCLProgramsManager
from OpenCLKernelsDispatch import OpenCLKernelsManager
from OpenCLCommandQueuesDispatch import OpenCLCommandQueuesManager
from RPCClient import RPCClient
from RPCClient import RPCServerResponse

class C(ConsumerMixin):
    def __init__(self, connection, strBroker):
        self.str_broker = strBroker
        self.rpcclient = RPCClient(self.str_broker)
        self.rpcserverresponse = RPCServerResponse
        self.connection = connection
        self.openclnodes = OpenCLNodesManager(self.str_broker)
        self.opencldevices = OpenCLDevicesManager(self.rpcclient,
                                                  self.openclnodes)
        self.openclcontexts = OpenCLContextsManager(self.rpcclient,
                                                    self.openclnodes,
                                                    self.opencldevices)
        self.openclbuffers = OpenCLBuffersManager(self.rpcclient,
                                                  self.openclnodes,
                                                  self.openclcontexts)
        self.openclprograms = OpenCLProgramsManager(self.rpcclient,
                                                    self.openclnodes,
                                                    self.openclcontexts,
                                                    self.opencldevices)
        self.openclkernels = OpenCLKernelsManager(self.rpcclient,
                                                  self.openclnodes,
                                                  self.openclbuffers,
                                                  self.openclprograms,
                                                  self.openclcontexts)
        self.openclcommandqueues = OpenCLCommandQueuesManager(self.rpcclient,
                                                              self.openclnodes,
                                                              self.openclcontexts,
                                                              self.opencldevices,
                                                              self.openclbuffers,
                                                              self.openclprograms,
                                                              self.openclkernels)
        return
    
    def get_consumers(self, Consumer, channel):
        return [Consumer( queue_opencl_devices, accept = ['json'], callbacks = [self.on_devices_message]),
                Consumer( queue_opencl_contexts, accept = ['json'], callbacks = [self.on_contexts_message]),
                Consumer( queue_opencl_programs, accept = ['json'], callbacks = [self.on_programs_message]),
                Consumer( queue_opencl_kernels, accept = ['json'], callbacks = [self.on_kernels_message]),
                Consumer( queue_opencl_buffers, accept = ['json'], callbacks = [self.on_buffers_message]),
                Consumer( queue_opencl_command_queues, accept = ['json'], callbacks = [self.on_command_queues_message]),
                Consumer( queue_opencl_nodes, accept = ['json'], callbacks = [self.on_nodes_message]),
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
            payload = {"Result": self.openclcommandqueues.dispatch(method, args)}
            self.rpcserverresponse(respTarget, respQueue, payload)
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
            payload = {"Result": self.opencldevices.dispatch(method, args)}
            self.rpcserverresponse(respTarget, respQueue, payload)
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
            payload = {"Result": self.openclcontexts.dispatch(method, args)}
            self.rpcserverresponse(respTarget, respQueue, payload)
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
            payload = {"Result": self.openclbuffers.dispatch(method, args)}
            self.rpcserverresponse(respTarget, respQueue, payload)
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
            payload = {"Result": self.openclprograms.dispatch(method, args)}
            self.rpcserverresponse(respTarget, respQueue, payload)
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
            payload = {"Result": self.openclkernels.dispatch(method, args)}
            self.rpcserverresponse(respTarget, respQueue, payload)
        except:
            print "Exception caught : %s" % sys.exc_info()[0]
        return

    def on_nodes_message(self, body, message):
        print ("notify: RECEIVED NODES MSG - body: %r" % (body,))
        print ("notify: RECEIVED NODES MSG - message: %r" % (message,))
        message.ack()
        try:
            respTarget = body['Source']
            respQueue = body['RespQueue']
            method = body['Method']
            args = body['args']
            idDict = self.openclnodes.dispatch(method, args)
            payload = {"Result": idDict}
            self.rpcserverresponse(respTarget, respQueue, payload)
            # call list devices method for new node and populate 
            # self.opencldevices if this NewNode
            if method == 'NewNode':
                self.opencldevices.RegisterDevices(idDict['NodeId'])
            elif method == "DeleteNode":
                self.opencldevices.DeleteNodeResources(idDict['NodeId'])
                self.openclcontexts.DeleteNodeResources(idDict['NodeId'])
                self.openclbuffers.DeleteNodeResources(idDict['NodeId'])
                self.openclprograms.DeleteNodeResources(idDict['NodeId'])
                self.openclkernels.DeleteNodeResources(idDict['NodeId'])
                self.openclcommandqueues.DeleteNodeResources(idDict['NodeId'])
        except:
            print "Exception caught : %s" % sys.exec_info()[0]
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

    with BrokerConnection(strBroker) as connection:
        try:
            print 'Starting OpenCL Proxy...'
            print 'Using rabbitmq: amqp://***:***@%s:%s//' % (rh, "5672")
            C(connection, strBroker).run()
        except KeyboardInterrupt:
            print("bye bye")
    print "Exiting..."

