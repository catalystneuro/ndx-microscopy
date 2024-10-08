import os

from pynwb import get_class, load_namespaces

try:
    from importlib.resources import files
except ImportError:
    # TODO: Remove when python 3.9 becomes the new minimum
    from importlib_resources import files

extension_name = "ndx-microscopy"

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / f"{extension_name}.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / f"{extension_name}.namespace.yaml"

load_namespaces(str(__spec_path))

Microscope = get_class("Microscope", extension_name)
MicroscopyLightSource = get_class("MicroscopyLightSource", extension_name)
MicroscopyOpticalChannel = get_class("MicroscopyOpticalChannel", extension_name)
ImagingSpace = get_class("ImagingSpace", extension_name)
PlanarImagingSpace = get_class("PlanarImagingSpace", extension_name)
VolumetricImagingSpace = get_class("VolumetricImagingSpace", extension_name)
MicroscopySegmentations = get_class("MicroscopySegmentations", extension_name)
MicroscopyPlaneSegmentation = get_class("MicroscopyPlaneSegmentation", extension_name)
MicroscopySeries = get_class("MicroscopySeries", extension_name)
PlanarMicroscopySeries = get_class("PlanarMicroscopySeries", extension_name)
VariableDepthMicroscopySeries = get_class("VariableDepthMicroscopySeries", extension_name)
VolumetricMicroscopySeries = get_class("VolumetricMicroscopySeries", extension_name)
MultiChannelMicroscopyVolume = get_class("MultiChannelMicroscopyVolume", extension_name)
VariableDepthMultiChannelMicroscopyVolume = get_class("VariableDepthMultiChannelMicroscopyVolume", extension_name)

MicroscopyResponseSeries = get_class("MicroscopyResponseSeries", extension_name)
MicroscopyResponseSeriesContainer = get_class("MicroscopyResponseSeriesContainer", extension_name)


__all__ = [
    "Microscope",
    "MicroscopyLightSource",
    "MicroscopyOpticalChannel",
    "ImagingSpace",
    "PlanarImagingSpace",
    "VolumetricImagingSpace",
    "MicroscopySegmentations",
    "MicroscopyPlaneSegmentation",
    "MicroscopySeries",
    "PlanarMicroscopySeries",
    "VariableDepthMicroscopySeries",
    "VolumetricMicroscopySeries",
    "MultiChannelMicroscopyVolume",
    "VariableDepthMultiChannelMicroscopyVolume",
    "MicroscopyResponseSeries",
    "MicroscopyResponseSeriesContainer",
]
