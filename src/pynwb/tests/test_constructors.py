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
    try:
        _ = mock_ExcitationLightPath(excitation_mode=excitation_mode)
    except ValueError as e:
        assert (
            str(e)
            == f"excitation_mode must be one of 'one-photon', 'two-photon', 'three-photon', 'multiphoton', not {excitation_mode}"
        )
    else:
        assert False, "Expected ValueError not raised"


def test_constructor_excitation_light_path_failing():
    from ndx_ophys_devices.testing import mock_ExcitationSource

    excitation_wavelength_in_nm = 600.0
    excitation_source = mock_ExcitationSource(excitation_wavelength_in_nm=488.0)
    try:
        _ = mock_ExcitationLightPath(
            excitation_wavelength_in_nm=excitation_wavelength_in_nm,
            excitation_source=excitation_source,
        )
    except ValueError as e:
        assert str(e) == (
            f"wavelength set in the light path ({excitation_wavelength_in_nm}) and the one set in the device "
            f"({excitation_source.excitation_wavelength_in_nm}) must be the same."
        )
    else:
        assert False, "Expected ValueError not raised"


def test_constructor_microscopy_emission_light_path():
    emission_light_path = mock_EmissionLightPath()
    assert (
        emission_light_path.description == "A mock instance of a EmissionLightPath type to be used for rapid testing."
    )


def test_constructor_emission_light_path_failing():
    from ndx_ophys_devices.testing import mock_Photodetector

    emission_wavelength_in_nm = 600.0
    photodetector = mock_Photodetector(detected_wavelength_in_nm=488.0)
    try:
        _ = mock_EmissionLightPath(emission_wavelength_in_nm=emission_wavelength_in_nm, photodetector=photodetector)
    except ValueError as e:
        assert str(e) == (
            f"wavelength set in the light path ({emission_wavelength_in_nm}) and the one set in the device "
            f"({photodetector.detected_wavelength_in_nm}) must be the same."
        )
    else:
        assert False, "Expected ValueError not raised"


def test_constructor_planar_image_space():
    planar_imaging_space = mock_PlanarImagingSpace()
    assert (
        planar_imaging_space.description == "A mock instance of a PlanarImagingSpace type to be used for rapid testing."
    )


def test_constructor_volumetric_image_space():
    volumetric_imaging_space = mock_VolumetricImagingSpace()
    assert (
        volumetric_imaging_space.description
        == "A mock instance of a VolumetricImagingSpace type to be used for rapid testing."
    )


def test_constructor_microscopy_segmentations():
    microscopy_segmentations = mock_MicroscopySegmentations()
    assert "MicroscopySegmentations" in microscopy_segmentations.name


def test_constructor_microscopy_plane_segmentation():
    imaging_space = mock_PlanarImagingSpace()
    microscopy_plane_segmentation = mock_MicroscopyPlaneSegmentation(imaging_space=imaging_space)
    assert (
        microscopy_plane_segmentation.description
        == "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing."
    )


def test_constructor_microscopy_image_segmentation_with_plane_segmentation():
    imaging_space = mock_PlanarImagingSpace()
    plane_segmentation_1 = mock_MicroscopyPlaneSegmentation(
        imaging_space=imaging_space, name="MicroscopyPlaneSegmentation1"
    )
    plane_segmentation_2 = mock_MicroscopyPlaneSegmentation(
        imaging_space=imaging_space, name="MicroscopyPlaneSegmentation2"
    )
    microscopy_plane_segmentations = [plane_segmentation_1, plane_segmentation_2]

    microscopy_segmentations = mock_MicroscopySegmentations(
        name="MicroscopySegmentations2", microscopy_plane_segmentations=microscopy_plane_segmentations
    )
    assert microscopy_segmentations.name == "MicroscopySegmentations2"


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

    plane_segmentation = pynwb.testing.mock.ophys.mock_PlaneSegmentation()

    table_region = pynwb.core.DynamicTableRegion(
        name="table_region",
        description="",
        data=[x for x in range(number_of_rois)],
        table=plane_segmentation,
    )

    microscopy_response_series = mock_MicroscopyResponseSeries(table_region=table_region)
    assert (
        microscopy_response_series.description
        == "A mock instance of a MicroscopyResponseSeries type to be used for rapid testing."
    )


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


def test_constructor_variable_depth_multi_channel_microscopy_volume():
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
    variable_depth_multi_channel_microscopy_volume = mock_VariableDepthMultiChannelMicroscopyVolume(
        microscope=microscope,
        volumetric_imaging_space=volumetric_imaging_space,
        excitation_light_paths=excitation_light_paths_used_by_volume,
        emission_light_paths=emission_light_paths_used_by_volume,
    )
    assert (
        variable_depth_multi_channel_microscopy_volume.description
        == "A mock instance of a VariableDepthMultiChannelMicroscopyVolume type to be used for rapid testing."
    )


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
