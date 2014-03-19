import unittest
import OpenCLCommandQueuesDispatch
import OpenCLResourcesAliasManager
import Fakes 
from uuid import uuid4 as uuid

class TestOpenCLCommandQueuesDispatch(unittest.TestCase):
    '''
    Test Command Queues
    '''

    def setUp(self):
        self.frpc = Fakes.FakeRPCClient('FakeBroker')
        self.fnm = Fakes.FakeNodeManager()
        self.nid = self.fnm.NewNode()
        self.exchange_key = self.fnm.GetExchangeName( self.nid )
        self.routing_key = self.fnm.GetExchangeName( self.nid ) + ".commandqueues"
        self.oclcontexts = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a context on node self.nid
        self.contextid = self.oclcontexts.Insert(self.nid, 0)
        self.ocldevices = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a context on node self.nid
        self.deviceid = self.ocldevices.Insert(self.nid, 0)
        self.oclprograms = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a program on node self.nid
        self.programid = self.oclprograms.Insert(self.nid, 0)
        self.oclbuffers = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a buffer on node self.nid
        self.bufferid = self.oclbuffers.Insert(self.nid, 0)
        self.oclkernels = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a buffer on node self.nid
        self.kernelid = self.oclkernels.Insert(self.nid, 0)
        self.oclcommandqueues = OpenCLCommandQueuesDispatch.OpenCLCommandQueuesManager(self.frpc, self.fnm, 
                                                   self.oclcontexts, self.ocldevices,
                                                   self.oclbuffers, self.oclprograms,
                                                   self.oclkernels) 

    def tearDown(self):
        self.oclprograms.DeleteNodeResources(self.nid)
        self.oclbuffers.DeleteNodeResources(self.nid)
        self.oclkernels.DeleteNodeResources(self.nid)
        self.oclcontexts.DeleteNodeResources(self.nid)
        self.ocldevices.DeleteNodeResources(self.nid)
        self.oclcommandqueues.DeleteNodeResources(self.nid)
        self.oclprograms = None
        self.oclbuffers = None
        self.oclkernels = None
        self.oclcontexts = None
        self.ocldevices = None
        self.oclcommandqueues = None
        self.fnm = None
        self.frpc = None
        self.nid = None

    def VerifyCall(self, method, args = None):
        self.assertEqual(self.frpc.calldict()['Method'], method)
        self.assertEqual(self.frpc.calldict()['args'], args)
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)

    def testCreateandListCommandQueues(self):
        '''
        Create a new commandqueue 
        List should return a list with one commandqueue
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        self.VerifyCall(method = 'CreateCommandQueue', args = args)
        # this should be the first commandqueue
        self.assertEqual(commandqueueID, 0)
        lc, retErr = self.oclcommandqueues.ListCommandQueues()
        self.assertEqual(lc, [commandqueueID])
        self.assertEqual(retErr, 0)

    def testGetCommandQueueProperties(self):
        '''
        GetCommandQueueProperties should return {'id': commandqueueID}
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID}
        commandqueueProps, retErr = self.oclcommandqueues.GetCommandQueueProperties({'id': commandqueueID})
        args = {'id': 0} # this is the first commandqueue on the device
        self.VerifyCall(method = 'GetCommandQueueProperties', args = args)
        self.assertEqual(commandqueueProps['id'], commandqueueID)

    def testGetCommandQueuePropertiesInexistentCommandQueue(self):
        '''
        GetCommandQueueProperties should return -128 for an inexistent device
        '''
        props = self.oclcommandqueues.GetCommandQueueProperties({'id': 10})
        self.assertEqual( props[1], -128)

    def testRetainCommandQueue(self):
        '''
        RetainCommandQueue should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID}
        retVal = self.oclcommandqueues.RetainCommandQueue({'id': commandqueueID})
        args = {'id': 0} # this is the first commandqueue on the device
        self.VerifyCall(method = 'RetainCommandQueue', args = args)
        self.assertEqual(retVal, 0)

    def testReleaseCommandQueue(self):
        '''
        ReleaseCommandQueue should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID}
        retVal = self.oclcommandqueues.ReleaseCommandQueue({'id': commandqueueID})
        args = {'id': 0} # this is the first commandqueue on the device
        self.VerifyCall(method = 'ReleaseCommandQueue', args = args)
        self.assertEqual(retVal, 0)

    def testEnqueueReadBuffer(self):
        '''
        EnqueueReadBuffer should return ({'Data': dataURI}, 0)
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID, 'MemBuffer': self.bufferid, 
                'ByteCount': 16, 'Offset': 0,
                'ContainerId': 'xyzw',
                'SwiftContext': {}}
        objID, retErr = self.oclcommandqueues.EnqueueReadBuffer(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'EnqueueReadBuffer', args = args)

    def testEnqueueWriteBuffer(self):
        '''
        EnqueueWriteBuffer should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID, 'MemBuffer': self.bufferid, 
                'ByteCount': 16, 'Offset': 0,
                'ContainerId': 'xyzw',
                'DataObjectId': 'asdfg', 
                'SwiftContext': {}}
        retErr = self.oclcommandqueues.EnqueueWriteBuffer(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'EnqueueWriteBuffer', args = args)

    def testEnqueueCopyBuffer(self):
        '''
        EnqueueCopyBuffer should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID, 
                'SourceBuffer': self.bufferid, 
                'DestinationBuffer': self.bufferid, 
                'ByteCount': 16, 
                'SourceOffset': 0,
                'DestinationOffset': 0}
        retErr = self.oclcommandqueues.EnqueueCopyBuffer(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'EnqueueCopyBuffer', args = args)

    def testEnqueueNDRangeKernel(self):
        '''
        EnqueueNDRangeKernel should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID, 
                'Kernel': self.kernelid,
                'GWO': [0, 0],
                'GWS': [2, 2],
                'LWS': [2, 2]}
        retErr = self.oclcommandqueues.EnqueueNDRangeKernel(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'EnqueueNDRangeKernel', args = args)

    def testEnqueueTask(self):
        '''
        EnqueueTask should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID, 
                'Kernel': self.kernelid}
        retErr = self.oclcommandqueues.EnqueueTask(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'EnqueueTask', args = args)

    def testEnqueueBarrier(self):
        '''
        EnqueueBarrier should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID}
        retErr = self.oclcommandqueues.EnqueueBarrier(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'EnqueueBarrier', args = args)

    def testFinish(self):
        '''
        Finish should return 0
        '''
        args = {'Context': self.contextid, 
                'Device': self.deviceid,
                'Properties': None}
        commandqueueID, retErr = self.oclcommandqueues.CreateCommandQueue(args)
        args = {'id': commandqueueID}
        retErr = self.oclcommandqueues.Finish(args)
        self.assertEqual(retErr, 0)
        self.VerifyCall(method = 'Finish', args = args)

if __name__ == "__main__":
    unittest.main()

