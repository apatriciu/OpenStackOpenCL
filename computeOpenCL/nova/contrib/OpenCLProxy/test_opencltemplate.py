import unittest
from OpenCLDevicesDispatch import OpenCLDevicesManager
from OpenCLResourcesAliasManager import OpenCLResourcesAliasManager
from FakeRPCClient import FakeRPCClient

class FakeRPCClient(object):
    def __init__(self, strBroker, timeout = None):
        self._strBroker = strBroker

    def call(self, node_exchange_object,
                   exchange_key,
                   routing_key,
                   method,
                   args = None):
        self.__call_dict = { 'exchange_key': exchange_key,
                             'routing_key': routing_key,
                             'method': method,
                             'args': args }

    def calldict(self):
        return self.__call_dict

class TestOpenCLDevicesDispatch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == "__main__"
    unittest.main()


