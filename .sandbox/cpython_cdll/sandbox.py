# -*- coding: utf-8 -*-
import ctypes

lib = ctypes.cdll.LoadLibrary("./sandbox.so")

# lib.new_TestStruct.argtypes = []
lib.new_TestStruct.restype = ctypes.c_void_p

lib.delete_TestStruct.argtypes = [ctypes.c_void_p]
# lib.delete_TestStruct.restype = ctypes.c_void_p

lib.TestStruct_incrementN.argtypes = [ctypes.c_void_p]
# lib.TestStruct_incrementN.restype = ctypes.c_int


class TestStruct:
    def __init__(self):
        self._obj = lib.new_TestStruct()

    def __del__(self):
        lib.delete_TestStruct(self._obj)

    def incrementN(self):
        return lib.TestStruct_incrementN(self._obj)


if __name__ == "__main__":
    t = TestStruct()
    print(t)
    print(t._obj)
    print(t.incrementN())
