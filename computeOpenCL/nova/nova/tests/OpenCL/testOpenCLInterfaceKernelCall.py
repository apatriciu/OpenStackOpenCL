import unittest
from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
from nova.OpenCL import OpenCLProgramsAPI
from nova.OpenCL import OpenCLKernelsAPI
from nova.OpenCL import OpenCLCommandQueuesAPI
from nova.OpenCL import OpenCLBuffersAPI
import binascii
import PyTestObjects
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    device_type = "GPU"

class ProgramAndKernels:
    programCodeStrings = ["__kernel void kernel1(int a, __global int *b){",
                          "  int ii = a;",
                          "  b[get_global_id(0)] = ii;",
                          "}",
                          "__kernel void kernel2(int a, __global int *b, __local int *sh){",
                          "  sh[0] = a;",
                          "  b[get_global_id(0)] = sh[0];",
                          "}",
                          "__kernel void kernel3(float a, __global float *b, __local float *sh){",
                          "  sh[0] = a + 1.5;",
                          "  b[get_global_id(0)] = sh[0];",
                          "}",
                          
                          ]
    kernelname1 = "kernel1"
    kernelname2 = "kernel2"
    kernelname3 = "kernel3"
 
class TestKernelCall(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    pkr = ProgramAndKernels()
    contexts_interface = OpenCLContextsAPI.API()
    buffers_interface = OpenCLBuffersAPI.API()
    command_queues_interface = OpenCLCommandQueuesAPI.API()
    programs_interface = OpenCLProgramsAPI.API()
    kernels_interface = OpenCLKernelsAPI.API()

    def setUp(self):
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, 
                self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueCreateFlags = []
        self.queueID, retErr = self.command_queues_interface.CreateQueue(self.contextID, 
                self.testResources.listDevicesIDs[0], queueCreateFlags)
        self.assertEqual(retErr, 0)
        self.nLocalThreads = 1
        self.nGlobalThreads = 1
        self.intVal = 101
        self.testByteArrayInts = PyTestObjects.VarAsByteArray(self.intVal, "i")
        self.testByteArrayIntsBase64 = str(binascii.b2a_base64(self.testByteArrayInts))
        self.bufferSizeInts = len(self.testByteArrayInts)
        zero = 0
        self.zeroByteArrayInts = PyTestObjects.VarAsByteArray(zero, "i")
        self.zeroByteArrayIntsBase64 = str(binascii.b2a_base64(self.zeroByteArrayInts))
        bufferCreateFlags = []
        self.bufferIntsID, retErr = self.buffers_interface.CreateBuffer(self.contextID, 
                self.nGlobalThreads * self.bufferSizeInts, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.floatVal = 3.5
        self.testByteArrayFloats = PyTestObjects.VarAsByteArray(self.floatVal, "f")
        self.testByteArrayFloatsBase64 = str(binascii.b2a_base64(self.testByteArrayFloats))
        self.bufferSizeFloats = len(self.testByteArrayFloats)
        self.bufferFloatsID, retErr = self.buffers_interface.CreateBuffer(self.contextID,
                self.nGlobalThreads * self.bufferSizeInts, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.programID, retErr = self.programs_interface.CreateProgram(self.contextID, 
                                          self.pkr.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = self.programs_interface.BuildProgram(self.programID, 
                                          self.testResources.listDevicesIDs, 
                                          buildOptions)
        if retErr != 0:
           buildInfo = "CL_PROGRAM_BUILD_STATUS"
           dictResp, retErr = self.programs_interface.GetProgramBuildInfo(self.programID, 
                                          self.testResources.listDevicesIDs[0], 
                                          buildInfo);
           self.assertEqual(retErr, 0)
           print dictResp
           if dictResp["CL_PROGRAM_BUILD_STATUS"] != "CL_BUILD_SUCCESS":
               buildInfo = "CL_PROGRAM_BUILD_LOG"
               dictRest, retErr = self.programs_interface.GetProgramBuildInfo(self.programID, 
                                          self.testResources.listDevicesIDs[0], 
                                          buildInfo); 
               print dictRest
           self.assertEqual(0, 1)
        self.kernelID1, retErr = self.kernels_interface.CreateKernel(self.programID, self.pkr.kernelname1)
        self.assertEqual(retErr, 0)
        self.kernelID2, retErr = self.kernels_interface.CreateKernel(self.programID, self.pkr.kernelname2)
        self.assertEqual(retErr, 0)
        self.kernelID3, retErr = self.kernels_interface.CreateKernel(self.programID, self.pkr.kernelname3)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.kernels_interface.ReleaseKernel(self.kernelID1)
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.ReleaseKernel(self.kernelID2)
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.ReleaseKernel(self.kernelID3)
        self.assertEqual(retErr, 0)
        retErr = self.programs_interface.ReleaseProgram(self.programID)
        self.assertEqual(retErr, 0)
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferIntsID)
        self.assertEqual(retErr, 0)
        retErr = self.buffers_interface.ReleaseBuffer(self.bufferFloatsID)
        self.assertEqual(retErr, 0)
        retErr = self.command_queues_interface.ReleaseQueue(self.queueID)
        self.assertEqual(retErr, 0)
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)


    def testKernelLaunch(self):
        """Launch the kernel"""
        # initialize the device memory to 0
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, self.bufferIntsID, 
                             self.bufferSizeInts, 0, self.zeroByteArrayIntsBase64)
        self.assertEqual(retErr, 0)
        # set kernel parameters
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID1, 
                                                          0, 
                                                          {'HostValue': self.testByteArrayIntsBase64});
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID1, 
                                                          1, 
                                                          {'DeviceMemoryObject': self.bufferIntsID});
        self.assertEqual(retErr, 0)
        globalOffset = [0]
        globalworksize = [self.nGlobalThreads]
        localworksize = [self.nLocalThreads]
        retErr = self.command_queues_interface.EnqueueNDRangeKernel(self.queueID, 
                                                                    self.kernelID1, 
                                                                    globalOffset, 
                                                                    globalworksize, 
                                                                    localworksize);
        self.assertEqual(retErr, 0)
        retDataBase64, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                        self.bufferIntsID, self.bufferSizeInts, 0)
        retData = bytearray(binascii.a2b_base64(retDataBase64))
        self.assertEqual(len(retData), self.bufferSizeInts)
        self.assertEqual(retErr, 0)
        retValue = PyTestObjects.ByteArrayAsVar( retData, "i" )
        self.assertEqual(retValue, self.intVal)

    def testKernelLaunchWSharedMemory(self):
        # Launch kernel with shared memory
        # initialize the device memory to 0
        retErr = self.command_queues_interface.EnqueueWriteBuffer(self.queueID, self.bufferIntsID, 
                                 self.bufferSizeInts, 0, self.zeroByteArrayIntsBase64)
        self.assertEqual(retErr, 0)
        # set kernel parameters
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID2, 
                                        0, {'HostValue': self.testByteArrayIntsBase64});
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID2, 
                                        1, {'DeviceMemoryObject': self.bufferIntsID});
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID2, 
                                        2, {'LocalMemory': self.bufferSizeInts});
        self.assertEqual(retErr, 0)
        globalOffset = [0]
        globalworksize = [self.nGlobalThreads]
        localworksize = [self.nLocalThreads]
        retErr = self.command_queues_interface.EnqueueNDRangeKernel(self.queueID, 
                                             self.kernelID2, 
                                             globalOffset, 
                                             globalworksize, 
                                             localworksize);
        self.assertEqual(retErr, 0)
        retDataBase64, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                             self.bufferIntsID, self.bufferSizeInts, 0)
        retData = bytearray(binascii.a2b_base64(retDataBase64))
        self.assertEqual(len(retData), self.bufferSizeInts)
        self.assertEqual(retErr, 0)
        retValue = PyTestObjects.ByteArrayAsVar( retData, "i" )
        self.assertEqual(retValue, self.intVal)

    def testKernelLaunchWSharedMemoryAndFloats(self):
        # Launch kernel with shared memory and float params
        # set kernel parameters
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID3, 
                                      0, {'HostValue': self.testByteArrayFloatsBase64});
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID3, 
                                      1, {'DeviceMemoryObject': self.bufferFloatsID});
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.KernelSetArgument(self.kernelID3, 
                                      2, {'LocalMemory': self.bufferSizeFloats});
        self.assertEqual(retErr, 0)
        globalOffset = [0]
        globalworksize = [self.nGlobalThreads]
        localworksize = [self.nLocalThreads]
        retErr = self.command_queues_interface.EnqueueNDRangeKernel(self.queueID, 
                                                                    self.kernelID3, 
                                                                    globalOffset, 
                                                                    globalworksize, 
                                                                    localworksize);
        self.assertEqual(retErr, 0)
        retDataBase64, retErr = self.command_queues_interface.EnqueueReadBuffer(self.queueID, 
                                                                          self.bufferFloatsID, 
                                                                          self.bufferSizeFloats, 0)
        retData = bytearray(binascii.a2b_base64(retDataBase64))
        self.assertEqual(len(retData), self.bufferSizeFloats)
        self.assertEqual(retErr, 0)
        retValue = PyTestObjects.ByteArrayAsVar( retData, "f" )
        self.assertEqual(retValue, 5.0)

if __name__ == "__main__":
    unittest.main()

