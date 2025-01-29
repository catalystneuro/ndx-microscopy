.. ndx-microscopy documentation master file

Welcome to the ndx-microscopy Extension
=====================================

The ndx-microscopy extension provides a standardized way to store and organize microscopy data in the Neurodata Without Borders (NWB) format. This extension supports various microscopy techniques including one-photon, two-photon, three-photon, and light sheet microscopy.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   description
   format
   visualization
   release_notes
   credits

Overview
--------

This extension enables:

* Storage of microscopy data with comprehensive metadata and unit handling
* Support for multiple microscopy techniques (one-photon, two-photon, three-photon, light sheet)
* Advanced light path tracking with pulsed and continuous excitation sources
* Detailed optical component specifications (filters, detectors, indicators)
* Sophisticated ROI/segmentation data organization with mask support
* Multi-channel data handling with regular and variable depth spacing
* Precise coordinate system and reference frame management
* Integration with common analysis tools and pipelines
* ROI response data extraction and analysis support

Key Features
-----------

1. **Comprehensive Data Types**
   * Microscope and optical component metadata
   * Advanced light path configurations (excitation and emission)
   * Pulsed and continuous excitation sources
   * Optical filters (band and edge types)
   * Photodetectors and indicators
   * Imaging space definitions with reference frames
   * Time series data with variable depth support
   * Advanced segmentation and ROI storage
   * Multi-channel volume organization
   * Response data handling

2. **Flexible Organization**
   * Support for 2D and 3D imaging
   * Variable depth imaging capabilities
   * Multi-channel data handling
   * Regular and irregular depth spacing
   * Precise coordinate system management
   * Comprehensive ROI/mask storage options
   * Extensible metadata with unit handling
   * Summary image support

3. **Analysis Integration**
   * ROI response data extraction
   * Coordinate system transformations
   * Unit conversion support
   * Standardized data access patterns
   * Compatible with common analysis pipelines
   * Performance optimizations
   * Quality control tools
   * Visualization support

Getting Started
-------------

Installation
^^^^^^^^^^

.. code-block:: bash

   pip install ndx-microscopy

For MATLAB users:

.. code-block:: matlab

   generateExtension('<directory path>/ndx-microscopy/spec/ndx-microscopy.namespace.yaml');

Basic Usage
^^^^^^^^^

The extension provides comprehensive support for microscopy data organization:

* See the :ref:`description` section for an overview and basic usage examples
* See the :ref:`format` section for detailed specifications of all data types
* See the :ref:`visualization` section for data visualization guidelines
* See the :ref:`release_notes` section for version history and updates

For detailed examples of common use cases:

* One-photon and two-photon calcium imaging
* Light sheet microscopy
* Multi-channel volumetric imaging
* ROI segmentation and response analysis
* Variable depth imaging

For Developers
------------

The extension is open source and welcomes contributions. See our `GitHub repository <https://github.com/catalystneuro/ndx-microscopy>`_ for:

* Source code and documentation
* Issue tracking and feature requests
* Development guidelines and best practices
* Contributing instructions and code review process

Extension Architecture:

* Integration with ndx-ophys-devices for optical component specifications
* Comprehensive test suite for data validation
* Support for both Python and MATLAB implementations
* Extensible design for future microscopy techniques
* Clear separation of data and metadata components
* Standardized coordinate system handling
* Flexible unit conversion system

Indices and tables
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
