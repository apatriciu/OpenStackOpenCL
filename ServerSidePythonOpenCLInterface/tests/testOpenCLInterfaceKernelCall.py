import unittest
import PyOpenCLInterface
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

    def setUp(self):
        retErr = PyOpenCLInterface.Initialize(self.testResources.device_type)
        self.assertEqual(retErr, 0)
        self.contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, 
                self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        queueCreateFlags = []
        self.queueID, retErr = PyOpenCLInterface.CreateQueue(self.contextID, 
                self.testResources.listDevicesIDs[0], queueCreateFlags)
        self.assertEqual(retErr, 0)
        self.nLocalThreads = 1
        self.nGlobalThreads = 1
        self.intVal = 101
        self.testByteArrayInts = PyTestObjects.VarAsByteArray(self.intVal, "i")
        self.bufferSizeInts = len(self.testByteArrayInts)
        zero = 0
        self.zeroByteArrayInts = PyTestObjects.VarAsByteArray(zero, "i")
        bufferCreateFlags = []
        self.bufferIntsID, retErr = PyOpenCLInterface.CreateBuffer(self.contextID, 
                self.nGlobalThreads * self.bufferSizeInts, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.floatVal = 3.5
        self.testByteArrayFloats = PyTestObjects.VarAsByteArray(self.floatVal, "f")
        self.bufferSizeFloats = len(self.testByteArrayFloats)
        self.bufferFloatsID, retErr = PyOpenCLInterface.CreateBuffer(self.contextID,
                self.nGlobalThreads * self.bufferSizeInts, bufferCreateFlags)
        self.assertEqual(retErr, 0)
        self.programID, retErr = PyOpenCLInterface.CreateProgram(self.contextID, self.pkr.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = PyOpenCLInterface.BuildProgram(self.programID, self.testResources.listDevicesIDs, buildOptions)
        if retErr != 0:
           buildInfo = "CL_PROGRAM_BUILD_STATUS"
           dictResp, retErr = PyOpenCLInterface.GetProgramBuildInfo(self.programID, self.testResources.listDevicesIDs[0], buildInfo);
           self.assertEqual(retErr, 0)
           print dictResp
           if dictResp["CL_PROGRAM_BUILD_STATUS"] != "CL_BUILD_SUCCESS":
               buildInfo = "CL_PROGRAM_BUILD_LOG"
               dictRest, retErr = PyOpenCLInterface.GetProgramBuildInfo(self.programID, self.testResources.listDevicesIDs[0], buildInfo); 
               print dictRest
           self.assertEqual(0, 1)
        self.kernelID1, retErr = PyOpenCLInterface.CreateKernel(self.programID, self.pkr.kernelname1)
        self.assertEqual(retErr, 0)
        self.kernelID2, retErr = PyOpenCLInterface.CreateKernel(self.programID, self.pkr.kernelname2)
        self.assertEqual(retErr, 0)
        self.kernelID3, retErr = PyOpenCLInterface.CreateKernel(self.programID, self.pkr.kernelname3)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = PyOpenCLInterface.ReleaseKernel(self.kernelID1)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseKernel(self.kernelID2)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseKernel(self.kernelID3)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseProgram(self.programID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseBuffer(self.bufferIntsID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseBuffer(self.bufferFloatsID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseQueue(self.queueID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)


    def testKernelLaunch(self):
        """Launch the kernel"""
        # initialize the device memory to 0
        retErr = PyOpenCLInterface.EnqueueWriteBuffer(self.queueID, self.bufferIntsID, 
                             self.bufferSizeInts, 0, self.zeroByteArrayInts)
        self.assertEqual(retErr, 0)
        # set kernel parameters
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID1, 0, {'HostValue': self.testByteArrayInts});
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID1, 1, {'DeviceMemoryObject': self.bufferIntsID});
        self.assertEqual(retErr, 0)
        globalOffset = [0]
        globalworksize = [self.nGlobalThreads]
        localworksize = [self.nLocalThreads]
        retErr = PyOpenCLInterface.EnqueueNDRangeKernel(self.queueID, self.kernelID1, globalOffset, globalworksize, localworksize);
        self.assertEqual(retErr, 0)
        retData, retErr = PyOpenCLInterface.EnqueueReadBuffer(self.queueID, self.bufferIntsID, self.bufferSizeInts, 0)
        self.assertEqual(len(retData), self.bufferSizeInts)
        self.assertEqual(retErr, 0)
        retValue = PyTestObjects.ByteArrayAsVar( retData, "i" )
        self.assertEqual(retValue, self.intVal)

    def testKernelLaunchWSharedMemory(self):
        """Launch kernel with shared memory"""
        # initialize the device memory to 0
        retErr = PyOpenCLInterface.EnqueueWriteBuffer(self.queueID, self.bufferIntsID, 
                                 self.bufferSizeInts, 0, self.zeroByteArrayInts)
        self.assertEqual(retErr, 0)
        # set kernel parameters
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID2, 0, {'HostValue': self.testByteArrayInts});
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID2, 1, {'DeviceMemoryObject': self.bufferIntsID});
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID2, 2, {'LocalMemory': self.bufferSizeInts});
        self.assertEqual(retErr, 0)
        globalOffset = [0]
        globalworksize = [self.nGlobalThreads]
        localworksize = [self.nLocalThreads]
        retErr = PyOpenCLInterface.EnqueueNDRangeKernel(self.queueID, self.kernelID2, globalOffset, globalworksize, localworksize);
        self.assertEqual(retErr, 0)
        retData, retErr = PyOpenCLInterface.EnqueueReadBuffer(self.queueID, self.bufferIntsID, self.bufferSizeInts, 0)
        self.assertEqual(len(retData), self.bufferSizeInts)
        self.assertEqual(retErr, 0)
        retValue = PyTestObjects.ByteArrayAsVar( retData, "i" )
        self.assertEqual(retValue, self.intVal)

    def testKernelLaunchWSharedMemoryAndFloats(self):
        """Launch kernel with shared memory"""
        # set kernel parameters
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID3, 0, {'HostValue': self.testByteArrayFloats});
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID3, 1, {'DeviceMemoryObject': self.bufferFloatsID});
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.KernelSetArgument(self.kernelID3, 2, {'LocalMemory': self.bufferSizeFloats});
        self.assertEqual(retErr, 0)
        globalOffset = [0]
        globalworksize = [self.nGlobalThreads]
        localworksize = [self.nLocalThreads]
        retErr = PyOpenCLInterface.EnqueueNDRangeKernel(self.queueID, self.kernelID3, globalOffset, globalworksize, localworksize);
        self.assertEqual(retErr, 0)
        retData, retErr = PyOpenCLInterface.EnqueueReadBuffer(self.queueID, self.bufferFloatsID, self.bufferSizeFloats, 0)
        self.assertEqual(len(retData), self.bufferSizeFloats)
        self.assertEqual(retErr, 0)
        retValue = PyTestObjects.ByteArrayAsVar( retData, "f" )
        self.assertEqual(retValue, 5.0)

if __name__ == "__main__":
    unittest.main()

