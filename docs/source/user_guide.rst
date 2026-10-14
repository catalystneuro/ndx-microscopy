.. _user_guide:

**********
User Guide
**********

This guide builds two example files step by step: a two-photon session in mouse primary visual cortex (V1),
and a one-photon miniscope session in hippocampal CA1 through a GRIN lens. The code blocks run in order.

Two-Photon Imaging Session
==========================

Setup
-----

.. code-block:: python

    from datetime import datetime, timezone
    from uuid import uuid4

    import numpy as np
    from pynwb import NWBHDF5IO, NWBFile
    from pynwb.image import RGBImage

    from ndx_microscopy import (
        IlluminationPattern,
        LineScan,
        Microscope,
        MicroscopeModel,
        MicroscopyChannel,
        MicroscopyExperimentMetadata,
        MicroscopyResponseSeries,
        MicroscopyResponseSeriesContainer,
        MicroscopyRig,
        MultiChannelMicroscopyContainer,
        MultiPlaneMicroscopyContainer,
        PlaneAcquisition,
        PlanarImagingSpace,
        PlanarMicroscopySeries,
        PlanarMicroscopyStaticImage,
        PlanarSegmentation,
        RandomAccessScan,
        SegmentationContainer,
        SummaryImage,
        VolumetricImagingSpace,
        VolumetricMicroscopySeries,
    )
    from ndx_ophys_devices import (
        BandOpticalFilter,
        BandOpticalFilterModel,
        DichroicMirror,
        DichroicMirrorModel,
        ExcitationSource,
        ExcitationSourceModel,
        Indicator,
        ObjectiveLens,
        ObjectiveLensModel,
        Photodetector,
        PhotodetectorModel,
        PulsedExcitationSource,
        StereotacticPosition,
        ViralVector,
        ViralVectorInjection,
    )

    nwbfile = NWBFile(
        session_description="Two-photon calcium imaging in mouse V1",
        identifier=str(uuid4()),
        session_start_time=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc),
    )

Devices and Rigs
----------------

Each device has a model, which holds the catalog specifications, and an instance, which holds the values
for this session. Models go in ``nwbfile.device_models`` and instances in ``nwbfile.devices``.

A ``MicroscopyRig`` links one microscope, one excitation source and one emission path (dichroic mirror,
emission filter and photodetector). When a microscope has several excitation sources or emission paths,
create one rig per combination and pass the same device objects to each rig. Here the green path images
GCaMP6f at 920 nm and the red path images tdTomato at 1040 nm; both rigs share the microscope, the laser,
the dichroic mirror and the objective.

.. code-block:: python

    microscope_model = MicroscopeModel(
        name="microscope_model",
        description="Two-photon microscope with resonant-galvo scanning",
        manufacturer="Thorlabs",
        model_number="Bergamo II",
    )
    laser_model = ExcitationSourceModel(
        name="laser_model",
        manufacturer="Coherent",
        model_number="Chameleon Discovery NX",
        source_type="laser",
        excitation_mode="two-photon",
        wavelength_range_in_nm=[660.0, 1320.0],
    )
    dichroic_mirror_model = DichroicMirrorModel(
        name="dichroic_mirror_model",
        manufacturer="Semrock",
        model_number="FF757-Di01",
        cut_on_wavelength_in_nm=757.0,
    )
    green_filter_model = BandOpticalFilterModel(
        name="green_filter_model",
        manufacturer="Semrock",
        model_number="FF01-510/84",
        filter_type="Bandpass",
        center_wavelength_in_nm=510.0,
        bandwidth_in_nm=84.0,
    )
    red_filter_model = BandOpticalFilterModel(
        name="red_filter_model",
        manufacturer="Semrock",
        model_number="FF01-607/70",
        filter_type="Bandpass",
        center_wavelength_in_nm=607.0,
        bandwidth_in_nm=70.0,
    )
    pmt_model = PhotodetectorModel(
        name="pmt_model",
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
        green_filter_model,
        red_filter_model,
        pmt_model,
        objective_lens_model,
    ):
        nwbfile.add_device_model(device_model)

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
        pulse_width_in_s=100.0e-15,
        peak_pulse_energy_in_J=0.05 / 80.0e6,  # average power / pulse rate
    )
    dichroic_mirror = DichroicMirror(name="dichroic_mirror", model=dichroic_mirror_model)
    green_filter = BandOpticalFilter(name="green_filter", model=green_filter_model)
    red_filter = BandOpticalFilter(name="red_filter", model=red_filter_model)
    green_pmt = Photodetector(name="green_pmt", model=pmt_model, serial_number="PMT-001")
    red_pmt = Photodetector(name="red_pmt", model=pmt_model, serial_number="PMT-002")
    objective_lens = ObjectiveLens(name="objective_lens", model=objective_lens_model)
    for device in (microscope, laser, dichroic_mirror, green_filter, red_filter, green_pmt, red_pmt, objective_lens):
        nwbfile.add_device(device)

    green_rig = MicroscopyRig(
        name="green_rig",
        description="920 nm excitation, green emission path",
        microscope=microscope,
        excitation_source=laser,
        dichroic_mirror=dichroic_mirror,
        emission_filter=green_filter,
        photodetector=green_pmt,
        objective_lens=objective_lens,
        # Optional image of the optical path; replace the placeholder with your diagram or photograph
        optical_path_scheme=RGBImage(
            name="optical_path_scheme",
            data=np.zeros((60, 80, 3), dtype=np.uint8),
            description="Diagram of the two-photon optical path",
        ),
    )
    red_rig = MicroscopyRig(
        name="red_rig",
        description="1040 nm excitation, red emission path",
        microscope=microscope,
        excitation_source=laser,
        dichroic_mirror=dichroic_mirror,
        emission_filter=red_filter,
        photodetector=red_pmt,
        objective_lens=objective_lens,
    )

Molecular Tools and Experiment Metadata
---------------------------------------

Indicators, viral vectors and injections come from ndx-ophys-devices. Stereotactic coordinates use the RAS
convention: x is right, y is anterior and z is superior, so ventral targets have negative z.
``MicroscopyExperimentMetadata`` holds the rigs and the molecular tools, and is added with
``nwbfile.add_lab_meta_data``.

.. code-block:: python

    gcamp_vector = ViralVector(
        name="gcamp_vector",
        description="AAV for pan-neuronal GCaMP6f expression",
        construct_name="AAV1-Syn-GCaMP6f-WPRE-SV40",
        manufacturer="Addgene",
        titer_in_vg_per_ml=1.0e13,
    )
    gcamp_injection = ViralVectorInjection(
        name="gcamp_injection",
        description="Injection into left V1",
        volume_in_uL=0.1,
        viral_vector=gcamp_vector,
        viral_injection_coordinates=StereotacticPosition(
            name="viral_injection_coordinates",
            anatomical_target="Primary visual cortex",
            origin="bregma (AP, ML); brain surface (DV)",
            orientation="RAS",
            x_in_mm=-2.5,  # 2.5 mm left of the midline
            y_in_mm=-3.8,  # 3.8 mm posterior to bregma
            z_in_mm=-0.3,  # 0.3 mm below the brain surface
        ),
    )
    gcamp_indicator = Indicator(
        name="gcamp_indicator",
        description="Genetically encoded calcium indicator",
        label="GCaMP6f",
        viral_vector_injection=gcamp_injection,
    )
    tdtomato_indicator = Indicator(
        name="tdtomato_indicator",
        description="Cre-dependent tdTomato reporter (Ai14) in inhibitory neurons",
        label="tdTomato",
    )

    nwbfile.add_lab_meta_data(
        MicroscopyExperimentMetadata(
            microscopy_rigs=[green_rig, red_rig],
            viral_vectors=[gcamp_vector],
            viral_vector_injections=[gcamp_injection],
            indicators=[gcamp_indicator, tdtomato_indicator],
        )
    )

When a file also uses ndx-optogenetics or ndx-fiber-photometry, store each viral vector, injection and
indicator once, in the metadata container of the main experiment, and pass the same Python object wherever
else it is needed. PyNWB writes the object once and links to it from the other locations.

Channels
--------

A ``MicroscopyChannel`` records the excitation and emission wavelengths and links the indicator. For
label-free channels, such as second-harmonic generation, intrinsic signal, autofluorescence or reflectance
imaging, link an ``Indicator`` whose label names the source of contrast, e.g.,
``Indicator(name="nadh_autofluorescence", label="NAD(P)H autofluorescence")``.

.. code-block:: python

    green_channel = MicroscopyChannel(
        name="green_channel",
        description="GCaMP6f emission",
        excitation_wavelength_in_nm=920.0,
        emission_wavelength_in_nm=510.0,
        indicator=gcamp_indicator,
    )
    red_channel = MicroscopyChannel(
        name="red_channel",
        description="tdTomato emission",
        excitation_wavelength_in_nm=1040.0,
        emission_wavelength_in_nm=581.0,
        indicator=tdtomato_indicator,
    )

Illumination Patterns
---------------------

The illumination pattern describes how the sample is illuminated or scanned. Each imaging space contains one.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Acquisition
     - Pattern
     - Typical parameters
   * - Point scanning that builds each frame from lines (two-photon, confocal)
     - ``LineScan``
     - ``line_rate_in_Hz``: about 8000 for a resonant scanner, about 1000 for galvo-galvo;
       ``dwell_time_in_s``: below 1e-6 for resonant, a few 1e-6 for galvo-galvo
   * - Camera-based full-field imaging (widefield, miniscope)
     - ``PlaneAcquisition``
     - ``plane_rate_in_Hz``: the camera frame rate
   * - Light sheet
     - ``PlaneAcquisition``
     - ``illumination_angle_in_degrees``, ``plane_rate_in_Hz``, and the sheet profile in
       ``point_spread_function``
   * - Targeted point scanning (acousto-optic deflectors)
     - ``RandomAccessScan``
     - ``max_scan_points``, ``dwell_time_in_s``, ``scanning_pattern``
   * - Anything else (e.g., holographic or spiral scanning)
     - ``IlluminationPattern``
     - a ``description`` of the method

.. code-block:: python

    # 256 lines at about 8 kHz give about 30 frames per second
    line_scan = LineScan(
        name="line_scan",
        description="Unidirectional raster scan with a resonant-galvo scanner",
        scan_direction="horizontal",
        line_rate_in_Hz=7910.0,
        dwell_time_in_s=0.25e-6,
    )

    # Other patterns, shown for reference
    light_sheet = PlaneAcquisition(
        name="light_sheet",
        description="Single-sided light sheet",
        point_spread_function="4 um ± 0.5 um",
        illumination_angle_in_degrees=90.0,
        plane_rate_in_Hz=50.0,
    )
    random_access_scan = RandomAccessScan(
        name="random_access_scan",
        description="Acousto-optic deflector scanning of selected somata",
        max_scan_points=500,
        dwell_time_in_s=10.0e-6,
        scanning_pattern="one point per soma, visited in a fixed order",
    )
    holographic_pattern = IlluminationPattern(
        name="holographic_pattern",
        description="Spatial light modulator patterns targeting selected neurons",
    )

Imaging Spaces
--------------

``PlanarImagingSpace`` and ``VolumetricImagingSpace`` describe the imaged region. Sizes are listed x first:
``pixel_size_in_um`` and ``dimensions_in_pixels`` are (x, y), while the data are (height, width).

The optional ``fov_center_coordinates`` is a ``StereotacticPosition`` for the center of the field of view (for
a volume, the center of the volume); its z coordinate gives the imaging depth. Localization of the field of
view against an atlas, such as the coordinates of each pixel, will be handled by the
`ndx-anatomical-localization <https://github.com/catalystneuro/ndx-anatomical-localization>`_ extension.

.. code-block:: python

    planar_imaging_space = PlanarImagingSpace(
        name="planar_imaging_space",
        description="Field of view 200 um below the pia",
        anatomical_target="Primary visual cortex, layer 2/3",
        pixel_size_in_um=[2.0, 2.0],  # (x, y)
        dimensions_in_pixels=[256, 256],  # (x, y)
        illumination_pattern=line_scan,
        fov_center_coordinates=StereotacticPosition(
            name="fov_center_coordinates",
            anatomical_target="Primary visual cortex, layer 2/3",
            origin="bregma (AP, ML); brain surface (DV)",
            orientation="RAS",
            x_in_mm=-2.5,
            y_in_mm=-3.8,
            z_in_mm=-0.2,  # 200 um below the brain surface
        ),
    )

Planar Imaging Series
---------------------

.. code-block:: python

    data = np.random.randint(0, 4096, size=(100, 256, 256), dtype=np.uint16)  # (frames, height, width)

    green_series = PlanarMicroscopySeries(
        name="green_series",
        description="GCaMP6f imaging during drifting gratings",
        microscopy_rig=green_rig,
        microscopy_channel=green_channel,
        planar_imaging_space=planar_imaging_space,
        data=data,
        unit="a.u.",
        rate=30.0,
        starting_time=0.0,
    )
    nwbfile.add_acquisition(green_series)

Sharing Channels and Imaging Spaces
-----------------------------------

The rig is linked from each series. The channel and the imaging space are stored inside the first series
that uses them; pass the same objects to other series, static images or segmentations and PyNWB writes links
to them. Here a second recording of the same field of view reuses both.

.. code-block:: python

    spontaneous_series = PlanarMicroscopySeries(
        name="spontaneous_series",
        description="GCaMP6f imaging in darkness, same field of view",
        microscopy_rig=green_rig,
        microscopy_channel=green_channel,  # same channel object
        planar_imaging_space=planar_imaging_space,  # same imaging space object
        data=np.random.randint(0, 4096, size=(100, 256, 256), dtype=np.uint16),
        unit="a.u.",
        rate=30.0,
        starting_time=600.0,
    )
    nwbfile.add_acquisition(spontaneous_series)

Volumetric Imaging
------------------

Volumetric data are shaped (frames, depths, height, width), the TZYX convention. ``voxel_size_in_um`` and
``dimensions_in_voxels`` are (x, y, z).

.. code-block:: python

    volumetric_imaging_space = VolumetricImagingSpace(
        name="volumetric_imaging_space",
        description="Volume from 100 to 300 um below the pia, 10 planes set with a piezo objective scanner",
        anatomical_target="Primary visual cortex, layers 2/3 and 4",
        voxel_size_in_um=[2.0, 2.0, 20.0],  # (x, y, z)
        dimensions_in_voxels=[256, 256, 10],  # (x, y, z)
        illumination_pattern=line_scan,
    )
    volume_series = VolumetricMicroscopySeries(
        name="volume_series",
        description="GCaMP6f volumetric imaging",
        microscopy_rig=green_rig,
        microscopy_channel=green_channel,
        volumetric_imaging_space=volumetric_imaging_space,
        data=np.random.randint(0, 4096, size=(20, 10, 256, 256), dtype=np.uint16),  # (frames, depths, height, width)
        unit="a.u.",
        rate=3.0,  # volumes per second
        starting_time=1200.0,
    )
    nwbfile.add_acquisition(volume_series)

Multi-Plane and Multi-Channel Imaging
-------------------------------------

``MultiPlaneMicroscopyContainer`` groups the planes of one channel acquired at several depths, for example
with an electrically tunable lens. ``MultiChannelMicroscopyContainer`` groups data from several channels and
can contain multi-plane containers.

Here the GCaMP6f planes are interleaved: the scanner acquires one frame per plane in turn at 30 Hz, so each
plane is sampled at 10 Hz and the planes are offset by 1/30 s. After the functional recording, one tdTomato
image per plane is acquired with the red rig.

.. code-block:: python

    depths_in_um = [150, 200, 250]  # below the pia
    frame_rate_in_Hz = 30.0

    gcamp_series = []
    tdtomato_images = []
    for plane_index, depth in enumerate(depths_in_um):
        plane_space = PlanarImagingSpace(
            name=f"plane_{depth}um",
            description=f"Plane {depth} um below the pia",
            anatomical_target="Primary visual cortex, layer 2/3",
            pixel_size_in_um=[2.0, 2.0],
            dimensions_in_pixels=[256, 256],
            illumination_pattern=line_scan,
        )
        gcamp_series.append(
            PlanarMicroscopySeries(
                name=f"gcamp_{depth}um",
                description=f"GCaMP6f imaging {depth} um below the pia",
                microscopy_rig=green_rig,
                microscopy_channel=green_channel,
                planar_imaging_space=plane_space,
                data=np.random.randint(0, 4096, size=(50, 256, 256), dtype=np.uint16),
                unit="a.u.",
                rate=frame_rate_in_Hz / len(depths_in_um),
                starting_time=1800.0 + plane_index / frame_rate_in_Hz,
            )
        )
        tdtomato_images.append(
            PlanarMicroscopyStaticImage(
                name=f"tdtomato_{depth}um",
                description=f"tdTomato image {depth} um below the pia, acquired after the functional recording",
                microscopy_rig=red_rig,
                microscopy_channel=red_channel,
                planar_imaging_space=plane_space,  # same plane as the GCaMP6f series
                data=np.random.randint(0, 4096, size=(256, 256), dtype=np.uint16),
            )
        )

    nwbfile.add_acquisition(
        MultiChannelMicroscopyContainer(
            name="multi_plane_multi_channel",
            multi_plane_microscopy_containers=[
                MultiPlaneMicroscopyContainer(name="gcamp_planes", planar_microscopy_series=gcamp_series),
                MultiPlaneMicroscopyContainer(name="tdtomato_planes", planar_microscopy_static_images=tdtomato_images),
            ],
        )
    )

The resulting hierarchy is::

    acquisition/
    └── multi_plane_multi_channel/      MultiChannelMicroscopyContainer
        ├── gcamp_planes/               MultiPlaneMicroscopyContainer
        │   ├── gcamp_150um/            PlanarMicroscopySeries
        │   ├── gcamp_200um/
        │   └── gcamp_250um/
        └── tdtomato_planes/            MultiPlaneMicroscopyContainer
            ├── tdtomato_150um/         PlanarMicroscopyStaticImage
            ├── tdtomato_200um/
            └── tdtomato_250um/

ROI Segmentation
----------------

ROIs can be stored as image masks, shaped (height, width) like the data, or as pixel masks, lists of
(x, y, weight). Each mask type is a column of the table, so every ROI in a segmentation must provide the
same mask types. ``PlanarSegmentation.pixel_to_image`` and ``image_to_pixel`` convert between the two.

.. code-block:: python

    mean_image = SummaryImage(name="mean", description="Mean projection", data=data.mean(axis=0))
    max_image = SummaryImage(name="max", description="Maximum projection", data=data.max(axis=0))

    planar_segmentation = PlanarSegmentation(
        name="planar_segmentation",
        description="Suite2p segmentation of green_series",
        planar_imaging_space=planar_imaging_space,  # links to the imaging space of the series
        summary_images=[mean_image, max_image],
    )

    for x, y in [(40, 60), (120, 80), (200, 180)]:  # ROI centers
        image_mask = np.zeros((256, 256), dtype=np.float32)  # (height, width)
        image_mask[y - 4 : y + 4, x - 4 : x + 4] = 1.0
        planar_segmentation.add_roi(image_mask=image_mask)

    # The equivalent pixel mask of the first ROI, as (x, y, weight) rows
    first_roi_pixels = PlanarSegmentation.image_to_pixel(planar_segmentation.image_mask[0])

    ophys_module = nwbfile.create_processing_module(name="ophys", description="Processed imaging data")
    ophys_module.add(SegmentationContainer(name="SegmentationContainer", segmentations=[planar_segmentation]))

ROI Responses
-------------

``MicroscopyResponseSeries`` stores traces shaped (frames, ROIs) and links the series they were extracted from.

.. code-block:: python

    rois = planar_segmentation.create_roi_table_region(description="All ROIs", region=[0, 1, 2])
    fluorescence = MicroscopyResponseSeries(
        name="fluorescence",
        description="Raw fluorescence traces",
        data=np.random.rand(100, 3).astype(np.float32),  # (frames, ROIs)
        rois=rois,
        unit="a.u.",
        rate=30.0,
        starting_time=0.0,
        microscopy_series=green_series,
    )
    ophys_module.add(
        MicroscopyResponseSeriesContainer(
            name="MicroscopyResponseSeriesContainer",
            microscopy_response_series=[fluorescence],
        )
    )

    with NWBHDF5IO("two_photon_session.nwb", "w") as io:
        io.write(nwbfile)

One-Photon Miniscope Session with a GRIN Lens
=============================================

A head-mounted miniscope images CA1 through an implanted gradient-index (GRIN) lens. The GRIN lens is stored
as the ``ObjectiveLens`` of the rig, and its implant coordinates go in ``lens_positioning``. Camera-based
imaging uses ``PlaneAcquisition``.

.. code-block:: python

    nwbfile = NWBFile(
        session_description="Miniscope calcium imaging in mouse CA1 during free exploration",
        identifier=str(uuid4()),
        session_start_time=datetime(2025, 2, 3, 14, 0, tzinfo=timezone.utc),
    )

    miniscope_model = MicroscopeModel(
        name="miniscope_model",
        description="Head-mounted one-photon miniscope",
        manufacturer="Open Ephys",
        model_number="UCLA Miniscope V4",
    )
    led_model = ExcitationSourceModel(
        name="led_model",
        description="Blue LED in the miniscope housing",
        manufacturer="Open Ephys",
        source_type="LED",
        excitation_mode="one-photon",
        wavelength_range_in_nm=[460.0, 480.0],
    )
    camera_model = PhotodetectorModel(
        name="camera_model",
        manufacturer="ON Semiconductor",
        model_number="PYTHON480",
        detector_type="CMOS camera",
    )
    emission_filter_model = BandOpticalFilterModel(
        name="emission_filter_model",
        manufacturer="Chroma",
        model_number="ET525/50m",
        filter_type="Bandpass",
        center_wavelength_in_nm=525.0,
        bandwidth_in_nm=50.0,
    )
    grin_lens_model = ObjectiveLensModel(
        name="grin_lens_model",
        description="GRIN lens, 1 mm diameter, 4 mm length",
        manufacturer="Inscopix",
        numerical_aperture=0.5,
    )
    for device_model in (miniscope_model, led_model, camera_model, emission_filter_model, grin_lens_model):
        nwbfile.add_device_model(device_model)

    miniscope = Microscope(name="miniscope", model=miniscope_model, technique="one-photon widefield")
    led = ExcitationSource(name="led", model=led_model, power_in_W=0.0005)  # at the front of the GRIN lens
    camera = Photodetector(name="camera", model=camera_model)
    emission_filter = BandOpticalFilter(name="emission_filter", model=emission_filter_model)
    grin_lens = ObjectiveLens(
        name="grin_lens",
        model=grin_lens_model,
        lens_positioning=StereotacticPosition(
            name="lens_positioning",
            anatomical_target="CA1, stratum pyramidale",
            origin="bregma (AP, ML); brain surface (DV)",
            orientation="RAS",
            x_in_mm=2.0,
            y_in_mm=-2.1,
            z_in_mm=-1.2,  # lens tip above stratum pyramidale
        ),
    )
    for device in (miniscope, led, camera, emission_filter, grin_lens):
        nwbfile.add_device(device)

    miniscope_rig = MicroscopyRig(
        name="miniscope_rig",
        description="Miniscope with an implanted GRIN lens",
        microscope=miniscope,
        excitation_source=led,
        emission_filter=emission_filter,
        photodetector=camera,
        objective_lens=grin_lens,
    )

    gcamp_vector = ViralVector(
        name="gcamp_vector",
        description="AAV for pan-neuronal GCaMP6f expression",
        construct_name="AAV1-Syn-GCaMP6f-WPRE-SV40",
        manufacturer="Addgene",
        titer_in_vg_per_ml=1.0e13,
    )
    gcamp_injection = ViralVectorInjection(
        name="gcamp_injection",
        volume_in_uL=0.5,
        viral_vector=gcamp_vector,
        viral_injection_coordinates=StereotacticPosition(
            name="viral_injection_coordinates",
            anatomical_target="CA1",
            origin="bregma (AP, ML); brain surface (DV)",
            orientation="RAS",
            x_in_mm=2.0,
            y_in_mm=-2.1,
            z_in_mm=-1.4,
        ),
    )
    gcamp_indicator = Indicator(name="gcamp_indicator", label="GCaMP6f", viral_vector_injection=gcamp_injection)

    nwbfile.add_lab_meta_data(
        MicroscopyExperimentMetadata(
            microscopy_rigs=[miniscope_rig],
            viral_vectors=[gcamp_vector],
            viral_vector_injections=[gcamp_injection],
            indicators=[gcamp_indicator],
        )
    )

    camera_acquisition = PlaneAcquisition(
        name="camera_acquisition",
        description="Full-field LED illumination, frames acquired by the CMOS camera",
        plane_rate_in_Hz=20.0,
    )
    planar_imaging_space = PlanarImagingSpace(
        name="planar_imaging_space",
        description="Field of view below the GRIN lens, frames binned 2x2 to 304 x 304 pixels",
        anatomical_target="CA1, stratum pyramidale",
        pixel_size_in_um=[3.3, 3.3],  # (x, y), after binning
        dimensions_in_pixels=[304, 304],  # (x, y)
        illumination_pattern=camera_acquisition,
    )
    miniscope_series = PlanarMicroscopySeries(
        name="miniscope_series",
        description="GCaMP6f imaging during free exploration",
        microscopy_rig=miniscope_rig,
        microscopy_channel=MicroscopyChannel(
            name="green_channel",
            description="GCaMP6f emission",
            excitation_wavelength_in_nm=470.0,
            emission_wavelength_in_nm=525.0,
            indicator=gcamp_indicator,
        ),
        planar_imaging_space=planar_imaging_space,
        data=np.random.randint(0, 256, size=(100, 304, 304), dtype=np.uint8),  # (frames, height, width)
        unit="a.u.",
        rate=20.0,
        starting_time=0.0,
    )
    nwbfile.add_acquisition(miniscope_series)

    with NWBHDF5IO("miniscope_session.nwb", "w") as io:
        io.write(nwbfile)
