from Dispatch import Dispatch
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager

class OpenCLContextsManager(Dispatch, 
                            OpenCLResourcesAliasManager):
    '''
    Manages the contexts on the proxy. Essentially maps external id into nodeID, ID and
    forwards the calls to the proper node
    '''

    def __init__(self, rpcclient, openclnodes, opencldevices):
        self.nodemanager = openclnodes
        self.devicesmanager = opencldevices
        self.rpcclient = rpcclient
        Dispatch.__init__(self)
        OpenCLResourcesAliasManager.__init__(self)

    def ListContexts(self, args = None):
        try:
            lstctxt = self.List()
            nErr = 0
        except:
            nErr = -128
            lstctxt = []
        return (lstctxt, nErr)

    def GetContextProperties(self, args):
        nid = int(args['id'])
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            newargs = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".contexts",
                                       method = 'GetContextProperties',
                                       args = newargs)
            ContextProperties = result[0]
            ContextProperties['id'] = nid
            listDevices = []
            for dev in result[0]['Devices']:
                devid = self.devicesmanager.FromNodeAndID(nodeID, dev)
                listDevices.append(devid)
            ContextProperties['Devices'] = listDevices
            nErr = result[1]
        except:
            nErr = -128
            ContextProperties = {}
        return (ContextProperties, nErr)

    def CreateContext(self, args):
        try:
            listDevices = args['Devices']
            listDevicesIDs = []
            listNodesIDs = []
            for devAlias in listDevices:
                nodeID, ID = self.devicesmanager.FromAlias(devAlias)
                listDevicesIDs.append(ID)
                listNodesIDs.append(nodeID)
            # ensure for now that all devices are on the same node
            nodeID = listNodesIDs[0]
            for nID in listNodesIDs:
                if nID != nodeID:
                    raise Exception("Can only create contexts with devices from the same node")
            properties = args['Properties']
            newargs = {'Devices': listDevicesIDs, 'Properties': properties}
            respCreateContext = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".contexts",
                                       method = 'CreateContext',
                                       args = newargs)
            contextID = respCreateContext[0]
            nErr = respCreateContext[1]
            aliasID = self.Insert(nodeID, contextID)
        except:
            return -128
        return aliasID, nErr

    def ReleaseContext(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".contexts",
                                       method = 'ReleaseContext',
                                       args = args)
            if result <= 0:
                # try to delete the context
                self.Delete(nid)
        except:
            return -128
        return result

    def RetainContext(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".contexts",
                                       method = 'RetainContext',
                                       args = args)
        except:
            return -128
        return result

