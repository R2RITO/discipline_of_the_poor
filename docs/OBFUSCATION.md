# Cython obfuscation

Although cython is mainly used to compile and use C code alongside python,
it can also be used to compile python files. This provides a minimal
improvement in running speed, while also obfuscating the source code.

### cython_setup file

The file is used to define a packaging function, that compiles the project
and copies the files that cannot be compiled.


### File instructions
The obfuscation process relies on the cython library's ability to compile even
native .py files to C files, and then compile these files into .so files.

This means, you can specify pure python files as part of a build process, and
cython will compile them without issue.

This is achieved using the distribution tools provided by python (distutils),
in order to build a package. A setup file has to be created, in order to
specify every dependency to be compiled and packaged.

The setup function is a standard setuptools setup function, but used in a
slightly different way.
The ext_modules parameter is normally used to give a list of C modules, called
Extensions. The cythonize function compiles a .py or .pyx files into
a C/C++ file, and then compiles said file to a .so module.


    setup(
        ext_modules=cythonize(
            sourcefiles,
            build_dir="build",
            compiler_directives=dict(
                always_allow_keywords=True,
                language_level=3,
            )
        ),
        cmdclass=dict(
            build_ext=MyBuildExt
        ),
        packages=[]
    )

The first parameter of the cythonize function is a list (or set) of Extension
objects, created with the setuptools constructor, and receiving as parameters
the full package name (dotted notation), and the full file(s) path.

As a special gotcha, if all the .py files on the package will be compiled, you
can specify '/path/to/files/*.py' as the path, and it will compile everything,
but if some file cannot be compiled (such as a Django model file), then every
file will have to be specified.

The build_dir parameter is used to name the folder in which the compiled files
will be located, the program will create said folder starting from the same
level of the setup file's location.

The always_allow_keywords argument explanation is found here:
https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-directives

The language_level argument is used to specify the python version to use

The cmdclass argument is used to pass the class that will be used to build the
Extensions

The packages argument tells the setup function the packages to bundle, but
since the goal is to obfuscate code and not to bundle a project, it has to
be empty.


    class MyBuildExt(build_ext):
        def run(self):
            build_ext.run(self)
    
            build_dir = Path(self.build_lib)
            root_dir = Path(__file__).parent
    
            target_dir = build_dir if not self.inplace else root_dir
    
            # Manage.py
            self._copy_file(Path('discipline_of_the_poor') / 'manage.py', root_dir, target_dir)
    
            # Locale files
            os.mkdir(target_dir / 'discipline_of_the_poor/locale')
            os.mkdir(target_dir / 'discipline_of_the_poor/locale/es')
            os.mkdir(target_dir / 'discipline_of_the_poor/locale/es/LC_MESSAGES')
            self._copy_file(Path('discipline_of_the_poor/locale/es/LC_MESSAGES') / 'django.po', root_dir, target_dir)
    
            # Model sources
            os.mkdir(target_dir / 'discipline_of_the_poor/budget/models')
            self._copy_file(Path('discipline_of_the_poor/budget/models') / '__init__.py', root_dir, target_dir)
            self._copy_file(Path('discipline_of_the_poor/budget/models') / 'budget.py', root_dir, target_dir)
    
            # Migrations folder
            os.mkdir(target_dir / 'discipline_of_the_poor/budget/migrations')
            self._copy_file(Path('discipline_of_the_poor/budget/migrations') / '__init__.py', root_dir, target_dir)
    
            # Wsgi file
            self._copy_file(Path('discipline_of_the_poor/discipline_of_the_poor') / 'wsgi.py', root_dir, target_dir)
            self._copy_file(Path('discipline_of_the_poor/discipline_of_the_poor') / 'asgi.py', root_dir, target_dir)
    
        def _copy_file(self, path, source_dir, destination_dir):
            if not (source_dir / path).exists():
                return
    
            shutil.copyfile(str(source_dir / path), str(destination_dir / path))

The custom extension builder class is used to copy the non-compiled files to the
build directory, in order to allow for a complete usable package inside the
directory.

Inside this class, the first thing to run is the parent's class run method,
which builds all the extensions. Then, the source and target directory are
determined in order to copy the relevant files.
If the subpackage to be copied had no previously compiled files, the directory
will not be created, and an additional mkdir instruction will have to be issued
to cover that case.

##### Important details

As a simple rule of thumb, you should not compile files that are executed from
a command line, or a similar tool that calls python file.py. Some examples
of these files are the manage.py and wsgi.py files used in django,
or the app.py file for flask.

The setup.py file should not live inside a package (a folder with an
__init__.py file). If it does, the target directory will not mirror the source
directory, it will have an additional parent folder and will break the script's
file copy section.

In Cython, some files are loaded in a different way than normal .py files, so
some functionality may break.

In Django, I was not able to compile the models files, the ones inheriting from
django.db.models.Model, they give an error related to a missing app name, which
is loaded from the settings file. This may be related to the statement above,
so I don't include the model files in the compilation, and just copy them as
pure .py files to the build folder.

For python2 projects, the __init__.py file for each package has to be copied as
a normal python file, it can be compiled as well, but it is needed for python
to locate the files inside the packages.
Also, in python2, any file that uses the magical variable __file__ cannot be
compiled due to the previous statement, the cython file is read before that
variable is set. 