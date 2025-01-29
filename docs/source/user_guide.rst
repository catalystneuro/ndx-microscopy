**********
User Guide
**********

This guide provides detailed information about using the ndx-microscopy extension.

Core Components
=============

Microscope Device
---------------

The Microscope class represents the physical microscope device:

.. code-block:: python

    microscope = Microscope(
        name='2p-scope',
        model='Custom two-photon microscope',
        description='Two-photon microscope for calcium imaging',
        manufacturer='Custom build'
    )
    nwbfile.add_device(microscope)

Light Path Configuration
---------------------

Light paths are defined using ExcitationLightPath and EmissionLightPath:

1. **ExcitationLightPath**: Defines how light reaches the sample
   
   .. code-block:: python

       excitation = ExcitationLightPath(
           name='2p_excitation',
           excitation_wavelength_in_nm=920.0,
           excitation_mode='two-photon',
           description='Femtosecond pulsed laser'
       )

2. **EmissionLightPath**: Defines how emitted light is collected
   
   .. code-block:: python

       emission = EmissionLightPath(
           name='gcamp_emission',
           emission_wavelength_in_nm=510.0,
           description='GCaMP6f emission path',
           indicator=indicator
       )

Imaging Spaces
------------

Imaging spaces define the physical region being imaged:

1. **PlanarImagingSpace**: For 2D imaging
   
   .. code-block:: python

       space_2d = PlanarImagingSpace(
           name='cortex_plane1',
           description='Layer 2/3 of visual cortex',
           grid_spacing_in_um=[1.0, 1.0],  # x, y spacing
           origin_coordinates=[100.0, 200.0, 300.0],  # x, y, z
           location='Visual cortex, layer 2/3',
           reference_frame='Bregma'
       )

2. **VolumetricImagingSpace**: For 3D imaging
   
   .. code-block:: python

       space_3d = VolumetricImagingSpace(
           name='cortex_volume1',
           description='Visual cortex volume',
           grid_spacing_in_um=[1.0, 1.0, 2.0],  # x, y, z spacing
           origin_coordinates=[100.0, 200.0, 300.0],
           location='Visual cortex',
           reference_frame='Bregma'
       )

Data Series Types
--------------

Different types of microscopy data series are available:

1. **PlanarMicroscopySeries**: For 2D time series
2. **VariableDepthMicroscopySeries**: For 2D series with variable depth
3. **VolumetricMicroscopySeries**: For 3D time series

Best Practices
============

Data Organization
--------------

1. **Consistent Naming**
   - Use descriptive names for devices and components
   - Follow a consistent naming convention
   - Include version information when relevant

2. **Metadata Documentation**
   - Document all known microscope parameters
   - Include calibration data when available
   - Specify coordinate systems clearly

3. **Data Hierarchy**
   - Group related data streams
   - Maintain clear relationships between raw and processed data
   - Include quality control metrics

Performance Optimization
---------------------

1. **Data Storage**
   - Use appropriate chunking for large datasets
   - Consider compression options
   - Balance between compression and access speed

2. **Memory Management**
   - Load data in chunks when processing
   - Use memory-mapped files when appropriate
   - Clear memory when processing large datasets

Common Use Cases
=============

Calcium Imaging
-------------

For calcium imaging experiments:

1. Set up the indicator:

.. code-block:: python

    indicator = Indicator(
        name='gcamp6f',
        label='GCaMP6f',
        description='Calcium indicator',
        manufacturer='Addgene',
        injection_brain_region='Visual cortex',
        injection_coordinates_in_mm=[-2.5, 3.2, 0.5]
    )

2. Configure appropriate light paths:

.. code-block:: python

    excitation = ExcitationLightPath(
        name='2p_excitation',
        excitation_wavelength_in_nm=920.0,
        excitation_mode='two-photon'
    )

    emission = EmissionLightPath(
        name='gcamp_emission',
        emission_wavelength_in_nm=510.0,
        indicator=indicator
    )

Voltage Imaging
-------------

For voltage imaging:

1. Set up voltage indicators:

.. code-block:: python

    indicator = Indicator(
        name='ace2n',
        label='Ace2N',
        description='Voltage indicator',
        manufacturer='Addgene'
    )

2. Configure high-speed imaging:

.. code-block:: python

    imaging_series = PlanarMicroscopySeries(
        name='voltage_imaging',
        rate=1000.0,  # 1 kHz acquisition
        ...
    )

Multi-Channel Imaging
------------------

For experiments with multiple channels:

.. code-block:: python

    volume = MultiChannelMicroscopyVolume(
        name='multi_channel_data',
        description='Multi-channel volume data',
        data=volume_data,  # [height, width, depth, channels]
        unit='n.a.',
        microscope=microscope,
        imaging_space=space_3d,
        excitation_light_paths=[excitation1, excitation2],
        emission_light_paths=[emission1, emission2]
    )