from Dispatch import Dispatch
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager

class OpenCLBuffersManager(Dispatch, OpenCLResourcesAliasManager):

    def __init__(self, rpcclient, openclnodes, openclcontexts):
        self.nodemanager = openclnodes
        self.contextsmanager = openclcontexts
        self.rpcclient = rpcclient
        Dispatch.__init__(self)
        OpenCLResourcesAliasManager.__init__(self)

    def ListBuffers(self, args = None):
        try:
            lb = self.List()
            retErr = 0
        except:
            lb = []
            retErr = 0
        return (lb, retErr)

    def GetBufferProperties(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            newargs = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".buffers",
                                       method = 'GetBufferProperties',
                                       args = newargs)
            nErr = result[1]
            BufferProperties = result[0]
            BufferProperties['id'] = nid
            context = BufferProperties['Context']
            contextID = self.contextsmanager.FromNodeAndID(nodeID, context)
            BufferProperties['Context'] = contextID
        except:
            nErr = -128
            BufferProperties = {}
        return (BufferProperties, nErr)

    def CreateBuffer(self, args):
        try:
            context = int(args['Context'])
            size = int(args['Size'])
            properties = args['Properties']
            nodeID, contextID = self.contextsmanager.FromAlias(context)
            newargs = {'Context': contextID, 'Properties': properties, 'Size': size}
            respCreate = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".buffers",
                                       method = 'CreateBuffer',
                                       args = newargs)
            aliasID = self.Insert(nodeID, respCreate[0])
        except:
            return -128
        return aliasID, respCreate[1]

    def ReleaseBuffer(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".buffers",
                                       method = 'ReleaseBuffer',
                                       args = args)
            if result <= 0:
                self.Delete(nid)
        except:
            return -128
        return result

    def RetainBuffer(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            args = {'id': ID}
            result = self.rpcclient.call(node_exchange_object = self.nodemanager.GetExchange(nodeID),
                                       exchange_key = self.nodemanager.GetExchangeName(nodeID),
                                       routing_key = self.nodemanager.GetExchangeName(nodeID) + ".buffers",
                                       method = 'RetainBuffer',
                                       args = args)
        except:
            return -128
        return result

