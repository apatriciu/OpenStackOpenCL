from distutils.core import setup, Extension

module1 = Extension('PyTestObjects',
                    sources = ['PyTestObjects.c',], 
		    include_dirs = [],
		    define_macros = [],
		    libraries = [],
		    library_dirs = [],
		    runtime_library_dirs = [])

setup (name = 'PyTestObjects',
       version = '1.0',
       description = 'Test Objects',
       ext_modules = [module1])

