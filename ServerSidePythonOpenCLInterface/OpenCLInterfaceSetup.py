from distutils.core import setup, Extension
"""
script to build the PyOpenCLInterface.so shared lib
  include dirs: NVIDIA -> /usr/local/cuda/include
                AMD -> /opt/AMDAPP/include
"""

module1 = Extension('PyOpenCLInterface',
                    sources = ['ContextsInterface.c',
                               'DevicesInterface.c',
                               'KernelsInterface.c',
                               'MemsInterface.c',
                               'OpenCLObjectsMaps.cpp',
                               'ProgramsInterface.c',
                               'PythonOpenCLInterface.c',
                               'QueuesInterface.c'],
		    include_dirs = ['/opt/AMDAPP/include'],
		    define_macros = [('C_INCLUDE', 1),],
		    libraries = ['OpenCL'],
		    library_dirs = [],
		    runtime_library_dirs = [])

setup (name = 'PyOpenCLInterface',
       version = '1.0',
       description = 'Small package that implements Python OpenCl interface',
       ext_modules = [module1])

