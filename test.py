import numpy as np

from astropy import units

# import inspect
#
# class MyClass:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#
# class MyClassLite:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
# obj = MyClass(**{"x":5.0, "y":10.0})
# print(obj.x)
# print(obj.y)
#
#
# argspec = inspect.getargspec(MyClassLite.__init__)
# args = {}
# for argname in argspec.args:
#     if argname not in ["self"]:
#         if hasattr(obj, argname):
#             args[argname] = getattr(obj, argname)
#
# objLite = MyClassLite(**args)
# print(objLite.x, objLite.y)
#
# # for name in signature:
# #     print(name)

# list1 = [0, 1, 2, 3, 4, 5, 6]
#
# idx = [0, 1]
#
# print(np.asarray(list1)[idx])


# a = 5.0 * units.micron
#
# print(a.to(units.m))
