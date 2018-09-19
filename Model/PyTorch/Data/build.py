from distutils.core import setup

from Cython.Build import cythonize


# Parameters:    build_ext --inplace

def runBuild():
      setup(name='Python Game Generator',
            ext_modules=cythonize("./*.pyx"))

if __name__ == "__main__":
      runBuild()