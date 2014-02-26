from nova.api.openstack.compute.contrib import openclqueuesinterface as os_openclqueuesinterface
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
    programCodeStrings = ['''__kernel void kernel2(int a, __global int *b, __local int *sh){
                               sh[0] = a;
                               b[get_global_id(0)] = sh[0];
                          }
                          ''',]
    KernelFunctionName = "kernel2"
    device_type = "GPU"

class Request:
    environ = {'nova.context': {'user': 'guest', 'project': 'guest'}}

class OpenclqueuesinterfaceTestCase(unittest.TestCase):

    def setUp(self):
        # super(OpenclinterfaceTestCase, self).setUp();
        super(OpenclqueuesinterfaceTestCase, self).setUp()
        self.testResources = LaptopResources()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts()
        self.Queues = os_openclqueuesinterface.OpenCLQueues();
        req = Request()
        body = {'Devices': self.testResources.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        self.contextID = resp['id']

    def tearDown(self):
        body = None
        req = Request()
        retErr = self.Contexts.release(req, str(self.contextID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

    def testCreateQueue(self):
        #create queue
        req = Request()
        listQueues = self.Queues.index(req)['Queues']
        self.assertEqual(len(listQueues), 0)
        kernelNam = self.testResources.KernelFunctionName
        body = {'Context': self.contextID, 'Device': self.testResources.listDevicesOnSystem[0]}
        resp = self.Queues.create(req, body)['CreateResp']
        queueID = resp['id']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        queueProperties = self.Queues.show(req, str(queueID))['Queue']
        self.assertEqual(queueProperties['Context'], self.contextID)
        self.assertEqual(queueProperties['id'], queueID)
        self.assertEqual(queueProperties['Device'], self.testResources.listDevicesOnSystem[0])
        listQueues = self.Queues.index(req)['Queues']
        self.assertEqual(listQueues, [{'id': queueID}])
        body = None
        retErr = self.Queues.release(req, str(queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listQueues = self.Queues.index(req)['Queues']
        self.assertEqual(len(listQueues), 0)

class OpenclqueuesinterfaceBufferCopyTestCase(unittest.TestCase):

    def setUp(self):
        # super(OpenclinterfaceTestCase, self).setUp();
        super(OpenclqueuesinterfaceBufferCopyTestCase, self).setUp()
        self.testResources = LaptopResources()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts()
        self.Queues = os_openclqueuesinterface.OpenCLQueues();
        self.Buffers = os_openclbuffersinterface.OpenCLBuffers()
        req = Request()
        body = {'Devices': self.testResources.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        self.contextID = resp['id']
        # create buffers
        self.bufferSize1 = 32
        body = {'Context': self.contextID, 'MEM_SIZE': self.bufferSize1, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        self.bufferID1 = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)
        self.bufferSize2 = 32
        body = {'Context': self.contextID, 'MEM_SIZE': self.bufferSize2, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        self.bufferID2 = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)
        # create queue
        body = {'Context': self.contextID, 'Device': self.testResources.listDevicesOnSystem[0]}
        resp = self.Queues.create(req, body)['CreateResp']
        self.queueID = resp['id']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)

    def tearDown(self):
        body = None
        req = Request()
        retErr = self.Contexts.release(req, str(self.contextID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        # release the buffers
        retErr = self.Buffers.release(req, str(self.bufferID1), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Buffers.release(req, str(self.bufferID2), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        # release the queue
        retErr = self.Queues.release(req, str(self.queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

    def testWriteReadSameBuffer(self):
        Data = bytearray('1111111111111111')
        base64Data = binascii.b2a_base64( Data  )
        req = Request()
        body = {'Data': base64Data, 'Buffer': self.bufferID1, 'Offset': 0, 'ByteCount': int(len(Data))}
        retErr = self.Queues.enqueuewritebuffer(req, str(self.queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'Buffer': self.bufferID1, 'Offset': 0, 'ByteCount': int(len(Data))}
        resp = self.Queues.enqueuereadbuffer(req, str(self.queueID), body)['ReadBufferResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        respData = bytearray( binascii.a2b_base64(resp['Data']) )
        self.assertEqual(respData, Data)

    def testWriteCopyRead2Buffers(self):
        Data = bytearray('1111111111111111')
        base64Data = binascii.b2a_base64( Data  )
        req = Request()
        body = {'Data': base64Data, 'Buffer': self.bufferID1, 'Offset': 0, 'ByteCount': int(len(Data))}
        retErr = self.Queues.enqueuewritebuffer(req, str(self.queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'SourceBuffer': self.bufferID1, 'DestinationBuffer': self.bufferID2, 
                'SourceOffset': 0, 'DestinationOffset': 0, 'ByteCount': int(len(Data))}
        retErr = self.Queues.enqueuecopybuffer(req, str(self.queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = None
        retErr = self.Queues.enqueuebarrier(req, str(self.queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'Buffer': self.bufferID2, 'Offset': 0, 'ByteCount': int(len(Data))}
        resp = self.Queues.enqueuereadbuffer(req, str(self.queueID), body)['ReadBufferResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        respData = bytearray( binascii.a2b_base64(resp['Data']) )
        #self.assertEqual(respData, Data)

class OpenclqueuesinterfaceKernelLaunchTestCase(unittest.TestCase):

    def setUp(self):
        # super(OpenclinterfaceTestCase, self).setUp();
        super(OpenclqueuesinterfaceKernelLaunchTestCase, self).setUp()
        self.testResources = LaptopResources()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts()
        self.Queues = os_openclqueuesinterface.OpenCLQueues()
        self.Buffers = os_openclbuffersinterface.OpenCLBuffers()
        self.Programs = os_openclprogramsinterface.OpenCLPrograms()
        self.Kernels = os_openclkernelsinterface.OpenCLKernels()
        req = Request()
        body = {'Devices': self.testResources.listDevicesIDs, 'Properties': []}
        resp = self.Contexts.create(req, body)['CreateResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        self.contextID = resp['id']
        # create buffers
        self.bufferSize1 = 32
        body = {'Context': self.contextID, 'MEM_SIZE': self.bufferSize1, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        self.bufferID1 = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)
        self.bufferSize2 = 32
        body = {'Context': self.contextID, 'MEM_SIZE': self.bufferSize2, 'BufferProperties': []}
        bufferCreateResp = self.Buffers.create(req, body)['CreateResp']
        self.bufferID2 = bufferCreateResp['id']
        self.assertEqual(bufferCreateResp['CL_ERROR_CODE'], 0)
        # create queue
        body = {'Context': self.contextID, 'Device': self.testResources.listDevicesOnSystem[0]}
        resp = self.Queues.create(req, body)['CreateResp']
        self.queueID = resp['id']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        # create and build program
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
        # create kernel
        kernelName = self.testResources.KernelFunctionName
        body = {'Program': self.programID, 'KernelName': kernelName}
        resp = self.Kernels.create(req, body)['CreateResp']
        self.kernelID = resp['id']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)

    def tearDown(self):
        body = None
        req = Request()
        # release the buffers
        retErr = self.Buffers.release(req, str(self.bufferID1), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Buffers.release(req, str(self.bufferID2), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        # release the queue
        retErr = self.Queues.release(req, str(self.queueID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Kernels.release(req, str(self.kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Programs.release(req, str(self.programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        retErr = self.Contexts.release(req, str(self.contextID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

    def testLaunchKernel1(self):
        # det kernel parameters
        req = Request()
        byteArrayParam = bytearray( '2222' )
        charArrayParambase64 = binascii.b2a_base64(byteArrayParam)
        body = {'ArgIndex': 0, 'HostValue': charArrayParambase64}
        retErr = self.Kernels.setkernelarg(req, str(self.kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'ArgIndex': 1, 'DeviceMemoryObject': self.bufferID1}
        retErr = self.Kernels.setkernelarg(req, str(self.kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'ArgIndex': 2, 'LocalMemory': 16}
        retErr = self.Kernels.setkernelarg(req, str(self.kernelID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        body = {'Kernel': self.kernelID, 'GlobalWorkOffset': [{'Size': 0}], 
                'GlobalWorkSize': [{'Size': 2}], 'LocalWorkSize':[{'Size': 2}]}
        req = Request()
        retErr = self.Queues.enqueuendrangekernel(req, str(self.queueID), body)['CL_ERROR_CODE']
        DataIntControl = bytearray('22222222')
        body = {'Buffer': self.bufferID1, 'Offset': 0, 'ByteCount': int(len(DataIntControl))}
        resp = self.Queues.enqueuereadbuffer(req, str(self.queueID), body)['ReadBufferResp']
        self.assertEqual(resp['CL_ERROR_CODE'], 0)
        respData = bytearray( binascii.a2b_base64(resp['Data']) )
        self.assertEqual(respData, DataIntControl)

if __name__ == "__main__":
    unittest.main()


