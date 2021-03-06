#    Copyright 2013-2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import warnings
from itertools import chain

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


devlib_dir = os.path.join(os.path.dirname(__file__), 'devlib')

sys.path.insert(0, os.path.join(devlib_dir, 'core'))

# happends if falling back to distutils
warnings.filterwarnings('ignore', "Unknown distribution option: 'install_requires'")
warnings.filterwarnings('ignore', "Unknown distribution option: 'extras_require'")

try:
    os.remove('MANIFEST')
except OSError:
    pass

packages = []
data_files = {}
source_dir = os.path.dirname(__file__)
for root, dirs, files in os.walk(devlib_dir):
    rel_dir = os.path.relpath(root, source_dir)
    data = []
    if '__init__.py' in files:
        for f in files:
            if os.path.splitext(f)[1] not in ['.py', '.pyc', '.pyo']:
                data.append(f)
        package_name = rel_dir.replace(os.sep, '.')
        package_dir = root
        packages.append(package_name)
        data_files[package_name] = data
    else:
        # use previous package name
        filepaths = [os.path.join(root, f) for f in files]
        data_files[package_name].extend([os.path.relpath(f, package_dir) for f in filepaths])

params = dict(
    name='devlib',
    description='A framework for automating workload execution and measurment collection on ARM devices.',
    version='0.0.4',
    packages=packages,
    package_data=data_files,
    url='https://github.com/ARM-software/devlib',
    license='Apache v2',
    maintainer='ARM Ltd.',
    install_requires=[
        'python-dateutil',  # converting between UTC and local time.
        'pexpect>=3.3',  # Send/recieve to/from device
        'pyserial',  # Serial port interface
        'wrapt',  # Basic for construction of decorator functions
        'future', # Python 2-3 compatibility
    ],
    extras_require={
        'daq': ['daqpower'],
        'doc': ['sphinx'],
        'monsoon': ['python-gflags'],
    },
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
    ],
)

all_extras = list(chain(iter(params['extras_require'].values())))
params['extras_require']['full'] = all_extras

setup(**params)
