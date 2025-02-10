"""Test in-memory Python API constructors for the ndx-microscopy extension."""

import numpy as np
import pytest
import pynwb

from ndx_microscopy.testing import (
    mock_EmissionLightPath,
    mock_ExcitationLightPath,
    mock_Microscope,
    mock_Segmentation,
    mock_Segmentation2D,
    mock_VolumetricSegmentation,
    mock_SegmentationContainer,
    mock_PlanarImagingSpace,
    mock_VolumetricImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VolumetricMicroscopySeries,
    mock_MultiChannelMicroscopyVolume,
    mock_MicroscopyResponseSeries,
    mock_MicroscopyResponseSeriesContainer,
)
from ndx_microscopy import (
    Segmentation,
    Segmentation2D,
    VolumetricSegmentation,
    PlanarImagingSpace,
    VolumetricImagingSpace,
)


def test_constructor_microscope():
    microscope = mock_Microscope()
    assert microscope.description == "A mock instance of a Microscope type to be used for rapid testing."


def test_constructor_excitation_light_path():
    excitation_light_path = mock_ExcitationLightPath()
    assert (
        excitation_light_path.description
        == "A mock instance of a ExcitationLightPath type to be used for rapid testing."
    )


def test_constructor_excitation_light_path_with_wrong_mode():
    excitation_mode = "2P"
    expected_error_message = (
        f"excitation_mode must be one of 'one-photon', 'two-photon', "
        f"'three-photon', 'other', not {excitation_mode}. "
        f"If you want to include a different excitation mode, please open an issue on GitHub at "
        f"https://github.com/CatalystNeuro/ndx-microscopy/issues"
    )
    with pytest.raises(ValueError, match=expected_error_message):
        _ = mock_ExcitationLightPath(excitation_mode=excitation_mode)


def test_constructor_excitation_light_path_failing():
    from ndx_ophys_devices.testing import mock_ExcitationSource

    excitation_wavelength_in_nm = 600.0
    excitation_source = mock_ExcitationSource(excitation_wavelength_in_nm=488.0)
    expected_error_message = (
        f"wavelength set in the light path \({excitation_wavelength_in_nm}\) and the one set in the device "
        f"\({excitation_source.excitation_wavelength_in_nm}\) must be the same\."
    )
    with pytest.raises(ValueError, match=expected_error_message):
        _ = mock_ExcitationLightPath(
            excitation_wavelength_in_nm=excitation_wavelength_in_nm,
            excitation_source=excitation_source,
        )


def test_constructor_emission_light_path():
    emission_light_path = mock_EmissionLightPath()
    assert (
        emission_light_path.description == "A mock instance of a EmissionLightPath type to be used for rapid testing."
    )


def test_constructor_emission_light_path_failing():
    from ndx_ophys_devices.testing import mock_Photodetector

    emission_wavelength_in_nm = 600.0
    photodetector = mock_Photodetector(detected_wavelength_in_nm=488.0)
    expected_error_message = (
        f"wavelength set in the light path \({emission_wavelength_in_nm}\) and the one set in the device "
        f"\({photodetector.detected_wavelength_in_nm}\) must be the same."
    )
    with pytest.raises(ValueError, match=expected_error_message):
        _ = mock_EmissionLightPath(emission_wavelength_in_nm=emission_wavelength_in_nm, photodetector=photodetector)


def test_constructor_planar_imaging_space():
    planar_imaging_space = mock_PlanarImagingSpace()
    assert (
        planar_imaging_space.description == "A mock instance of a PlanarImagingSpace type to be used for rapid testing."
    )
    assert isinstance(planar_imaging_space, PlanarImagingSpace)


def test_constructor_volumetric_imaging_space():
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    assert (
        volumetric_imaging_space.description
        == "A mock instance of a VolumetricImagingSpace type to be used for rapid testing."
    )
    assert isinstance(volumetric_imaging_space, VolumetricImagingSpace)


def test_constructor_segmentation():
    """Test constructor for base Segmentation class."""
    segmentation = mock_Segmentation()
    assert segmentation.description == "A mock instance of a Segmentation type to be used for rapid testing."
    assert len(segmentation.summary_images) == 2
    assert "mean" in segmentation.summary_images
    assert "max" in segmentation.summary_images
    assert isinstance(segmentation, Segmentation)


def test_constructor_segmentation_2D():
    """Test constructor for Segmentation2D class."""
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space)
    assert segmentation.description == "A mock instance of a Segmentation2D type to be used for rapid testing."
    assert len(segmentation.id) == 5  # Default number_of_rois
    assert "image_mask" in segmentation.colnames
    assert isinstance(segmentation.planar_imaging_space, PlanarImagingSpace)
    assert isinstance(segmentation, Segmentation2D)
    assert isinstance(segmentation, Segmentation)  # Test inheritance


def test_constructor_volumetric_segmentation():
    """Test constructor for VolumetricSegmentation class."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation = mock_VolumetricSegmentation(volumetric_imaging_space=volumetric_imaging_space)
    assert segmentation.description == "A mock instance of a VolumetricSegmentation type to be used for rapid testing."
    assert len(segmentation.id) == 5  # Default number_of_rois
    assert "image_mask" in segmentation.colnames
    assert isinstance(segmentation.volumetric_imaging_space, VolumetricImagingSpace)
    assert isinstance(segmentation, VolumetricSegmentation)
    assert isinstance(segmentation, Segmentation)  # Test inheritance


def test_constructor_segmentation_container():
    """Test constructor for SegmentationContainer class."""
    container = mock_SegmentationContainer()
    assert len(container.segmentations) == 2  # Default includes both planar and volumetric
    segmentation_names = [seg_name for seg_name in container.segmentations]
    assert isinstance(container.segmentations[segmentation_names[0]], Segmentation2D)
    assert isinstance(container.segmentations[segmentation_names[1]], VolumetricSegmentation)


def test_constructor_planar_microscopy_series():
    microscope = mock_Microscope()
    excitation_light_path = mock_ExcitationLightPath()
    planar_imaging_space = mock_PlanarImagingSpace()
    emission_light_path = mock_EmissionLightPath()

    planar_microscopy_series = mock_PlanarMicroscopySeries(
        microscope=microscope,
        excitation_light_path=excitation_light_path,
        planar_imaging_space=planar_imaging_space,
        emission_light_path=emission_light_path,
    )
    assert (
        planar_microscopy_series.description
        == "A mock instance of a PlanarMicroscopySeries type to be used for rapid testing."
    )


def test_constructor_variable_depth_microscopy_series():
    microscope = mock_Microscope()
    excitation_light_path = mock_ExcitationLightPath()
    planar_imaging_space = mock_PlanarImagingSpace()
    emission_light_path = mock_EmissionLightPath()

    variable_depth_microscopy_series = mock_VariableDepthMicroscopySeries(
        microscope=microscope,
        excitation_light_path=excitation_light_path,
        planar_imaging_space=planar_imaging_space,
        emission_light_path=emission_light_path,
    )
    assert (
        variable_depth_microscopy_series.description
        == "A mock instance of a VariableDepthMicroscopySeries type to be used for rapid testing."
    )


def test_constructor_volumetric_microscopy_series():
    microscope = mock_Microscope()
    excitation_light_path = mock_ExcitationLightPath()
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    emission_light_path = mock_EmissionLightPath()

    volumetric_microscopy_series = mock_VolumetricMicroscopySeries(
        microscope=microscope,
        excitation_light_path=excitation_light_path,
        volumetric_imaging_space=volumetric_imaging_space,
        emission_light_path=emission_light_path,
    )
    assert (
        volumetric_microscopy_series.description
        == "A mock instance of a VolumetricMicroscopySeries type to be used for rapid testing."
    )


def test_constructor_microscopy_response_series():
    number_of_rois = 10
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space, number_of_rois=number_of_rois)

    rois = segmentation.create_roi_table_region(
        description="test region",
        region=[x for x in range(number_of_rois)],
    )

    microscopy_response_series = mock_MicroscopyResponseSeries(rois=rois)
    assert (
        microscopy_response_series.description
        == "A mock instance of a MicroscopyResponseSeries type to be used for rapid testing."
    )


def test_constructor_microscopy_response_series_container():
    number_of_rois = 10
    planar_imaging_space = mock_PlanarImagingSpace()
    segmentation = mock_Segmentation2D(planar_imaging_space=planar_imaging_space, number_of_rois=number_of_rois)

    rois = segmentation.create_roi_table_region(
        description="test region",
        region=[x for x in range(number_of_rois)],
    )

    microscopy_response_series = mock_MicroscopyResponseSeries(rois=rois)

    microscopy_response_series_container = mock_MicroscopyResponseSeriesContainer(
        microscopy_response_series=[microscopy_response_series]
    )
    assert microscopy_response_series_container.name == "MicroscopyResponseSeriesContainer"


def test_constructor_multi_channel_microscopy_volume():
    microscope = mock_Microscope()
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    excitation_light_paths = [mock_ExcitationLightPath()]
    emission_light_paths = [mock_EmissionLightPath()]

    excitation_light_paths_used_by_volume = pynwb.base.VectorData(
        name="excitation_light_paths",
        description="Light sources used by this MultiChannelVolume.",
        data=excitation_light_paths,
    )
    emission_light_paths_used_by_volume = pynwb.base.VectorData(
        name="emission_light_paths",
        description=(
            "Optical channels ordered to correspond to the third axis (e.g., [0, 0, :, 0]) "
            "of the data for this MultiChannelVolume."
        ),
        data=emission_light_paths,
    )
    multichannel_microscopy_volume = mock_MultiChannelMicroscopyVolume(
        microscope=microscope,
        volumetric_imaging_space=volumetric_imaging_space,
        excitation_light_paths=excitation_light_paths_used_by_volume,
        emission_light_paths=emission_light_paths_used_by_volume,
    )
    assert (
        multichannel_microscopy_volume.description
        == "A mock instance of a MultiChannelMicroscopyVolume type to be used for rapid testing."
    )


if __name__ == "__main__":
    pytest.main([__file__])
