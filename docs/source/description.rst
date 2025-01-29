Overview
========

This extension enables:

Storage of microscopy data with comprehensive metadata and unit handling

* Support for multiple microscopy techniques (one-photon, two-photon, three-photon, light sheet)

* Advanced light path tracking with pulsed and continuous excitation sources

* Detailed optical component specifications (filters, detectors, indicators)

* Sophisticated ROI/segmentation data organization with mask support

* Multi-channel data handling with regular and variable depth spacing

* Precise coordinate system and reference frame management

* Integration with common analysis tools and pipelines

* ROI response data extraction and analysis support

Key Features
===========

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
=============

Installation
-----------

.. code-block:: bash

   pip install ndx-microscopy

For MATLAB users:

.. code-block:: matlab

   generateExtension('<directory path>/ndx-microscopy/spec/ndx-microscopy.namespace.yaml');

Basic Usage
----------

The extension provides comprehensive support for microscopy data organization:


* See the :ref:`description` section for an overview and basic usage examples

* See the :ref:`format` section for detailed specifications of all data types

* See the :ref:`release_notes` section for version history and updates

For Developers
============

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


The ndx-microscopy Extension
===========================

The ndx-microscopy extension for NWB provides a standardized way to store and organize microscopy data in neuroscience research. This extension is designed to accommodate various microscopy techniques while maintaining detailed metadata about the imaging setup, experimental conditions, and acquired data.

Supported Microscopy Techniques
=============================

1. One-photon Microscopy (Widefield)

2. Two-photon Microscopy
 
3. Three-photon Microscopy

4. Light Sheet Microscopy

5. Others: open an issue on `GitHub <https://github.com/catalystneuro/ndx-microscopy/issues>`_ to request support for additional techniques

Common Use Cases
==============

Calcium Imaging
-------------
One of the most common applications in neuroscience:

* GCaMP and other calcium indicator imaging

* Both one-photon and multi-photon implementations

* Often requires ROI segmentation

* Time series analysis of neural activity

Voltage Imaging
-------------
Emerging technique for direct measurement of neural activity, using voltage-sensitive fluorescent proteins or dyes. Voltage-sensitive fluorescent proteins or dyes can be store in the Indicator object.

Structural Imaging
----------------
For anatomical studies and long-term tracking:

* Fixed tissue imaging

* Cellular morphology

* Brain structure mapping

* Often involves multi-channel acquisition

Multi-Channel Fluorescence
------------------------
Complex experiments with multiple labels:

* Multiple fluorophores

* 3D reconstruction

Data Organization
===============

Example data organization::

    nwbfile
    ├── devices
    │   └── microscope: Microscope
    ├── lab_meta_data
    │   ├── excitation_path: ExcitationLightPath
    │   └── emission_path: EmissionLightPath
    ├── acquisition
    │   └── MicroscopySeries
    └── processing
        └── ophys
            └── MicroscopySegmentations

The extension organizes microscopy data hierarchically:

1. **Device Metadata**
   
* Microscope specifications
   
* Optical configurations
   
* Calibration information

2. **Light Path Tracking**
   
* Excitation sources and parameters 
   
* Emission filters and detectors
    
* Optical element specifications

3. **Spatial Information**
   
* Imaging space definitions  
   
* Coordinate systems 
   
* Resolution and scaling

4. **Time Series Data**
  
* Raw imaging data  
   
* Processed signals 
   
* Temporal annotations

5. **Segmentation and ROIs**
  
* Region definitions
   
* Mask specifications   
   
* Segmentation algorithms

Best Practices
============

1. **Metadata Documentation**
   
* Document all known microscope parameters
      
* Include calibration data when available
     
* Specify coordinate systems clearly
    

2. **Data Organization**
  
* Group related data streams  
   
* Maintain clear relationships between raw and processed data 
   
* Include quality control metrics

3. **Performance Considerations**
 
* Use appropriate chunking for large datasets
     
* Consider compression options
   
