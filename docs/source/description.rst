Overview
========

The ndx-microscopy Extension
---------------------------

The ndx-microscopy extension for NWB provides a standardized way to store and organize microscopy data in neuroscience research. This extension is designed to accommodate various microscopy techniques while maintaining detailed metadata about the imaging setup, experimental conditions, and acquired data.

Supported Microscopy Techniques
-----------------------------

One-photon Microscopy (Widefield)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
One-photon microscopy, also known as widefield fluorescence microscopy, is widely used for large-scale neural imaging. 

Two-photon Microscopy
^^^^^^^^^^^^^^^^^^^
Two-photon microscopy is a powerful technique for deep tissue imaging with high spatial resolution. 

Three-photon Microscopy
^^^^^^^^^^^^^^^^^^^^
Three-photon microscopy extends imaging capabilities even deeper into tissue.

Light Sheet Microscopy
^^^^^^^^^^^^^^^^^^^
Light sheet microscopy offers high-speed volumetric imaging.

Common Use Cases
--------------

Calcium Imaging
^^^^^^^^^^^^^
One of the most common applications in neuroscience:

* GCaMP and other calcium indicator imaging
* Both one-photon and multi-photon implementations
* Often requires ROI segmentation
* Time series analysis of neural activity

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

Voltage Imaging
^^^^^^^^^^^^^
Emerging technique for direct measurement of neural activity, using voltage-sensitive fluorescent proteins or dyes. Voltage-sensitive fluorescent proteins or dyes can be store in the Indicator object.

Structural Imaging
^^^^^^^^^^^^^^^^
For anatomical studies and long-term tracking:

* Fixed tissue imaging
* Cellular morphology
* Brain structure mapping
* Often involves multi-channel acquisition

Multi-Channel Fluorescence
^^^^^^^^^^^^^^^^^^^^^^^^
Complex experiments with multiple labels:

* Multiple fluorophores
* 3D reconstruction

Data Organization
---------------

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
------------

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

