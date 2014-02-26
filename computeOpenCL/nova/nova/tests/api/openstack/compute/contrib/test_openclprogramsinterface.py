from nova.api.openstack.compute.contrib import openclprogramsinterface as os_openclprogramsinterface
from nova.api.openstack.compute.contrib import openclinterface as os_openclinterface
import unittest
import webob

#from nova import test

class LaptopResources:
    listDevicesOnSystem = [0]
    listDevicesIDs = [{"Device": 0}]
    inexistentProgram = 100
    programCodeStrings = ["__kernel void dummy(int a){ int ii = a; }",]
    programCodeStringsCompilationError = ["__kernel void dummy(int a){ int ii = a }",]
    device_type = "GPU"

class Request:
    environ = {'nova.context': {'user': 'guest', 'project': 'guest'}}

class OpenclprogramsinterfaceTestCase(unittest.TestCase):

    def setUp(self):
        # super(OpenclinterfaceTestCase, self).setUp();
        super(OpenclprogramsinterfaceTestCase, self).setUp()
        self.testResources = LaptopResources()
        self.Devices = os_openclinterface.OpenCLDevices()
        self.Contexts = os_openclinterface.OpenCLContexts()
        self.Programs = os_openclprogramsinterface.OpenCLPrograms();
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

    def testCreateProgram(self):
        """Creates a new program"""
        # create mem program
        req = Request()
        listProgramStringsPairs = []
        for progstr in self.testResources.programCodeStrings:
            listProgramStringsPairs.append({'ProgramString': progstr})
        body = {'Context': self.contextID, 'ListProgramStrings': listProgramStringsPairs}
        resp = self.Programs.create(req, body)['CreateResp']
        programID = resp['id']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listPrograms = self.Programs.index(req)['Programs']
        self.assertEqual(listPrograms, [{'id': programID}]) 
        programProperty= self.Programs.show(req, str(programID))['Program']
        self.assertEqual(programProperty['CL_ERROR_CODE'], 0)
        self.assertEqual(programProperty['id'], programID)
        self.assertEqual(programProperty['ListDevices'], self.testResources.listDevicesIDs)
        self.assertEqual(programProperty['Context'], self.contextID)
        body = None
        retErr = self.Programs.release(req, str(programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        listPrograms = self.Programs.index(req)['Programs']
        self.assertEqual(len(listPrograms), 0) 

    def testBuildProgramSuccess(self):
        """Program compiling to SUCCESS"""
        req = Request()
        listProgramStringsPairs = []
        for progstr in self.testResources.programCodeStrings:
            listProgramStringsPairs.append({'ProgramString': progstr})
        body = {'Context': self.contextID, 'ListProgramStrings': listProgramStringsPairs}
        resp = self.Programs.create(req, body)['CreateResp']
        programID = resp['id']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        buildOptions = ""
        body = {'ListDevices': self.testResources.listDevicesIDs, 'CompileOptions': buildOptions}
        retErr = self.Programs.build(req, str(programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        body = {'Device': self.testResources.listDevicesIDs[0]['Device'], 'ParamName': buildInfo}
        resp = self.Programs.buildinfo(req, str(programID), body)['BuildInfoResp']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        self.assertEqual(resp['ParamData'], 'CL_BUILD_SUCCESS')
        body = None
        retErr = self.Programs.release(req, str(programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)


    def testBuildProgramFail(self):
        """Program with compilation error"""
        req = Request()
        listProgramStringsPairs = []
        for progstr in self.testResources.programCodeStringsCompilationError:
            listProgramStringsPairs.append({'ProgramString': progstr})
        body = {'Context': self.contextID, 'ListProgramStrings': listProgramStringsPairs}
        resp = self.Programs.create(req, body)['CreateResp']
        programID = resp['id']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        buildOptions = ""
        body = {'ListDevices': self.testResources.listDevicesIDs, 'CompileOptions': buildOptions}
        retErr = self.Programs.build(req, str(programID), body)['CL_ERROR_CODE']
        buildInfo = "CL_PROGRAM_BUILD_STATUS"
        body = {'Device': self.testResources.listDevicesIDs[0]['Device'], 'ParamName': buildInfo}
        resp = self.Programs.buildinfo(req, str(programID), body)['BuildInfoResp']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        self.assertEqual(resp['ParamData'], 'CL_BUILD_ERROR')
        buildInfo = "CL_PROGRAM_BUILD_LOG"
        body = {'Device': self.testResources.listDevicesIDs[0]['Device'], 'ParamName': buildInfo}
        resp = self.Programs.buildinfo(req, str(programID), body)['BuildInfoResp']
        retErr = resp['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)
        print 'Build Log : ', resp['ParamData']
        body = None
        retErr = self.Programs.release(req, str(programID), body)['CL_ERROR_CODE']
        self.assertEqual(retErr, 0)

if __name__ == "__main__":
    unittest.main()

