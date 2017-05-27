import sys
from cx_Freeze import Executable

from setuptools import setup, find_packages

# Borrowed from:
#   http://cx-freeze.readthedocs.io/en/latest/distutils.html#distutils
# build_exe_options = {}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='password-generator',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'rdoclient',
        'pytest',
    ],
    entry_points="""
        [console_scripts]
        generate=scripts.generate:cli
    """,

    # options={"build_exe": build_exe_options},
    executables=[Executable("generate-password.py", base=base)],

    # Metadata for upload to PyPI
    author='Nick Vincent-Maloney (nicorellius)',
    author_email='nick@cistech.io',
    description="""PyPass3: Password Generator GUI.
        Dice Roll Optional, Mostly-Random Word, Number,
        and Mixed Character Password Generator""",
    license='MIT',
    keywords='password passphrase numbers words mixed eff dice roll',
    url='http://cistech.io/projects/password-generator/',
)
