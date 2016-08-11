# visitor.py -- Simple Visitor Pattern implementation in Python3
# Copyright (C) <2016>  <Germano Gabbianelli>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import functools
import types
import typing


def swap_self(func):
    def wrapper(obj, self, *args, **kwargs):
        return func(self, obj, *args, **kwargs)
    return wrapper


class _ns(dict):
    KEY = 'visit'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = d = functools.singledispatch(self.default)

        def visit(self, obj, *args, **kwargs):
            return d(obj, self, *args, **kwargs)

        super().__setitem__(self.KEY, visit)

    @staticmethod
    def default(obj, self, *args, **kwargs):
        try:
            fn = self.default
        except AttributeError:
            raise TypeError("No method")

        return fn(obj, *args, **kwargs)


    def __setitem__(self, key, func):
        # should I use MethodType?
        if key != self.KEY or not isinstance(func, types.FunctionType):
            return super().__setitem__(key, func)

        obj_name = func.__code__.co_varnames[1] # FIXME handle error
        cls = typing.get_type_hints(func)[obj_name]

        self.dispatcher.register(cls, swap_self(func))



class Visitor(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return _ns()
