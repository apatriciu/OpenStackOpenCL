# test OpenCL extension for nova compute service

import math

from novaclient import extension
from novaclient.v1_1 import client
from novaclient.v1_1 import services
from novaclient import utils
from novaclient.v1_1.contrib import list_extensions
from novaclient.v1_1.contrib import openclcontexts
from novaclient.v1_1.contrib import opencldevices
from novaclient.v1_1.contrib import openclprograms
from novaclient.v1_1.contrib import openclbuffers
from novaclient.v1_1.contrib import openclkernels
from novaclient.v1_1.contrib import openclqueues

from credentials import get_nova_creds

creds = get_nova_creds()
extensions = [
    extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
    extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
    extension.Extension(openclqueues.__name__.split(".")[-1], openclqueues),
    ]
cl = client.Client(http_log_debug = True, extensions=extensions, **creds)

print "Create a Context: "
devices = [0, ]
properties = []
context, retVal = cl.openclcontexts.create(devices, properties)
print("Context ID : ", context)
print("retErr : ", retVal)
device = devices[0]

contexts = cl.openclcontexts.list()
print "Contexts : ", contexts

print("create the queue")
properties = []
queue_id, retVal = cl.openclqueues.create(device, context, properties)
print("Queue ID : ", queue_id)
print("retErr : ", retVal)

command_queue_created = True
if retVal != 0: 
    print 'Failed to allocate execution queue resources'
    command_queue_created = False
    
if command_queue_created:
    print("release the queue")
    retVal = cl.openclqueues.release(queue_id)
    print("retErr : ", retVal)

print "Release the Context: "
retVal = cl.openclcontexts.release(context)
print("retErr : ", retVal)

