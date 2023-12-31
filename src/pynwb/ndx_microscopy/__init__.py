import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_microscopy_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-microscopy.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_microscopy_specpath):
    ndx_microscopy_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-microscopy.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_microscopy_specpath)

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package level
TetrodeSeries = get_class('TetrodeSeries', 'ndx-microscopy')
