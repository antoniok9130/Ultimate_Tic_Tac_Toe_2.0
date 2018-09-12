from distutils.core import setup

from Cython.Build import cythonize


def runBuild():
      setup(name='Python MCTS',
            ext_modules=cythonize("./*.pyx"))

if __name__ == "__main__":
      runBuild()