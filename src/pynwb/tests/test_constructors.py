"""Test in-memory Python API constructors for ndx-microscopy extension."""

import pytest

from ndx_ophys_devices.testing import (
    mock_Indicator,
    mock_Photodetector,
    mock_DichroicMirror,
    mock_BandOpticalFilter,
    mock_EdgeOpticalFilter,
    mock_ObjectiveLens,
    mock_ExcitationSource,
    mock_Microscope,
)

from ndx_microscopy.testing import (
    mock_Microscopy,
    mock_MicroscopyTable,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
)
def test_constructor_microscopy():
    mock_Microscopy()


def test_constructor_microscopy_table():
    mock_MicroscopyTable()


def test_constructor_planar_image_space():
    mock_PlanarImagingSpace()


def test_constructor_volumetric_image_space():
    mock_VolumetricImagingSpace()


def test_constructor_planar_microscopy_series():
    imaging_space = mock_PlanarImagingSpace()
    mock_PlanarMicroscopySeries(imaging_space=imaging_space)


def test_constructor_variable_depth_microscopy_series():
    imaging_space = mock_PlanarImagingSpace()

    mock_VariableDepthMicroscopySeries(imaging_space=imaging_space    )


def test_constructor_volumetric_microscopy_series():
    imaging_space = mock_VolumetricImagingSpace()

    mock_VolumetricMicroscopySeries(imaging_space=imaging_space)


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
