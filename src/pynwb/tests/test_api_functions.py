"""Test API functions for the ndx-microscopy extension."""

import numpy as np
import pytest

from ndx_microscopy.testing import (
    mock_PlanarImagingSpace,
    mock_VolumetricImagingSpace,
    mock_Segmentation2D,
    mock_Segmentation3D,
    mock_SegmentationContainer,
    mock_Segmentation,
    mock_EmissionLightPath,
    mock_ExcitationLightPath,
)
from ndx_microscopy import (
    Segmentation2D,
    Segmentation3D,
    Segmentation,
)


def test_planar_pixel_to_image_conversion():
    """Test conversion from pixel_mask to image_mask for 2D."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    pixel_mask = [[0, 0, 1.0], [1, 0, 2.0], [2, 0, 2.0]]
    image_shape = (3, 3)
    image_mask = segmentation.pixel_to_image(pixel_mask, image_shape)
    np.testing.assert_allclose(image_mask, np.asarray([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [2.0, 0.0, 0.0]]))


def test_planar_image_to_pixel_conversion():
    """Test conversion from image_mask to pixel_mask for 2D."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    image_mask = np.asarray([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [2.0, 0.0, 0.0]])

    pixel_mask = segmentation.image_to_pixel(image_mask)
    np.testing.assert_allclose(pixel_mask, np.asarray([[0, 0, 1.0], [1, 0, 2.0], [2, 0, 2.0]]))


def test_volumetric_voxel_to_image_conversion():
    """Test conversion from voxel_mask to image_mask for 3D."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)

    voxel_mask = [[0, 0, 0, 1.0], [1, 0, 0, 2.0], [2, 0, 0, 2.0]]
    image_shape = (3, 3, 3)

    image_mask = segmentation.voxel_to_image(voxel_mask, image_shape)

    expected_image_mask = np.asarray(
        [
            [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        ]
    )
    np.testing.assert_allclose(image_mask, expected_image_mask)


def test_volumetric_image_to_voxel_conversion():
    """Test conversion from image_mask to voxel_mask for 3D."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)

    image_mask = np.asarray(
        [
            [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[2.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        ]
    )

    voxel_mask = segmentation.image_to_voxel(image_mask)

    expected_voxel_mask = [[0, 0, 0, 1.0], [1, 0, 0, 2.0], [2, 0, 0, 2.0]]
    np.testing.assert_allclose(voxel_mask, expected_voxel_mask)


def test_pixel_to_image_value_error():
    """Test ValueError for pixel_to_image with invalid pixel mask shape."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation_2d = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    invalid_pixel_mask = np.array([[0, 0]])  # Missing weight column
    with pytest.raises(ValueError, match="pixel_mask must have shape \\(N, 3\\) where each row is \\(x, y, weight\\)"):
        segmentation_2d.pixel_to_image(invalid_pixel_mask)


def test_voxel_to_image_value_error():
    """Test ValueError for voxel_to_image with invalid voxel mask shape."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation_3d = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)

    invalid_voxel_mask = np.array([[0, 0, 0]])  # Missing weight column
    with pytest.raises(
        ValueError, match="voxel_mask must have shape \\(N, 4\\) where each row is \\(x, y, z, weight\\)"
    ):
        segmentation_3d.voxel_to_image(invalid_voxel_mask)


def test_image_to_pixel_value_error():
    """Test ValueError for image_to_pixel with wrong dimensions."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation_2d = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    invalid_image = np.ones((3,))  # 1D array
    with pytest.raises(ValueError, match="image_mask must be 2D \\(height, width\\)"):
        segmentation_2d.image_to_pixel(invalid_image)


def test_image_to_voxel_value_error():
    """Test ValueError for image_to_voxel with wrong dimensions."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation_3d = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)

    invalid_image = np.ones((3, 3))  # 2D array
    with pytest.raises(ValueError, match="image_mask must be 3D \\(depth, height, width\\)"):
        segmentation_3d.image_to_voxel(invalid_image)


def test_add_roi_2d_value_error():
    """Test ValueError for add_roi in 2D when no masks are provided."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation_2d = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    with pytest.raises(ValueError, match="Must provide 'image_mask' and/or 'pixel_mask'"):
        segmentation_2d.add_roi()  # No masks provided


def test_add_roi_3d_value_error():
    """Test ValueError for add_roi in 3D when no masks are provided."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation_3d = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)

    with pytest.raises(ValueError, match="Must provide 'image_mask' and/or 'voxel_mask'"):
        segmentation_3d.add_roi()  # No masks provided


def test_planar_add_roi_with_pixel_mask():
    """Test adding ROI with pixel_mask."""
    pixel_mask = [[1, 2, 1.0], [3, 4, 1.0], [5, 6, 1.0], [7, 8, 2.0], [9, 10, 2.0]]

    planar_imaging_space = mock_PlanarImagingSpace()

    name = "Segmentation2D"
    description = "A mock instance of a Segmentation2D type to be used for rapid testing."

    planar_seg = Segmentation2D(name=name, description=description, planar_imaging_space=planar_imaging_space)

    planar_seg.add_roi(pixel_mask=pixel_mask)
    assert planar_seg.pixel_mask[:] == pixel_mask


def test_planar_add_roi_with_image_mask():
    """Test adding ROI with image_mask."""
    image_shape = (5, 5)
    image_mask = np.ones(image_shape, dtype=bool)

    planar_imaging_space = mock_PlanarImagingSpace()

    name = "Segmentation2D"
    description = "A mock instance of a Segmentation2D type to be used for rapid testing."

    planar_seg = Segmentation2D(name=name, description=description, planar_imaging_space=planar_imaging_space)

    planar_seg.add_roi(image_mask=image_mask)
    assert np.array_equal(planar_seg.image_mask[0], image_mask)


def test_volumetric_add_roi_with_voxel_mask():
    """Test adding ROI with voxel_mask."""
    voxel_mask = [[1, 2, 3, 1.0], [3, 4, 5, 1.0], [5, 6, 7, 1.0], [7, 8, 9, 2.0], [9, 10, 11, 2.0]]

    volumetric_imaging_space = mock_VolumetricImagingSpace()

    name = "Segmentation3D"
    description = "A mock instance of a Segmentation3D type to be used for rapid testing."

    segmentation_3D = Segmentation3D(
        name=name, description=description, volumetric_imaging_space=volumetric_imaging_space
    )

    segmentation_3D.add_roi(voxel_mask=voxel_mask)
    assert segmentation_3D.voxel_mask[:] == voxel_mask


def test_volumetric_add_roi_with_image_mask():
    """Test adding ROI with image_mask."""
    image_shape = (5, 5, 5)
    image_mask = np.ones(image_shape, dtype=bool)

    volumetric_imaging_space = mock_VolumetricImagingSpace()

    name = "Segmentation3D"
    description = "A mock instance of a Segmentation3D type to be used for rapid testing."

    segmentation_3D = Segmentation3D(
        name=name, description=description, volumetric_imaging_space=volumetric_imaging_space
    )

    segmentation_3D.add_roi(image_mask=image_mask)
    assert np.array_equal(segmentation_3D.image_mask[0], image_mask)


def test_add_roi_without_masks():
    """Test error when adding ROI without any mask."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    with pytest.raises(ValueError, match="Must provide 'image_mask' and/or 'pixel_mask'"):
        segmentation.add_roi(id=len(segmentation.id))


def test_create_roi_table_region():
    """Test creation of ROI table region."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation_2D = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)

    region = segmentation_2D.create_roi_table_region(description="test region", region=[0, 2, 4])
    assert len(region) == 3
    assert np.array_equal(region.data, [0, 2, 4])


def test_summary_images_access():
    """Test adding and accessing summary images."""
    segmentation = mock_Segmentation()

    # Test default summary images
    assert len(segmentation.summary_images) == 2
    assert "mean" in segmentation.summary_images
    assert "max" in segmentation.summary_images

    # Test custom summary images
    mean_image = segmentation.summary_images["mean"]
    assert mean_image.data.shape == (10, 10)
    assert np.all(mean_image.data == 1.0)


def test_segmentation_container_add():
    """Test adding different types of segmentation to container."""
    container = mock_SegmentationContainer()

    # Test default segmentations
    assert len(container.segmentations) == 2

    # Test adding new segmentation
    planar_imaging_space = mock_PlanarImagingSpace()
    new_segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)
    container.add_segmentation(segmentations=new_segmentation)
    assert len(container.segmentations) == 3


def test_segmentation_inheritance():
    """Test inheritance relationships between segmentation types."""
    planar_imaging_space = mock_PlanarImagingSpace()
    volumetric_imaging_space = mock_VolumetricImagingSpace()

    # Test that concrete classes inherit from Segmentation
    segmentation_2D = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)
    segmentation_3D = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)

    assert isinstance(segmentation_2D, Segmentation)
    assert isinstance(segmentation_3D, Segmentation)

    # Test that each has appropriate summary images
    assert len(segmentation_2D.summary_images) == 2
    assert len(segmentation_3D.summary_images) == 2


def test_get_excitation_wavelength():
    """Test getting excitation wavelength from excitation source."""
    from ndx_ophys_devices.testing import mock_ExcitationSource

    excitation_source = mock_ExcitationSource()
    light_path = mock_ExcitationLightPath()

    wavelength = light_path.get_excitation_wavelength(excitation_source=excitation_source)
    assert wavelength == excitation_source.excitation_wavelength_in_nm


def test_get_emission_wavelength():
    """Test getting emission wavelength from photodetector."""
    from ndx_ophys_devices.testing import mock_Photodetector

    photodetector = mock_Photodetector()
    light_path = mock_EmissionLightPath()

    wavelength = light_path.get_emission_wavelength(photodetector=photodetector)
    assert wavelength == photodetector.detected_wavelength_in_nm


def test_get_indicator_label():
    """Test getting label from indicator."""
    from ndx_ophys_devices.testing import mock_Indicator

    indicator = mock_Indicator()
    light_path = mock_EmissionLightPath()

    label = light_path.get_indicator_label(indicator=indicator)
    assert label == indicator.label


if __name__ == "__main__":
    pytest.main([__file__])
