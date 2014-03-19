import unittest
import OpenCLBuffersDispatch
import OpenCLResourcesAliasManager
import Fakes 
from uuid import uuid4 as uuid

class TestOpenCLBuffersDispatch(unittest.TestCase):

    def setUp(self):
        self.frpc = Fakes.FakeRPCClient('FakeBroker')
        self.fnm = Fakes.FakeNodeManager()
        self.nid = self.fnm.NewNode()
        self.exchange_key = self.fnm.GetExchangeName( self.nid )
        self.routing_key = self.fnm.GetExchangeName( self.nid ) + ".buffers"
        self.oclcontexts = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a device on node self.nid
        self.contextid = self.oclcontexts.Insert(self.nid, 0)
        self.oclbuffers = OpenCLBuffersDispatch.OpenCLBuffersManager(self.frpc, self.fnm, self.oclcontexts) 

    def tearDown(self):
        self.oclcontexts.DeleteNodeResources(self.nid)
        self.oclbuffers.DeleteNodeResources(self.nid)
        self.oclcontexts = None
        self.oclbuffers = None
        self.fnm = None
        self.frpc = None
        self.nid = None

    def VerifyCall(self, method, args = None):
        self.assertEqual(self.frpc.calldict()['Method'], method)
        self.assertEqual(self.frpc.calldict()['args'], args)
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)

    def testCreateandListBuffers(self):
        '''
        Create a new buffer 
        List should return a list with one buffer
        '''
        args = {'Context': self.contextid, 'Size': 64, 'Properties': None}
        bufferID, retErr = self.oclbuffers.CreateBuffer(args)
        self.VerifyCall(method = 'CreateBuffer', args = args)
        # this should be the first buffer
        self.assertEqual(bufferID, 0)
        lc, retErr = self.oclbuffers.ListBuffers()
        self.assertEqual(lc, [bufferID])
        self.assertEqual(retErr, 0)

    def testGetBufferProperties(self):
        '''
        GetBufferProperties should return {'id': bufferID}
        '''
        args = {'Context': self.contextid, 'Size': 64, 'Properties': None}
        bufferID, retErr = self.oclbuffers.CreateBuffer(args)
        args = {'id': bufferID}
        bufferProps, retErr = self.oclbuffers.GetBufferProperties({'id': bufferID})
        args = {'id': 0} # this is the first buffer on the device
        self.VerifyCall(method = 'GetBufferProperties', args = args)
        self.assertEqual(bufferProps['id'], bufferID)

    def testGetBufferPropertiesInexistentContext(self):
        '''
        GetBufferProperties should return -128 for an inexistent device
        '''
        devProps = self.oclbuffers.GetBufferProperties({'id': 10})
        self.assertEqual( devProps[1], -128)

    def testRetainBuffer(self):
        '''
        RetainBuffer should return 0
        '''
        args = {'Context': self.contextid, 'Size': 64, 'Properties': None}
        bufferID, retErr = self.oclbuffers.CreateBuffer(args)
        args = {'id': bufferID}
        retVal = self.oclbuffers.RetainBuffer({'id': bufferID})
        args = {'id': 0} # this is the first buffer on the device
        self.VerifyCall(method = 'RetainBuffer', args = args)
        self.assertEqual(retVal, 0)

    def testReleaseBuffer(self):
        '''
        ReleaseBuffer should return 0
        '''
        args = {'Context': self.contextid, 'Size': 64, 'Properties': None}
        bufferID, retErr = self.oclbuffers.CreateBuffer(args)
        args = {'id': bufferID}
        retVal = self.oclbuffers.ReleaseBuffer({'id': bufferID})
        args = {'id': 0} # this is the first buffer on the device
        self.VerifyCall(method = 'ReleaseBuffer', args = args)
        self.assertEqual(retVal, 0)

if __name__ == "__main__":
    unittest.main()


