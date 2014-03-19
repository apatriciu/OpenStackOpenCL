import unittest
import PyOpenCLInterface
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

    def setUp(self):
        retErr = PyOpenCLInterface.Initialize(self.testResources.device_type)
        self.assertEqual(retErr, 0)

    def tearDown(self):
        pass

    def testCreateProgram(self):
        """Creates a new program"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create mem program
        programID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [programID])
        programProperty, retErr = PyOpenCLInterface.GetProgramProperties(programID)
        self.assertEqual(programProperty['id'], programID)
        self.assertEqual(programProperty['Devices'], self.testResources.listDevicesIDs)
        self.assertEqual(programProperty['Context'], contextID)
        retErr = PyOpenCLInterface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testGetUnknownObjectProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        programID = self.testResources.invalidProgramID
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.GetProgramProperties, programID)
       
    def testRetainAndRelease(self):
        """
        Create and release a context
        """
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        programID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [programID])
        retErr = PyOpenCLInterface.ReleaseProgram( programID )
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        # try to release again
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.RetainProgram, programID)
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testMultiplePrograms(self):
        """
        Creates multiple programs
        """
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        program1ID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [program1ID])
        program2ID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [program1ID, program2ID])
        program1Property, retErr = PyOpenCLInterface.GetProgramProperties(program1ID)
        self.assertEqual(program1Property['id'], program1ID)
        self.assertEqual(program1Property['Devices'], self.testResources.listDevicesIDs)
        self.assertEqual(program1Property['Context'], contextID)
        program2Property, retErr = PyOpenCLInterface.GetProgramProperties(program2ID)
        self.assertEqual(program2Property['id'], program2ID)
        self.assertEqual(program2Property['Devices'], self.testResources.listDevicesIDs)
        self.assertEqual(program2Property['Context'], contextID)
        retErr = PyOpenCLInterface.ReleaseProgram( program1ID )
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [program2ID])
        retErr = PyOpenCLInterface.ReleaseProgram( program2ID )
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testBuildProgramSuccess(self):
        """Creates a new context"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create mem program
        programID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = PyOpenCLInterface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        self.assertEqual(retErr, 0)
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        dictResp, retErr = PyOpenCLInterface.GetProgramBuildInfo(programID, self.testResources.listDevicesIDs[0], buildInfo);
        self.assertEqual(retErr, 0)
        self.assertEqual(dictResp['CL_PROGRAM_BUILD_STATUS'], 'CL_BUILD_SUCCESS')
        retErr = PyOpenCLInterface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testBuildProgramFail(self):
        """Program with compilation error"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create program
        programID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStringsCompilationError)
        buildOptions = ""
        retErr = PyOpenCLInterface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        dictResp, retErr = PyOpenCLInterface.GetProgramBuildInfo(programID, self.testResources.listDevicesIDs[0], buildInfo);
        self.assertEqual(retErr, 0)
        self.assertEqual(dictResp['CL_PROGRAM_BUILD_STATUS'], 'CL_BUILD_ERROR')
        buildInfo = "CL_PROGRAM_BUILD_LOG"
        dictResp, retErr = PyOpenCLInterface.GetProgramBuildInfo(programID, self.testResources.listDevicesIDs[0], buildInfo);
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testCreateKernel(self):
        """Creates a new context"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create program
        programID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = PyOpenCLInterface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        self.assertEqual(retErr, 0)
        #create kernel
        kernelName = self.testResources.KernelFunctionName
        kernelID, retErr = PyOpenCLInterface.CreateKernel(programID, kernelName)
        self.assertEqual(retErr, 0)
        kernelProperties, retErr = PyOpenCLInterface.GetKernelProperties(kernelID)
        self.assertEqual(kernelProperties['Program'], programID)
        self.assertEqual(kernelProperties['id'], kernelID)
        self.assertEqual(kernelProperties['Context'], contextID)
        self.assertEqual(kernelProperties['KernelFunctionName'], kernelName)
        retErr = PyOpenCLInterface.ReleaseKernel(kernelID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)

    def testGetUnknownKernelObjectProperties(self):
        """Tries to retrieve the properties of an inexistent device"""
        programID = self.testResources.invalidKernelID
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.GetProgramProperties, programID)

    def testRetainAndReleaseKernels(self):
        """Creates a new context"""
        contextID, retErr = PyOpenCLInterface.CreateContext(self.testResources.listDevicesIDs, self.testResources.dictProperties)
        self.assertEqual(retErr, 0)
        # create program
        programID, retErr = PyOpenCLInterface.CreateProgram(contextID, self.testResources.programCodeStrings)
        self.assertEqual(retErr, 0)
        buildOptions = ""
        retErr = PyOpenCLInterface.BuildProgram(programID, self.testResources.listDevicesIDs, buildOptions)
        self.assertEqual(retErr, 0)
        #create kernel
        kernelName = self.testResources.KernelFunctionName
        kernelID, retErr = PyOpenCLInterface.CreateKernel(programID, kernelName)
        self.assertEqual(retErr, 0)
        listKernels = PyOpenCLInterface.ListKernels()
        self.assertEqual(listKernels, [kernelID])
        retErr = PyOpenCLInterface.RetainKernel(kernelID)
        self.assertEqual(retErr, 0)
        retErr = PyOpenCLInterface.ReleaseKernel(kernelID)
        self.assertEqual(retErr, 1)
        retErr = PyOpenCLInterface.ReleaseKernel(kernelID)
        self.assertEqual(retErr, 0)
        listKernels = PyOpenCLInterface.ListKernels()
        self.assertEqual(listKernels, [])
        # try to release again
        self.assertRaises(PyOpenCLInterface.error, PyOpenCLInterface.RetainKernel, kernelID)
        retErr = PyOpenCLInterface.ReleaseProgram(programID)
        self.assertEqual(retErr, 0)
        listPrograms = PyOpenCLInterface.ListPrograms()
        self.assertEqual(listPrograms, [])
        retErr = PyOpenCLInterface.ReleaseContext(contextID)
        self.assertEqual(retErr, 0)


if __name__ == "__main__":
    unittest.main()

