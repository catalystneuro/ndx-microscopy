from hdmf.utils import docval, popargs_to_dict, get_docval, popargs
from pynwb import get_class, register_class
from pynwb.file import LabMetaData
from ndx_ophys_devices import ExcitationSource, OpticalFilter, DichroicMirror, Photodetector, Indicator
import numpy as np

extension_name = "ndx-microscopy"

MicroscopyPlaneSegmentation = get_class("MicroscopyPlaneSegmentation", extension_name)


@docval(
    {
        "name": "pixel_mask",
        "type": "array_data",
        "default": None,
        "doc": "pixel mask for 2D ROIs: [(x1, y1, weight1), (x2, y2, weight2), ...]",
        "shape": (None, 3),
    },
    {
        "name": "voxel_mask",
        "type": "array_data",
        "default": None,
        "doc": "voxel mask for 3D ROIs: [(x1, y1, z1, weight1), (x2, y2, z2, weight2), ...]",
        "shape": (None, 4),
    },
    {
        "name": "image_mask",
        "type": "array_data",
        "default": None,
        "doc": "image with the same size of image where positive values mark this ROI",
        "shape": [[None] * 2, [None] * 3],
    },
    {"name": "id", "type": int, "doc": "the ID for the ROI", "default": None},
    allow_extra=True,
)
def add_roi(self, **kwargs):
    """Add a Region Of Interest (ROI) data to this"""
    pixel_mask, voxel_mask, image_mask = popargs("pixel_mask", "voxel_mask", "image_mask", kwargs)
    if image_mask is None and pixel_mask is None and voxel_mask is None:
        raise ValueError("Must provide 'image_mask' and/or 'pixel_mask'")
    rkwargs = dict(kwargs)
    if image_mask is not None:
        rkwargs["image_mask"] = image_mask
    if pixel_mask is not None:
        rkwargs["pixel_mask"] = pixel_mask
    if voxel_mask is not None:
        rkwargs["voxel_mask"] = voxel_mask
    return super(MicroscopyPlaneSegmentation, self).add_row(**rkwargs)


@staticmethod
def pixel_to_image(pixel_mask):
    """Converts a 2D pixel_mask of a ROI into an image_mask."""
    image_matrix = np.zeros(np.shape(pixel_mask))
    npmask = np.asarray(pixel_mask)
    x_coords = npmask[:, 0].astype(np.int32)
    y_coords = npmask[:, 1].astype(np.int32)
    weights = npmask[:, -1]
    image_matrix[y_coords, x_coords] = weights
    return image_matrix


@staticmethod
def image_to_pixel(image_mask):
    """Converts an image_mask of a ROI into a pixel_mask"""
    pixel_mask = []
    it = np.nditer(image_mask, flags=["multi_index"])
    while not it.finished:
        weight = it[0][()]
        if weight > 0:
            x = it.multi_index[0]
            y = it.multi_index[1]
            pixel_mask.append([x, y, weight])
        it.iternext()
    return pixel_mask


MicroscopyPlaneSegmentation.add_roi = add_roi
MicroscopyPlaneSegmentation.pixel_to_image = pixel_to_image
MicroscopyPlaneSegmentation.image_to_pixel = image_to_pixel


@docval(
    {"name": "description", "type": str, "doc": "a brief description of what the region is"},
    {"name": "region", "type": (slice, list, tuple), "doc": "the indices of the table", "default": slice(None)},
    {"name": "name", "type": str, "doc": "the name of the ROITableRegion", "default": "rois"},
)
def create_roi_table_region(self, **kwargs):
    return super(MicroscopyPlaneSegmentation, self).create_region(**kwargs)


MicroscopyPlaneSegmentation.create_roi_table_region = create_roi_table_region


def check_wavelength(wavelengthset_in_light_path, wavelength_set_in_device):
    if not wavelengthset_in_light_path == wavelength_set_in_device:
        raise ValueError(
            f"wavelength set in the light path ({wavelengthset_in_light_path}) and the one set in the device ({wavelength_set_in_device}) must be the same."
        )


@register_class("ExcitationLightPath", extension_name)
class ExcitationLightPath(LabMetaData):
    __nwbfields__ = (
        "excitation_wavelength_in_nm",
        "description",
        "excitation_source",
        "excitation_filter",
        "dichroic_mirror",
    )

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "excitation_wavelength_in_nm",
            "type": float,
            "doc": "The excitation wavelength of light, in nanometers.",
        },
        {
            "name": "description",
            "type": str,
            "doc": "Link to ExcitationSource object which contains metadata about the excitation source device. If it is a pulsed excitation source link a PulsedExcitationSource object.",
        },
        {"name": "excitation_source", "type": ExcitationSource, "doc": "The excitation source", "default": None},
        {
            "name": "excitation_filter",
            "type": OpticalFilter,
            "doc": "Link to OpticalFilter object which contains metadata about the optical filter in this excitation light path. It can be either a BandOpticalFilter (e.g., 'Bandpass', 'Bandstop', 'Longpass', 'Shortpass') or a EdgeOpticalFilter (Longpass or Shortpass).",
            "default": None,
        },
        {
            "name": "dichroic_mirror",
            "type": DichroicMirror,
            "doc": "Link to DichroicMirror object which contains metadata about the dichroic mirror in the excitation light path.",
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = (
            "excitation_wavelength_in_nm",
            "description",
            "excitation_source",
            "excitation_filter",
            "dichroic_mirror",
        )
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)
        excitation_wavelength_in_nm = args_to_set["excitation_wavelength_in_nm"]
        excitation_source = args_to_set["excitation_source"]
        if excitation_source is not None:
            check_wavelength(excitation_wavelength_in_nm, excitation_source.excitation_wavelength_in_nm)


@register_class("EmissionLightPath", extension_name)
class EmissionLightPath(LabMetaData):
    __nwbfields__ = (
        "emission_wavelength_in_nm",
        "description",
        {"name": "indicator", "child": True},
        "photodetector",
        "emission_filter",
        "dichroic_mirror",
    )

    @docval(
        *get_docval(LabMetaData.__init__, "name"),
        {
            "name": "emission_wavelength_in_nm",
            "type": float,
            "doc": "The emission wavelength of light, in nanometers.",
        },
        {
            "name": "description",
            "type": str,
            "doc": "Description of the emission light path",
        },
        {
            "name": "indicator",
            "type": Indicator,
            "doc": "Indicator object which contains metadata about the indicator used in this light path.",
        },
        {
            "name": "photodetector",
            "type": Photodetector,
            "doc": "Link to Photodetector object which contains metadata about the photodetector device.",
            "default": None,
        },
        {
            "name": "emission_filter",
            "type": OpticalFilter,
            "doc": "Link to OpticalFilter object which contains metadata about the optical filter in this emission light path. It can be either a BandOpticalFilter (e.g., 'Bandpass', 'Bandstop', 'Longpass', 'Shortpass') or a EdgeOpticalFilter (Longpass or Shortpass).",
            "default": None,
        },
        {
            "name": "dichroic_mirror",
            "type": DichroicMirror,
            "doc": "Link to DichroicMirror object which contains metadata about the dichroic mirror in the emission light path.",
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        keys_to_set = (
            "emission_wavelength_in_nm",
            "description",
            "indicator",
            "photodetector",
            "emission_filter",
            "dichroic_mirror",
        )
        args_to_set = popargs_to_dict(keys_to_set, kwargs)
        super().__init__(**kwargs)
        for key, val in args_to_set.items():
            setattr(self, key, val)
        emission_wavelength_in_nm = args_to_set["emission_wavelength_in_nm"]
        photodetector = args_to_set["photodetector"]
        if photodetector is not None:
            check_wavelength(emission_wavelength_in_nm, photodetector.detected_wavelength_in_nm)
