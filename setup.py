import re
from pathlib import Path
from setuptools import setup
from setuptools import find_packages


here = Path(__file__).parent

txt = (here / 'src' / 'robo_navigation' / '__init__.py').read_text('utf-8')
try:
    version = re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


requires = []

args = dict(
    name='robo_navigation',
    version=version,
    description="",
    author='Alex Lisovoy',
    author_email='lisovoy.a.s@gmail.com',
    url='https://github.com/AlexLisovoy/robo_navigation.git',
    python_requires='>=3.7',
    packages=find_packages('src'),
    py_modules=[path.stem for path in Path('src').glob('*.py')],
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'robo-navigation=robo_navigation.navigation:main',
        ],
    }
)

setup(**args)
