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

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', "primaryBorderColor': '#144E73', 'lineColor': '#D96F32'}}}%%


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
        --> unit : text

        --------------------------------------
        links
        --------------------------------------
        imaging_space : PlanarImagingSpace
    }

    class VariableDepthMicroscopySeries {
        <<MicroscopySeries>>

        --------------------------------------
        datasets
        --------------------------------------
        data : numeric, frame x height x width
        --> unit : text
        depth_per_frame_in_um : numeric, length of frames

        --------------------------------------
        links
        --------------------------------------
        imaging_space : PlanarImagingSpace
    }

    class VolumetricMicroscopySeries {
        <<MicroscopySeries>>

        --------------------------------------
        datasets
        --------------------------------------
        data : numeric, frame x height x width x depth
        --> unit : text

        --------------------------------------
        links
        --------------------------------------
        imaging_space : VolumetricImageSpace
    }

    class MultiChannelMicroscopyVolume {
        <<NWBDataInterface>>
        
        --------------------------------------
        attributes
        --------------------------------------
        description : text, optional
        unit : text, optional
        conversion : numeric, optional
        offset : numeric, optional

        --------------------------------------
        datasets
        --------------------------------------
        data : numeric, frame x height x width x depth x emission_light_paths
        --> unit : text
        excitation_light_paths : ExcitationLightPath, excitation_light_paths
        emission_light_paths : EmissionLightPath, emission_light_paths
        
        --------------------------------------
        links
        --------------------------------------
        imaging_space : VolumetricImageSpace
        microscope : Microscope
    }
    
    class ImagingSpace{
        <<NWBContainer>>

        --------------------------------------
        datasets
        --------------------------------------
        description : text
        origin_coordinates : numeric, length 3, optional
        --> unit : text, default="micrometers"

        --------------------------------------
        attributes
        --------------------------------------
        location : text, optional
    }

    class PlanarImagingSpace{
        <<ImagingSpace>>

        --------------------------------------
        datasets
        --------------------------------------
        grid_spacing : numeric, length 2, optional
        --> unit : text, default="micrometers"

        --------------------------------------
        attributes
        --------------------------------------
        reference_frame : text, optional
    }

    class VolumetricImagingSpace{
        <<ImagingSpace>>

        --------------------------------------
        datasets
        --------------------------------------
        grid_spacing : numeric, length 2, optional
        --> unit : text, default="micrometers"

        --------------------------------------
        attributes
        --------------------------------------
        reference_frame : text, optional
    }

    class ExcitationLightPath{
        <<NWBContainer>>

        --------------------------------------
        links
        --------------------------------------
        excitation_source : ExcitationSource, optional
        excitation_filter : OpticalFilter, optional

        --------------------------------------
        attributes
        --------------------------------------
        excitation_wavelength_in_nm : numeric
    }

    class EmissionLightPath{
        <<NWBContainer>>

        --------------------------------------
        links
        --------------------------------------
        photodetector : Photodetector, optional
        emission_filter : OpticalFilter, optional

        --------------------------------------
        attributes
        --------------------------------------
        emission_wavelength_in_nm : numeric
    }

    class Microscope{
        <<Device>>

        --------------------------------------
        attributes
        --------------------------------------
        model : text, optional
    }

    PlanarMicroscopySeries *-- MicroscopySeries : extends
    PlanarMicroscopySeries -- PlanarImagingSpace : links
    VariableDepthMicroscopySeries *-- MicroscopySeries : extends
    VariableDepthMicroscopySeries -- PlanarImagingSpace : links
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
