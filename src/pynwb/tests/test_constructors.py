"""Test in-memory Python API constructors for the ndx-microscopy extension."""

import pytest
from ndx_ophys_devices import ObjectiveLens
from ndx_ophys_devices.testing import mock_Indicator, mock_ViralVector, mock_ViralVectorInjection

from ndx_microscopy.testing import (
    mock_MicroscopyRig,
    mock_MicroscopeModel,
    mock_Microscope,
    mock_MicroscopyChannel,
    mock_Segmentation,
    mock_PlanarSegmentation,
    mock_VolumetricSegmentation,
    mock_SegmentationContainer,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_PlanarMicroscopyStaticImage,
    mock_VolumetricMicroscopyStaticImage,
    mock_MultiPlaneMicroscopyContainer,
    mock_MultiChannelMicroscopyContainer,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
    mock_MicroscopyResponseSeries,
    mock_MicroscopyResponseSeriesContainer,
    mock_IlluminationPattern,
    mock_LineScan,
    mock_PlaneAcquisition,
    mock_RandomAccessScan,
)

from ndx_microscopy import (
    Microscope,
    MicroscopeModel,
    MicroscopyRig,
    MicroscopyExperimentMetadata,
    Segmentation,
    PlanarSegmentation,
    VolumetricSegmentation,
    PlanarImagingSpace,
    VolumetricImagingSpace,
    IlluminationPattern,
    LineScan,
    PlaneAcquisition,
    RandomAccessScan,
)


@pytest.fixture
def microscopy_rig():
    return mock_MicroscopyRig()


@pytest.fixture
def microscopy_channel():
    return mock_MicroscopyChannel(indicator=mock_Indicator(name="Indicator1"))


@pytest.mark.parametrize(
    "mock_function, expected_type",
    [
        (mock_MicroscopeModel, MicroscopeModel),
        (mock_Microscope, Microscope),
        (mock_MicroscopyRig, MicroscopyRig),
        (mock_IlluminationPattern, IlluminationPattern),
        (mock_PlanarImagingSpace, PlanarImagingSpace),
        (mock_VolumetricImagingSpace, VolumetricImagingSpace),
    ],
)
def test_constructor_without_arguments(mock_function, expected_type):
    assert isinstance(mock_function(), expected_type)


def test_constructor_microscope():
    microscope = mock_Microscope()
    assert isinstance(microscope.model, MicroscopeModel)
    assert microscope.technique == "A fake technique used by the mock microscope."


def test_constructor_microscopy_rig(microscopy_rig):
    assert isinstance(microscopy_rig.microscope, Microscope)
    assert isinstance(microscopy_rig.objective_lens, ObjectiveLens)
    assert microscopy_rig.optical_path_scheme is None


def test_constructor_microscopy_channel():
    indicator = mock_Indicator(name="Indicator1")
    microscopy_channel = mock_MicroscopyChannel(indicator=indicator)
    assert microscopy_channel.indicator is indicator
    assert microscopy_channel.excitation_wavelength_in_nm == 488.0
    assert microscopy_channel.emission_wavelength_in_nm == 520.0


def test_constructor_microscopy_experiment_metadata(microscopy_rig):
    viral_vector = mock_ViralVector(name="ViralVector1")
    viral_vector_injection = mock_ViralVectorInjection(name="ViralVectorInjection1", viral_vector=viral_vector)
    indicator = mock_Indicator(name="Indicator1", viral_vector_injection=viral_vector_injection)

    metadata = MicroscopyExperimentMetadata(
        viral_vectors=[viral_vector],
        viral_vector_injections=[viral_vector_injection],
        indicators=[indicator],
        microscopy_rigs=[microscopy_rig],
    )
    assert metadata.name == "microscopy_experiment_metadata"
    assert metadata.viral_vectors["ViralVector1"] is viral_vector
    assert metadata.viral_vector_injections["ViralVectorInjection1"] is viral_vector_injection
    assert metadata.indicators["Indicator1"] is indicator
    assert metadata.microscopy_rigs[microscopy_rig.name] is microscopy_rig


def test_constructor_line_scan():
    line_scan = mock_LineScan()
    assert line_scan.scan_direction == "horizontal"
    assert line_scan.line_rate_in_Hz == 1000.0
    assert line_scan.dwell_time_in_s == 1e-6
    assert isinstance(line_scan, LineScan)
    assert isinstance(line_scan, IlluminationPattern)


def test_constructor_plane_acquisition():
    plane_acquisition = mock_PlaneAcquisition()
    assert plane_acquisition.point_spread_function == "32 um ± 1.6 um"
    assert plane_acquisition.illumination_angle_in_degrees == 45.0
    assert plane_acquisition.plane_rate_in_Hz == 100.0
    assert isinstance(plane_acquisition, PlaneAcquisition)
    assert isinstance(plane_acquisition, IlluminationPattern)


def test_constructor_random_access_scan():
    random_access_scan = mock_RandomAccessScan()
    assert random_access_scan.max_scan_points == 1000
    assert random_access_scan.dwell_time_in_s == 1.0e-6
    assert random_access_scan.scanning_pattern == "spiral"
    assert isinstance(random_access_scan, RandomAccessScan)
    assert isinstance(random_access_scan, IlluminationPattern)


def test_constructor_segmentation():
    segmentation = mock_Segmentation()
    assert set(segmentation.summary_images) == {"mean", "max"}
    assert isinstance(segmentation, Segmentation)


def test_constructor_planar_segmentation():
    planar_imaging_space = mock_PlanarImagingSpace(dimensions_in_pixels=(20, 10))
    segmentation = mock_PlanarSegmentation(planar_imaging_space=planar_imaging_space)
    assert len(segmentation.id) == 5  # Default number_of_rois
    assert segmentation.image_mask[0].shape == (10, 20)  # (height, width)
    assert segmentation.planar_imaging_space is planar_imaging_space
    assert isinstance(segmentation, PlanarSegmentation)
    assert isinstance(segmentation, Segmentation)


def test_constructor_volumetric_segmentation():
    volumetric_imaging_space = mock_VolumetricImagingSpace(dimensions_in_voxels=(20, 10, 5))
    segmentation = mock_VolumetricSegmentation(volumetric_imaging_space=volumetric_imaging_space)
    assert len(segmentation.id) == 5  # Default number_of_rois
    assert segmentation.volume_mask[0].shape == (5, 10, 20)  # (depth, height, width)
    assert segmentation.volumetric_imaging_space is volumetric_imaging_space
    assert isinstance(segmentation, VolumetricSegmentation)
    assert isinstance(segmentation, Segmentation)


def test_constructor_segmentation_container():
    container = mock_SegmentationContainer()
    segmentations = list(container.segmentations.values())
    assert len(segmentations) == 2  # Default includes both planar and volumetric
    assert isinstance(segmentations[0], PlanarSegmentation)
    assert isinstance(segmentations[1], VolumetricSegmentation)


@pytest.mark.parametrize(
    "mock_function, imaging_space_argument, mock_imaging_space, data_ndim",
    [
        (mock_PlanarMicroscopySeries, "planar_imaging_space", mock_PlanarImagingSpace, 3),
        (mock_VolumetricMicroscopySeries, "volumetric_imaging_space", mock_VolumetricImagingSpace, 4),
        (mock_PlanarMicroscopyStaticImage, "planar_imaging_space", mock_PlanarImagingSpace, 2),
        (mock_VolumetricMicroscopyStaticImage, "volumetric_imaging_space", mock_VolumetricImagingSpace, 3),
    ],
)
def test_constructor_imaging_data(
    microscopy_rig, microscopy_channel, mock_function, imaging_space_argument, mock_imaging_space, data_ndim
):
    imaging_space = mock_imaging_space()
    imaging_data = mock_function(
        microscopy_rig=microscopy_rig,
        microscopy_channel=microscopy_channel,
        **{imaging_space_argument: imaging_space},
    )
    assert imaging_data.microscopy_rig is microscopy_rig
    assert imaging_data.microscopy_channel is microscopy_channel
    assert getattr(imaging_data, imaging_space_argument) is imaging_space
    assert imaging_data.data.ndim == data_ndim


def test_constructor_multi_plane_microscopy_container(microscopy_rig, microscopy_channel):
    planar_imaging_space = mock_PlanarImagingSpace()
    planar_microscopy_series = mock_PlanarMicroscopySeries(
        microscopy_rig=microscopy_rig,
        microscopy_channel=microscopy_channel,
        planar_imaging_space=planar_imaging_space,
    )
    planar_microscopy_static_image = mock_PlanarMicroscopyStaticImage(
        microscopy_rig=microscopy_rig,
        microscopy_channel=microscopy_channel,
        planar_imaging_space=planar_imaging_space,
    )

    container = mock_MultiPlaneMicroscopyContainer(
        planar_microscopy_series=[planar_microscopy_series],
        planar_microscopy_static_images=[planar_microscopy_static_image],
    )
    assert list(container.planar_microscopy_series.values()) == [planar_microscopy_series]
    assert list(container.planar_microscopy_static_images.values()) == [planar_microscopy_static_image]


def test_constructor_multi_channel_microscopy_container(microscopy_rig):
    planar_imaging_space_1 = mock_PlanarImagingSpace(name="PlanarImagingSpace_depth1")
    planar_imaging_space_2 = mock_PlanarImagingSpace(name="PlanarImagingSpace_depth2")

    # Channel 1: functional indicator (GCaMP) at two depths
    gcamp_channel = mock_MicroscopyChannel(indicator=mock_Indicator(name="Indicator_GCaMP"), name="GCaMPChannel")
    multi_plane_gcamp = mock_MultiPlaneMicroscopyContainer(
        name="GCaMP_planes",
        planar_microscopy_series=[
            mock_PlanarMicroscopySeries(
                name=f"GCaMP_depth{depth}",
                microscopy_rig=microscopy_rig,
                microscopy_channel=gcamp_channel,
                planar_imaging_space=planar_imaging_space,
            )
            for depth, planar_imaging_space in enumerate((planar_imaging_space_1, planar_imaging_space_2), start=1)
        ],
    )

    # Channel 2: anatomical marker (mCherry) static image
    mcherry_channel = mock_MicroscopyChannel(indicator=mock_Indicator(name="Indicator_mCherry"), name="mCherryChannel")
    mcherry_image = mock_PlanarMicroscopyStaticImage(
        name="mCherry_depth1",
        microscopy_rig=microscopy_rig,
        microscopy_channel=mcherry_channel,
        planar_imaging_space=planar_imaging_space_1,
    )

    container = mock_MultiChannelMicroscopyContainer(
        microscopy_static_images=[mcherry_image],
        multi_plane_microscopy_containers=[multi_plane_gcamp],
    )
    assert list(container.microscopy_static_images.values()) == [mcherry_image]
    assert list(container.multi_plane_microscopy_containers.values()) == [multi_plane_gcamp]
    assert len(container.microscopy_series) == 0


def test_constructor_microscopy_response_series(microscopy_rig, microscopy_channel):
    planar_imaging_space = mock_PlanarImagingSpace()
    microscopy_series = mock_PlanarMicroscopySeries(
        microscopy_channel=microscopy_channel,
        microscopy_rig=microscopy_rig,
        planar_imaging_space=planar_imaging_space,
    )
    segmentation = mock_PlanarSegmentation(planar_imaging_space=planar_imaging_space, number_of_rois=10)
    rois = segmentation.create_roi_table_region(description="test region", region=list(range(10)))

    microscopy_response_series = mock_MicroscopyResponseSeries(rois=rois, microscopy_series=microscopy_series)
    assert microscopy_response_series.data.shape == (100, 10)  # (frames, ROIs)
    assert microscopy_response_series.rois.table is segmentation
    assert microscopy_response_series.microscopy_series is microscopy_series


def test_constructor_microscopy_response_series_container():
    segmentation = mock_PlanarSegmentation(planar_imaging_space=mock_PlanarImagingSpace(), number_of_rois=10)
    rois = segmentation.create_roi_table_region(description="test region", region=list(range(10)))
    microscopy_response_series = mock_MicroscopyResponseSeries(rois=rois)

    container = mock_MicroscopyResponseSeriesContainer(microscopy_response_series=[microscopy_response_series])
    assert list(container.microscopy_response_series.values()) == [microscopy_response_series]


if __name__ == "__main__":
    pytest.main([__file__])
