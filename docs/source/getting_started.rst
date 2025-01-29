***************
Getting Started
***************

Installation
===========

Python Installation
-----------------

The ndx-microscopy extension can be installed via pip:

.. code-block:: bash

   pip install ndx-microscopy

MATLAB Installation
-----------------

For MATLAB users:

.. code-block:: matlab

   generateExtension('<directory path>/ndx-microscopy/spec/ndx-microscopy.namespace.yaml');

Quick Start
==========

Here's a basic example of using ndx-microscopy for two-photon calcium imaging:

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
    from ndx_ophys_devices import Indicator

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

    # Create indicator
    indicator = Indicator(
        name='gcamp6f',
        label='GCaMP6f',
        description='Calcium indicator',
        manufacturer='Addgene'
    )

    # Configure light paths
    excitation = ExcitationLightPath(
        name='2p_excitation',
        excitation_wavelength_in_nm=920.0,
        excitation_mode='two-photon',
        description='Femtosecond pulsed laser'
    )
    nwbfile.add_lab_meta_data(excitation)

    emission = EmissionLightPath(
        name='gcamp_emission',
        emission_wavelength_in_nm=510.0,
        description='GCaMP6f emission path',
        indicator=indicator
    )
    nwbfile.add_lab_meta_data(emission)

    # Save file
    with NWBHDF5IO('calcium_imaging.nwb', 'w') as io:
        io.write(nwbfile)

Key Concepts
===========

The ndx-microscopy extension provides several key components for organizing microscopy data:

1. **Microscope**
   - Represents the microscope device and its properties
   - Stores metadata about the microscope model and configuration

2. **Light Paths**
   - ExcitationLightPath: Defines the illumination pathway
   - EmissionLightPath: Defines the collection pathway
   - Includes wavelengths, modes, and optical components

3. **Imaging Spaces**
   - Defines the physical space being imaged
   - Supports both 2D (planar) and 3D (volumetric) imaging
   - Includes coordinate systems and grid spacing

4. **Data Series**
   - MicroscopySeries: Base type for time series data
   - Supports various imaging modalities (2D, 3D, variable depth)
   - Handles multi-channel data

Next Steps
=========

- Check out the :ref:`user_guide` for detailed usage information
- See :ref:`examples` for more complex examples
- Review the :ref:`api` for complete API documentation
