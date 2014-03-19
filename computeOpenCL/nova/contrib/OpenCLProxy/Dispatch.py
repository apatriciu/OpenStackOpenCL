
class Dispatch(object):
    def __init__(self):
        pass

    def dispatch(self, method, args = None):
        func = getattr(self, method)
        if not func:
            raise Exception("Method %s is not implemented" % method)
        return func(args)

