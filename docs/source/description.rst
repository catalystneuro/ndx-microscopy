.. _description:

Overview
========

The ndx-microscopy extension for NWB stores microscopy imaging data together with metadata about the
microscope, its optical components, the illumination pattern, and the imaged region. Optical components and
molecular tools (indicators, viral vectors and injections) come from
`ndx-ophys-devices <https://github.com/catalystneuro/ndx-ophys-devices>`_.

Key Features
------------

Device and Optical Components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``MicroscopeModel`` and ``Microscope``, which extend the core ``DeviceModel`` and ``Device`` types
- ``MicroscopyRig``, which links the microscope and the optical components used for an acquisition
- ``MicroscopyChannel``, which records the excitation and emission wavelengths and links the indicator
- Optical components from ndx-ophys-devices:

  - Excitation sources (continuous and pulsed)
  - Optical filters (band and edge types)
  - Dichroic mirrors
  - Photodetectors
  - Objective lenses, with an optional stereotactic position

- ``MicroscopyExperimentMetadata``, which holds the rigs, indicators, viral vectors and injections

Illumination Patterns
^^^^^^^^^^^^^^^^^^^^^

- ``IlluminationPattern``, a base class for patterns not covered below
- ``LineScan`` for point-scanning systems that build each frame from scanned lines
- ``PlaneAcquisition`` for whole-plane acquisition, such as light sheet or camera-based widefield imaging
- ``RandomAccessScan`` for targeted scanning of selected points

Imaging Spaces
^^^^^^^^^^^^^^

- ``PlanarImagingSpace`` and ``VolumetricImagingSpace`` record the targeted anatomical region, the pixel or
  voxel size, and the dimensions in pixels or voxels
- Each imaging space contains the illumination pattern used to acquire it
- The optional ``fov_center_coordinates`` stores the stereotactic position of the center of the field of view,
  including the imaging depth; atlas localization of the field of view will be handled by the
  `ndx-anatomical-localization <https://github.com/catalystneuro/ndx-anatomical-localization>`_ extension

Imaging Data
^^^^^^^^^^^^

- ``PlanarMicroscopySeries`` and ``VolumetricMicroscopySeries`` for data acquired over time
- ``PlanarMicroscopyStaticImage`` and ``VolumetricMicroscopyStaticImage`` for single images
- ``MultiPlaneMicroscopyContainer`` for planes acquired at several depths, for example with an electrically
  tunable lens
- ``MultiChannelMicroscopyContainer`` for data acquired in several channels, including multi-plane containers

Segmentation and Responses
^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``PlanarSegmentation`` and ``VolumetricSegmentation`` store ROI masks as image or volume masks, or as lists
  of pixels or voxels
- ``SummaryImage`` stores mean, maximum or correlation images with the segmentation
- ``MicroscopyResponseSeries`` stores ROI traces and links the imaging series they were extracted from

Dimension Order
---------------

Imaging data and masks are stored in (time, [depth], height, width) order, the TZYX convention used by OME,
ImageJ and scikit-image. Sizes and coordinates are listed x first.

.. list-table::
   :header-rows: 1

   * - Field
     - Order
   * - ``PlanarMicroscopySeries.data``
     - (frames, height, width)
   * - ``VolumetricMicroscopySeries.data``
     - (frames, depths, height, width)
   * - ``PlanarMicroscopyStaticImage.data``
     - (height, width)
   * - ``VolumetricMicroscopyStaticImage.data``
     - (depths, height, width)
   * - ``PlanarSegmentation.image_mask``
     - (ROIs, height, width)
   * - ``VolumetricSegmentation.volume_mask``
     - (ROIs, depth, height, width)
   * - ``SummaryImage.data``
     - (height, width) or (depth, height, width)
   * - ``MicroscopyResponseSeries.data``
     - (frames, ROIs)
   * - ``PlanarSegmentation.pixel_mask`` rows
     - (x, y, weight)
   * - ``VolumetricSegmentation.voxel_mask`` rows
     - (x, y, z, weight)
   * - ``PlanarImagingSpace.pixel_size_in_um`` and ``dimensions_in_pixels``
     - (x, y)
   * - ``VolumetricImagingSpace.voxel_size_in_um`` and ``dimensions_in_voxels``
     - (x, y, z)

Data Structure
--------------

A file with one planar series and its segmentation is organized as follows::

    nwbfile
    ├── general
    │   ├── devices
    │   │   ├── models
    │   │   │   └── MicroscopeModel, ExcitationSourceModel, ...
    │   │   └── Microscope, ExcitationSource, Photodetector, ObjectiveLens, ...
    │   └── microscopy_experiment_metadata: MicroscopyExperimentMetadata
    │       ├── MicroscopyRig  (links to the devices)
    │       ├── Indicator
    │       ├── ViralVector
    │       └── ViralVectorInjection
    ├── acquisition
    │   └── PlanarMicroscopySeries
    │       ├── microscopy_rig  (link to the MicroscopyRig)
    │       ├── MicroscopyChannel  (links to the Indicator)
    │       └── PlanarImagingSpace
    │           └── IlluminationPattern
    └── processing
        └── ophys
            ├── SegmentationContainer
            │   └── PlanarSegmentation  (links to the PlanarImagingSpace)
            └── MicroscopyResponseSeriesContainer
                └── MicroscopyResponseSeries  (links to the PlanarMicroscopySeries)

For Developers
--------------

The source code, issue tracker and development guidelines are in the
`GitHub repository <https://github.com/catalystneuro/ndx-microscopy>`_.
