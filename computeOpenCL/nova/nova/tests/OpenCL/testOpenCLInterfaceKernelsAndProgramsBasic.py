import unittest
from nova.OpenCL import OpenCLContextsAPI
from nova.OpenCL import OpenCLClientException
from nova.OpenCL import OpenCLProgramsAPI
from nova.OpenCL import OpenCLKernelsAPI
import sys

class LaptopResources:
    listDevicesIDs = [0]
    dictProperties = {}
    invalidProgramID = 10
    invalidKernelID = 10
    programCodeStrings = ["__kernel void dummy(int a){ int ii = a; }",]
    programCodeStringsCompilationError = ["__kernel void dummy(int a){ int ii = a }",]
    KernelFunctionName = "dummy"
    device_type = "GPU"

class TestPrograms(unittest.TestCase):
    # define the expected response
    testResources = LaptopResources()
    contexts_interface = OpenCLContextsAPI.API()
    programs_interface = OpenCLProgramsAPI.API()
    kernels_interface = OpenCLKernelsAPI.API()

    def setUp(self):
        self.contextID, retErr = self.contexts_interface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        retErr = self.contexts_interface.ReleaseContext(self.contextID)
        self.assertEqual(retErr, 0)

    def testCreateProgram(self):
        # creates a new program
        programID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [programID])
        programProperty, retErr = self.programs_interface.GetProgramProperties(programID)
        self.assertEqual(programProperty['id'], programID)
        self.assertEqual(programProperty['Devices'], self.testResources.listDevicesIDs)
        self.assertEqual(programProperty['Context'], self.contextID)
        retErr = self.programs_interface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])

    def testGetUnknownObjectProperties(self):
        # Tries to retrieve the properties of an inexistent device
        programID = self.testResources.invalidProgramID
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.programs_interface.GetProgramProperties, programID)
       
    def testRetainAndRelease(self):
        # Create and release a context
        
        programID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [programID])
        retErr = self.programs_interface.ReleaseProgram( programID )
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])
        # try to release again
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.programs_interface.ReleaseProgram, programID)
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.programs_interface.RetainProgram, programID)

    def testMultiplePrograms(self):
        # Creates multiple programs
        
        program1ID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [program1ID])
        program2ID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [program1ID, program2ID])
        program1Property, retErr = self.programs_interface.GetProgramProperties(program1ID)
        self.assertEqual(program1Property['id'], program1ID)
        self.assertEqual(program1Property['Devices'], self.testResources.listDevicesIDs)
        self.assertEqual(program1Property['Context'], self.contextID)
        program2Property, retErr = self.programs_interface.GetProgramProperties(program2ID)
        self.assertEqual(program2Property['id'], program2ID)
        self.assertEqual(program2Property['Devices'], self.testResources.listDevicesIDs)
        self.assertEqual(program2Property['Context'], self.contextID)
        retErr = self.programs_interface.ReleaseProgram( program1ID )
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [program2ID])
        retErr = self.programs_interface.ReleaseProgram( program2ID )
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])

    def testBuildProgramSuccess(self):
        programID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = self.programs_interface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        self.assertEqual(retErr, 0)
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        dictResp, retErr = self.programs_interface.GetProgramBuildInfo(programID, self.testResources.listDevicesIDs[0], buildInfo);
        self.assertEqual(retErr, 0)
        self.assertEqual(dictResp['CL_PROGRAM_BUILD_STATUS'], 'CL_BUILD_SUCCESS')
        retErr = self.programs_interface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])

    def testBuildProgramFail(self):
        programID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStringsCompilationError)
        buildOptions = ""
        retErr = self.programs_interface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        dictResp, retErr = self.programs_interface.GetProgramBuildInfo(programID, self.testResources.listDevicesIDs[0], buildInfo);
        self.assertEqual(retErr, 0)
        self.assertEqual(dictResp['CL_PROGRAM_BUILD_STATUS'], 'CL_BUILD_ERROR')
        buildInfo = "CL_PROGRAM_BUILD_LOG"
        dictResp, retErr = self.programs_interface.GetProgramBuildInfo(programID, self.testResources.listDevicesIDs[0], buildInfo);
        self.assertEqual(retErr, 0)
        retErr = self.programs_interface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])

    def testCreateKernel(self):
        # create program
        programID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = self.programs_interface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        self.assertEqual(retErr, 0)
        #create kernel
        kernelName = self.testResources.KernelFunctionName
        kernelID, retErr = self.kernels_interface.CreateKernel(programID, kernelName)
        self.assertEqual(retErr, 0)
        kernelProperties, retErr = self.kernels_interface.GetKernelProperties(kernelID)
        self.assertEqual(kernelProperties['Program'], programID)
        self.assertEqual(kernelProperties['id'], kernelID)
        self.assertEqual(kernelProperties['Context'], self.contextID)
        self.assertEqual(kernelProperties['KernelFunctionName'], kernelName)
        retErr = self.kernels_interface.ReleaseKernel(kernelID)
        self.assertEqual(retErr, 0)
        retErr = self.programs_interface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])

    def testGetUnknownKernelObjectProperties(self):
        programID = self.testResources.invalidKernelID
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.kernels_interface.GetKernelProperties, programID)

    def testRetainAndReleaseKernels(self):
        # create program
        programID, retErr = self.programs_interface.CreateProgram(self.contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = self.programs_interface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        self.assertEqual(retErr, 0)
        #create kernel
        kernelName = self.testResources.KernelFunctionName
        kernelID, retErr = self.kernels_interface.CreateKernel(programID, kernelName)
        self.assertEqual(retErr, 0)
        listKernels = self.kernels_interface.ListKernels()
        self.assertEqual(listKernels, [kernelID])
        retErr = self.kernels_interface.RetainKernel(kernelID)
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.ReleaseKernel(kernelID)
        self.assertEqual(retErr, 0)
        retErr = self.kernels_interface.ReleaseKernel(kernelID)
        self.assertEqual(retErr, 0)
        listKernels = self.kernels_interface.ListKernels()
        self.assertEqual(listKernels, [])
        # try to release again
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.kernels_interface.ReleaseKernel, kernelID)
        self.assertRaises(OpenCLClientException.OpenCLClientException, self.kernels_interface.RetainKernel, kernelID)
        retErr = self.programs_interface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = self.programs_interface.ListPrograms()
        self.assertEqual(listPrograms, [])


if __name__ == "__main__":
    unittest.main()

