"""Test in-memory Python API constructors for ndx-microscopy extension."""

import pytest

from ndx_microscopy.testing import (
    mock_LightSource,
    mock_Microscope,
    mock_MicroscopyOpticalChannel,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
)


def test_constructor_microscope():
    mock_Microscope()


def test_constructor_light_source():
    mock_LightSource()


def test_constructor_microscopy_optical_channel():
    mock_MicroscopyOpticalChannel()


def test_constructor_planar_image_space():
    microscope = mock_Microscope()

    mock_PlanarImagingSpace(microscope=microscope)


def test_constructor_volumetric_image_space():
    microscope = mock_Microscope()

    mock_VolumetricImagingSpace(microscope=microscope)


def test_constructor_planar_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_PlanarMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_variable_depth_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VariableDepthMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_volumetric_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_VolumetricImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VolumetricMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
