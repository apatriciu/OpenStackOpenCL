
class Dispatch(object):
    def __init__(self):
        pass

    def dispatch(self, method, args = None):
        func = getattr(self, method)
        if not func:
            print ("Method %s id not implemented" % method)
            return -128
        return func(args)

