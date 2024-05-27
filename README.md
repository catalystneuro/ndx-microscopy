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
        datasets
        --------------------------------------
        microscopy_table_region : DynamicTableRegion
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
        depth_per_frame : numeric, length of frames
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

    class MicroscopyTable{
        <<DynamicTable>>

        --------------------------------------
        datasets
        --------------------------------------
        VectorData :
        - location : text, optional
        - coordinates : numeric, length 2, optional
        --> unit : text, default="micrometers"
        - indicator : Indicator
        - notes : text, optional
        - microscope : Microscope
        - excitation_source : ExcitationSource
        - photodetector : Photodetector
        - dichroic_mirror : DichroicMirror
        - emission_filter : OpticalFilter
        - excitation_filter : OpticalFilter
        - objective_lens : ObjectiveLens
    }

    class Microscopy{
        <<LabMetaData>>

        --------------------------------------
        groups
        --------------------------------------
        microscopy_table : MicroscopyTable
    }

    PlanarMicroscopySeries *-- MicroscopySeries : extends
    PlanarMicroscopySeries -- PlanarImagingSpace : links
    VariableDepthMicroscopySeries *-- MicroscopySeries : extends
    VariableDepthMicroscopySeries -- PlanarImagingSpace : links
    VolumetricMicroscopySeries *-- MicroscopySeries : extends
    VolumetricMicroscopySeries -- VolumetricImagingSpace : links
    PlanarImagingSpace *-- ImagingSpace : extends
    VolumetricImagingSpace *-- ImagingSpace : extends
    MicroscopySeries ..> MicroscopyTable : reference rows
    Microscopy ..> MicroscopyTable : links
```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
