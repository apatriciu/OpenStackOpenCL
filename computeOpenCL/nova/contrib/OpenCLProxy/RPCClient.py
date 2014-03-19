from __future__ import with_statement
import sys
from kombu.common import maybe_declare
from kombu.pools import producers
from kombu import BrokerConnection
from kombu.utils import uuid

class RPCClient(object):
    def __init__(self, strBroker, timeout = None):
        self._strBroker = strBroker
        if not timeout:
            self._timeout = 1

    def call(self, node_exchange_object, 
                   exchange_key,
                   routing_key, 
                   method, 
                   args = None):
        try:
            connection = BrokerConnection(self._strBroker)
            # create the response channel
            respQueueName = str(uuid())
            respQueue = connection.SimpleQueue(respQueueName,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
            with producers[connection].acquire(block=True) as producer:
                maybe_declare(node_exchange_object, producer.channel)
                payload = {"RespQueue": respQueueName, "Source": self._strBroker, 'Method': method, 'args': args}
                producer.publish(payload, exchange = exchange_key, serializer="json", routing_key = routing_key)
            # wait for the response
            resp_message = respQueue.get(block=True, timeout=self._timeout)
            resp_message.ack()
            respQueue.close()
        #respQueue.delete()
        except:
            print ("Exception caught in RPCClient.call: %s" % sys.exc_info()[0])
            raise Exception("RPCClient Exception")
        if type(resp_message.payload['Result']).__name__ in ('list', 'tuple'):
            nElems = len(resp_message.payload['Result'])
            if resp_message.payload['Result'][ nElems - 1 ] == -128:
                raise Exception("RPCClient Exception")
        elif type(resp_message.payload['Result']).__name__ == 'int':
            if resp_message.payload['Result'] == -128:
                raise Exception("RPCClient Exception")
        else:
            raise Exception("RPCClient Exception")
        return resp_message.payload['Result']

def RPCServerResponse(respBrokerUrl, respQueue, payload):
    resp_connection = BrokerConnection(respBrokerUrl)
    resp_queue = resp_connection.SimpleQueue(respQueue,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
    resp_queue.put(payload, serializer='json')
    resp_queue.close()


