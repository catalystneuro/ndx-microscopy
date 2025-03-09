.. _release_notes:

*************
Release Notes
*************

Version 0.1.0
============

Initial release of ndx-microscopy extension.

Features
--------

* Microscope metadata: `Microscope`
* Integration with ndx-ophys-devices for optical component specifications: `ExcitationSource`/`PulsedExcitationSource`,`BandOpticalFilter`/`EdgeOpticalFilter`,`DichroicMirror`,`Photodetector`,`Indicator`
* Advanced light path configurations: `ExcitationLightPath`,`EmissionLightPath` 
* Imaging space definitions: `PlanarImagingSpace`,`VolumetricImagingSpace`
* Support for 2D and 3D imaging: `PlanarMicroscopySeries`,`VolumetricMicroscopySeries`,`MultiPlaneMicroscopyContainer`
* ROI/segmentation storage: `SummaryImages`,`Segmentation2D`,`Segmentation3D`,`SegmentationContainer`,`MicroscopyResponseSeries`,`MicroscopyResponseSeriesContainer`
* Abstract Neurodata types: `ImagingSpace`, `MicroscopySeries`,`Segmentation`

Changes
-------

* Initial implementation of all neurodata data types
* Basic documentation and examples
* Integration tests and validation
