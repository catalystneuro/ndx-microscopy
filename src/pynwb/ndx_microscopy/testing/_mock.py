import warnings
from typing import Optional, Tuple

import numpy as np
from pynwb.testing.mock.utils import name_generator

import ndx_microscopy


def mock_Microscopy(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a Microscopy type to be used for rapid testing.",
) -> ndx_microscopy.Microscopy:
    microscopy = ndx_microscopy.Microscopy(
        name=name or name_generator("Microscopy"),
        description=description,
    )
    return microscopy


def mock_MicroscopyTable(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a Microscopy Table type to be used for rapid testing.",
) -> ndx_microscopy.MicroscopyTable:
    microscopy_table = ndx_microscopy.MicroscopyTable(
        name=name or name_generator("MicroscopyTable"),
        description=description,
    )
    return microscopy_table


def mock_PlanarImagingSpace(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a PlanarImagingSpace type to be used for rapid testing.",
    origin_coordinates: Tuple[float, float, float] = (-1.2, -0.6, -2),
    grid_spacing: Tuple[float, float, float] = (0.2, 0.2),
    location: str = "The location targeted by the mock imaging space.",
    reference_frame: str = "The reference frame of the mock planar imaging space.",
) -> ndx_microscopy.PlanarImagingSpace:
    planar_imaging_space = ndx_microscopy.PlanarImagingSpace(
        name=name or name_generator("PlanarImagingSpace"),
        description=description,
        origin_coordinates=origin_coordinates,
        grid_spacing=grid_spacing,
        location=location,
        reference_frame=reference_frame,
    )
    return planar_imaging_space


def mock_VolumetricImagingSpace(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a VolumetricImagingSpace type to be used for rapid testing.",
    origin_coordinates: Tuple[float, float, float] = (-1.2, -0.6, -2),
    grid_spacing: Tuple[float, float, float] = (0.2, 0.2, 0.5),
    location: str = "The location targeted by the mock imaging space.",
    reference_frame: str = "The reference frame of the mock volumetric imaging space.",
) -> ndx_microscopy.VolumetricImagingSpace:
    volumetric_imaging_space = ndx_microscopy.VolumetricImagingSpace(
        name=name or name_generator("VolumetricImagingSpace"),
        description=description,
        origin_coordinates=origin_coordinates,
        grid_spacing=grid_spacing,
        location=location,
        reference_frame=reference_frame,
    )
    return volumetric_imaging_space


def mock_PlanarMicroscopySeries(
    *,
    name: Optional[str] = None,
    description: str = "This is a mock instance of a PlanarMicroscopySeries type to be used for rapid testing.",
    microscopy_table_region: list = [0],
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
        microscopy_table_region = microscopy_table_region,
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
    name: Optional[str] = None,
    description: str = "This is a mock instance of a PlanarMicroscopySeries type to be used for rapid testing.",
    microscopy_table_region: list = [0],
    data: Optional[np.ndarray] = None,
    depth_per_frame_in_mm: Optional[np.ndarray] = None,
    unit: str = "a.u.",
    conversion: float = 1.0,
    offset: float = 0.0,
    starting_time: Optional[float] = None,
    rate: Optional[float] = None,
    timestamps: Optional[np.ndarray] = None,
) -> ndx_microscopy.VariableDepthMicroscopySeries:
    series_name = name or name_generator("VariableDepthMicroscopySeries")
    series_data = data if data is not None else np.ones(shape=(15, 5, 5))

    series_depth_per_frame_in_mm = (
        depth_per_frame_in_mm
        if depth_per_frame_in_mm is not None
        else np.linspace(start=0.0, stop=1.0, num=series_data.shape[0])
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
        microscopy_table_region = microscopy_table_region,
        data=series_data,
        depth_per_frame_in_mm=series_depth_per_frame_in_mm,
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
    name: Optional[str] = None,
    description: str = "This is a mock instance of a VolumetricMicroscopySeries type to be used for rapid testing.",
    microscopy_table_region: list = [0],
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
        microscopy_table_region = microscopy_table_region,
        data=series_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )
    return volumetric_microscopy_series
