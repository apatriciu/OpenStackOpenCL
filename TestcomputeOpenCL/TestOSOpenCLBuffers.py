# test OpenCL extension for nova compute service

from novaclient import extension
from novaclient.v1_1 import client
from novaclient.v1_1 import services
from novaclient import utils
from novaclient.v1_1.contrib import list_extensions
from novaclient.v1_1.contrib import openclcontexts
from novaclient.v1_1.contrib import openclbuffers
from novaclient.v1_1.contrib import opencldevices
from credentials import get_nova_creds

creds = get_nova_creds()
extensions = [
    extension.Extension(list_extensions.__name__.split(".")[-1], list_extensions),
    extension.Extension(openclbuffers.__name__.split(".")[-1], openclbuffers),
    extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
    extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
    ]
cl = client.Client(http_log_debug = True, extensions=extensions, **creds)

print("Create a Context: ")
devices = [0, ]
properties = []
context, retErr = cl.openclcontexts.create(devices, properties)
print("Context ID : ", context)
print("retErr : ", retErr)

print("create Buffer")
size = 256
properties = []
buffer_id, retErr = cl.openclbuffers.create(context, size, properties)
print("Buffer ID: ", buffer_id)
print("retErr : ", retErr)

print("list Buffers")
# check openclinterface list
listbuffers = cl.openclbuffers.list()
print("List buffers : ", listbuffers)

print("show Buffer")
oc_buffer = cl.openclbuffers.show(buffer_id)
print("buffer id : ", oc_buffer.id)
print("buffer context : ", oc_buffer.Context)
print("buffer size : ", oc_buffer.MEM_SIZE)

print("retain Buffer")
retErr = cl.openclbuffers.retain(buffer_id)
print("retErr : ", retErr)

print("release Buffer")
retErr = cl.openclbuffers.release(buffer_id)
print("retErr : ", retErr)

print("release Buffer")
retErr = cl.openclbuffers.release(buffer_id)
print("retErr : ", retErr)

print("list Buffers")
# check openclinterface list
listbuffers = cl.openclbuffers.list()
print("List buffers : ", listbuffers)

print "Release the Context: "
retErr = cl.openclcontexts.release(context)
print("retErr : ", retErr)

