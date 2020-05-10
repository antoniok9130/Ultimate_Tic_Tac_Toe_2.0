# -*- coding: utf-8 -*-
import ctypes
import os

file_dir = os.path.dirname(os.path.abspath(__file__))

lib = ctypes.CDLL(os.path.join(file_dir, "..", "C++", "libUTTT.so"), mode=1)

# try:
#     if "Linux" in esmfos:
#     _ESMF = ctypes.CDLL(libsdir+'/libesmf.so',mode=ctypes.RTLD_GLOBAL)
#     else:
#     _ESMF = numpy.ctypeslib.load_library('libesmf',libsdir)
# except:
#     traceback.print_exc(file=sys.stdout)
#     sys.exit(ESMP_ERROR_SHAREDLIB)


# Signatures
lib.new_UTTT.restype = ctypes.c_void_p
lib.delete_UTTT.argtypes = [ctypes.c_void_p]

lib.UTTT_empty.argtypes = [ctypes.c_void_p]

lib.UTTT_getCurrentPlayer.argtypes = [ctypes.c_void_p]
lib.UTTT_setCurrentPlayer.argtypes = [ctypes.c_void_p, ctypes.c_int32]
lib.UTTT_switchPlayer.argtypes = [ctypes.c_void_p]

lib.UTTT_getWinner.argtypes = [ctypes.c_void_p]

lib.UTTT_getQuadrant.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.UTTT_getQuadrant.restype = ctypes.c_uint32
lib.UTTT_getQuadrantForPlayer.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint32,
    ctypes.c_int32,
]
lib.UTTT_getQuadrantForPlayer.restype = ctypes.c_uint32

lib.UTTT_getPlayerAt.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.UTTT_getPlayerAtQuadrant.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint32,
    ctypes.c_uint32,
]

lib.UTTT_setMove.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64]
lib.UTTT_updateBoard.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64]

lib.UTTT_getBoard.argtypes = [ctypes.c_void_p]
lib.UTTT_getBoard.restype = ctypes.c_uint32
lib.UTTT_getBoardForPlayer.argtypes = [ctypes.c_void_p, ctypes.c_int32]
lib.UTTT_getBoardForPlayer.restype = ctypes.c_uint32

lib.UTTT_getLocal.argtypes = [ctypes.c_void_p]
lib.UTTT_getLocal.restype = ctypes.c_uint32
lib.UTTT_getGlobal.argtypes = [ctypes.c_void_p]
lib.UTTT_getGlobal.restype = ctypes.c_uint32

lib.UTTT_check3InRow.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
lib.UTTT_printBoard.argtypes = [ctypes.c_void_p]
lib.UTTT_printBoard.restype = ctypes.c_char_p


class UTTT:
    N = lib.UTTT_N()
    P1 = lib.UTTT_P1()
    P2 = lib.UTTT_P2()
    T = lib.UTTT_T()

    def __init__(self):
        self.obj = lib.new_UTTT()

    def __del__(self):
        lib.delete_UTTT(self.obj)

    @property
    def empty(self):
        """Returns true iff the board is empty"""
        return bool(lib.UTTT_empty(self.obj))

    @property
    def player(self):
        """Returns the current player"""
        p = lib.UTTT_getCurrentPlayer(self.obj)
        if p == 0:
            return self.P1
        else:
            return self.P2

    @player.setter
    def player(self, p):
        if p == self.P1:
            lib.UTTT_setCurrentPlayer(self.obj, 0)
        elif p == self.P2:
            lib.UTTT_setCurrentPlayer(self.obj, 1)

    def switch_player(self):
        lib.UTTT_switchPlayer(self.obj)

    @property
    def winner(self):
        return lib.UTTT_getWinner(self.obj)

    def quadrant(self, quadrant, player=None):
        if player is None:
            return lib.UTTT_getQuadrant(self.obj, quadrant)
        else:
            return lib.UTTT_getQuadrantForPlayer(self.obj, quadrant, player)

    def __getitem__(self, loc):
        if isinstance(loc, tuple) and len(loc) == 2:
            return lib.UTTT_getPlayerAtQuadrant(self.obj, loc[0], loc[1])
        else:
            return lib.UTTT_getPlayerAt(self.obj, loc)

    @property
    def move(self):
        return (lib.UTTT_getGlobal(self.obj), lib.UTTT_getLocal(self.obj))

    @move.setter
    def move(self, move):
        g, l = move  # noqa: E741
        lib.UTTT_setMove(self.obj, g, l)

    def updateBoard(self, g, l):
        lib.UTTT_updateBoard(self.obj, g, l)

    def getBoard(self, player=None):
        if player is None:
            return lib.UTTT_getBoard(self.obj)
        else:
            return lib.UTTT_getBoardForPlayer(self.obj, player)

    def __str__(self):
        return lib.UTTT_printBoard(self.obj).decode("UTF-8")

    def __repr__(self):
        return str(id(self.obj))

    @staticmethod
    def check3InRow(quadrant, local):
        return lib.UTTT_check3InRow(quadrant, local)
