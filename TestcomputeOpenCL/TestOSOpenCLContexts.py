# test OpenCL extension for nova compute service

from novaclient import extension
from novaclient.v1_1 import client
from novaclient.v1_1 import services
from novaclient import utils
from novaclient.v1_1.contrib import list_extensions
from novaclient.v1_1.contrib import openclcontexts
from credentials import get_nova_creds

creds = get_nova_creds()
extensions = [
    extension.Extension(list_extensions.__name__.split(".")[-1], list_extensions),
    extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
    ]
cl = client.Client(http_log_debug = True, extensions=extensions, **creds)

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

