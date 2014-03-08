# test OpenCL extension for nova compute service

import math
from openclclient import client

cl = client.Client()

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

