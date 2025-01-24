"""Test API functions for the ndx-microscopy extension."""

import numpy as np
import pytest
from ndx_microscopy.testing import (
    mock_PlanarImagingSpace,
    mock_MicroscopyPlaneSegmentation,
)
from ndx_microscopy import MicroscopyPlaneSegmentation


def test_add_roi_with_pixel_mask():
    """Test adding ROI with pixel mask."""

    pixel_mask = [[1, 2, 1.0], [3, 4, 1.0], [5, 6, 1.0], [7, 8, 2.0], [9, 10, 2.0]]

    imaging_space = mock_PlanarImagingSpace()
    name = "MicroscopyPlaneSegmentation"
    description = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."

    plane_seg = MicroscopyPlaneSegmentation(name=name, description=description, imaging_space=imaging_space)

    plane_seg.add_roi(pixel_mask=pixel_mask)
    assert plane_seg.pixel_mask[:] == pixel_mask


def test_add_roi_with_voxel_mask():
    """Test adding ROI with voxel mask."""
    voxel_mask = [[1, 2, 3, 1.0], [3, 4, 5, 1.0], [5, 6, 7, 1.0], [7, 8, 9, 2.0], [9, 10, 11, 2.0]]

    imaging_space = mock_PlanarImagingSpace()
    name = "MicroscopyPlaneSegmentation"
    description = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."

    plane_seg = MicroscopyPlaneSegmentation(name=name, description=description, imaging_space=imaging_space)

    plane_seg.add_roi(voxel_mask=voxel_mask)
    assert plane_seg.voxel_mask[:] == voxel_mask


def test_add_roi_with_image_mask():
    """Test adding ROI with image mask."""
    w, h = 5, 5
    image_mask = [[[1.0 for x in range(w)] for y in range(h)], [[2.0 for x in range(w)] for y in range(h)]]

    imaging_space = mock_PlanarImagingSpace()
    name = "MicroscopyPlaneSegmentation"
    description = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."
    plane_seg = MicroscopyPlaneSegmentation(name=name, description=description, imaging_space=imaging_space)

    plane_seg.add_roi(image_mask=image_mask)

    assert plane_seg.image_mask[0] == image_mask


def test_add_roi_without_masks():
    """Test adding ROI without any masks raises ValueError."""
    imaging_space = mock_PlanarImagingSpace()
    plane_seg = mock_MicroscopyPlaneSegmentation(imaging_space=imaging_space)

    with pytest.raises(ValueError, match="Must provide 'image_mask' and/or 'pixel_mask"):
        plane_seg.add_roi(id=4)


def test_pixel_to_image():
    """Test conversion from pixel mask to image mask."""
    imaging_space = mock_PlanarImagingSpace()
    name = "MicroscopyPlaneSegmentation"
    description = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."
    plane_seg = MicroscopyPlaneSegmentation(name=name, description=description, imaging_space=imaging_space)

    pixel_mask = [[0, 0, 1.0], [1, 0, 2.0], [2, 0, 2.0]]

    img_mask = plane_seg.pixel_to_image(pixel_mask)
    np.testing.assert_allclose(img_mask, np.asarray([[1, 2, 2.0], [0, 0, 0.0], [0, 0, 0.0]]))


def test_image_to_pixel():
    """Test conversion from image mask to pixel mask."""
    imaging_space = mock_PlanarImagingSpace()
    name = "MicroscopyPlaneSegmentation"
    description = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."
    plane_seg = MicroscopyPlaneSegmentation(name=name, description=description, imaging_space=imaging_space)

    image_mask = np.asarray([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

    pixel_mask = plane_seg.image_to_pixel(image_mask)
    np.testing.assert_allclose(pixel_mask, np.asarray([[0, 0, 1.0], [1, 1, 1.0], [2, 2, 1.0]]))


def test_create_roi_table_region():
    """Test creating ROI table region."""
    imaging_space = mock_PlanarImagingSpace()
    name = "MicroscopyPlaneSegmentation"
    description = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."
    plane_seg = MicroscopyPlaneSegmentation(name=name, description=description, imaging_space=imaging_space)

    # Add some ROIs first
    pixel_mask = [[0, 0, 1.0], [1, 0, 2.0], [2, 0, 2.0]]

    plane_seg.add_roi(pixel_mask=pixel_mask)
    plane_seg.add_roi(pixel_mask=pixel_mask)

    # Test with specific region indices
    region = plane_seg.create_roi_table_region(
        description="Test region",
        name="test_region",
        region=[0],  # Only include first ROI
    )

    assert region.name == "test_region"
    assert region.description == "Test region"
    assert len(region.data) == 1
    assert region.data[0] == 0


if __name__ == "__main__":
    pytest.main([__file__])
