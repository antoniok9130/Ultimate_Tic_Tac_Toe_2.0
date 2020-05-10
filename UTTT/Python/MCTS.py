# -*- coding: utf-8 -*-
import ctypes

from UTTT import lib, UTTT


# Signatures
lib.new_MCTS.restype = ctypes.c_void_p
lib.delete_MCTS.argtypes = [ctypes.c_void_p]

lib.MCTS_getParent.argtypes = [ctypes.c_void_p]
lib.MCTS_getParent.restype = ctypes.c_void_p
lib.MCTS_setParent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

lib.MCTS_getNumChildren.argtypes = [ctypes.c_void_p]

lib.MCTS_setMove.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64]

lib.MCTS_getNumWins.argtypes = [ctypes.c_void_p]
lib.MCTS_getNumWins.restype = ctypes.c_uint64
lib.MCTS_getNumVisits.argtypes = [ctypes.c_void_p]
lib.MCTS_getNumVisits.restype = ctypes.c_uint64
lib.MCTS_incrementWins.argtypes = [ctypes.c_void_p]
lib.MCTS_incrementVisits.argtypes = [ctypes.c_void_p]

lib.MCTS_select.argtypes = [ctypes.c_void_p]
lib.MCTS_select.restype = ctypes.c_void_p
lib.MCTS_expand.argtypes = [ctypes.c_void_p]
lib.MCTS_expand.restype = ctypes.c_void_p
lib.MCTS_simulate.argtypes = [ctypes.c_void_p]
lib.MCTS_backprop.argtypes = [ctypes.c_void_p, ctypes.c_int32]


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
    def move(self):
        return (lib.UTTT_getGlobal(self.obj), lib.UTTT_getLocal(self.obj))

    @move.setter
    def move(self, move):
        g, l = move  # noqa: E741
        return lib.MCTS_setMove(self.obj, g, l)

    @property
    def num_wins(self):
        return lib.MCTS_getNumWins(self.obj)

    @property
    def num_visits(self):
        return lib.MCTS_getNumVisits(self.obj)

    def increment_wins(self):
        lib.MCTS_incrementWins(self.obj)

    def increment_visits(self):
        lib.MCTS_incrementVisits(self.obj)

    def select(self):
        return MCTS(lib.MCTS_select(self.obj))

    def expand(self):
        return MCTS(lib.MCTS_expand(self.obj))

    def simulate(self):
        return lib.MCTS_simulate(self.obj)

    def backprop(self, winner):
        return lib.MCTS_backprop(self.obj, winner)
