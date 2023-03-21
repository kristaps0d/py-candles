class ExceptionHandler(object):
    
    def __init__(self):
        pass

    def Try(self, function:callable, args:tuple=()):
        try:
            return function(*args)
        except:
            return None

    def TryExcept(self, function:callable, exception:callable):

        try:
            return function()
        except:
            return exception()
