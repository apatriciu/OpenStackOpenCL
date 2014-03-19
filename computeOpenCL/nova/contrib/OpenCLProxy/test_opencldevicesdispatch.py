import unittest
from OpenCLDevicesDispatch import OpenCLDevicesManager
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager
from Fakes import FakeRPCClient
from Fakes import FakeNodeManager
from uuid import uuid4 as uuid

class TestOpenCLDevicesDispatch(unittest.TestCase):

    def setUp(self):
        self.frpc = FakeRPCClient('FakeBroker')
        self.fnm = FakeNodeManager()
        self.nid = self.fnm.NewNode()
        self.exchange_key = self.fnm.GetExchangeName( self.nid )
        self.routing_key = self.fnm.GetExchangeName( self.nid ) + ".devices"
        self.ocldm = OpenCLDevicesManager(self.frpc, self.fnm)

    def tearDown(self):
        self.ocldm.DeleteNodeResources(self.nid)
        self.ocldm = None
        self.fnm = None
        self.frpc = None
        self.nid = None

    def testRegisterDevices(self):
        '''
        Test if register devices call List on the node and adds 
        them to the list of nodes
        '''
        retVal = self.ocldm.RegisterDevices(self.nid)
        self.assertEqual(retVal, True)
        lk = self.ocldm.List()
        self.assertEqual(lk, [0])
        self.assertEqual(self.frpc.calldict()['Method'], 'ListDevices')
        self.assertEqual(self.frpc.calldict()['args'], None)
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)

    def testGetDeviceProperties(self):
        '''
        GetDeviceProperties should return {'id': deviceID}
        '''
        retVal = self.ocldm.RegisterDevices(self.nid)
        self.assertEqual(retVal, True)
        lk = self.ocldm.List()
        devProps = self.ocldm.GetDeviceProperties({'id': lk[0]})
        self.assertEqual(self.frpc.calldict()['Method'], 'GetDeviceProperties')
        self.assertEqual(self.frpc.calldict()['args'], {'id': lk[0]})
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)
        self.assertEqual(devProps['id'], lk[0])

    def testGetDevicePropertiesInexistentDevice(self):
        '''
        GetDeviceProperties should return -128 for an inexistent device
        '''
        retVal = self.ocldm.RegisterDevices(self.nid)
        self.assertEqual(retVal, True)
        lk = self.ocldm.List()
        devProps = self.ocldm.GetDeviceProperties({'id': lk[0] + 10})
        self.assertEqual( devProps, -128)

if __name__ == "__main__":
    unittest.main()


