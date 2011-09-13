#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from Queue import Queue, Empty, Full
from litebrowser import Browser
from threading import Thread


class Asyncobj(Thread):
    def __init__(self, func, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = func
        Thread.__init__(self)
        self.result = None


    def __call__(self):
        return self


    def is_alive(self):
        try:
            return Thread.is_alive(self)
        except AttributeError:
            return Thread.isAlive(self)


    def run(self):
        self.result = self.func(*self.args, **self.kwargs)


    def get_result(self, timeout=None):
        self.join(timeout)
        return self.result


class Async:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kw):
        func = Asyncobj(self.func, *args, **kw)
        func.start()
        return func

    def __repr__(self):
        return self.func.func_name


class Sender:
    def __init__(dst_num, message, captcha_ callback=None):
        self._callback = callback


class Server:
    def __init__(captcher, callback=None):
        self._callback = callback


def main():
    pass

if __name__ == "__main__":
    exit(main())
