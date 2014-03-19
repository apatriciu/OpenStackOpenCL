from Dispatch import Dispatch
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager

class OpenCLProgramsManager(Dispatch, OpenCLResourcesAliasManager):

    def __init__(self, rpcclient, openclnodes, openclcontexts, opencldevices):
        self.nodesmanager = openclnodes
        self.contextsmanager = openclcontexts
        self.devicesmanager = opencldevices
        self.rpcclient = rpcclient
        Dispatch.__init__(self)
        OpenCLResourcesAliasManager.__init__(self)

    def ListPrograms(self, args = None):
        '''
        List all the programs on the controller
        '''
        try:
            lp = self.List()
            retErr = 0
        except:
            lp = []
            retErr = -128
        return (lp, retErr)

    def GetProgramProperties(self, args):
        '''
        Forwards a GetProgramProperties to the proper compute 
        node and returns the result
        '''
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            newargs = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".programs",
                                       method = 'GetProgramProperties',
                                       args = newargs)
            ProgramProperties = result[0]
            ProgramProperties['id'] = nid
            devList = ProgramProperties['Devices']
            devIDList = []
            for dev in devList:
               devID = self.devicesmanager.FromNodeAndID(nodeID, dev)
               devIDList.append(devID)
            ProgramProperties['Devices'] = devIDList
            oclctxt = ProgramProperties['Context']
            ctxtID = self.contextsmanager.FromNodeAndID(nodeID, oclctxt)
            ProgramProperties['Context'] = ctxtID
            nErr = result[1]
        except:
            nErr = -128
            ProgramProperties = {}
        return (ProgramProperties, nErr)

    def CreateProgram(self, args):
        try:
            context = int(args['Context'])
            programStringsList = args['ProgramStrings']
            nodeID, contextID = self.contextsmanager.FromAlias(context)
            newargs = {'Context': contextID, 'ProgramStrings': programStringsList}
            createProgramResp = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".programs",
                                       method = 'CreateProgram',
                                       args = newargs)
            aliasID = self.Insert(nodeID, createProgramResp[0])
        except:
            return -128
        return aliasID, createProgramResp[1]

    def ReleaseProgram(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".programs",
                                       method = 'ReleaseProgram',
                                       args = args)
            if result <= 0:
                self.Delete(nid)
        except:
            return -128
        return result

    def RetainProgram(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".programs",
                                       method = 'RetainProgram',
                                       args = args)
        except:
            return -128
        return result

    def BuildProgram(self, args):
        try:
            nid = int(args['id'])
            nodeID, progID = self.FromAlias(nid)
            listDevices = args['Devices']
            listDevicesIDs = []
            listNodesIDs = []
            for aliasID in listDevices:
                nID, devID = self.devicesmanager.FromAlias(aliasID)
                listDevicesIDs.append(devID)
                if nID != nodeID:
                    raise Exception("All Devices must be on the same node")
            buildOptions = args['Options']
            newargs = {'Devices': listDevicesIDs, 
                       'Options': buildOptions,
                       'id': progID}
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".programs",
                                       method = 'BuildProgram',
                                       args = newargs)
        except:
            return -128
        return result

    def GetProgramBuildInfo(self, args):
        try:
            nid = int(args['id'])
            npID, progID = self.FromAlias(nid)
            device = int(args['Device'])
            ndID, devID = self.devicesmanager.FromAlias(device)
            if npID != ndID:
                raise Exception('The program must be on the same node as the device')
            buildInfo = args['BuildInfo']
            newargs = {'id': progID, 'Device': devID, 'BuildInfo': buildInfo}
            nodeID = ndID
            result = self.rpcclient.call(node_exchange_object = self.nodesmanager.GetExchange(nodeID),
                                       exchange_key = self.nodesmanager.GetExchangeName(nodeID),
                                       routing_key = self.nodesmanager.GetExchangeName(nodeID) + ".programs",
                                       method = 'GetProgramBuildInfo',
                                       args = newargs)
        except:
            return -128
        return result

