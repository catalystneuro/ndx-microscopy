# ndx-microscopy Extension for NWB

A Neurodata Without Borders (NWB) extension for storing microscopy data and associated metadata in a standardized format. This extension integrates with [ndx-ophys-devices](https://github.com/catalystneuro/ndx-ophys-devices) to provide comprehensive optical component specifications.

## Features

**Comprehensive Neurodata Types**
- Microscope and optical component metadata (integration with [ndx-ophys-devices](https://github.com/catalystneuro/ndx-ophys-devices)):
    - `Microscope`
    - `ExcitationSource` / `PulsedExcitationSource`
    - `BandOpticalFilter` / `EdgeOpticalFilter` / 
    - `DichroicMirror` 
    - `Photodetector` 
    - `Indicator`
- Advanced light path configurations: 
    - `ExcitationLightPath`
    - `EmissionLightPath` 
- Imaging space definitions: 
    - `PlanarImagingSpace`
    - `VolumetricImagingSpace`
- Support for 2D and 3D imaging: 
    - `PlanarMicroscopySeries`
    - `VolumetricMicroscopySeries`
    - `MultiPlaneMicroscopyContainer`
- ROI/segmentation storage: 
    - `Segmentation2D`
    - `Segmentation3D`
    - `SegmentationContainer`
    - `MicroscopyResponseSeries`
    - `MicroscopyResponseSeriesContainer`
- Abstract Neurodata types: `ImagingSpace`, `MicroscopySeries`,`Segmentation`

## Entity relationship diagram

#### Entity relationship diagram for ndx-ophys-devices objects in ndx-microscopy 

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryBorderColor': '#144E73', 'lineColor': '#D96F32'}}}%%

classDiagram

    direction TB

    class DeviceModel {
        <<Device>>
        --------------------------------------
        attributes
        --------------------------------------
        model : text, optional
    }

    class ExcitationLightPath {
        <<LabMetaData>>
        --------------------------------------
        attributes
        --------------------------------------
        description : text
        --------------------------------------
        links
        --------------------------------------
        excitation_source : ExcitationSource
        excitation_filter : OpticalFilter, optional
        dichroic_mirror : DichroicMirror, optional
    }

    class EmissionLightPath {
        <<LabMetaData>>
        --------------------------------------
        attributes
        --------------------------------------
        description : text
        --------------------------------------
        groups
        --------------------------------------
        indicator : Indicator
        --------------------------------------
        links
        --------------------------------------
        photodetector : Photodetector
        emission_filter : OpticalFilter, optional
        dichroic_mirror : DichroicMirror, optional
    }

    class ExcitationSource {
        <<DeviceModel>>
        --------------------------------------
        attributes
        --------------------------------------
        illumination_type : text
        excitation_wavelength_in_nm : float
        excitation_mode: text
        power_in_W : float, optional
        intensity_in_W_per_m2 : float, optional
        exposure_time_in_s : float, optional
    }

    class PulsedExcitationSource {
        <<ExcitationSource>>
        --------------------------------------
        attributes
        --------------------------------------
        peak_power_in_W : float, optional
        peak_pulse_energy_in_J : float, optional
        pulse_rate_in_Hz : float, optional
    }

    class OpticalFilter {
        <<DeviceModel>>
        --------------------------------------
        attributes
        --------------------------------------
        filter_type : text
    }

    class BandOpticalFilter {
        <<OpticalFilter>>
        --------------------------------------
        attributes
        --------------------------------------
        center_wavelength_in_nm : float
        bandwidth_in_nm : float
    }

    class EdgeOpticalFilter {
        <<OpticalFilter>>
        --------------------------------------
        attributes
        --------------------------------------
        cut_wavelength_in_nm : float
        slope_in_percent_cut_wavelength : float, optional
        slope_starting_transmission_in_percent : float, optional
        slope_ending_transmission_in_percent : float, optional
    }

    class DichroicMirror{
        <<DeviceModel>>
        --------------------------------------
        attributes
        --------------------------------------
        cut_on_wavelength_in_nm : numeric, optional
        cut_off_wavelength_in_nm : numeric, optional
        reflection_band_in_nm : numeric, optional
        transmission_band_in_nm : numeric, optional
        angle_of_incidence_in_degrees : numeric, optional
    }
    
    class Photodetector {
        <<DeviceModel>>
        --------------------------------------
        attributes
        --------------------------------------
        detector_type : text
        detected_wavelength_in_nm : float
        gain : float, optional
        gain_unit : text, optional
    }

    class Indicator {
        <<NWBContainer>>
        --------------------------------------
        attributes
        --------------------------------------
        label : text
        description : text, optional
        manufacturer : text, optional
        injection_brain_region : text, optional
        injection_coordinates_in_mm : float[3], optional
    }

    DeviceModel <|-- ExcitationSource : extends
    DeviceModel <|-- OpticalFilter : extends
    DeviceModel <|-- Photodetector : extends
    DeviceModel <|-- DichroicMirror : extends
    ExcitationSource <|-- PulsedExcitationSource : extends
    OpticalFilter <|-- BandOpticalFilter : extends
    OpticalFilter <|-- EdgeOpticalFilter : extends

    ExcitationLightPath ..> ExcitationSource : links
    ExcitationLightPath ..> OpticalFilter : links
    ExcitationLightPath ..> DichroicMirror : links
    EmissionLightPath ..> Photodetector : links
    EmissionLightPath ..> OpticalFilter : links
    EmissionLightPath ..> DichroicMirror : links
    EmissionLightPath *-- Indicator : contains
```

#### Entity relationship diagram for ndx-microscopy 

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryBorderColor': '#144E73', 'lineColor': '#D96F32'}}}%%

classDiagram
    direction BT

    class MicroscopySeries {
        <<TimeSeries>>
        --------------------------------------
        links
        --------------------------------------
        microscope : Microscope
        excitation_light_path : ExcitationLightPath
        emission_light_path : EmissionLightPath
    }

    class PlanarMicroscopySeries {
        <<MicroscopySeries>>
        --------------------------------------
        datasets
        --------------------------------------
        data : numeric, frame x height x width
        --------------------------------------
        groups
        --------------------------------------
        imaging_space : PlanarImagingSpace
    }

    class MultiPlaneMicroscopyContainer {
        <<NWBDataInterface>>
        --------------------------------------
        groups
        --------------------------------------
        planar_microscopy_series : PlanarMicroscopySeries, number of depths scanned
    }

    class VolumetricMicroscopySeries {
        <<MicroscopySeries>>
        --------------------------------------
        datasets
        --------------------------------------
        data : numeric, frame x height x width x depth
        --------------------------------------
        groups
        --------------------------------------
        imaging_space : VolumetricImagingSpace
    }
   
    class ImagingSpace {
        <<NWBContainer>>
        --------------------------------------
        datasets
        --------------------------------------
        description : text
        origin_coordinates : float64[3], optional
        --> unit : text, default="micrometers"
        --------------------------------------
        attributes
        --------------------------------------
        location : text, optional
    }

    class PlanarImagingSpace {
        <<ImagingSpace>>
        --------------------------------------
        datasets
        --------------------------------------
        grid_spacing_in_um : float64[2], optional
        --------------------------------------
        attributes
        --------------------------------------
        reference_frame : text, optional
    }

    class VolumetricImagingSpace {
        <<ImagingSpace>>
        --------------------------------------
        datasets
        --------------------------------------
        grid_spacing_in_um : float64[3], optional
        --------------------------------------
        attributes
        --------------------------------------
        reference_frame : text, optional
    }

    class ExcitationLightPath {
        <<LabMetaData>>
        --------------------------------------
        attributes
        --------------------------------------
        excitation_wavelength_in_nm : numeric
        excitation_mode : txt
        description : text
        --------------------------------------
        links
        --------------------------------------
        excitation_source : ExcitationSource, optional
        excitation_filter : OpticalFilter, optional
        dichroic_mirror : DichroicMirror, optional
    }

    class EmissionLightPath {
        <<LabMetaData>>
        --------------------------------------
        attributes
        --------------------------------------
        emission_wavelength_in_nm : numeric
        description : text
        --------------------------------------
        groups
        --------------------------------------
        indicator : Indicator
        --------------------------------------
        links
        --------------------------------------
        photodetector : Photodetector, optional
        emission_filter : OpticalFilter, optional
        dichroic_mirror : DichroicMirror, optional
    }

    class Microscope {
        <<Device>>
        --------------------------------------
        attributes
        --------------------------------------
        model : text, optional
    }

    PlanarMicroscopySeries *-- MicroscopySeries : extends
    PlanarMicroscopySeries -- PlanarImagingSpace : links
    MultiPlaneMicroscopyContainer ..> PlanarMicroscopySeries : links
    VolumetricMicroscopySeries *-- MicroscopySeries : extends
    VolumetricMicroscopySeries -- VolumetricImagingSpace : links
    PlanarImagingSpace *-- ImagingSpace : extends
    VolumetricImagingSpace *-- ImagingSpace : extends
    MicroscopySeries ..> Microscope : links
    MicroscopySeries ..> ExcitationLightPath : links
    MicroscopySeries ..> EmissionLightPath : links
```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).

## Installation

```bash
pip install ndx-microscopy
```

## Documentation

For detailed documentation, including API reference and additional examples, please visit our [documentation site](https://ndx-microscopy.readthedocs.io/).


## Contributing

To help ensure a smooth Pull Request (PR) process, please always begin by raising an issue on the main repository so we can openly discuss any problems/additions before taking action.

The main branch of ndx-microscopy is protected; you cannot push to it directly. You must upload your changes by pushing a new branch, then submit your changes to the main branch via a Pull Request. This allows us to conduct automated testing of your contribution, and gives us a space for developers to discuss the contribution and request changes. If you decide to tackle an issue, please make yourself an assignee on the issue to communicate this to the team. Don’t worry - this does not commit you to solving this issue. It just lets others know who they should talk to about it.

From your local copy directory, use the following commands.

If you have not already, you will need to clone the repo:
```bash
$ git clone https://github.com/catalystneuro/ndx-microscopy
```

First create a new branch to work on
```bash
$ git checkout -b <new_branch>
```

Make your changes. Add new objects related to optical experiment or add more attributes on the existing ones. To speed up the process, you can write mock function (see _mock.py) that would be used to test the new neurodata type

We will automatically run tests to ensure that your contributions didn’t break anything and that they follow our style guide. You can speed up the testing cycle by running these tests locally on your own computer by calling pytest from the top-level directory.
Push your feature branch to origin (i.e. GitHub)

```bash
$ git push origin <new_branch>
```

Once you have tested and finalized your changes, create a pull request (PR) targeting dev as the base branch:
Ensure the PR description clearly describes the problem and solution.
Include the relevant issue number if applicable. TIP: Writing e.g. “fix #613” will automatically close issue #613 when this PR is merged.
Before submitting, please ensure that the code follows the standard coding style of the respective repository.
If you would like help with your contribution, or would like to communicate contributions that are not ready to merge, submit a PR where the title begins with “[WIP].”

Update the CHANGELOG.md regularly to document changes to the extension.

## License

MIT License. See [LICENSE.txt](LICENSE.txt) for details.
