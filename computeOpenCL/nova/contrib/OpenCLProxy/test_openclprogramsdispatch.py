import unittest
import OpenCLProgramsDispatch
import OpenCLResourcesAliasManager
import Fakes 
from uuid import uuid4 as uuid

class TestOpenCLProgramsDispatch(unittest.TestCase):

    def setUp(self):
        self.frpc = Fakes.FakeRPCClient('FakeBroker')
        self.fnm = Fakes.FakeNodeManager()
        self.nid = self.fnm.NewNode()
        self.exchange_key = self.fnm.GetExchangeName( self.nid )
        self.routing_key = self.fnm.GetExchangeName( self.nid ) + ".programs"
        self.oclcontexts = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        self.ocldevices = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a context on node self.nid
        self.contextid = self.oclcontexts.Insert(self.nid, 0)
        # insert a device on node self.nid
        self.deviceid = self.ocldevices.Insert(self.nid, 0)
        self.oclprograms = OpenCLProgramsDispatch.OpenCLProgramsManager(self.frpc, self.fnm, self.oclcontexts, self.ocldevices) 

    def tearDown(self):
        self.ocldevices.DeleteNodeResources(self.nid)
        self.oclcontexts.DeleteNodeResources(self.nid)
        self.oclprograms.DeleteNodeResources(self.nid)
        self.oclprograms = None
        self.oclcontexts = None
        self.ocldevices = None
        self.fnm = None
        self.frpc = None
        self.nid = None

    def VerifyCall(self, method, args = None):
        self.assertEqual(self.frpc.calldict()['Method'], method)
        self.assertEqual(self.frpc.calldict()['args'], args)
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)

    def testCreateandListPrograms(self):
        '''
        Create a new program 
        List should return a list with one program
        '''
        args = {'Context': self.contextid, 'ProgramStrings': ['xyz', 'asd', 'ssd']}
        programID, retErr = self.oclprograms.CreateProgram(args)
        self.VerifyCall(method = 'CreateProgram', args = args)
        # this should be the first program
        self.assertEqual(programID, 0)
        lp, retErr = self.oclprograms.ListPrograms()
        self.assertEqual(lp, [programID])
        self.assertEqual(retErr, 0)

    def testGetProgramProperties(self):
        '''
        GetProgramProperties should return {'id': programID}
        '''
        args = {'Context': self.contextid, 'ProgramStrings': ['xyz', 'asd', 'ssd']}
        programID, retErr = self.oclprograms.CreateProgram(args)
        args = {'id': programID}
        programProps, retVal = self.oclprograms.GetProgramProperties({'id': programID})
        args = {'id': 0} # this is the first program on the device
        self.VerifyCall(method = 'GetProgramProperties', args = args)
        self.assertEqual(programProps['id'], programID)

    def testGetProgramPropertiesInexistentProgram(self):
        '''
        GetProgramProperties should return -128 for an inexistent device
        '''
        props = self.oclprograms.GetProgramProperties({'id': 10})
        self.assertEqual( props[1], -128)

    def testRetainProgram(self):
        '''
        RetainProgram should return 0
        '''
        args = {'Context': self.contextid, 'ProgramStrings': ['xyz', 'asd', 'ssd']}
        programID, retErr = self.oclprograms.CreateProgram(args)
        args = {'id': programID}
        retVal = self.oclprograms.RetainProgram({'id': programID})
        args = {'id': 0} # this is the first program on the device
        self.VerifyCall(method = 'RetainProgram', args = args)
        self.assertEqual(retVal, 0)

    def testReleaseProgram(self):
        '''
        ReleaseProgram should return 0
        '''
        args = {'Context': self.contextid, 'ProgramStrings': ['xyz', 'asd', 'ssd']}
        programID, retErr = self.oclprograms.CreateProgram(args)
        args = {'id': programID}
        retVal = self.oclprograms.ReleaseProgram({'id': programID})
        args = {'id': 0} # this is the first program on the device
        self.VerifyCall(method = 'ReleaseProgram', args = args)
        self.assertEqual(retVal, 0)

    def testBuildProgram(self):
        '''
        BuildProgram should return 0
        '''
        args = {'Context': self.contextid, 'ProgramStrings': ['xyz', 'asd', 'ssd']}
        programID, retErr = self.oclprograms.CreateProgram(args)
        args = {'id': programID, 
                'Devices': [self.deviceid,], 
                'Options': None}
        retVal = self.oclprograms.BuildProgram(args)
        args = {'id': 0, 
                'Devices': [0,], 
                'Options': None} 
                         # this is the first program on the device;
                         # calls SetArgument with the first buffer
        self.VerifyCall(method = 'BuildProgram', args = args)
        self.assertEqual(retVal, 0)

    def testGetProgramBuildInfo(self):
        '''
        GetProgramBuildInfo should return ({'BuildData': 1}, 0)
        '''
        args = {'Context': self.contextid, 'ProgramStrings': ['xyz', 'asd', 'ssd']}
        programID, retErr = self.oclprograms.CreateProgram(args)
        args = {'id': programID, 
                'Device': self.deviceid, 
                'BuildInfo': 'Dummy'}
        retVal = self.oclprograms.GetProgramBuildInfo(args)
        args = {'id': 0, 
                'Device': 0, 
                'BuildInfo': 'Dummy'} 
                         # this is the first program on the device;
        self.VerifyCall(method = 'GetProgramBuildInfo', args = args)
        self.assertEqual(retVal, ({'BuildData': 1}, 0))

if __name__ == "__main__":
    unittest.main()

