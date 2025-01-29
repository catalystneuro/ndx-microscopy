********
Examples
********

This section provides detailed examples of using the ndx-microscopy extension for various microscopy techniques.

Two-photon Calcium Imaging
========================

Complete example of two-photon calcium imaging with full optical path configuration:

.. code-block:: python

    from datetime import datetime
    from uuid import uuid4
    from pynwb import NWBFile, NWBHDF5IO
    from ndx_microscopy import (
        Microscope, 
        ExcitationLightPath,
        EmissionLightPath,
        PlanarImagingSpace,
        PlanarMicroscopySeries
    )
    from ndx_ophys_devices import (
        ExcitationSource,
        OpticalFilter,
        DichroicMirror,
        Photodetector,
        Indicator
    )

    # Create NWB file
    nwbfile = NWBFile(
        session_description='Two-photon calcium imaging session',
        identifier=str(uuid4()),
        session_start_time=datetime.now()
    )

    # Set up microscope
    microscope = Microscope(
        name='2p-scope',
        model='Custom two-photon microscope'
    )
    nwbfile.add_device(microscope)

    # Set up optical components
    laser = PulsedExcitationSource(
        name='chameleon',
        illumination_type='Laser',
        manufacturer='Coherent',
        model='Chameleon Ultra II',
        excitation_wavelength_in_nm=920.0,
        power_in_W=1.2,
        peak_power_in_W=100e3,
        peak_pulse_energy_in_J=1.25e-9,
        pulse_rate_in_Hz=80e6
    )
    nwbfile.add_device(laser)

    excitation_filter = BandOpticalFilter(
        name='excitation_filter',
        filter_type='Bandpass',
        manufacturer='Semrock',
        model='FF01-920/80',
        center_wavelength_in_nm=920.0,
        bandwidth_in_nm=80.0
    )
    nwbfile.add_device(excitation_filter)

    dichroic = DichroicMirror(
        name='primary_dichroic',
        manufacturer='Semrock',
        model='FF695-Di02',
        center_wavelength_in_nm=695.0
    )
    nwbfile.add_device(dichroic)

    emission_filter = BandOpticalFilter(
        name='emission_filter',
        filter_type='Bandpass',
        manufacturer='Semrock',
        model='FF01-510/84',
        center_wavelength_in_nm=510.0,
        bandwidth_in_nm=84.0
    )
    nwbfile.add_device(emission_filter)

    detector = Photodetector(
        name='pmt',
        detector_type='PMT',
        manufacturer='Hamamatsu',
        model='R6357',
        detected_wavelength_in_nm=510.0,
        gain=70.0,
        gain_unit='dB'
    )
    nwbfile.add_device(detector)

    # Create indicator
    indicator = Indicator(
        name='gcamp6f',
        label='GCaMP6f',
        description='Calcium indicator for two-photon imaging',
        manufacturer='Addgene',
        injection_brain_region='Visual cortex',
        injection_coordinates_in_mm=[-2.5, 3.2, 0.5]
    )

    # Configure light paths with optical components
    excitation = ExcitationLightPath(
        name='2p_excitation',
        excitation_wavelength_in_nm=920.0,
        excitation_mode='two-photon',
        description='Femtosecond pulsed laser pathway',
        excitation_source=laser,
        excitation_filter=excitation_filter,
        dichroic_mirror=dichroic
    )
    nwbfile.add_lab_meta_data(excitation)

    emission = EmissionLightPath(
        name='gcamp_emission',
        emission_wavelength_in_nm=510.0,
        description='GCaMP6f emission pathway',
        indicator=indicator,
        photodetector=detector,
        emission_filter=emission_filter,
        dichroic_mirror=dichroic
    )
    nwbfile.add_lab_meta_data(emission)

    # Define imaging space
    imaging_space = PlanarImagingSpace(
        name='cortex_plane1',
        description='Layer 2/3 of visual cortex',
        grid_spacing_in_um=[1.0, 1.0],
        origin_coordinates=[100.0, 200.0, 300.0]
    )

    # Create microscopy series
    imaging_series = PlanarMicroscopySeries(
        name='imaging_data',
        microscope=microscope,
        excitation_light_path=excitation,
        emission_light_path=emission,
        imaging_space=imaging_space,
        data=data_array,  # Your imaging data array
        unit='n.a.',
        rate=30.0
    )

    # Add to file
    nwbfile.add_acquisition(imaging_series)

    # Save file
    with NWBHDF5IO('calcium_imaging.nwb', 'w') as io:
        io.write(nwbfile)

One-photon (Widefield) Imaging
===========================

Example of one-photon widefield imaging setup:

.. code-block:: python

    # Set up optical components for one-photon imaging
    led = ExcitationSource(
        name='led_source',
        illumination_type='LED',
        manufacturer='Thorlabs',
        model='M480L4',
        excitation_wavelength_in_nm=480.0,
        power_in_W=0.340,
        intensity_in_W_per_m2=1000.0,
        exposure_time_in_s=0.020
    )
    nwbfile.add_device(led)

    excitation_filter = BandOpticalFilter(
        name='excitation_filter',
        filter_type='Bandpass',
        manufacturer='Semrock',
        model='FF01-480/40',
        center_wavelength_in_nm=480.0,
        bandwidth_in_nm=40.0
    )
    nwbfile.add_device(excitation_filter)

    dichroic = DichroicMirror(
        name='primary_dichroic',
        manufacturer='Semrock',
        model='FF495-Di03',
        center_wavelength_in_nm=495.0
    )
    nwbfile.add_device(dichroic)

    emission_filter = BandOpticalFilter(
        name='emission_filter',
        filter_type='Bandpass',
        manufacturer='Semrock',
        model='FF01-510/84',
        center_wavelength_in_nm=510.0,
        bandwidth_in_nm=84.0
    )
    nwbfile.add_device(emission_filter)

    camera = Photodetector(
        name='camera',
        detector_type='Camera',
        manufacturer='Hamamatsu',
        model='ORCA-Flash4.0',
        detected_wavelength_in_nm=510.0,
        gain=1.0,
        gain_unit='relative'
    )
    nwbfile.add_device(camera)

    # Configure light paths
    excitation = ExcitationLightPath(
        name='1p_excitation',
        excitation_wavelength_in_nm=480.0,
        excitation_mode='one-photon',
        description='LED illumination pathway',
        excitation_source=led,
        excitation_filter=excitation_filter,
        dichroic_mirror=dichroic
    )
    nwbfile.add_lab_meta_data(excitation)

    emission = EmissionLightPath(
        name='gcamp_emission',
        emission_wavelength_in_nm=510.0,
        description='GCaMP6f emission pathway',
        indicator=indicator,
        photodetector=camera,
        emission_filter=emission_filter,
        dichroic_mirror=dichroic
    )
    nwbfile.add_lab_meta_data(emission)

Multi-Channel Volume Imaging
=========================

Example of multi-channel volumetric imaging:

.. code-block:: python

    # Set up multiple light paths
    excitation1 = ExcitationLightPath(
        name='excitation_ch1',
        excitation_wavelength_in_nm=920.0,
        excitation_mode='two-photon'
    )
    nwbfile.add_lab_meta_data(excitation1)

    excitation2 = ExcitationLightPath(
        name='excitation_ch2',
        excitation_wavelength_in_nm=1040.0,
        excitation_mode='two-photon'
    )
    nwbfile.add_lab_meta_data(excitation2)

    emission1 = EmissionLightPath(
        name='emission_ch1',
        emission_wavelength_in_nm=510.0,
        indicator=indicator1
    )
    nwbfile.add_lab_meta_data(emission1)

    emission2 = EmissionLightPath(
        name='emission_ch2',
        emission_wavelength_in_nm=610.0,
        indicator=indicator2
    )
    nwbfile.add_lab_meta_data(emission2)

    # Create volumetric imaging space
    space_3d = VolumetricImagingSpace(
        name='cortex_volume',
        description='Visual cortex volume',
        grid_spacing_in_um=[1.0, 1.0, 2.0],
        origin_coordinates=[100.0, 200.0, 300.0],
        location='Visual cortex',
        reference_frame='Bregma'
    )

    # Create multi-channel volume
    volume = MultiChannelMicroscopyVolume(
        name='multi_channel_data',
        description='Two-channel volume data',
        data=volume_data,  # [height, width, depth, channels]
        unit='n.a.',
        microscope=microscope,
        imaging_space=space_3d,
        excitation_light_paths=[excitation1, excitation2],
        emission_light_paths=[emission1, emission2]
    )
    nwbfile.add_acquisition(volume)

Variable Depth Imaging
===================

Example of variable depth imaging:

.. code-block:: python

    # Create imaging series with variable depth
    variable_series = VariableDepthMicroscopySeries(
        name='variable_depth_data',
        microscope=microscope,
        excitation_light_path=excitation,
        emission_light_path=emission,
        imaging_space=imaging_space,
        data=data_array,  # [frames, height, width]
        depth_per_frame_in_um=depth_array,  # [frames]
        unit='n.a.',
        rate=30.0
    )
    nwbfile.add_acquisition(variable_series)

ROI Response Data
===============

Example of storing ROI response data:

.. code-block:: python

    # Create response series
    response_series = MicroscopyResponseSeries(
        name='roi_responses',
        data=response_data,  # [frames, rois]
        unit='dF/F',
        rate=30.0,
        table_region=roi_table_region  # Reference to segmentation table
    )
    nwbfile.add_acquisition(response_series)
