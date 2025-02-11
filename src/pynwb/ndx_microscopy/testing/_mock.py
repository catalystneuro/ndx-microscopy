import warnings
from typing import Iterable, List, Optional, Tuple

import numpy as np
import pynwb.base
from ndx_ophys_devices import ExcitationSource, Indicator, OpticalFilter, Photodetector, DichroicMirror
from ndx_ophys_devices.testing import (
    mock_ExcitationSource,
    mock_Indicator,
    mock_OpticalFilter,
    mock_Photodetector,
    mock_DichroicMirror,
)
from pynwb.testing.mock.utils import name_generator

import ndx_microscopy


def mock_Microscope(
    *,
    name: Optional[str] = None,
    description: str = "A mock instance of a Microscope type to be used for rapid testing.",
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


def mock_ExcitationLightPath(
    *,
    name: Optional[str] = None,
    description: str = None,
    excitation_wavelength_in_nm: float = 500.0,
    excitation_mode: str = "two-photon",
    excitation_source: ExcitationSource = None,
    excitation_filter: OpticalFilter = None,
    dichroic_mirror: DichroicMirror = None,
) -> ndx_microscopy.ExcitationLightPath:
    excitation_light_path = ndx_microscopy.ExcitationLightPath(
        name=name or name_generator("ExcitationLightPath"),
        description=description or "A mock instance of a ExcitationLightPath type to be used for rapid testing.",
        excitation_wavelength_in_nm=excitation_wavelength_in_nm,
        excitation_mode=excitation_mode,
        excitation_source=excitation_source or mock_ExcitationSource(),
        excitation_filter=excitation_filter or mock_OpticalFilter(),
        dichroic_mirror=dichroic_mirror or mock_DichroicMirror(),
    )
    return excitation_light_path


def mock_EmissionLightPath(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    indicator: Indicator = None,
    photodetector: Photodetector = None,
    emission_filter: OpticalFilter = None,
    emission_wavelength_in_nm: float = 520.0,
    dichroic_mirror: DichroicMirror = None,
) -> ndx_microscopy.EmissionLightPath:
    emission_light_path = ndx_microscopy.EmissionLightPath(
        name=name or name_generator("EmissionLightPath"),
        description=description or "A mock instance of a EmissionLightPath type to be used for rapid testing.",
        indicator=indicator or mock_Indicator(),
        photodetector=photodetector or mock_Photodetector(),
        emission_filter=emission_filter or mock_OpticalFilter(),
        emission_wavelength_in_nm=emission_wavelength_in_nm,
        dichroic_mirror=dichroic_mirror or mock_DichroicMirror(),
    )
    return emission_light_path


def mock_PlanarImagingSpace(
    *,
    name: Optional[str] = None,
    description: str = "A mock instance of a PlanarImagingSpace type to be used for rapid testing.",
    origin_coordinates: Tuple[float, float, float] = (-1.2, -0.6, -2),
    grid_spacing_in_um: Tuple[float, float, float] = (20, 20),
    location: str = "The location targeted by the mock imaging space.",
    reference_frame: str = "The reference frame of the mock planar imaging space.",
) -> ndx_microscopy.PlanarImagingSpace:
    planar_imaging_space = ndx_microscopy.PlanarImagingSpace(
        name=name or name_generator("PlanarImagingSpace"),
        description=description,
        origin_coordinates=origin_coordinates,
        grid_spacing_in_um=grid_spacing_in_um,
        location=location,
        reference_frame=reference_frame,
    )
    return planar_imaging_space


def mock_VolumetricImagingSpace(
    *,
    name: Optional[str] = None,
    description: str = "A mock instance of a VolumetricImagingSpace type to be used for rapid testing.",
    origin_coordinates: Tuple[float, float, float] = (-1.2, -0.6, -2),
    grid_spacing_in_um: Tuple[float, float, float] = (20, 20, 50),
    location: str = "The location targeted by the mock imaging space.",
    reference_frame: str = "The reference frame of the mock volumetric imaging space.",
) -> ndx_microscopy.VolumetricImagingSpace:
    volumetric_imaging_space = ndx_microscopy.VolumetricImagingSpace(
        name=name or name_generator("VolumetricImagingSpace"),
        description=description,
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
    imaging_space = mock_PlanarImagingSpace()
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
    description: str = "A mock instance of a MicroscopyPlaneSegmentation type to be used for rapid testing.",
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
    excitation_light_path: ndx_microscopy.ExcitationLightPath,
    planar_imaging_space: ndx_microscopy.PlanarImagingSpace,
    emission_light_path: ndx_microscopy.EmissionLightPath,
    name: Optional[str] = None,
    description: str = "A mock instance of a PlanarMicroscopySeries type to be used for rapid testing.",
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
        excitation_light_path=excitation_light_path,
        planar_imaging_space=planar_imaging_space,
        emission_light_path=emission_light_path,
        data=series_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )
    return planar_microscopy_series


def mock_MultiPlaneMicroscopyContainer(
    *,
    planar_microscopy_series: List[ndx_microscopy.PlanarMicroscopySeries],
    name: Optional[str] = None,
) -> ndx_microscopy.MultiPlaneMicroscopyContainer:
    container_name = name or name_generator("MultiPlaneMicroscopyContainer")

    multi_plane_microscopy_container = ndx_microscopy.MultiPlaneMicroscopyContainer(
        name=container_name, planar_microscopy_series=planar_microscopy_series
    )

    return multi_plane_microscopy_container


def mock_VolumetricMicroscopySeries(
    *,
    microscope: ndx_microscopy.Microscope,
    excitation_light_path: ndx_microscopy.ExcitationLightPath,
    volumetric_imaging_space: ndx_microscopy.VolumetricImagingSpace,
    emission_light_path: ndx_microscopy.EmissionLightPath,
    name: Optional[str] = None,
    description: str = "A mock instance of a VolumetricMicroscopySeries type to be used for rapid testing.",
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
        excitation_light_path=excitation_light_path,
        volumetric_imaging_space=volumetric_imaging_space,
        emission_light_path=emission_light_path,
        data=series_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )
    return volumetric_microscopy_series


def mock_MicroscopyResponseSeries(
    *,
    table_region: pynwb.core.DynamicTableRegion,
    name: Optional[str] = None,
    description: str = "A mock instance of a MicroscopyResponseSeries type to be used for rapid testing.",
    data: Optional[np.ndarray] = None,
    unit: str = "a.u.",
    conversion: float = 1.0,
    offset: float = 0.0,
    starting_time: Optional[float] = None,
    rate: Optional[float] = None,
    timestamps: Optional[np.ndarray] = None,
) -> ndx_microscopy.MicroscopyResponseSeries:
    series_name = name or name_generator("MicroscopyResponseSeries")

    number_of_frames = 100
    number_of_rois = len(table_region.data)
    series_data = data if data is not None else np.ones(shape=(number_of_frames, number_of_rois))

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

    microscopy_response_series = ndx_microscopy.MicroscopyResponseSeries(
        name=series_name,
        description=description,
        table_region=table_region,
        data=series_data,
        unit=unit,
        conversion=conversion,
        offset=offset,
        starting_time=series_starting_time,
        rate=series_rate,
        timestamps=series_timestamps,
    )

    return microscopy_response_series


def mock_MicroscopyResponseSeriesContainer(
    *,
    microscopy_response_series: List[ndx_microscopy.MicroscopyResponseSeries],
    name: Optional[str] = None,
) -> ndx_microscopy.MicroscopyResponseSeriesContainer:
    container_name = name or name_generator("MicroscopyResponseSeriesContainer")

    microscopy_response_series_container = ndx_microscopy.MicroscopyResponseSeriesContainer(
        name=container_name, microscopy_response_series=microscopy_response_series
    )

    return microscopy_response_series_container
