import warnings
from typing import Iterable, List, Optional, Tuple

import numpy as np
import pynwb.base
from pynwb.testing.mock.utils import name_generator

import ndx_microscopy


def mock_Microscope(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a Microscope type to be used for rapid testing.",
    manufacturer: str = "A fake manufacturer of the mock microscope.",
    model: str = "A fake model of the mock microscope.",
) -> ndx_microscopy.Microscope:
    microscope = ndx_microscopy.Microscope(
        name=name or name_generator("Microscope"),
        description=description,
        manufacturer=manufacturer,
        model=model,
    )
    return microscope


def mock_MicroscopyLightSource(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a MicroscopyLightSource type to be used for rapid testing.",
    manufacturer: str = "A fake manufacturer of the mock light source.",
    model: str = "A fake model of the mock light source.",
    filter_description: str = "A description about the fake filter used by the mock light source.",
    excitation_wavelength_in_nm: float = 500.0,
    peak_power_in_W: float = 0.7,
    peak_pulse_energy_in_J: float = 0.7,
    intensity_in_W_per_m2: float = 0.005,
    exposure_time_in_s: float = 2.51e-13,
    pulse_rate_in_Hz: float = 2.0e6,
) -> ndx_microscopy.MicroscopyLightSource:
    light_source = ndx_microscopy.MicroscopyLightSource(
        name=name or name_generator("MicroscopyLightSource"),
        description=description,
        manufacturer=manufacturer,
        model=model,
        filter_description=filter_description,
        excitation_wavelength_in_nm=excitation_wavelength_in_nm,
        peak_power_in_W=peak_power_in_W,
        peak_pulse_energy_in_J=peak_pulse_energy_in_J,
        intensity_in_W_per_m2=intensity_in_W_per_m2,
        exposure_time_in_s=exposure_time_in_s,
        pulse_rate_in_Hz=pulse_rate_in_Hz,
    )
    return light_source


def mock_MicroscopyOpticalChannel(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a MicroscopyOpticalChannel type to be used for rapid testing.",
    indicator: str = "The indicator targeted by the mock optical channel.",
    filter_description: str = "A description about the fake filter used by the mock optical channel.",
    emission_wavelength_in_nm: float = 450.0,
) -> ndx_microscopy.MicroscopyOpticalChannel:
    optical_channel = ndx_microscopy.MicroscopyOpticalChannel(
        name=name or name_generator("MicroscopyOpticalChannel"),
        description=description,
        indicator=indicator,
        filter_description=filter_description,
        emission_wavelength_in_nm=emission_wavelength_in_nm,
    )
    return optical_channel


def mock_PlanarImagingSpace(
    *,
    microscope: ndx_microscopy.Microscope,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a PlanarImagingSpace type to be used for rapid testing.",
    origin_coordinates: Tuple[float, float, float] = (-1.2, -0.6, -2),
    grid_spacing_in_um: Tuple[float, float, float] = (20, 20),
    location: str = "The location targeted by the mock imaging space.",
    reference_frame: str = "The reference frame of the mock planar imaging space.",
) -> ndx_microscopy.PlanarImagingSpace:
    planar_imaging_space = ndx_microscopy.PlanarImagingSpace(
        name=name or name_generator("PlanarImagingSpace"),
        description=description,
        microscope=microscope,
        origin_coordinates=origin_coordinates,
        grid_spacing_in_um=grid_spacing_in_um,
        location=location,
        reference_frame=reference_frame,
    )
    return planar_imaging_space


def mock_VolumetricImagingSpace(
    *,
    microscope: ndx_microscopy.Microscope,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a VolumetricImagingSpace type to be used for rapid testing.",
    origin_coordinates: Tuple[float, float, float] = (-1.2, -0.6, -2),
    grid_spacing_in_um: Tuple[float, float, float] = (20, 20, 50),
    location: str = "The location targeted by the mock imaging space.",
    reference_frame: str = "The reference frame of the mock volumetric imaging space.",
) -> ndx_microscopy.VolumetricImagingSpace:
    volumetric_imaging_space = ndx_microscopy.VolumetricImagingSpace(
        name=name or name_generator("VolumetricImagingSpace"),
        description=description,
        microscope=microscope,
        origin_coordinates=origin_coordinates,
        grid_spacing_in_um=grid_spacing_in_um,
        location=location,
        reference_frame=reference_frame,
    )
    return volumetric_imaging_space


def mock_MicroscopySegmentations(
    *,
    name: Optional[str] = None,
    microscopy_plane_segmentations: Optional[Iterable[ndx_microscopy.MicroscopyPlaneSegmentation]] = None,
) -> ndx_microscopy.MicroscopySegmentations:
    name = name or name_generator("MicroscopySegmentations")

    microscope = mock_Microscope()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    microscopy_plane_segmentations = microscopy_plane_segmentations or [
        mock_MicroscopyPlaneSegmentation(imaging_space=imaging_space)
    ]

    segmentations = ndx_microscopy.MicroscopySegmentations(
        name=name, microscopy_plane_segmentations=microscopy_plane_segmentations
    )

    return segmentations


def mock_MicroscopyPlaneSegmentation(
    *,
    imaging_space: ndx_microscopy.ImagingSpace,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing.",
    number_of_rois: int = 5,
    image_shape: Tuple[int, int] = (10, 10),
) -> ndx_microscopy.MicroscopyPlaneSegmentation:
    name = name or name_generator("MicroscopyPlaneSegmentation")

    plane_segmentation = ndx_microscopy.MicroscopyPlaneSegmentation(
        name=name, description=description, imaging_space=imaging_space, id=list(range(number_of_rois))
    )
    # plane_segmentation.add_column(name="id", description="", data=list(range(number_of_rois)))

    image_masks = list()
    for _ in range(number_of_rois):
        image_masks.append(np.zeros(image_shape, dtype=bool))
    plane_segmentation.add_column(name="image_mask", description="", data=image_masks)

    return plane_segmentation


def mock_PlanarMicroscopySeries(
    *,
    microscope: ndx_microscopy.Microscope,
    light_source: ndx_microscopy.MicroscopyLightSource,
    imaging_space: ndx_microscopy.PlanarImagingSpace,
    optical_channel: ndx_microscopy.MicroscopyOpticalChannel,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a PlanarMicroscopySeries type to be used for rapid testing.",
    data: Optional[np.ndarray] = None,
    unit: str = "a.u.",
    conversion: float = 1.0,
    offset: float = 0.0,
    starting_time: Optional[float] = None,
    rate: Optional[float] = None,
    timestamps: Optional[np.ndarray] = None,
) -> ndx_microscopy.PlanarMicroscopySeries:
    series_name = name or name_generator("PlanarMicroscopySeries")
    series_data = data if data is not None else np.ones(shape=(15, 5, 5))

    if timestamps is None:
        series_starting_time = starting_time or 0.0
        series_rate = rate or 10.0
        series_timestamps = None
    else:
        if starting_time is not None or rate is not None:
            warnings.warn(
                message=(
                    "Timestamps were provided in addition to either rate or starting_time! "
                    "Please specify only timestamps, or both starting_time and rate. Timestamps will take precedence."
                ),
                stacklevel=2,
            )

        series_starting_time = None
        series_rate = None
        series_timestamps = timestamps

    planar_microscopy_series = ndx_microscopy.PlanarMicroscopySeries(
        name=series_name,
        description=description,
        microscope=microscope,
        light_source=light_source,
        imaging_space=imaging_space,
        optical_channel=optical_channel,
        data=series_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )
    return planar_microscopy_series


def mock_VariableDepthMicroscopySeries(
    *,
    microscope: ndx_microscopy.Microscope,
    light_source: ndx_microscopy.MicroscopyLightSource,
    imaging_space: ndx_microscopy.PlanarImagingSpace,
    optical_channel: ndx_microscopy.MicroscopyOpticalChannel,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a PlanarMicroscopySeries type to be used for rapid testing.",
    data: Optional[np.ndarray] = None,
    depth_per_frame_in_um: Optional[np.ndarray] = None,
    unit: str = "a.u.",
    conversion: float = 1.0,
    offset: float = 0.0,
    starting_time: Optional[float] = None,
    rate: Optional[float] = None,
    timestamps: Optional[np.ndarray] = None,
) -> ndx_microscopy.VariableDepthMicroscopySeries:
    series_name = name or name_generator("VariableDepthMicroscopySeries")
    series_data = data if data is not None else np.ones(shape=(15, 5, 5))
    depth_per_frame_in_um = (
        depth_per_frame_in_um
        if depth_per_frame_in_um is not None
        else np.linspace(start=0.0, stop=30.0, num=series_data.shape[0])
    )

    if timestamps is None:
        series_starting_time = starting_time or 0.0
        series_rate = rate or 10.0
        series_timestamps = None
    else:
        if starting_time is not None or rate is not None:
            warnings.warn(
                message=(
                    "Timestamps were provided in addition to either rate or starting_time! "
                    "Please specify only timestamps, or both starting_time and rate. Timestamps will take precedence."
                ),
                stacklevel=2,
            )

        series_starting_time = None
        series_rate = None
        series_timestamps = timestamps

    variable_depth_microscopy_series = ndx_microscopy.VariableDepthMicroscopySeries(
        name=series_name,
        description=description,
        microscope=microscope,
        light_source=light_source,
        imaging_space=imaging_space,
        optical_channel=optical_channel,
        data=series_data,
        depth_per_frame_in_um=depth_per_frame_in_um,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )
    return variable_depth_microscopy_series


def mock_VolumetricMicroscopySeries(
    *,
    microscope: ndx_microscopy.Microscope,
    light_source: ndx_microscopy.MicroscopyLightSource,
    imaging_space: ndx_microscopy.VolumetricImagingSpace,
    optical_channel: ndx_microscopy.MicroscopyOpticalChannel,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a VolumetricMicroscopySeries type to be used for rapid testing.",
    data: Optional[np.ndarray] = None,
    unit: str = "a.u.",
    conversion: float = 1.0,
    offset: float = 0.0,
    starting_time: Optional[float] = None,
    rate: Optional[float] = None,
    timestamps: Optional[np.ndarray] = None,
) -> ndx_microscopy.VolumetricMicroscopySeries:
    series_name = name or name_generator("VolumetricMicroscopySeries")
    series_data = data if data is not None else np.ones(shape=(5, 5, 5, 3))

    if timestamps is None:
        series_starting_time = starting_time or 0.0
        series_rate = rate or 10.0
        series_timestamps = None
    else:
        if starting_time is not None or rate is not None:
            warnings.warn(
                message=(
                    "Timestamps were provided in addition to either rate or starting_time! "
                    "Please specify only timestamps, or both starting_time and rate. Timestamps will take precedence."
                ),
                stacklevel=2,
            )

        series_starting_time = None
        series_rate = None
        series_timestamps = timestamps

    volumetric_microscopy_series = ndx_microscopy.VolumetricMicroscopySeries(
        name=series_name,
        description=description,
        microscope=microscope,
        light_source=light_source,
        imaging_space=imaging_space,
        optical_channel=optical_channel,
        data=series_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )
    return volumetric_microscopy_series


def mock_MultiChannelMicroscopyVolume(
    *,
    microscope: ndx_microscopy.Microscope,
    imaging_space: ndx_microscopy.VolumetricImagingSpace,
    light_sources: pynwb.base.VectorData,
    optical_channels: pynwb.base.VectorData,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a MultiChannelMicroscopyVolume type to be used for rapid testing.",
    data: Optional[np.ndarray] = None,
    unit: str = "n.a.",
    conversion: float = 1.0,
    offset: float = 0.0,
) -> ndx_microscopy.MultiChannelMicroscopyVolume:
    series_name = name or name_generator("MultiChannelMicroscopyVolume")
    imaging_data = data if data is not None else np.ones(shape=(10, 20, 7, 3))

    volumetric_microscopy_series = ndx_microscopy.MultiChannelMicroscopyVolume(
        name=series_name,
        description=description,
        microscope=microscope,
        imaging_space=imaging_space,
        light_sources=light_sources,
        optical_channels=optical_channels,
        data=imaging_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
    )
    return volumetric_microscopy_series


def mock_VariableDepthMultiChannelMicroscopyVolume(
    *,
    microscope: ndx_microscopy.Microscope,
    imaging_space: ndx_microscopy.VolumetricImagingSpace,
    light_sources: pynwb.base.VectorData,
    optical_channels: pynwb.base.VectorData,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a MultiChannelMicroscopyVolume type to be used for rapid testing.",
    data: Optional[np.ndarray] = None,
    depth_per_frame_in_um: Optional[np.ndarray] = None,
    unit: str = "n.a.",
    conversion: float = 1.0,
    offset: float = 0.0,
) -> ndx_microscopy.VariableDepthMultiChannelMicroscopyVolume:
    series_name = name or name_generator("MultiChannelMicroscopyVolume")

    series_data = data if data is not None else np.ones(shape=(15, 5, 5))
    volume_depth_per_frame_in_um = (
        depth_per_frame_in_um
        if depth_per_frame_in_um is not None
        else np.linspace(start=0.0, stop=30.0, num=series_data.shape[0])
    )

    imaging_data = data if data is not None else np.ones(shape=(10, 20, 7, 3))
    variable_depth_multi_channel_microscopy_volume = ndx_microscopy.VariableDepthMultiChannelMicroscopyVolume(
        name=series_name,
        description=description,
        microscope=microscope,
        imaging_space=imaging_space,
        light_sources=light_sources,
        optical_channels=optical_channels,
        data=imaging_data,
        depth_per_frame_in_um=volume_depth_per_frame_in_um,
        unit=unit,
        conversion=conversion,
        offset=offset,
    )
    return variable_depth_multi_channel_microscopy_volume
