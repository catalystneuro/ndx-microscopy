# ndx-microscopy Extension for NWB

An enhancement to core NWB schema types related to microscopy data.

Planned for an eventual NWBEP with the TAB.


## Installation

```
git clone https://github.com/catalystneuro/ndx-microscopy
pip install ndx-microscopy
```


## Usage

```python
# TODO
```


## Entity relationship diagram

In this PR I added neurodatatypes from ndx-ophys-devices:

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

    class ExcitationSource {
        <<DeviceModel>>
        --------------------------------------
        attributes
        --------------------------------------
        illumination_type : text
        excitation_wavelength_in_nm : float
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
    ExcitationSource <|-- PulsedExcitationSource : extends
    OpticalFilter <|-- BandOpticalFilter : extends
    OpticalFilter <|-- EdgeOpticalFilter : extends

    ExcitationLightPath ..> ExcitationSource : links
    ExcitationLightPath ..> OpticalFilter : links
    EmissionLightPath ..> Photodetector : links
    EmissionLightPath ..> OpticalFilter : links
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

    class VariableDepthMicroscopySeries {
        <<PlanarMicroscopySeries>>
        --------------------------------------
        datasets
        --------------------------------------
        depth_per_frame_in_um : numeric, length of frames
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
    VariableDepthMicroscopySeries *-- PlanarMicroscopySeries : extends
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
