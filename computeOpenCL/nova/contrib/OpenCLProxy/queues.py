from kombu import Exchange, Queue

task_exchange = Exchange("opencl", type="topic", delivery_mode = 1)#, 
                         # auto_delete = True, durable = False)
queue_opencl_devices = Queue("opencl.devices", task_exchange, routing_key = 'opencl.devices') #,
                             # durable = False , auto_delete = True)
queue_opencl_contexts = Queue("opencl.contexts", task_exchange, routing_key = 'opencl.contexts') #,
                             # durable = False) #, auto_delete = True)
queue_opencl_buffers = Queue("opencl.buffers", task_exchange, routing_key = 'opencl.buffers') #,
                             # durable = False) #, auto_delete = True)
queue_opencl_programs = Queue("opencl.programs", task_exchange, routing_key = 'opencl.programs') #, 
                             # durable = False) #, auto_delete = True)
queue_opencl_kernels = Queue("opencl.kernels", task_exchange, routing_key = 'opencl.kernels') #,
                             # durable = False) #, auto_delete = True)
queue_opencl_command_queues = Queue("opencl.commandqueues", task_exchange, 
                             routing_key = 'opencl.commandqueues') #,
                             # durable = False) #, auto_delete = True)
queue_opencl_nodes = Queue("opencl.nodes", task_exchange, routing_key = 'opencl.nodes') #,
                             # durable = False) #, auto_delete = True)
queue_opencl_notify = Queue("openclnotify", task_exchange, routing_key = 'opencl.#'),
                             # durable = False) #, auto_delete = True)

