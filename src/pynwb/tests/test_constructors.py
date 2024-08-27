"""Test in-memory Python API constructors for the ndx-microscopy extension."""

import pynwb.testing.mock.ophys
import pytest

import ndx_microscopy.testing
import pynwb


def test_constructor_microscope():
    ndx_microscopy.testing.mock_Microscope()


def test_constructor_light_source():
    ndx_microscopy.testing.mock_MicroscopyLightSource()


def test_constructor_microscopy_optical_channel():
    ndx_microscopy.testing.mock_MicroscopyOpticalChannel()


def test_constructor_planar_image_space():
    microscope = ndx_microscopy.testing.mock_Microscope()

    ndx_microscopy.testing.mock_PlanarImagingSpace(microscope=microscope)


def test_constructor_volumetric_image_space():
    microscope = ndx_microscopy.testing.mock_Microscope()

    ndx_microscopy.testing.mock_VolumetricImagingSpace(microscope=microscope)


def test_constructor_microscopy_segmentations():
    ndx_microscopy.testing.mock_MicroscopySegmentations()


def test_constructor_microscopy_plane_segmentation():
    microscope = ndx_microscopy.testing.mock_Microscope()
    imaging_space = ndx_microscopy.testing.mock_PlanarImagingSpace(microscope=microscope)

    ndx_microscopy.testing.mock_MicroscopyPlaneSegmentation(imaging_space=imaging_space)


def test_constructor_microscopy_image_segmentation_with_plane_segmentation():
    microscope = ndx_microscopy.testing.mock_Microscope()
    imaging_space = ndx_microscopy.testing.mock_PlanarImagingSpace(microscope=microscope)

    plane_segmentation_1 = ndx_microscopy.testing.mock_MicroscopyPlaneSegmentation(
        imaging_space=imaging_space, name="MicroscopyPlaneSegmentation1"
    )
    plane_segmentation_2 = ndx_microscopy.testing.mock_MicroscopyPlaneSegmentation(
        imaging_space=imaging_space, name="MicroscopyPlaneSegmentation2"
    )
    microscopy_plane_segmentations = [plane_segmentation_1, plane_segmentation_2]

    ndx_microscopy.testing.mock_MicroscopySegmentations(microscopy_plane_segmentations=microscopy_plane_segmentations)


def test_constructor_planar_microscopy_series():
    microscope = ndx_microscopy.testing.mock_Microscope()
    light_source = ndx_microscopy.testing.mock_MicroscopyLightSource()
    imaging_space = ndx_microscopy.testing.mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = ndx_microscopy.testing.mock_MicroscopyOpticalChannel()

    ndx_microscopy.testing.mock_PlanarMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_variable_depth_microscopy_series():
    microscope = ndx_microscopy.testing.mock_Microscope()
    light_source = ndx_microscopy.testing.mock_MicroscopyLightSource()
    imaging_space = ndx_microscopy.testing.mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = ndx_microscopy.testing.mock_MicroscopyOpticalChannel()

    ndx_microscopy.testing.mock_VariableDepthMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_volumetric_microscopy_series():
    microscope = ndx_microscopy.testing.mock_Microscope()
    light_source = ndx_microscopy.testing.mock_MicroscopyLightSource()
    imaging_space = ndx_microscopy.testing.mock_VolumetricImagingSpace(microscope=microscope)
    optical_channel = ndx_microscopy.testing.mock_MicroscopyOpticalChannel()

    ndx_microscopy.testing.mock_VolumetricMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
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

    ndx_microscopy.testing.mock_MicroscopyResponseSeries(table_region=table_region)


def test_constructor_microscopy_response_series_container():
    number_of_rois = 10

    plane_segmentation = pynwb.testing.mock.ophys.mock_PlaneSegmentation()

    table_region = pynwb.core.DynamicTableRegion(
        name="table_region",
        description="",
        data=[x for x in range(number_of_rois)],
        table=plane_segmentation,
    )

    microscopy_response_series = [ndx_microscopy.testing.mock_MicroscopyResponseSeries(table_region=table_region)]

    ndx_microscopy.testing.mock_MicroscopyResponseSeriesContainer(microscopy_response_series=microscopy_response_series)


def test_constructor_multi_channel_microscopy_volume():
    microscope = ndx_microscopy.testing.mock_Microscope()
    imaging_space = ndx_microscopy.testing.mock_VolumetricImagingSpace(microscope=microscope)
    light_sources = [ndx_microscopy.testing.mock_MicroscopyLightSource()]
    optical_channels = [ndx_microscopy.testing.mock_MicroscopyOpticalChannel()]

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
    ndx_microscopy.testing.mock_MultiChannelMicroscopyVolume(
        microscope=microscope,
        imaging_space=imaging_space,
        light_sources=light_sources_used_by_volume,
        optical_channels=optical_channels_used_by_volume,
    )


def test_constructor_variable_depth_multi_channel_microscopy_volume():
    microscope = ndx_microscopy.testing.mock_Microscope()
    imaging_space = ndx_microscopy.testing.mock_VolumetricImagingSpace(microscope=microscope)
    light_sources = [ndx_microscopy.testing.mock_MicroscopyLightSource()]
    optical_channels = [ndx_microscopy.testing.mock_MicroscopyOpticalChannel()]

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
    ndx_microscopy.testing.mock_VariableDepthMultiChannelMicroscopyVolume(
        microscope=microscope,
        imaging_space=imaging_space,
        light_sources=light_sources_used_by_volume,
        optical_channels=optical_channels_used_by_volume,
    )


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
