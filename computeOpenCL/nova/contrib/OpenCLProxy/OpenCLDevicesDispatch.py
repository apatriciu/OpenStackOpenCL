from Dispatch import Dispatch
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager
import sys

class OpenCLDevicesManager(Dispatch, OpenCLResourcesAliasManager):

    def __init__(self, rpcclient, openclnodes):
        self.openclnodemanager = openclnodes
        self.rpcclient = rpcclient
        OpenCLResourcesAliasManager.__init__(self)
        Dispatch.__init__(self)

    def ListDevices(self, args = None):
        devlist = self.List()
        return (devlist, 0)

    def RegisterDevices(self, nodeID):
        '''
        Retrieve and register all devices from node nodeID
        '''
        try:
            listDevices, retErr = self.rpcclient.call(node_exchange_object = self.openclnodemanager.GetExchange(nodeID),
                                       exchange_key = self.openclnodemanager.GetExchangeName(nodeID),
                                       routing_key = self.openclnodemanager.GetExchangeName(nodeID) + ".devices",
                                       method = 'ListDevices')
            if retErr != 0:
                raise Exception('ListDevices error node : %s' % nodeID)
            for devID in listDevices:
                self.Insert(nodeID, devID)
        except:
            print "Exception info %s " %  sys.exc_info()[0]
            return False
        return True

    def GetDeviceProperties(self, args):
        try:
            nid = int(args['id'])
            nodeID, ID = self.FromAlias(nid)
            result = self.rpcclient.call(node_exchange_object = self.openclnodemanager.GetExchange(nodeID),
                                       exchange_key = self.openclnodemanager.GetExchangeName(nodeID),
                                       routing_key = self.openclnodemanager.GetExchangeName(nodeID) + ".devices",
                                       method = 'GetDeviceProperties',
                                       args = {'id': ID})
            print 'Device Properties : ', result
            # change the id of the device to the global alias
            result[0]['id'] = nid
        except:
            nErr = -128
            DeviceProperties = {}
            return nErr
        return result

