"""Test in-memory Python API constructors for the ndx-microscopy extension."""

import pytest

from ndx_microscopy.testing import (
    mock_EmissionLightPath,
    mock_ExcitationLightPath,
    mock_Microscope,
    mock_Segmentation,
    mock_Segmentation2D,
    mock_Segmentation3D,
    mock_SegmentationContainer,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_MultiPlaneMicroscopyContainer,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
    mock_MicroscopyResponseSeries,
    mock_MicroscopyResponseSeriesContainer,
    mock_ImagingModality,
    mock_LineScanning,
    mock_RasterScanning,
    mock_ResonantScanning,
    mock_TemporalFocusing,
    mock_LightSheet,
    mock_RandomAccessScanning,
)
from ndx_microscopy import (
    Segmentation,
    Segmentation2D,
    Segmentation3D,
    PlanarImagingSpace,
    VolumetricImagingSpace,
    ImagingModality,
    LineScanning,
    RasterScanning,
    ResonantScanning,
    TemporalFocusing,
    LightSheet,
    RandomAccessScanning,
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


def test_constructor_emission_light_path():
    emission_light_path = mock_EmissionLightPath()
    assert (
        emission_light_path.description == "A mock instance of a EmissionLightPath type to be used for rapid testing."
    )


def test_constructor_imaging_modality():
    """Test constructor for base ImagingModality class."""
    imaging_modality = mock_ImagingModality()
    assert imaging_modality.description == "A mock instance of an ImagingModality type to be used for rapid testing."
    assert isinstance(imaging_modality, ImagingModality)


def test_constructor_line_scanning():
    """Test constructor for LineScanning class."""
    line_scanning = mock_LineScanning()
    assert line_scanning.description == "A mock instance of a LineScanning type to be used for rapid testing."
    assert line_scanning.scan_direction == "horizontal"
    assert line_scanning.line_rate_in_Hz == 1000.0
    assert line_scanning.dwell_time_in_s == 1e-6
    assert isinstance(line_scanning, LineScanning)
    assert isinstance(line_scanning, ImagingModality)  # Test inheritance


def test_constructor_raster_scanning():
    """Test constructor for RasterScanning class."""
    raster_scanning = mock_RasterScanning()
    assert raster_scanning.description == "A mock instance of a RasterScanning type to be used for rapid testing."
    assert raster_scanning.scan_pattern == "bidirectional"
    assert raster_scanning.dwell_time_in_s == 1.0e-6
    assert isinstance(raster_scanning, RasterScanning)
    assert isinstance(raster_scanning, ImagingModality)  # Test inheritance


def test_constructor_resonant_scanning():
    """Test constructor for ResonantScanning class."""
    resonant_scanning = mock_ResonantScanning()
    assert resonant_scanning.description == "A mock instance of a ResonantScanning type to be used for rapid testing."
    assert resonant_scanning.resonant_frequency_in_Hz == 8000.0
    assert resonant_scanning.resonant_amplitude == 1.5
    assert isinstance(resonant_scanning, ResonantScanning)
    assert isinstance(resonant_scanning, ImagingModality)  # Test inheritance


def test_constructor_temporal_focusing():
    """Test constructor for TemporalFocusing class."""
    temporal_focusing = mock_TemporalFocusing()
    assert temporal_focusing.description == "A mock instance of a TemporalFocusing type to be used for rapid testing."
    assert temporal_focusing.lateral_point_spread_function_in_um == "0.5 ± 0.1"
    assert temporal_focusing.axial_point_spread_function_in_um == "2.0 ± 0.3"
    assert temporal_focusing.pulse_duration_in_s == 0.0000001
    assert isinstance(temporal_focusing, TemporalFocusing)
    assert isinstance(temporal_focusing, ImagingModality)  # Test inheritance


def test_constructor_light_sheet():
    """Test constructor for LightSheet class."""
    light_sheet = mock_LightSheet()
    assert light_sheet.description == "A mock instance of a LightSheet type to be used for rapid testing."
    assert light_sheet.sheet_thickness_in_um == 5.0
    assert light_sheet.illumination_angle_in_degrees == 45.0
    assert isinstance(light_sheet, LightSheet)
    assert isinstance(light_sheet, ImagingModality)  # Test inheritance


def test_constructor_random_access_scanning():
    """Test constructor for RandomAccessScanning class."""
    random_access_scanning = mock_RandomAccessScanning()
    assert (
        random_access_scanning.description
        == "A mock instance of a RandomAccessScanning type to be used for rapid testing."
    )
    assert random_access_scanning.max_scan_points == 1000
    assert random_access_scanning.dwell_time_in_s == 1.0e-6
    assert random_access_scanning.scanning_pattern == "spiral"
    assert isinstance(random_access_scanning, RandomAccessScanning)
    assert isinstance(random_access_scanning, ImagingModality)  # Test inheritance


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
    """Test constructor for Segmentation3D class."""
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    segmentation = mock_Segmentation3D(volumetric_imaging_space=volumetric_imaging_space)
    assert segmentation.description == "A mock instance of a Segmentation3D type to be used for rapid testing."
    assert len(segmentation.id) == 5  # Default number_of_rois
    assert "image_mask" in segmentation.colnames
    assert isinstance(segmentation.volumetric_imaging_space, VolumetricImagingSpace)
    assert isinstance(segmentation, Segmentation3D)
    assert isinstance(segmentation, Segmentation)  # Test inheritance


def test_constructor_segmentation_container():
    """Test constructor for SegmentationContainer class."""
    container = mock_SegmentationContainer()
    assert len(container.segmentations) == 2  # Default includes both planar and volumetric
    segmentation_names = [seg_name for seg_name in container.segmentations]
    assert isinstance(container.segmentations[segmentation_names[0]], Segmentation2D)
    assert isinstance(container.segmentations[segmentation_names[1]], Segmentation3D)


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


def test_constructor_multi_plane_microscopy_container():

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

    multi_plane_microscopy_container = mock_MultiPlaneMicroscopyContainer(
        planar_microscopy_series=[planar_microscopy_series]
    )
    assert multi_plane_microscopy_container.name == "MultiPlaneMicroscopyContainer"


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


if __name__ == "__main__":
    pytest.main([__file__])
