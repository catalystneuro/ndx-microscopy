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
        light_source : LightSource
        optical_channel : MicroscopyOpticalChannel
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
        depth_per_frame : (frame,) numeric
        -- > unit : text, default="micrometers"
        
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

    class MicroscopyOpticalChannel{
        <<NWBContainer>>

        --------------------------------------
        datasets
        --------------------------------------
        description : text
        
        --------------------------------------
        attributes
        --------------------------------------
        indicator : text
        filter_description : text, optional
        emission_wavelength_in_nm : numeric, optional
    }

    class LightSource{
        <<Device>>

        --------------------------------------
        attributes
        --------------------------------------
        model : text, optional
        filter_description : text, optional
        excitation_wavelength_in_nm : numeric, optional
        peak_power_in_W : numeric, optional
        peak_pulse_energy_in_J : numeric, optional
        intensity_in_W_per_m2 : numeric, optional
        exposure_time_in_s : numeric, optional
        pulse_rate_in_Hz : numeric, optional
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
    MicroscopySeries ..> LightSource : links
    MicroscopySeries ..> MicroscopyOpticalChannel : links
```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
