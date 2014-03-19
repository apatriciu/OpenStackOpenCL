import unittest
import OpenCLContextsDispatch
import OpenCLResourcesAliasManager
import Fakes 
import Fakes 
from uuid import uuid4 as uuid

class TestOpenCLContextsDispatch(unittest.TestCase):

    def setUp(self):
        self.frpc = Fakes.FakeRPCClient('FakeBroker')
        self.fnm = Fakes.FakeNodeManager()
        self.nid = self.fnm.NewNode()
        self.exchange_key = self.fnm.GetExchangeName( self.nid )
        self.routing_key = self.fnm.GetExchangeName( self.nid ) + ".contexts"
        self.ocldevices = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a device on node self.nid
        self.deviceid = self.ocldevices.Insert(self.nid, 0)
        self.oclcontexts = OpenCLContextsDispatch.OpenCLContextsManager(self.frpc, self.fnm, self.ocldevices) 

    def tearDown(self):
        self.ocldevices.DeleteNodeResources(self.nid)
        self.oclcontexts.DeleteNodeResources(self.nid)
        self.ocldevices = None
        self.oclcontexts = None
        self.fnm = None
        self.frpc = None
        self.nid = None

    def VerifyCallContext(self, method, args = None):
        self.assertEqual(self.frpc.calldict()['Method'], method)
        self.assertEqual(self.frpc.calldict()['args'], args)
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)

    def testCreateandListContexts(self):
        '''
        Create a new context 
        List should return a list with one context
        '''
        devicesList = [ self.deviceid ]
        args = {'Devices': devicesList, 'Properties': None}
        contextID, retErr = self.oclcontexts.CreateContext(args)
        self.VerifyCallContext(method = 'CreateContext', args = args)
        # this should be the first context
        self.assertEqual(contextID, 0)
        lc, nErr = self.oclcontexts.ListContexts()
        self.assertEqual(lc, [contextID])
        self.assertEqual(nErr, 0)

    def testGetContextProperties(self):
        '''
        GetContextProperties should return {'id': contextID}
        '''
        devicesList = [ self.deviceid ]
        args = {'Devices': devicesList, 'Properties': None}
        contextID, retErr = self.oclcontexts.CreateContext(args)
        args = {'id': contextID}
        contextProps, retErr = self.oclcontexts.GetContextProperties({'id': contextID})
        args = {'id': 0} # this is the first context on the device
        self.VerifyCallContext(method = 'GetContextProperties', args = args)
        self.assertEqual(contextProps['id'], contextID)
        self.assertEqual(retErr, 0)

    def testGetContextPropertiesInexistentContext(self):
        '''
        GetContextProperties should return -128 for an inexistent device
        '''
        devProps = self.oclcontexts.GetContextProperties({'id': 10})
        self.assertEqual( devProps[1], -128)

    def testRetainContext(self):
        '''
        RetainContext should return 0
        '''
        devicesList = [ self.deviceid ]
        args = {'Devices': devicesList, 'Properties': None}
        contextID, retErr = self.oclcontexts.CreateContext(args)
        args = {'id': contextID}
        retVal = self.oclcontexts.RetainContext({'id': contextID})
        args = {'id': 0} # this is the first context on the device
        self.VerifyCallContext(method = 'RetainContext', args = args)
        self.assertEqual(retVal, 0)

    def testReleaseContext(self):
        '''
        ReleaseContext should return 0
        '''
        devicesList = [ self.deviceid ]
        args = {'Devices': devicesList, 'Properties': None}
        contextID, retErr = self.oclcontexts.CreateContext(args)
        args = {'id': contextID}
        retVal = self.oclcontexts.ReleaseContext({'id': contextID})
        args = {'id': 0} # this is the first context on the device
        self.VerifyCallContext(method = 'ReleaseContext', args = args)
        self.assertEqual(retVal, 0)

if __name__ == "__main__":
    unittest.main()


