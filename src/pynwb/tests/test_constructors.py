"""Test in-memory Python API constructors for the ndx-microscopy extension."""

import pynwb.testing.mock.ophys
import pytest

import pynwb
from ndx_microscopy.testing import (
    mock_EmissionLightPath,
    mock_ExcitationLightPath,
    mock_Microscope,
    mock_MicroscopyPlaneSegmentation,
    mock_MicroscopySegmentations,
    mock_MicroscopyResponseSeries,
    mock_MicroscopyResponseSeriesContainer,
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


def test_constructor_excitation_light_path():
    mock_ExcitationLightPath()


def test_constructor_microscopy_emission_light_path():
    mock_EmissionLightPath()


def test_constructor_planar_image_space():
    mock_PlanarImagingSpace()


def test_constructor_volumetric_image_space():
    mock_VolumetricImagingSpace()


def test_constructor_microscopy_segmentations():
    mock_MicroscopySegmentations()


def test_constructor_microscopy_plane_segmentation():
    imaging_space = mock_PlanarImagingSpace()
    mock_MicroscopyPlaneSegmentation(imaging_space=imaging_space)


def test_constructor_microscopy_image_segmentation_with_plane_segmentation():
    imaging_space = mock_PlanarImagingSpace()
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
    excitation_light_path = mock_ExcitationLightPath()
    imaging_space = mock_PlanarImagingSpace()
    emission_light_path = mock_EmissionLightPath()

    mock_PlanarMicroscopySeries(
        microscope=microscope,
        excitation_light_path=excitation_light_path,
        imaging_space=imaging_space,
        emission_light_path=emission_light_path,
    )


def test_constructor_variable_depth_microscopy_series():
    microscope = mock_Microscope()
    excitation_light_path = mock_ExcitationLightPath()
    imaging_space = mock_PlanarImagingSpace()
    emission_light_path = mock_EmissionLightPath()

    mock_VariableDepthMicroscopySeries(
        microscope=microscope,
        excitation_light_path=excitation_light_path,
        imaging_space=imaging_space,
        emission_light_path=emission_light_path,
    )


def test_constructor_volumetric_microscopy_series():
    microscope = mock_Microscope()
    excitation_light_path = mock_ExcitationLightPath()
    imaging_space = mock_VolumetricImagingSpace()
    emission_light_path = mock_EmissionLightPath()

    mock_VolumetricMicroscopySeries(
        microscope=microscope,
        excitation_light_path=excitation_light_path,
        imaging_space=imaging_space,
        emission_light_path=emission_light_path,
    )


def test_constructor_microscopy_response_series():
    number_of_rois = 10

    plane_segmentation = pynwb.testing.mock.ophys.mock_PlaneSegmentation()

    table_region = pynwb.core.DynamicTableRegion(
        name="table_region",
        description="",
        data=[x for x in range(number_of_rois)],
        table=plane_segmentation,
    )

    mock_MicroscopyResponseSeries(table_region=table_region)


def test_constructor_microscopy_response_series_container():
    number_of_rois = 10

    plane_segmentation = pynwb.testing.mock.ophys.mock_PlaneSegmentation()

    table_region = pynwb.core.DynamicTableRegion(
        name="table_region",
        description="",
        data=[x for x in range(number_of_rois)],
        table=plane_segmentation,
    )

    microscopy_response_series = mock_MicroscopyResponseSeries(table_region=table_region)

    mock_MicroscopyResponseSeriesContainer(
        microscopy_response_series=[microscopy_response_series]
    )


def test_constructor_multi_channel_microscopy_volume():
    microscope = mock_Microscope()
    imaging_space = mock_VolumetricImagingSpace()
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
    mock_MultiChannelMicroscopyVolume(
        microscope=microscope,
        imaging_space=imaging_space,
        excitation_light_paths=excitation_light_paths_used_by_volume,
        emission_light_paths=emission_light_paths_used_by_volume,
    )


def test_constructor_variable_depth_multi_channel_microscopy_volume():
    microscope = mock_Microscope()
    imaging_space = mock_VolumetricImagingSpace()
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
    mock_VariableDepthMultiChannelMicroscopyVolume(
        microscope=microscope,
        imaging_space=imaging_space,
        excitation_light_paths=excitation_light_paths_used_by_volume,
        emission_light_paths=emission_light_paths_used_by_volume,
    )


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
