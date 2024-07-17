"""Test in-memory Python API constructors for the ndx-microscopy extension."""

import pytest

import pynwb
from ndx_microscopy.testing import (
    mock_Microscope,
    mock_MicroscopyLightSource,
    mock_MicroscopyOpticalChannel,
    mock_MicroscopyPlaneSegmentation,
    mock_MicroscopySegmentations,
    mock_MultiChannelMicroscopyVolume,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VariableDepthMultiChannelMicroscopyVolume,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
)


def test_constructor_microscope():
    mock_Microscope()


def test_constructor_light_source():
    mock_MicroscopyLightSource()


def test_constructor_microscopy_optical_channel():
    mock_MicroscopyOpticalChannel()


def test_constructor_planar_image_space():
    microscope = mock_Microscope()

    mock_PlanarImagingSpace(microscope=microscope)


def test_constructor_volumetric_image_space():
    microscope = mock_Microscope()

    mock_VolumetricImagingSpace(microscope=microscope)


def test_constructor_microscopy_segmentations():
    mock_MicroscopySegmentations()


def test_constructor_microscopy_plane_segmentation():
    microscope = mock_Microscope()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)

    mock_MicroscopyPlaneSegmentation(imaging_space=imaging_space)


def test_constructor_microscopy_image_segmentation_with_plane_segmentation():
    microscope = mock_Microscope()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)

    plane_segmentation_1 = mock_MicroscopyPlaneSegmentation(
        imaging_space=imaging_space, name="MicroscopyPlaneSegmentation1"
    )
    plane_segmentation_2 = mock_MicroscopyPlaneSegmentation(
        imaging_space=imaging_space, name="MicroscopyPlaneSegmentation2"
    )
    microscopy_plane_segmentations = [plane_segmentation_1, plane_segmentation_2]

    mock_MicroscopySegmentations(microscopy_plane_segmentations=microscopy_plane_segmentations)


def test_constructor_planar_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_MicroscopyLightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_PlanarMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_variable_depth_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_MicroscopyLightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VariableDepthMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_volumetric_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_MicroscopyLightSource()
    imaging_space = mock_VolumetricImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VolumetricMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_multi_channel_microscopy_volume():
    microscope = mock_Microscope()
    imaging_space = mock_VolumetricImagingSpace(microscope=microscope)
    light_sources = [mock_MicroscopyLightSource()]
    optical_channels = [mock_MicroscopyOpticalChannel()]

    light_sources_used_by_volume = pynwb.base.VectorData(
        name="light_sources", description="Light sources used by this MultiChannelVolume.", data=light_sources
    )
    optical_channels_used_by_volume = pynwb.base.VectorData(
        name="optical_channels",
        description=(
            "Optical channels ordered to correspond to the third axis (e.g., [0, 0, :, 0]) "
            "of the data for this MultiChannelVolume."
        ),
        data=optical_channels,
    )
    mock_MultiChannelMicroscopyVolume(
        microscope=microscope,
        imaging_space=imaging_space,
        light_sources=light_sources_used_by_volume,
        optical_channels=optical_channels_used_by_volume,
    )


def test_constructor_variable_depth_multi_channel_microscopy_volume():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_VolumetricImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VariableDepthMultiChannelMicroscopyVolume(
        microscope=microscope,
        light_source=light_source,
        imaging_space=imaging_space,
        optical_channels=[optical_channel],
    )


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
