from __future__ import with_statement
from queues import task_exchange
import sys
from kombu.common import maybe_declare
from kombu.pools import producers
from kombu import BrokerConnection
import OpenCLClientException
from nova.openstack.common.gettextutils import _
from nova.openstack.common import log as logging
from kombu.utils import uuid

LOG = logging.getLogger(__name__)

class OpenCLRPCAPI(object):
    def __init__(self, routing_key, exchange, respQueueName, target = None, source = None, timeout = None):
        if not target:
            self._target = "amqp://guest:supersecret@192.168.2.20:5672//"
        if not source:
            self._source = "amqp://guest:supersecret@192.168.2.20:5672//"
        if not timeout:
            self._timeout = 1
        self._routing_key = routing_key
        self._exchange = exchange
        self._respQueueName = respQueueName

    def CallServer(self, method, args = None):
        try:
            connection = BrokerConnection(self._target)
            # create the response channel
            respQueueName = self._respQueueName + str(uuid())
            respconnection = BrokerConnection(self._source)
            respQueue = respconnection.SimpleQueue(respQueueName,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
            with producers[connection].acquire(block=True) as producer:
                maybe_declare(task_exchange, producer.channel)
                payload = {"RespQueue": respQueueName, "Source": self._source, 'Method': method, 'args': args}
                producer.publish(payload, exchange = self._exchange, serializer="json", routing_key = self._routing_key)
            # wait for the response
            resp_message = respQueue.get(block=True, timeout=1)
            resp_message.ack()
            respQueue.close()
            #respQueue.delete()
        except:
            LOG.debug(_("Exception caught : %s"), sys.exc_info()[0])
            raise OpenCLClientException.OpenCLClientException("OpenCL Interface Exception")
        if type(resp_message.payload['Result']).__name__ in ('list', 'tuple'):
            nElems = len(resp_message.payload['Result'])
            if resp_message.payload['Result'][ nElems - 1 ] == -128:
                raise OpenCLClientException.OpenCLClientException("OpenCL Interface Exception")
        elif type(resp_message.payload['Result']).__name__ == 'int':
            if resp_message.payload['Result'] == -128:
                raise OpenCLClientException.OpenCLClientException("OpenCL Interface Exception")
        else:
            raise OpenCLClientException.OpenCLClientException("OpenCL Interface Exception")
        return resp_message.payload['Result']

