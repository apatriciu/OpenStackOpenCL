from Dispatch import Dispatch
from kombu import Exchange
from uuid import uuid4 as uuid

class OpenCLNode:
    def __init__(self, 
                 nodeID):
        self.ID = nodeID
        self.exchange_name = "openclproxy"+self.ID
        self.exchange = Exchange(self.exchange_name, 
                                 type="topic", 
                                 delivery_mode = 1,
                                 durable = False)#, 
                                 # auto_delete = True, 
                                 # durable = False)

class OpenCLNodesManager(Dispatch):

    def __init__(self, str_broker):
        self.str_broker = str_broker
        self.map_opencl_nodes = {}

    def NewNode(self, args = None):
        nodeID = str(uuid())
        self.map_opencl_nodes[nodeID] = OpenCLNode(nodeID)
        return {'NodeId': nodeID}

    def GetExchange(self, NodeId):
        return self.map_opencl_nodes[NodeId].exchange

    def GetExchangeName(self, NodeId):
        return self.map_opencl_nodes[NodeId].exchange_name

    def DeleteNode(self, args = None):
        NodeID = args['NodeId']
        try:
            del self.map_opencl_nodes[NodeId]
        except:
            pass
        return {'NodeId': NodeID}
