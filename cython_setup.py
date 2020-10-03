from setuptools.extension import Extension
from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from pathlib import Path
import shutil
import os


sourcefiles = set()

# Main sources
sourcefiles.add(Extension('discipline_of_the_poor.*',
                          ['discipline_of_the_poor/__init__.py']))
sourcefiles.add(Extension('discipline_of_the_poor.*',
                          ['discipline_of_the_poor/prepare_database.py']))

# Budget sources
sourcefiles.add(Extension('discipline_of_the_poor.budget.*',
                          ['discipline_of_the_poor/budget/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.async_processes.*',
                          ['discipline_of_the_poor/budget/async_processes/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.business.*',
                          ['discipline_of_the_poor/budget/business/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.business.email.*',
                          ['discipline_of_the_poor/budget/business/email/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.business.budget_stats.*',
                          ['discipline_of_the_poor/budget/business/budget_stats/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.business.budget_periodic_movement.*',
                          ['discipline_of_the_poor/budget/business/budget_periodic_movement/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.fixtures.*',
                          ['discipline_of_the_poor/budget/fixtures/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.middlewares.*',
                          ['discipline_of_the_poor/budget/middlewares/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.serializers.*',
                          ['discipline_of_the_poor/budget/serializers/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.signals.*',
                          ['discipline_of_the_poor/budget/signals/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.utils.*',
                          ['discipline_of_the_poor/budget/utils/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.budget.views.*',
                          ['discipline_of_the_poor/budget/views/*.py']))


# Main app sources
sourcefiles.add(Extension('discipline_of_the_poor.discipline_of_the_poor.*',
                          ['discipline_of_the_poor/discipline_of_the_poor/__init__.py']))
sourcefiles.add(Extension('discipline_of_the_poor.discipline_of_the_poor.*',
                          ['discipline_of_the_poor/discipline_of_the_poor/permissions.py']))
sourcefiles.add(Extension('discipline_of_the_poor.discipline_of_the_poor.*',
                          ['discipline_of_the_poor/discipline_of_the_poor/settings.py']))
sourcefiles.add(Extension('discipline_of_the_poor.discipline_of_the_poor.*',
                          ['discipline_of_the_poor/discipline_of_the_poor/urls.py']))

# Dotp user sources
sourcefiles.add(Extension('discipline_of_the_poor.dotp_users.*',
                          ['discipline_of_the_poor/dotp_users/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.dotp_users.serializers.*',
                          ['discipline_of_the_poor/dotp_users/serializers/*.py']))
sourcefiles.add(Extension('discipline_of_the_poor.dotp_users.views.*',
                          ['discipline_of_the_poor/dotp_users/views/*.py']))


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
        self._copy_file(Path('discipline_of_the_poor/budget/models') / 'budget_movement.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/budget/models') / 'mixins.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/budget/models') / 'movement.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/budget/models') / 'movement_category.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/budget/models') / 'periodic_movement.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/budget/models') / 'single_movement.py', root_dir, target_dir)

        # Migrations folder
        os.mkdir(target_dir / 'discipline_of_the_poor/budget/migrations')
        self._copy_file(Path('discipline_of_the_poor/budget/migrations') / '__init__.py', root_dir, target_dir)

        # Wsgi file
        self._copy_file(Path('discipline_of_the_poor/discipline_of_the_poor') / 'wsgi.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/discipline_of_the_poor') / 'asgi.py', root_dir, target_dir)

        # Dotp_users model sources
        os.mkdir(target_dir / 'discipline_of_the_poor/dotp_users/models')
        self._copy_file(Path('discipline_of_the_poor/dotp_users/models') / '__init__.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/dotp_users/models') / 'dotp_user.py', root_dir, target_dir)
        self._copy_file(Path('discipline_of_the_poor/dotp_users/models') / 'mixins.py', root_dir, target_dir)

        # Dotp_users migrations folder
        os.mkdir(target_dir / 'discipline_of_the_poor/dotp_users/migrations')
        self._copy_file(Path('discipline_of_the_poor/dotp_users/migrations') / '__init__.py', root_dir, target_dir)

    def _copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


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
