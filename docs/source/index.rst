.. ndx-microscopy documentation master file

ndx-microscopy: NWB Extension for Microscopy Data
**********************************************

The ndx-microscopy extension provides a standardized way to store and organize microscopy data in the Neurodata Without Borders (NWB) format. This extension supports various microscopy techniques including one-photon, two-photon, three-photon, and light sheet microscopy.

Key Features
===========

- **Comprehensive Data Types**: Store microscope metadata, light paths, imaging spaces, and more
- **Multiple Modalities**: Support for various microscopy techniques
- **Flexible Organization**: Handle 2D/3D imaging, multi-channel data, and variable depth
- **Rich Metadata**: Track optical components, coordinate systems, and experimental parameters
- **Analysis Integration**: Compatible with common analysis pipelines and tools

Documentation
============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   user_guide
   examples
   api
   format
   release_notes
   credits

Installation
===========

Python Installation
-----------------

.. code-block:: bash

   pip install ndx-microscopy

MATLAB Installation
-----------------

.. code-block:: matlab

   generateExtension('<directory path>/ndx-microscopy/spec/ndx-microscopy.namespace.yaml');

Quick Example
===========

Here's a basic example of using ndx-microscopy:

.. code-block:: python

    from ndx_microscopy import Microscope, ExcitationLightPath, EmissionLightPath
    from ndx_ophys_devices import Indicator

    # Set up microscope
    microscope = Microscope(
        name='2p-scope',
        model='Custom two-photon microscope'
    )

    # Create indicator
    indicator = Indicator(
        name='gcamp6f',
        label='GCaMP6f',
        description='Calcium indicator'
    )

    # Configure light paths
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

See the :ref:`examples` section for more detailed examples.

Contributing
===========

Contributions are welcome! Please feel free to submit a Pull Request. For more information, see our `GitHub repository <https://github.com/catalystneuro/ndx-microscopy>`_.

Indices and Tables
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
