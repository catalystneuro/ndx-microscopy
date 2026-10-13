.. _release_notes:

*************
Release Notes
*************

Version 0.4.0 (Upcoming)
========================

Deprecations and Changes
------------------------

* **Breaking Change**: ``OpticalLens`` renamed to ``ObjectiveLens``
* **Breaking Change**: ``Microscope`` extends the core ``Device`` type and ``MicroscopeModel`` the core ``DeviceModel`` type (pynwb 3.1), replacing ``DeviceInstance`` and ``DeviceModel`` from ndx-ophys-devices
* **Breaking Change**: ``MicroscopyChannel.indicator`` changed from a nested group to a link reference
* **Breaking Change**: ``MicroscopySeries.microscopy_rig`` changed from a nested group to a link reference
* **Breaking Change**: Simplified ``ImagingSpace`` class by removing coordinate system metadata:

  * Removed ``origin_coordinates`` dataset and its ``unit`` attribute
  * Renamed ``location`` attribute to ``anatomical_target`` for clearer semantics
  * Removed ``reference_frame`` attribute
  * Removed ``orientation`` attribute

* Updated ``ndx-ophys-devices`` dependency from v0.2.0 to v0.4.0
* Require Python >=3.10, pynwb >=3.1.0 and hdmf >=4.1.0
* **Breaking Change**: Reordered volumetric and planar dataset dimensions to follow the TZYX convention shared with OME, ImageJ, and scikit-image (see `#77 <https://github.com/catalystneuro/ndx-microscopy/issues/77>`_):

  * ``VolumetricMicroscopySeries.data``: ``(frames, height, width, depths)`` → ``(frames, depths, height, width)``
  * ``VolumetricMicroscopyStaticImage.data``: ``(height, width, depths)`` → ``(depths, height, width)``
  * ``VolumetricSegmentation.volume_mask``: ``(num_roi, num_x, num_y, num_z)`` → ``(num_roi, num_z, num_y, num_x)``
  * ``SummaryImage.data`` (3D variant): ``(height, width, depth)`` → ``(depth, height, width)``
  * ``VolumetricSegmentation.voxel_to_volume`` / ``volume_to_voxel`` now build/parse volumes in ``(depth, height, width)`` order. The ``voxel_mask`` compound dtype remains ``(x, y, z, weight)``.
  * ``PlanarSegmentation.image_mask``: ``(num_roi, num_x, num_y)`` → ``(num_roi, num_y, num_x)``
  * ``PlanarSegmentation.pixel_to_image`` / ``image_to_pixel`` now build/parse images in ``(height, width)`` order, so pixel ``(x, y)`` is stored at ``image_mask[y, x]``. The ``pixel_mask`` compound dtype remains ``(x, y, weight)``.

* **Breaking Change**: Renamed ``PlaneAcquisition.point_spread_function_in_um`` to ``point_spread_function``, since it is a text value such as "32 um ± 1.6 um"
* **Breaking Change**: Changed ``RandomAccessScan.max_scan_points`` dtype from ``numeric`` to ``int32``
* Changed the dtype of ``PlanarImagingSpace.dimensions_in_pixels`` and ``VolumetricImagingSpace.dimensions_in_voxels`` from ``uint32`` to ``int32``, so that Python integers are written without a dtype conversion warning
* Removed the redundant ``name`` attribute from ``MicroscopyChannel`` and ``MicroscopyStaticImage``; the object name is the group name
* Removed the custom ``SegmentationContainer.add_segmentation(imaging_space=...)``, which was never callable; use the generated ``add_segmentation(segmentations=...)``

Bug Fixes
---------

* Indexing a ``PlanarSegmentation`` or ``VolumetricSegmentation`` (e.g., ``segmentation[0]``, ``segmentation["image_mask"]``) returns table rows and columns with hdmf 4.1, as with later hdmf versions. It previously looked up summary images by name and failed, which also broke the HTML repr in Jupyter.

Features
--------

* Extended ``MultiChannelMicroscopyContainer`` to support nesting ``MultiPlaneMicroscopyContainer`` objects, enabling combined multi-plane and multi-channel acquisition workflows (e.g., a functional indicator imaged at several depths alongside anatomical markers)
* Added static image support for microscopy experiments:

  * ``MicroscopyStaticImage``: Base class for static images
  * ``PlanarMicroscopyStaticImage``: For 2D static images
  * ``VolumetricMicroscopyStaticImage``: For 3D static images

* Added ``MicroscopyExperimentMetadata`` (extends ``LabMetaData``) as a centralized container for experiment metadata, including:

  * ``MicroscopyRig`` objects
  * ``ViralVector`` objects (from ndx-ophys-devices)
  * ``ViralVectorInjection`` objects (from ndx-ophys-devices)
  * ``Indicator`` objects (from ndx-ophys-devices)

* Added support for ``ViralVector`` and ``ViralVectorInjection`` imports from ndx-ophys-devices
* Added optional ``fov_center_coordinates`` (a ``StereotacticPosition`` from ndx-ophys-devices) to ``ImagingSpace`` for the stereotactic position of the center of the field of view, including the imaging depth. Atlas localization of the field of view will be handled by `ndx-anatomical-localization <https://github.com/catalystneuro/ndx-anatomical-localization>`_
* Added optional ``optical_path_scheme`` dataset to ``MicroscopyRig`` (a contained ``Image``, e.g. ``RGBImage``) for storing an annotated diagram or picture of the microscope's optical path layout

Notes
-----

* These changes improve metadata organization by centralizing all experiment-related objects in ``MicroscopyExperimentMetadata``
* The use of links instead of nested groups provides better data reusability and reduces duplication
* Users should add ``MicroscopyExperimentMetadata`` to NWBFile using ``nwbfile.add_lab_meta_data()``

Reading files written with earlier versions
-------------------------------------------

Files written with ndx-microscopy 0.3.x cannot be read in a Python session that has imported ndx-microscopy 0.4.0,
because the installed namespace takes precedence over the one cached in the file.
To read such files, open them in a session that does not import ndx-microscopy; pynwb then loads the cached namespaces.

Version 0.3.0 (Jun 3, 2025)
==============================

Deprecations and Changes
-------------------------

* Removed ``ExcitationLightPath`` and ``EmissionLightPath`` classes in favor of a more integrated approach with ``MicroscopyRig``
* Changed ``Microscope`` to inherit from ``DeviceInstance`` instead of ``Device``
* Updated ``MicroscopySeries`` to use ``MicroscopyRig`` instead of individual ``microscope``, ``excitation_light_path``, and ``emission_light_path`` references
* Refactored segmentation classes:

  * Renamed ``Segmentation2D`` to ``PlanarSegmentation``
  * Renamed ``Segmentation3D`` to ``VolumetricSegmentation``

* Changed ``image_to_voxel`` in ``volume_to_voxel``
* Changed ``voxel_to_image`` in ``voxel_to_volume``
* Changed ``image_mask`` in ``volume_mask`` in VolumetricSegmentation

Features
--------

* Added ``MicroscopeModel`` class to define microscope models (inherits from ``DeviceModel``)
* Added ``MicroscopyRig`` class to organize all optical components in a single container, including:

  * ``microscope``: Link to the Microscope instance
  * ``excitation_source``: Link to ExcitationSource (optional)
  * ``excitation_filter``: Link to OpticalFilter (optional)
  * ``dichroic_mirror``: Link to DichroicMirror (optional)
  * ``photodetector``: Link to Photodetector (optional)
  * ``emission_filter``: Link to OpticalFilter (optional)

* Added ``MicroscopyChannel`` class to represent a single channel in a microscopy series, which includes:

  * ``excitation_wavelength``: Excitation wavelength for the channel
  * ``emission_wavelength``: Emission wavelength for the channel 
  * ``indicator``: Link to Indicator

* Added ``MultiChannelMicroscopyContainer`` class to support multi-channel imaging data.

  * This class allows for the storage of multiple ``MicroscopySeries`` objects, each representing a different channel of imaging data.
  * It provides methods to access and manipulate individual channels, facilitating the analysis of multi-channel datasets.

* Added ``dimensions_in_pixels`` to ``PlanarImagingSpace`` and ``dimensions_in_voxels`` to ``VolumetricImagingSpace``
* Added ``get_FOV_size()`` method to both ``PlanarImagingSpace`` and ``VolumetricImagingSpace`` classes for calculating Field of View size in micrometers
* Added ``microscopy_series`` link to ``MicroscopyResponseSeries`` class to point the ``MicroscopySeries`` this response series is derived from.


Improvements
------------

* Simplified the optical path configuration by consolidating components into a single ``MicroscopyRig`` container
* Improved organization of device components with the addition of ``MicroscopeModel`` and clearer inheritance structure
* Updated all documentation and examples to reflect the new structure

Notes
------

* These changes are NOT backward compatible and require updating existing code to use the new structure
* The ``MicroscopyRig`` approach provides a more flexible and intuitive way to organize optical components
* Improved organization of multi channel imaging data

Version 0.2.0 (March 19, 2025)
==============================

Deprecations and Changes
-------------------------

* Change ``grid_spacing_in_um`` in ``pixel_size_in_um`` and ``voxel_size_in_um`` (and relative doc string) to better represent the physical dimension of the fundamental unit of the image (pixel or voxel).

Improvements
------------

* New illumination pattern classes to represent different microscopy scanning methods:

  * ``IlluminationPattern``: Base class for describing the illumination pattern used to acquire images
  * ``LineScan``: Line scanning method commonly used in two-photon microscopy
  * ``PlaneAcquisition``: Whole plane acquisition method, common for light sheet and one-photon techniques
  * ``RandomAccessScan``: Random access method for targeted, high-speed imaging of specific regions

* Added ``technique`` attribute to the ``Microscope`` class to describe the imaging technique used
* Updated ``ImagingSpace`` classes to include an ``illumination_pattern`` parameter, creating a direct link between the imaging space and the acquisition method
* Added mock implementations for all new classes in ``_mock.py`` for testing purposes
* Updated example notebooks to demonstrate the use of different scanning methods

Notes
-----

* These changes are backward compatible and add new functionality without removing existing features
* The ``illumination_pattern`` parameter is now required when creating ``ImagingSpace`` objects

Version 0.1.0 (March 10, 2025)
==============================

Initial release of ndx-microscopy extension.

Features
--------

* Microscope metadata: ``Microscope``
* Integration with ndx-ophys-devices for optical component specifications: ``ExcitationSource``/``PulsedExcitationSource``, ``BandOpticalFilter``/``EdgeOpticalFilter``, ``DichroicMirror``, ``Photodetector``, ``Indicator``
* Advanced light path configurations: ``ExcitationLightPath``, ``EmissionLightPath`` 
* Imaging space definitions: ``PlanarImagingSpace``, ``VolumetricImagingSpace``
* Support for 2D and 3D imaging: ``PlanarMicroscopySeries``, ``VolumetricMicroscopySeries``, ``MultiPlaneMicroscopyContainer``
* ROI/segmentation storage: ``SummaryImages``, ``PlanarSegmentation``, ``VolumetricSegmentation``, ``SegmentationContainer``, ``MicroscopyResponseSeries``, ``MicroscopyResponseSeriesContainer``
* Abstract Neurodata types: ``ImagingSpace``, ``MicroscopySeries``, ``Segmentation``

Changes
-------

* Initial implementation of all neurodata data types
* Basic documentation and examples
* Integration tests and validation
