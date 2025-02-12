import os

from pynwb import get_class, load_namespaces

try:
    from importlib.resources import files
except ImportError:
    # TODO: Remove when python 3.9 becomes the new minimum
    from importlib_resources import files

# NOTE: ndx-ophys-devices needs to be imported first because loading the ndx-microscopy namespace depends on
# having the ndx-ophys-devices namespace loaded into the global type map.
from ndx_ophys_devices import ExcitationSource, Indicator, OpticalFilter, Photodetector, DichroicMirror

extension_name = "ndx-microscopy"

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / f"{extension_name}.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / f"{extension_name}.namespace.yaml"

load_namespaces(str(__spec_path))

from .ndx_microscopy import MicroscopyPlaneSegmentation, ExcitationLightPath, EmissionLightPath

Microscope = get_class("Microscope", extension_name)

ImagingSpace = get_class("ImagingSpace", extension_name)
PlanarImagingSpace = get_class("PlanarImagingSpace", extension_name)
VolumetricImagingSpace = get_class("VolumetricImagingSpace", extension_name)

MicroscopySeries = get_class("MicroscopySeries", extension_name)
PlanarMicroscopySeries = get_class("PlanarMicroscopySeries", extension_name)
VolumetricMicroscopySeries = get_class("VolumetricMicroscopySeries", extension_name)
MultiPlaneMicroscopyContainer = get_class("MultiPlaneMicroscopyContainer", extension_name)

MicroscopyResponseSeries = get_class("MicroscopyResponseSeries", extension_name)
MicroscopyResponseSeriesContainer = get_class("MicroscopyResponseSeriesContainer", extension_name)

MicroscopySegmentations = get_class("MicroscopySegmentations", extension_name)
# from .ndx_microscopy import MicroscopyPlaneSegmentation, ExcitationLightPath, EmissionLightPath

__all__ = [
    "OpticalFilter",
    "ExcitationSource",
    "Indicator",
    "Photodetector",
    "DichroicMirror",
    "Microscope",
    "ExcitationLightPath",
    "EmissionLightPath",
    "ImagingSpace",
    "PlanarImagingSpace",
    "VolumetricImagingSpace",
    "MicroscopySegmentations",
    "MicroscopyPlaneSegmentation",
    "MicroscopySeries",
    "PlanarMicroscopySeries",
    "VolumetricMicroscopySeries",
    "MultiPlaneMicroscopyContainer",
    "MicroscopyResponseSeries",
    "MicroscopyResponseSeriesContainer",
]
