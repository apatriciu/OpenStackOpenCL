from nova.api.openstack.compute.contrib import openclbuffersinterface as os_openclbuffersinterface
from nova.api.openstack.compute.contrib import openclkernelsinterface as os_openclkernelsinterface
from nova.api.openstack.compute.contrib import openclprogramsinterface as os_openclprogramsinterface
from nova.api.openstack.compute.contrib import openclinterface as os_openclinterface
import unittest
import webob
import binascii

#from nova import test

class LaptopResources:
    listDevicesOnSystem = [0]
    listDevicesIDs = [{"Device": 0}]
    inexistentKernel = 100
    programCodeStrings = ["__kernel void dummy(int a, __global float* b, __local float* sha){ int ii = a; }",]
    KernelFunctionName = "dummy"
    device_type = "GPU"

class Request:
    environ = {'nova.context': {'user': 'guest', 'project': 'guest'}}

class OpenclkernelsinterfaceTestCase(unittest.TestCase):


    def setUp(self):
        # super(OpenclinterfaceTestCase, self).setUp();
        super(OpenclkernelsinterfaceTestCase, self).setUp()
        self.testResources = LaptopResources()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts()
        self.Programs = os_openclprogramsinterface.OpenCLPrograms()
        self.Kernels = os_openclkernelsinterface.OpenCLKernels()
        self.Buffers = os_openclbuffersinterface.OpenCLBuffers()
        req = Request()
        body = {'Devices': self.testResources.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        self.contextID = resp['id']
        req = Request()
        listProgramStringsPairs = []
        for progstr in self.testResources.programCodeStrings:
            listProgramStringsPairs.append({'ProgramString': progstr})
        body = {'Context': self.contextID, 'ListProgramStrings': listProgramStringsPairs}
        resp = self.Programs.create(req, body)['CreateResp']
        self.programID = resp['id']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        buildOptions = ""
        body = {'ListDevices': self.testResources.listDevicesIDs, 'CompileOptions': buildOptions}
        retErr = self.Programs.build(req, str(self.programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        # create buffers
        bufferSize = 512
        body = {'Context': self.contextID, 'MEM_SIZE': bufferSize, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        self.bufferID = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)

    def tearDown(self):
        body = None
        req = Request()
        retErr = self.Contexts.release(req, str(self.contextID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Programs.release(req, str(self.programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Buffers.release(req, str(self.bufferID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

    def testCreateKernel(self):
        #create kernel
        req = Request()
        listKernels = self.Kernels.index(req)['Kernels']
        self.assertEqual(len(listKernels), 0)
        kernelName = self.testResources.KernelFunctionName
        body = {'Program': self.programID, 'KernelName': kernelName}
        resp = self.Kernels.create(req, body)['CreateResp']
        kernelID = resp['id']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        kernelProperties = self.Kernels.show(req, str(kernelID))['Kernel']
        self.assertEqual(kernelProperties['Program'], self.programID)
        self.assertEqual(kernelProperties['id'], kernelID)
        self.assertEqual(kernelProperties['Context'], self.contextID)
        self.assertEqual(kernelProperties['KernelFunctionName'], kernelName)
        listKernels = self.Kernels.index(req)['Kernels']
        self.assertEqual(listKernels, [{'id': kernelID}])
        body = None
        retErr = self.Kernels.release(req, str(kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listKernels = self.Kernels.index(req)['Kernels']
        self.assertEqual(len(listKernels), 0)

    def testKernelSetParam(self):
        #create kernel
        req = Request()
        listKernels = self.Kernels.index(req)['Kernels']
        self.assertEqual(len(listKernels), 0)
        kernelName = self.testResources.KernelFunctionName
        body = {'Program': self.programID, 'KernelName': kernelName}
        resp = self.Kernels.create(req, body)['CreateResp']
        kernelID = resp['id']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        byteArrayParam = bytearray( '1111' )
        charArrayParambase64 = binascii.b2a_base64(byteArrayParam)
        body = {'ArgIndex': 0, 'HostValue': charArrayParambase64}
        retErr = self.Kernels.setkernelarg(req, str(kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'ArgIndex': 1, 'DeviceMemoryObject': self.bufferID}
        retErr = self.Kernels.setkernelarg(req, str(kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'ArgIndex': 2, 'LocalMemory': 64}
        retErr = self.Kernels.setkernelarg(req, str(kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = None
        retErr = self.Kernels.release(req, str(kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

if __name__ == "__main__":
    unittest.main()

