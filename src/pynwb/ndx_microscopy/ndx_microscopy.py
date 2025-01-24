from hdmf.utils import docval, popargs
from pynwb import get_class
import numpy as np

extension_name = "ndx_microscopy"

MicroscopyPlaneSegmentation = get_class("MicroscopyPlaneSegmentation", extension_name)

@docval({'name': 'pixel_mask', 'type': 'array_data', 'default': None,
            'doc': 'pixel mask for 2D ROIs: [(x1, y1, weight1), (x2, y2, weight2), ...]',
            'shape': (None, 3)},
        {'name': 'voxel_mask', 'type': 'array_data', 'default': None,
            'doc': 'voxel mask for 3D ROIs: [(x1, y1, z1, weight1), (x2, y2, z2, weight2), ...]',
            'shape': (None, 4)},
        {'name': 'image_mask', 'type': 'array_data', 'default': None,
            'doc': 'image with the same size of image where positive values mark this ROI',
            'shape': [[None]*2, [None]*3]},
        {'name': 'id', 'type': int, 'doc': 'the ID for the ROI', 'default': None},
        allow_extra=True)

def add_roi(self, **kwargs):
    """Add a Region Of Interest (ROI) data to this"""
    pixel_mask, voxel_mask, image_mask = popargs('pixel_mask', 'voxel_mask', 'image_mask', kwargs)
    if image_mask is None and pixel_mask is None and voxel_mask is None:
        raise ValueError("Must provide 'image_mask' and/or 'pixel_mask'")
    rkwargs = dict(kwargs)
    if image_mask is not None:
        rkwargs['image_mask'] = image_mask
    if pixel_mask is not None:
        rkwargs['pixel_mask'] = pixel_mask
    if voxel_mask is not None:
        rkwargs['voxel_mask'] = voxel_mask
    return super(MicroscopyPlaneSegmentation,self).add_row(**rkwargs)


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
    it = np.nditer(image_mask, flags=['multi_index'])
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

@docval({'name': 'description', 'type': str, 'doc': 'a brief description of what the region is'},
        {'name': 'region', 'type': (slice, list, tuple), 'doc': 'the indices of the table', 'default': slice(None)},
        {'name': 'name', 'type': str, 'doc': 'the name of the ROITableRegion', 'default': 'rois'})
def create_roi_table_region(self, **kwargs):
    return super(MicroscopyPlaneSegmentation,self).create_region(**kwargs)

MicroscopyPlaneSegmentation.create_roi_table_region = create_roi_table_region

MicroscopySegmentation = get_class("MicroscopySegmentation", extension_name)
ImagingSpace = get_class("ImagingSpace", extension_name)

@docval({'name': 'imaging_space', 'type': ImagingSpace, 'doc': 'the ImagingSpace this ROI applies to'},
        {'name': 'description', 'type': str,
            'doc': 'Description of image space, recording wavelength, depth, etc.', 'default': None},
        {'name': 'name', 'type': str, 'doc': 'name of PlaneSegmentation.', 'default': None})

def add_segmentation(self, **kwargs):
    kwargs.setdefault('description', kwargs['imaging_space'].description)
    return super(MicroscopySegmentation,self).create_plane_segmentation(**kwargs)

MicroscopySegmentation.add_segmentation = add_segmentation