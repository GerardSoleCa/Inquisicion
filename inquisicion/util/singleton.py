from abc import abstractmethod


class Singleton(object):
    """Use to create a singleton"""

    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    @abstractmethod
    def init(self, *args, **kwds):
        raise NotImplementedError
