import unittest
import OpenCLKernelsDispatch
import OpenCLResourcesAliasManager
import Fakes 
from uuid import uuid4 as uuid

class TestOpenCLKernelsDispatch(unittest.TestCase):

    def setUp(self):
        self.frpc = Fakes.FakeRPCClient('FakeBroker')
        self.fnm = Fakes.FakeNodeManager()
        self.nid = self.fnm.NewNode()
        self.exchange_key = self.fnm.GetExchangeName( self.nid )
        self.routing_key = self.fnm.GetExchangeName( self.nid ) + ".kernels"
        self.oclprograms = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        self.oclbuffers = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a program on node self.nid
        self.programid = self.oclprograms.Insert(self.nid, 0)
        # insert a buffer on node self.nid
        self.bufferid = self.oclbuffers.Insert(self.nid, 0)
        self.oclcontexts = OpenCLResourcesAliasManager.OpenCLResourcesAliasManager()
        # insert a context on node self.nid
        self.contextid = self.oclcontexts.Insert(self.nid, 0)
        self.oclkernels = OpenCLKernelsDispatch.OpenCLKernelsManager(self.frpc, self.fnm, self.oclbuffers, 
                                                                     self.oclprograms, self.oclcontexts) 

    def tearDown(self):
        self.oclprograms.DeleteNodeResources(self.nid)
        self.oclbuffers.DeleteNodeResources(self.nid)
        self.oclcontexts.DeleteNodeResources(self.nid)
        self.oclkernels.DeleteNodeResources(self.nid)
        self.oclprograms = None
        self.oclbuffers = None
        self.oclkernels = None
        self.oclcontexts = None
        self.fnm = None
        self.frpc = None
        self.nid = None

    def VerifyCall(self, method, args = None):
        self.assertEqual(self.frpc.calldict()['Method'], method)
        self.assertEqual(self.frpc.calldict()['args'], args)
        self.assertEqual(self.frpc.calldict()['exchange_key'], self.exchange_key)
        self.assertEqual(self.frpc.calldict()['routing_key'], self.routing_key)

    def testCreateandListKernels(self):
        '''
        Create a new kernel 
        List should return a list with one kernel
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        self.VerifyCall(method = 'CreateKernel', args = args)
        # this should be the first kernel
        self.assertEqual(kernelID, 0)
        lk, retErr = self.oclkernels.ListKernels()
        self.assertEqual(lk, [kernelID])
        self.assertEqual(retErr, 0)

    def testGetKernelProperties(self):
        '''
        GetKernelProperties should return {'id': kernelID}
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        args = {'id': kernelID}
        kernelProps, retErr = self.oclkernels.GetKernelProperties({'id': kernelID})
        args = {'id': 0} # this is the first kernel on the device
        self.VerifyCall(method = 'GetKernelProperties', args = args)
        self.assertEqual(kernelProps['id'], kernelID)

    def testGetKernelPropertiesInexistentKernel(self):
        '''
        GetKernelProperties should return -128 for an inexistent device
        '''
        props = self.oclkernels.GetKernelProperties({'id': 10})
        self.assertEqual( props[1], -128)

    def testRetainKernel(self):
        '''
        RetainKernel should return 0
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        args = {'id': kernelID}
        retVal = self.oclkernels.RetainKernel({'id': kernelID})
        args = {'id': 0} # this is the first kernel on the device
        self.VerifyCall(method = 'RetainKernel', args = args)
        self.assertEqual(retVal, 0)

    def testReleaseKernel(self):
        '''
        ReleaseKernel should return 0
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        args = {'id': kernelID}
        retVal = self.oclkernels.ReleaseKernel({'id': kernelID})
        args = {'id': 0} # this is the first kernel on the device
        self.VerifyCall(method = 'ReleaseKernel', args = args)
        self.assertEqual(retVal, 0)

    def testKernelSetArgumentMemBuffer(self):
        '''
        KernelSetArgument with membuffer param should return 0
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        args = {'id': kernelID, 'ParamIndex': 0, 'ParamDict': {'DeviceMemoryObject': self.bufferid}}
        retVal = self.oclkernels.KernelSetArgument(args)
        args = {'id': 0, 'ParamIndex': 0, 
                         'ParamDict': {'DeviceMemoryObject': 0}} 
                         # this is the first kernel on the device;
                         # calls SetArgument with the first buffer
        self.VerifyCall(method = 'KernelSetArgument', args = args)
        self.assertEqual(retVal, 0)

    def testKernelSetArgumentLocalMemory(self):
        '''
        KernelSetArgument with local memory size should return 0
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        args = {'id': kernelID, 'ParamIndex': 0, 'ParamDict': {'LocalMemory': 128}}
        retVal = self.oclkernels.KernelSetArgument(args)
        args = {'id': 0, 'ParamIndex': 0, 
                         'ParamDict': {'LocalMemory': 128}} 
                         # this is the first kernel on the device;
        self.VerifyCall(method = 'KernelSetArgument', args = args)
        self.assertEqual(retVal, 0)

    def testKernelSetArgumentMemValue(self):
        '''
        KernelSetArgument with value should return 0
        '''
        args = {'Program': self.programid, 'KernelName': 'xyz'}
        kernelID, retErr = self.oclkernels.CreateKernel(args)
        memValue = str('AABCD')
        args = {'id': kernelID, 'ParamIndex': 0, 'ParamDict': {'HostValue': memValue}}
        retVal = self.oclkernels.KernelSetArgument(args)
        args = {'id': 0, 'ParamIndex': 0, 
                         'ParamDict': {'HostValue': memValue}} 
                         # this is the first kernel on the device;
        self.VerifyCall(method = 'KernelSetArgument', args = args)
        self.assertEqual(retVal, 0)

if __name__ == "__main__":
    unittest.main()

