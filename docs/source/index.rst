.. ndx-microscopy documentation master file

ndx-microscopy: NWB Extension for Microscopy Data
*************************************************

The ndx-microscopy extension provides a standardized way to store and organize microscopy data in the Neurodata Without Borders (NWB) format. This extension integrates with  `ndx-ophys-devices <https://github.com/catalystneuro/ndx-ophys-devices>`_ to provide comprehensive optical component specifications.

Key Features
------------

- Device components: MicroscopeModel, Microscope and MicroscopyRig, with optical components from ndx-ophys-devices
- Illumination patterns for line scanning, plane acquisition and random access scanning
- Planar and volumetric imaging spaces with the targeted anatomical region and pixel or voxel size
- Planar and volumetric series and static images, with multi-plane and multi-channel containers
- Segmentation, summary images and ROI response series

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   description
   getting_started
   user_guide
   examples
   format
   api
   release_notes
   credits

Installation
------------

Python Installation
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install ndx-microscopy


Contributing
------------

Contributions are welcome! Please see our `GitHub repository <https://github.com/catalystneuro/ndx-microscopy>`_ for:

- Source code and documentation
- Issue tracking and feature requests
- Development guidelines
- Contributing instructions

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
