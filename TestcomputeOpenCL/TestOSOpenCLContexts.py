# test OpenCL extension for nova compute service

from openclclient import client

cl = client.Client()

# check openclinterface list
print "Contexts Initial: "
listcontexts = cl.openclcontexts.list()
print("list contexts : ", listcontexts)

print "Create a Context: "
devices = [0, ]
properties = []
context_id, retErr = cl.openclcontexts.create(devices, properties)
print("Context ID : ", context_id)
print("retErr : ", retErr)

print "Show Context Properties: "
context = cl.openclcontexts.show(context_id)
print(context)
print("Context Devices : ", context.ListDevices)

listcontexts = cl.openclcontexts.list()
print("list contexts : ", listcontexts)

print "Release a Context: "
retErr = cl.openclcontexts.release(context_id)
print("retErr : ", retErr)

listcontexts = cl.openclcontexts.list()
print("list contexts : ", listcontexts)

