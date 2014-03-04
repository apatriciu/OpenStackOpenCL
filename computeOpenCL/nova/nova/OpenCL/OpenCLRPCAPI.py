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
from oslo.config import cfg

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

class OpenCLRPCAPI(object):
    def __init__(self, routing_key, exchange, respQueueName, target = None, source = None, timeout = None):
        try:
            config_file = CONF.config_file[0]
        except AttributeError:
            config_file = "/etc/nova/nova.conf"
        configs = cfg.ConfigOpts()
        options = [ cfg.StrOpt('rabbit_host', default = 'localhost'),
                    cfg.StrOpt('rabbit_password', required = 'true'),
                    cfg.StrOpt('rabbit_user', default = 'guest')]
        configs.register_opts( options )
        params_config = ['--config-file', config_file]     
        configs(params_config)
        rh = configs.rabbit_host
        rp = configs.rabbit_password
        ru = configs.rabbit_user
        self._strBroker = "amqp://" + ru + ":" + rp + "@" + rh + ":5672//"
        if not timeout:
            self._timeout = 1
        self._routing_key = routing_key
        self._exchange = exchange
        self._respQueueName = respQueueName

    def CallServer(self, method, args = None):
        try:
            LOG.debug(_("strBroker : %s "), self._strBroker)
            connection = BrokerConnection(self._strBroker)
            # create the response channel
            respQueueName = self._respQueueName + str(uuid())
            respconnection = BrokerConnection(self._strBroker)
            respQueue = respconnection.SimpleQueue(respQueueName,
                                  queue_opts = {'durable': False, 'auto_delete': True},
                                  exchange_opts = {'delivery_mode' : 1,
                                                   'auto_delete' : True,
                                                   'durable' : False})
            with producers[connection].acquire(block=True) as producer:
                maybe_declare(task_exchange, producer.channel)
                payload = {"RespQueue": respQueueName, "Source": self._strBroker, 'Method': method, 'args': args}
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

