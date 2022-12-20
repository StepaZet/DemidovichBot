class Event:
    def __init__(self, *args, **kwargs):
        self._functions = []

    def __call__(self, *args, **kwargs):
        for function in self._functions:
            function(*args, **kwargs)

    def __iadd__(self, function):
        self._functions.append(function)
        return self

    def __isub__(self, function):
        self._functions.remove(function)
        return self
