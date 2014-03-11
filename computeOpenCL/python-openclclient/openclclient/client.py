from novaclient import extension
from novaclient.v1_1 import client
from swiftclient import client as cs
from novaclient import utils
from novaclient.v1_1.contrib import list_extensions
from novaclient.v1_1.contrib import openclcontexts
from novaclient.v1_1.contrib import opencldevices
from novaclient.v1_1.contrib import openclprograms
from novaclient.v1_1.contrib import openclbuffers
from novaclient.v1_1.contrib import openclkernels
from novaclient.v1_1.contrib import openclqueues
from binascii import unhexlify
from binascii import hexlify
import random
import os
import uuid 

class Client(object):
    def __init__(self, username = None, api_key = None, 
                 auth_url = None, project_id = None,
                 tenant_name = None):
        if (username == None) :
            username = os.environ['OS_USERNAME']
        if (api_key == None) :
            api_key = os.environ['OS_PASSWORD']
        if (auth_url == None) :
            auth_url = os.environ['OS_AUTH_URL']
        if (project_id == None) : 
            project_id = os.environ['OS_TENANT_NAME']
        if (tenant_name == None) :
            tenant_name = os.environ['OS_TENANT_NAME']
        self.username = username
        self.api_key = api_key
        self.auth_url = auth_url
        self.tenant_name = tenant_name
        self.project_id = project_id
        extensions = [
            extension.Extension(openclcontexts.__name__.split(".")[-1], openclcontexts),
            extension.Extension(opencldevices.__name__.split(".")[-1], opencldevices),
            extension.Extension(openclprograms.__name__.split(".")[-1], openclprograms),
            extension.Extension(openclbuffers.__name__.split(".")[-1], openclbuffers),
            extension.Extension(openclkernels.__name__.split(".")[-1], openclkernels),
            extension.Extension(openclqueues.__name__.split(".")[-1], openclqueues),
            ]
        d = {}
        d['username'] = self.username
        d['api_key'] = self.api_key
        d['auth_url'] = self.auth_url
        d['project_id'] = self.project_id
        self.cl = client.Client(http_log_debug = True, extensions=extensions, **d)
        self.swift_url, self.swift_token = cs.get_keystoneclient_2_0(self.auth_url, 
                                                                     self.username,
                                                                     self.api_key,
                                                                     {'tenant_name': self.tenant_name})
        self.opencldevices = self.cl.opencldevices
        self.openclcontexts = self.cl.openclcontexts
        self.openclprograms = self.cl.openclprograms
        self.openclkernels = self.cl.openclkernels
        self.openclbuffers = self.cl.openclbuffers
        self.openclqueues = self.OpenCLQueues( self.cl, self.swift_url, self.swift_token, 
                                               self.username, self.api_key, self.tenant_name)

    class OpenCLQueues( object ):
        def __init__(self, novaclient, swifturl, swifttoken, 
                      username, password, tenant_name ):
            self.nc = novaclient
            self.swifturl = swifturl
            self.swifttoken = swifttoken
            self.username = username
            self.password = password
            self.tenant_name = tenant_name

        def list(self):
            return self.nc.openclqueues.list()

        def show(self, queue_id):
            return self.nc.openclqueues.show(queue_id)

        def create(self, Device, Context, listProperties):
            return self.nc.openclqueues.create(Device, Context, listProperties)

        def retain(self, queue_id):
            return self.nc.openclqueues.retain(queue_id)

        def release(self, queue_id):
            return self.nc.openclqueues.release(queue_id)
        
        def enqueuereadbuffer(self, queue_id, buffer_id, ByteCount,
                              blocking_read=True, Offset=0,
                              wait_event_list=None, done_event=None):
            container_id = str(uuid.uuid4())
            cs.put_container(url = self.swifturl, token = self.swifttoken, container = container_id)
            resp =  self.nc.openclqueues.enqueuereadbuffer(queue_id, buffer_id, ByteCount,
                                              self.username, self.password,
                                              self.tenant_name, container_id,
                                              self.swifturl,
                                              self.swifttoken,
                                              blocking_read, Offset,
                                              wait_event_list, done_event)
            # retrieve the object from swift
            respdict, data = cs.get_object(url = self.swifturl, 
                                           token = self.swifttoken, 
                                           container = container_id,
                                           name = resp[0])
            # delete the object
            cs.delete_object(url = self.swifturl, 
                             token = self.swifttoken, 
                             container = container_id,
                             name = resp[0])
            # delete the container
            cs.delete_container(url = self.swifturl, 
                                token = self.swifttoken, 
                                container = container_id)
            return data, resp[1]
 
        def enqueuewritebuffer(self, queue_id, buffer_id, ByteCount, 
                           data, 
                           blocking_write=True, Offset=0,
                           wait_event_list=None, done_event=None):
            container_id = str(uuid.uuid4())
            cs.put_container(url = self.swifturl, token = self.swifttoken, container = container_id)
            object_id = str(uuid.uuid4())
            cs.put_object(url = self.swifturl, token = self.swifttoken, 
                          container = container_id, 
                          name = object_id,
                          contents = data,
                          content_length = len(data))
            resp = self.nc.openclqueues.enqueuewritebuffer(queue_id, buffer_id, ByteCount, 
                           object_id, container_id, 
                           self.username, self.password,
                           self.tenant_name, 
                           self.swifturl,
                           self.swifttoken,
                           blocking_write, Offset,
                           wait_event_list, done_event)
            # delete the object
            cs.delete_object(url = self.swifturl, 
                             token = self.swifttoken, 
                             container = container_id,
                             name = object_id)
            # delete the container
            cs.delete_container(url = self.swifturl, 
                                token = self.swifttoken, 
                                container = container_id)
            return resp
 
        def enqueuecopybuffer(self, queue_id, source_buffer_id, destination_buffer_id, 
                              ByteCount,
                              blocking_copy=True, 
                              source_offset=0, destination_offset=0, 
                              wait_event_list=None, done_event=None):
            return self.nc.openclqueues.enqueuecopybuffer(queue_id, source_buffer_id, 
                                             destination_buffer_id, 
                                             ByteCount, blocking_copy, 
                                             source_offset, destination_offset, 
                                             wait_event_list, done_event)

        def enqueuendrangekernel(self, queue_id, kernel_id, 
                                 global_size, global_offset, local_size,
                                 wait_event_list=None, done_event=None):
            return self.nc.openclqueues.enqueuendrangekernel(queue_id, kernel_id, 
                                     global_size, global_offset, local_size,
                                     wait_event_list, done_event)
 
        def enqueuetask(self, queue_id, kernel_id, 
                      wait_event_list=None, done_event=None):
            return self.nc.openclqueues.enqueuetask(queue_id, kernel_id, 
                      wait_event_list, done_event)

        def enqueuebarrier(self, queue_id):
            return self.nc.openclqueues.enqueuebarrier(queue_id)
 
        def finish(self, queue_id):
            return self.nc.openclqueues.finish(queue_id)
     
