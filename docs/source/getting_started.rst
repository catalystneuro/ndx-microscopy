.. _getting_started:

***************
Getting Started
***************

Prerequisites
=============

- Python 3.10 or later
- PyNWB 3.1 or later
- ndx-ophys-devices 0.4, which provides the optical components and molecular tools

Installation
============

.. code-block:: bash

   pip install ndx-microscopy

This installs PyNWB and ndx-ophys-devices as dependencies.

Basic Concepts
==============

Device Components
-----------------

- ``MicroscopeModel``: the microscope model, with manufacturer and model number
- ``Microscope``: the microscope instance, with the imaging technique (e.g., resonant scanning, light sheet)
- ``MicroscopyRig``: links the microscope and the optical components used for an acquisition
- Optical components from ndx-ophys-devices, each with a model and an instance type:

  - ``ExcitationSource`` and ``PulsedExcitationSource`` (LEDs, lasers)
  - ``BandOpticalFilter`` and ``EdgeOpticalFilter``
  - ``DichroicMirror``
  - ``Photodetector`` (PMTs, cameras)
  - ``ObjectiveLens``

- ``Indicator``, ``ViralVector`` and ``ViralVectorInjection`` from ndx-ophys-devices describe the molecular tools
- ``MicroscopyExperimentMetadata`` holds the rigs and molecular tools in ``nwbfile.lab_meta_data``

Illumination Patterns
---------------------

- ``IlluminationPattern``: base class for patterns not covered below
- ``LineScan``: point-scanning systems that build each frame from scanned lines, e.g., two-photon raster scanning
- ``PlaneAcquisition``: the whole plane is illuminated at once, e.g., light sheet or camera-based widefield imaging
- ``RandomAccessScan``: targeted scanning of selected points, e.g., with acousto-optic deflectors

Imaging Spaces
--------------

- ``PlanarImagingSpace``: a single plane
- ``VolumetricImagingSpace``: a volume
- Each space records the anatomical target, the pixel or voxel size and the dimensions, listed x first
- Each space contains the illumination pattern used to acquire it

Imaging Data
------------

- ``PlanarMicroscopySeries``: planar data over time, shaped (frames, height, width)
- ``VolumetricMicroscopySeries``: volumetric data over time, shaped (frames, depths, height, width)
- ``PlanarMicroscopyStaticImage`` and ``VolumetricMicroscopyStaticImage``: single images, e.g., an anatomical reference
- ``MultiPlaneMicroscopyContainer``: series or static images acquired at several depths
- ``MultiChannelMicroscopyContainer``: series, static images or multi-plane containers acquired in several channels

Quick Start Example
===================

This example writes a two-photon calcium imaging session with one imaging plane.

.. code-block:: python

    from datetime import datetime, timezone
    from uuid import uuid4

    import numpy as np
    from pynwb import NWBHDF5IO, NWBFile

    from ndx_microscopy import (
        LineScan,
        Microscope,
        MicroscopeModel,
        MicroscopyChannel,
        MicroscopyExperimentMetadata,
        MicroscopyRig,
        PlanarImagingSpace,
        PlanarMicroscopySeries,
    )
    from ndx_ophys_devices import (
        BandOpticalFilter,
        BandOpticalFilterModel,
        DichroicMirror,
        DichroicMirrorModel,
        ExcitationSourceModel,
        Indicator,
        ObjectiveLens,
        ObjectiveLensModel,
        Photodetector,
        PhotodetectorModel,
        PulsedExcitationSource,
    )

    nwbfile = NWBFile(
        session_description="Two-photon calcium imaging in mouse V1",
        identifier=str(uuid4()),
        session_start_time=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc),
    )

    # Device models describe the catalog specifications
    microscope_model = MicroscopeModel(
        name="microscope_model",
        description="Two-photon microscope with resonant-galvo scanning",
        manufacturer="Thorlabs",
        model_number="Bergamo II",
    )
    laser_model = ExcitationSourceModel(
        name="laser_model",
        manufacturer="Coherent",
        model_number="Chameleon Ultra II",
        source_type="laser",
        excitation_mode="two-photon",
        wavelength_range_in_nm=[680.0, 1080.0],
    )
    dichroic_mirror_model = DichroicMirrorModel(
        name="dichroic_mirror_model",
        manufacturer="Semrock",
        model_number="FF757-Di01",
        cut_on_wavelength_in_nm=757.0,
    )
    emission_filter_model = BandOpticalFilterModel(
        name="emission_filter_model",
        manufacturer="Semrock",
        model_number="FF01-510/84",
        filter_type="Bandpass",
        center_wavelength_in_nm=510.0,
        bandwidth_in_nm=84.0,
    )
    photodetector_model = PhotodetectorModel(
        name="photodetector_model",
        manufacturer="Hamamatsu",
        model_number="H10770PA-40",
        detector_type="PMT",
        wavelength_range_in_nm=[300.0, 720.0],
    )
    objective_lens_model = ObjectiveLensModel(
        name="objective_lens_model",
        manufacturer="Nikon",
        model_number="N16XLWD-PF",
        numerical_aperture=0.8,
        magnification=16.0,
    )
    for device_model in (
        microscope_model,
        laser_model,
        dichroic_mirror_model,
        emission_filter_model,
        photodetector_model,
        objective_lens_model,
    ):
        nwbfile.add_device_model(device_model)

    # Device instances describe the devices used in this session
    microscope = Microscope(
        name="microscope",
        model=microscope_model,
        serial_number="2P-001",
        technique="resonant-galvo scanning",
    )
    laser = PulsedExcitationSource(
        name="laser",
        model=laser_model,
        power_in_W=0.05,  # average power at the sample
        pulse_rate_in_Hz=80.0e6,
        pulse_width_in_s=140.0e-15,
        peak_pulse_energy_in_J=0.05 / 80.0e6,  # average power / pulse rate
    )
    dichroic_mirror = DichroicMirror(name="dichroic_mirror", model=dichroic_mirror_model)
    emission_filter = BandOpticalFilter(name="emission_filter", model=emission_filter_model)
    photodetector = Photodetector(name="photodetector", model=photodetector_model)
    objective_lens = ObjectiveLens(name="objective_lens", model=objective_lens_model)
    for device in (microscope, laser, dichroic_mirror, emission_filter, photodetector, objective_lens):
        nwbfile.add_device(device)

    microscopy_rig = MicroscopyRig(
        name="microscopy_rig",
        description="Two-photon rig with a green emission path",
        microscope=microscope,
        excitation_source=laser,
        dichroic_mirror=dichroic_mirror,
        emission_filter=emission_filter,
        photodetector=photodetector,
        objective_lens=objective_lens,
    )

    indicator = Indicator(name="indicator", label="GCaMP6f", description="Genetically encoded calcium indicator")

    nwbfile.add_lab_meta_data(
        MicroscopyExperimentMetadata(microscopy_rigs=[microscopy_rig], indicators=[indicator])
    )

    microscopy_channel = MicroscopyChannel(
        name="green_channel",
        description="GCaMP6f emission",
        excitation_wavelength_in_nm=920.0,
        emission_wavelength_in_nm=510.0,
        indicator=indicator,
    )

    # A resonant scanner at about 8 kHz acquires 256 lines in about 1/30 s
    line_scan = LineScan(
        name="line_scan",
        description="Unidirectional raster scan with a resonant-galvo scanner",
        scan_direction="horizontal",
        line_rate_in_Hz=7910.0,
        dwell_time_in_s=0.25e-6,
    )

    planar_imaging_space = PlanarImagingSpace(
        name="planar_imaging_space",
        description="Field of view in layer 2/3 of V1",
        anatomical_target="Primary visual cortex, layer 2/3",
        pixel_size_in_um=[2.0, 2.0],  # (x, y)
        dimensions_in_pixels=[256, 256],  # (x, y)
        illumination_pattern=line_scan,
    )

    # Imaging data are shaped (frames, height, width)
    data = np.random.randint(0, 4096, size=(100, 256, 256), dtype=np.uint16)

    microscopy_series = PlanarMicroscopySeries(
        name="microscopy_series",
        description="Two-photon calcium imaging",
        microscopy_rig=microscopy_rig,
        microscopy_channel=microscopy_channel,
        planar_imaging_space=planar_imaging_space,
        data=data,
        unit="a.u.",
        rate=30.0,
        starting_time=0.0,
    )
    nwbfile.add_acquisition(microscopy_series)

    with NWBHDF5IO("microscopy_session.nwb", "w") as io:
        io.write(nwbfile)

Next Steps
==========

1. The :ref:`examples` section shows volumetric, multi-plane and multi-channel imaging, and ROI
   segmentation with response series.
2. The :ref:`user_guide` covers the components in more detail.
3. The :ref:`api` documents the Python classes.
4. The :ref:`format` section documents the specification.
