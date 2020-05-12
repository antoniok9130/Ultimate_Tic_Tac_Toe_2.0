# -*- coding: utf-8 -*-
import ctypes

from .UTTT import lib, UTTT


# Signatures
lib.new_MCTS.restype = ctypes.c_void_p
lib.delete_MCTS.argtypes = [ctypes.c_void_p]

lib.MCTS_getParent.argtypes = [ctypes.c_void_p]
lib.MCTS_getParent.restype = ctypes.c_void_p
lib.MCTS_setParent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

lib.MCTS_getNumChildren.argtypes = [ctypes.c_void_p]

lib.MCTS_makeMove.argtypes = [ctypes.c_void_p]
lib.MCTS_chooseMove.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint32,
    ctypes.c_uint32,
]

lib.MCTS_getNumWins.argtypes = [ctypes.c_void_p]
lib.MCTS_getNumWins.restype = ctypes.c_uint64
lib.MCTS_getNumVisits.argtypes = [ctypes.c_void_p]
lib.MCTS_getNumVisits.restype = ctypes.c_uint64
lib.MCTS_incrementWins.argtypes = [ctypes.c_void_p, ctypes.c_int32]
lib.MCTS_incrementVisits.argtypes = [ctypes.c_void_p, ctypes.c_int32]

lib.MCTS_select.argtypes = [ctypes.c_void_p]
lib.MCTS_select.restype = ctypes.c_void_p
lib.MCTS_expand.argtypes = [ctypes.c_void_p]
lib.MCTS_expand.restype = ctypes.c_void_p
lib.MCTS_simulate.argtypes = [ctypes.c_void_p]
lib.MCTS_backprop.argtypes = [ctypes.c_void_p, ctypes.c_int32]
lib.MCTS_select_expand.argtypes = [ctypes.c_void_p]
lib.MCTS_select_expand.restype = ctypes.c_void_p
lib.MCTS_runIterations.argtypes = [ctypes.c_void_p, ctypes.c_int32]
lib.MCTS_runParallelIterations.argtypes = [ctypes.c_void_p, ctypes.c_int32]

lib.MCTS_getHardcodedMove.argtypes = [
    ctypes.c_uint32,
    ctypes.c_uint32,
]


class MCTS(UTTT):
    def __init__(self, obj=None):
        if obj is None:
            self.obj = lib.new_MCTS()
            self.owner = True
        else:
            self.obj = obj
            self.owner = False

    def __del__(self):
        if self.owner:
            lib.delete_MCTS(self.obj)

    @property
    def parent(self):
        return MCTS(lib.MCTS_getParent(self.obj))

    @parent.setter
    def parent(self, p):
        return lib.MCTS_setParent(self.obj, p.obj)

    def num_children(self):
        return lib.MCTS_getNumChildren(self.obj)

    @property
    def num_wins(self):
        return lib.MCTS_getNumWins(self.obj)

    @property
    def num_visits(self):
        return lib.MCTS_getNumVisits(self.obj)

    def increment_wins(self, amount=1):
        lib.MCTS_incrementWins(self.obj, amount)

    def increment_visits(self, amount=1):
        lib.MCTS_incrementVisits(self.obj, amount)

    def make_move(self):
        lib.MCTS_makeMove(self.obj)
        return self.move

    def choose_move(self, g, l):
        lib.MCTS_chooseMove(self.obj, g, l)

    def select(self):
        return MCTS(lib.MCTS_select(self.obj))

    def expand(self):
        return MCTS(lib.MCTS_expand(self.obj))

    def simulate(self):
        return lib.MCTS_simulate(self.obj)

    def backprop(self, winner):
        return lib.MCTS_backprop(self.obj, winner)

    def select_expand(self):
        return MCTS(lib.MCTS_select_expand(self.obj))

    def runIterations(self, numIterations):
        lib.MCTS_runIterations(self.obj, numIterations)

    def runParallelIterations(self, numIterations):
        lib.MCTS_runParallelIterations(self.obj, numIterations)


def getHardcodedMove(g, l):
    return lib.MCTS_getHardcodedMove(g, l)
