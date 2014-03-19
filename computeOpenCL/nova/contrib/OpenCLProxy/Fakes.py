import Dispatch
from uuid import uuid4 as uuid

class FakeRPCClient(Dispatch.Dispatch):

    # command queues responses
    def ListCommandQueues(self, args):
        return [0]

    def GetCommandQueueProperties(self, args):
        return ({'id': args['id'], 'Device': 0, 'Context': 0}, 0)

    def CreateCommandQueue(self, args):
        return [0, 0]

    def ReleaseCommandQueue(self, args):
        return 0

    def RetainCommandQueue(self, args):
        return 0

    def EnqueueReadBuffer(self, args):
        return ('zxcvb', 0)

    def EnqueueWriteBuffer(self, args):
        return 0

    def EnqueueCopyBuffer(self, args):
        return 0

    def EnqueueNDRangeKernel(self, args):
        return 0

    def EnqueueTask(self, args):
        return 0

    def EnqueueBarrier(self, args):
        return 0

    def Finish(self, args):
        return 0

    # programs responses
    def ListPrograms(self, args):
        return [0]

    def GetProgramProperties(self, args):
        return ({'id': args['id'], 'Devices': [0], 'Context': 0}, 0)

    def CreateProgram(self, args):
        return [0, 0]

    def ReleaseProgram(self, args):
        return 0

    def RetainProgram(self, args):
        return 0

    def BuildProgram(self, args):
        return 0

    def GetProgramBuildInfo(self, args):
        return ({'BuildData': 1}, 0)

    # kernels responses
    def ListKernels(self, args):
        return [0]

    def GetKernelProperties(self, args):
        return ({'id': args['id'], 'Program': 0, 'Context': 0}, 0)

    def CreateKernel(self, args):
        return [0, 0]

    def ReleaseKernel(self, args):
        return 0

    def RetainKernel(self, args):
        return 0

    def KernelSetArgument(self, args):
        return 0

    # buffers responses
    def ListBuffers(self, args):
        return [0]

    def GetBufferProperties(self, args):
        return ({'id': args['id'], 'Context': 0}, 0)

    def CreateBuffer(self, args):
        return [0, 0]

    def ReleaseBuffer(self, args):
        return 0

    def RetainBuffer(self, args):
        return 0

    # contexts responses
    def ListContexts(self, args):
        return [0]

    def GetContextProperties(self, args):
        return ({'id': args['id'], 'Devices': [0]}, 0)

    def CreateContext(self, args):
        return [0, 0]

    def ReleaseContext(self, args):
        return 0

    def RetainContext(self, args):
        return 0

    # devices responses
    def ListDevices(self, args):
        return ([0], 0)

    def GetDeviceProperties(self, args):
        '''
        Return fake properties; args should be {'id': device_id}
        '''
        return {'id': args['id']}

    def __init__(self, strBroker, timeout = None):
        self._strBroker = strBroker
        self.call_dict = {}

    def call(self, node_exchange_object,
                   exchange_key,
                   routing_key,
                   method,
                   args = None):
        self.call_dict = { 'exchange_key': exchange_key,
                             'routing_key': routing_key,
                             'Method': method,
                             'args': args }
        # calls the desired method
        return self.dispatch(method, args)

    def calldict(self):
        return self.call_dict

class FakeNodeManager(object):
    '''
    fake node manager; just a map between uuids and exchange names
    '''

    def __init__(self):
        self.exchange_name_dict = {}

    def GetExchange(self, nodeID):
        ''' 
        There is no exchange
        '''
        return None

    def GetExchangeName(self, nodeID):
        '''
        return the exchange name from the map
        '''
        return self.exchange_name_dict[nodeID]

    def NewNode(self):
        '''
        add a new node
        '''
        node_id = str(uuid())
        exchange_name = "openclproxy%s" % node_id
        self.exchange_name_dict[node_id] = exchange_name
        return node_id

    def DeleteNode(self, node_id):
        '''
        Delete the node
        '''
        try:
            del self.exchange_name_dict[node_id]
        except:
            pass

    def Clear(self):
        '''
        Delete all the nodes from the dictionary
        '''
        self.exchange_name_dict = {}

    def GetDict(self):
        return self.exchange_name_dict

