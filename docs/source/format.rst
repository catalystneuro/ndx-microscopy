*******
Format
*******


The ndx-microscopy extension defines several neurodata types to represent microscopy data and metadata in a standardized way.

Neurodata Types
-------------

Microscope
^^^^^^^^^
A device for acquiring imaging data.

.. code-block:: yaml

    groups:
      - neurodata_type_def: Microscope
        neurodata_type_inc: Device
        doc: A microscope used to acquire imaging data.
        attributes:
          - name: model
            dtype: text
            doc: Model identifier of the microscope.
            required: false

Light Path Components
^^^^^^^^^^^^^^^^^^

ExcitationLightPath
""""""""""""""""""
Represents the excitation light path that illuminates an imaging space.

.. code-block:: yaml

    groups:
      - neurodata_type_def: ExcitationLightPath
        neurodata_type_inc: LabMetaData
        doc: Excitation light path that illuminates an imaging space.
        attributes:
          - name: excitation_wavelength_in_nm
            dtype: numeric
            doc: Excitation wavelength of light, in nanometers.
          - name: excitation_mode
            dtype: text
            doc: The type of excitation used in the light path (e.g., 'one-photon', 'two-photon', 'three-photon', 'other').
          - name: description
            dtype: text
            doc: Description of the excitation light path.
        links:
          - name: excitation_source
            target_type: ExcitationSource
            doc: Link to ExcitationSource object which contains metadata about the excitation source device. If it is a pulsed excitation source link a PulsedExcitationSource object.
            quantity: '?'
          - name: excitation_filter
            target_type: OpticalFilter
            doc: Link to OpticalFilter object which contains metadata about the optical filter in this excitation light path. It can be either a BandOpticalFilter (e.g., 'Bandpass', 'Bandstop', 'Longpass', 'Shortpass') or a EdgeOpticalFilter (Longpass or Shortpass).
            quantity: '?'
          - name: dichroic_mirror
            target_type: DichroicMirror
            doc: Link to DichroicMirror object which contains metadata about the dichroic mirror in the excitation light path.
            quantity: '?'

EmissionLightPath
"""""""""""""""
Represents the emission light path from an imaging space.

.. code-block:: yaml

    groups:
      - neurodata_type_def: EmissionLightPath
        neurodata_type_inc: LabMetaData
        doc: Emission light path from an imaging space.
        attributes:
          - name: emission_wavelength_in_nm
            dtype: numeric
            doc: Emission wavelength of light, in nanometers.
          - name: description
            dtype: text
            doc: Description of the emission light path.
        groups:
          - neurodata_type_inc: Indicator
            doc: Indicator object which contains metadata about the indicator used in this light path.
            quantity: 1
        links:
          - name: photodetector
            target_type: Photodetector
            doc: Link to Photodetector object which contains metadata about the photodetector device.
            quantity: '?'
          - name: emission_filter
            target_type: OpticalFilter
            doc: Link to OpticalFilter object which contains metadata about the optical filter in this emission light path. It can be either a BandOpticalFilter (e.g., 'Bandpass', 'Bandstop', 'Longpass', 'Shortpass') or a EdgeOpticalFilter (Longpass or Shortpass).
            quantity: '?'
          - name: dichroic_mirror
            target_type: DichroicMirror
            doc: Link to DichroicMirror object which contains metadata about the dichroic mirror in the emission light path.
            quantity: '?'

Imaging Spaces
^^^^^^^^^^^^

ImagingSpace
"""""""""""
Base type for metadata about the region being imaged.

.. code-block:: yaml

    groups:
      - neurodata_type_def: ImagingSpace
        neurodata_type_inc: NWBContainer
        doc: Metadata about the region of physical space that imaging data was recorded from.
        datasets:
          - name: description
            dtype: text
            doc: Description of the imaging space.
          - name: origin_coordinates
            dtype: float64
            dims:
              - - x, y, z
            shape:
              - - 3
            doc: Physical location in stereotactic coordinates for the first element of the grid.
              See reference_frame to determine what the coordinates are relative to (e.g., bregma).
            quantity: '?'
            attributes:
              - name: unit
                dtype: text
                default_value: micrometers
                doc: Measurement units for origin coordinates. The default value is 'micrometers'.
        attributes:
          - name: location
            dtype: text
            doc: General estimate of location in the brain being subset by this space.
              Specify the area, layer, etc.
              Use standard atlas names for anatomical regions when possible.
              Specify 'whole brain' if the entire brain is strictly contained within the space.
            required: false

PlanarImagingSpace
""""""""""""""""
For 2D imaging planes.

.. code-block:: yaml

    groups:
      - neurodata_type_def: PlanarImagingSpace
        neurodata_type_inc: ImagingSpace
        doc: Metadata about the 2-dimensional slice of physical space that imaging data was recorded from.
        datasets:
          - name: grid_spacing_in_um
            dtype: float64
            dims:
              - - x, y
            shape:
              - - 2
            doc: Amount of space between pixels in micrometers.
            quantity: '?'
        attributes:
          - name: reference_frame
            dtype: text
            doc: Describes the reference frame of origin_coordinates and grid_spacing.
              For example, this can be a text description of the anatomical location and orientation of the grid
              defined by origin_coords and grid_spacing or the vectors needed to transform or rotate the grid to
              a common anatomical axis (e.g., AP/DV/ML).
              This field is necessary to interpret origin_coords and grid_spacing.
              If origin_coords and grid_spacing are not present, then this field is not required.
              For example, if the microscope returns 10 x 10 images, where the first value of the data matrix
              (index (0, 0)) corresponds to (-1.2, -0.6, -2) mm relative to bregma, the spacing between pixels is 0.2 mm in
              x, 0.2 mm in y and 0.5 mm in z, and larger numbers in x means more anterior, larger numbers in y means more
              rightward, and larger numbers in z means more ventral, then enter the following --
              origin_coords = (-1.2, -0.6, -2)
              grid_spacing = (0.2, 0.2)
              reference_frame = "Origin coordinates are relative to bregma. First dimension corresponds to anterior-posterior
              axis (larger index = more anterior). Second dimension corresponds to medial-lateral axis (larger index = more
              rightward). Third dimension corresponds to dorsal-ventral axis (larger index = more ventral)."
            required: false

VolumetricImagingSpace
""""""""""""""""""""
For 3D imaging volumes.

.. code-block:: yaml

    groups:
      - neurodata_type_def: VolumetricImagingSpace
        neurodata_type_inc: ImagingSpace
        doc: Metadata about the 3-dimensional region of physical space that imaging data was recorded from.
        datasets:
          - name: grid_spacing_in_um
            dtype: float64
            dims:
              - - x, y, z
            shape:
              - - 3
            doc: Amount of space between voxels in micrometers.
            quantity: '?'
        attributes:
          - name: reference_frame
            dtype: text
            doc: Describes the reference frame of origin_coordinates and grid_spacing.
              For example, this can be a text description of the anatomical location and orientation of the grid
              defined by origin_coords and grid_spacing or the vectors needed to transform or rotate the grid to
              a common anatomical axis (e.g., AP/DV/ML).
              This field is necessary to interpret origin_coords and grid_spacing.
              If origin_coords and grid_spacing are not present, then this field is not required.
              For example, if the microscope returns 10 x 10 x 2 images, where the first value of the data matrix
              (index (0, 0, 0)) corresponds to (-1.2, -0.6, -2) mm relative to bregma, the spacing between pixels is 0.2 mm in
              x, 0.2 mm in y and 0.5 mm in z, and larger numbers in x means more anterior, larger numbers in y means more
              rightward, and larger numbers in z means more ventral, then enter the following --
              origin_coords = (-1.2, -0.6, -2)
              grid_spacing = (0.2, 0.2, 0.5)
              reference_frame = "Origin coordinates are relative to bregma. First dimension corresponds to anterior-posterior
              axis (larger index = more anterior). Second dimension corresponds to medial-lateral axis (larger index = more
              rightward). Third dimension corresponds to dorsal-ventral axis (larger index = more ventral)."
            required: false

Microscopy Data Series
^^^^^^^^^^^^^^^^^^^

MicroscopySeries
"""""""""""""""
Base type for microscopy time series data.

.. code-block:: yaml

    groups:
      - neurodata_type_def: MicroscopySeries
        neurodata_type_inc: TimeSeries
        doc: Imaging data acquired over time from an optical channel in a microscope while a light source illuminates the
          imaging space.
        links:
          - name: microscope
            doc: Link to a Microscope object containing metadata about the device used to acquire this imaging data.
            target_type: Microscope
          - name: excitation_light_path
            doc: Link to a ExcitationLightPath object containing metadata about the device used to illuminate the imaging space.
            target_type: LabMetaData
          - name: emission_light_path
            doc: Link to a EmissionLightPath object containing metadata about the indicator and filters used to collect
              this data.
            target_type: LabMetaData

PlanarMicroscopySeries
""""""""""""""""""""
For 2D time series data.

.. code-block:: yaml

    groups:
      - neurodata_type_def: PlanarMicroscopySeries
        neurodata_type_inc: MicroscopySeries
        doc: Imaging data acquired over time from an optical channel in a microscope while a light source illuminates a
          planar imaging space.
        datasets:
          - name: data
            doc: Recorded imaging data, shaped by (number of frames, frame height, frame width).
            dtype: numeric
            dims:
              - frames
              - height
              - width
            shape:
              - null
              - null
              - null
        groups:
          - neurodata_type_inc: PlanarImagingSpace
            doc: PlanarImagingSpace object containing metadata about the region of physical space this imaging data
              was recorded from.

VariableDepthMicroscopySeries
""""""""""""""""""""""""""
For 2D time series data with variable depth.

.. code-block:: yaml

    groups:
      - neurodata_type_def: VariableDepthMicroscopySeries
        neurodata_type_inc: PlanarMicroscopySeries
        doc: Volumetric imaging data acquired over an irregular number and amount of depths; for instance, when using an
          electrically tunable lens.
        datasets:
          - name: depth_per_frame_in_um
            doc: Depth in micrometers of each frame in the data array.
              These values offset the 'z' value of the `origin_coordinates` of the linked `imaging_space` object.
            dtype: numeric
            dims:
              - frames
            shape:
              - null

VolumetricMicroscopySeries
"""""""""""""""""""""""""
For 3D time series data.

.. code-block:: yaml

    groups:
      - neurodata_type_def: VolumetricMicroscopySeries
        neurodata_type_inc: MicroscopySeries
        doc: Volumetric imaging data acquired over time from an optical channel in a microscope while a light source
          illuminates a volumetric imaging space.
          Assumes the number of depth scans used to construct the volume is regular.
        datasets:
          - name: data
            doc: Recorded imaging data, shaped by (number of frames, frame height, frame width, number of depth planes).
            dtype: numeric
            dims:
              - frames
              - height
              - width
              - depths
            shape:
              - null
              - null
              - null
              - null
        groups:
          - neurodata_type_inc: VolumetricImagingSpace
            doc: VolumetricImagingSpace object containing metadata about the region of physical space this imaging data
              was recorded from.

Segmentation Types
^^^^^^^^^^^^^^^

MicroscopySegmentations
"""""""""""""""""""""
Container for segmentation data.

.. code-block:: yaml

    groups:
      - neurodata_type_def: MicroscopySegmentations
        neurodata_type_inc: NWBDataInterface
        default_name: MicroscopySegmentations
        doc: Stores pixels in an image that represent different regions of interest (ROIs)
          or masks. All segmentation for a given imaging plane is stored together, with
          storage for multiple imaging planes (masks) supported. Each ROI is stored in its
          own subgroup, with the ROI group containing both a 2D mask and a list of pixels
          that make up this mask. Segments can also be used for masking neuropil. If segmentation
          is allowed to change with time, a new imaging plane (or module) is required and
          ROI names should remain consistent between them.
        groups:
          - neurodata_type_inc: MicroscopyPlaneSegmentation
            doc: Results from image segmentation of a specific imaging plane.
            quantity: '+'

MicroscopyPlaneSegmentation
"""""""""""""""""""""""""
Detailed segmentation for a single imaging plane.

.. code-block:: yaml

    groups:
      - neurodata_type_def: MicroscopyPlaneSegmentation
        neurodata_type_inc: DynamicTable
        doc: Results from image segmentation of a specific imaging plane.
        datasets:
          - name: image_mask
            neurodata_type_inc: VectorData
            dims:
              - - num_roi
                - num_x
                - num_y
              - - num_roi
                - num_x
                - num_y
                - num_z
            shape:
              - - null
                - null
                - null
              - - null
                - null
                - null
                - null
            doc: ROI masks for each ROI. Each image mask is the size of the original imaging
              plane (or volume) and members of the ROI are finite non-zero.
            quantity: '?'
          - name: pixel_mask_index
            neurodata_type_inc: VectorIndex
            doc: Index into pixel_mask.
            quantity: '?'
          - name: pixel_mask
            neurodata_type_inc: VectorData
            dtype:
              - name: x
                dtype: uint32
                doc: Pixel x-coordinate.
              - name: y
                dtype: uint32
                doc: Pixel y-coordinate.
              - name: weight
                dtype: float32
                doc: Weight of the pixel.
            doc: 'Pixel masks for each ROI: a list of indices and weights for the ROI. Pixel
              masks are concatenated and parsing of this dataset is maintained by the PlaneSegmentation'
            quantity: '?'
          - name: voxel_mask_index
            neurodata_type_inc: VectorIndex
            doc: Index into voxel_mask.
            quantity: '?'
          - name: voxel_mask
            neurodata_type_inc: VectorData
            dtype:
              - name: x
                dtype: uint32
                doc: Voxel x-coordinate.
              - name: y
                dtype: uint32
                doc: Voxel y-coordinate.
              - name: z
                dtype: uint32
                doc: Voxel z-coordinate.
              - name: weight
                dtype: float32
                doc: Weight of the voxel.
            doc: 'Voxel masks for each ROI: a list of indices and weights for the ROI. Voxel
              masks are concatenated and parsing of this dataset is maintained by the PlaneSegmentation'
            quantity: '?'
        groups:
          - name: summary_images
            doc: Summary images that are related to the plane segmentation, e.g., mean, correlation, maximum projection.
            groups:
              - neurodata_type_inc: Images
                doc: An container for the estimated summary images.
                quantity: '*'
          - neurodata_type_inc: ImagingSpace
            doc: ImagingSpace object from which this data was generated.

Multi-Channel Data
^^^^^^^^^^^^^^^

MultiChannelMicroscopyVolume
""""""""""""""""""""""""""
For static multi-channel volumetric data.

.. code-block:: yaml

    groups:
      - neurodata_type_def: MultiChannelMicroscopyVolume
        neurodata_type_inc: NWBDataInterface
        doc: Static (not time-varying) volumetric imaging data acquired from multiple optical channels.
        attributes:
          - name: description
            dtype: text
            doc: Description of the MultiChannelVolume.
            required: false
          - name: unit
            dtype: text
            doc: Base unit of measurement for working with the data. Actual stored values are
              not necessarily stored in these units. To access the data in these units,
              multiply 'data' by 'conversion' and add 'offset'.
          - name: conversion
            dtype: float32
            default_value: 1.0
            doc: Scalar to multiply each element in data to convert it to the specified 'unit'.
              If the data are stored in acquisition system units or other units
              that require a conversion to be interpretable, multiply the data by 'conversion'
              to convert the data to the specified 'unit'.
            required: false
          - name: offset
            dtype: float32
            default_value: 0.0
            doc: Scalar to add to the data after scaling by 'conversion' to finalize its coercion
              to the specified 'unit'.
            required: false
        datasets:
          - name: data
            doc: Recorded imaging data, shaped by (frame height, frame width, number of depth planes, number of optical channels).
            dtype: numeric
            dims:
              - height
              - width
              - depths
              - emission_light_paths
            shape:
              - null
              - null
              - null
              - null
          - name: excitation_light_paths
            doc: An ordered list of references to ExcitationLightPath objects containing metadata about the excitation methods.
            neurodata_type_inc: VectorData
            dtype:
              reftype: object
              target_type: LabMetaData
            dims:
              - excitation_light_paths
            shape:
              - null
          - name: emission_light_paths
            doc: An ordered list of references to EmissionLightPath objects containing metadata about the indicator and filters used to collect this data.
            neurodata_type_inc: VectorData
            dtype:
              reftype: object
              target_type: LabMetaData
            dims:
              - emission_light_paths
            shape:
              - null
        links:
          - name: microscope
            doc: Link to a Microscope object containing metadata about the device used to acquire this imaging data.
            target_type: Microscope
        groups:
          - neurodata_type_inc: VolumetricImagingSpace
            doc: VolumetricImagingSpace object containing metadata about the region of physical space this imaging data was recorded from.

VariableDepthMultiChannelMicroscopyVolume
"""""""""""""""""""""""""""""""""""""""
For static multi-channel volumetric data with irregular depth spacing.

.. code-block:: yaml

    groups:
      - neurodata_type_def: VariableDepthMultiChannelMicroscopyVolume
        neurodata_type_inc: NWBDataInterface
        doc: Static (not time-varying) irregularly spaced volumetric imaging data acquired from multiple optical channels.
        attributes:
          - name: description
            dtype: text
            doc: Description of the VariableDepthMultiChannelMicroscopyVolume.
            required: false
          - name: unit
            dtype: text
            doc: Base unit of measurement for working with the data.
          - name: conversion
            dtype: float32
            default_value: 1.0
            doc: Scalar to multiply each element in data to convert it to the specified 'unit'.
            required: false
          - name: offset
            dtype: float32
            default_value: 0.0
            doc: Scalar to add to the data after scaling by 'conversion'.
            required: false
        datasets:
          - name: data
            doc: Recorded imaging data, shaped by (frame height, frame width, number of depth planes, number of optical channels).
            dtype: numeric
            dims:
              - height
              - width
              - depths
              - channels
            shape:
              - null
              - null
              - null
              - null
          - name: depth_per_frame_in_um
            doc: Depth in micrometers of each frame in the data array.
            dtype: numeric
            dims:
              - depths
            shape:
              - null
          - name: excitation_light_paths
            doc: An ordered list of references to ExcitationLightPath objects containing metadata about the excitation methods.
            neurodata_type_inc: VectorData
            dtype:
              reftype: object
              target_type: LabMetaData
            dims:
              - excitation_light_paths
            shape:
              - null
          - name: emission_light_paths
            doc: An ordered list of references to EmissionLightPath objects containing metadata about the indicator and filters used to collect this data.
            neurodata_type_inc: VectorData
            dtype:
              reftype: object
              target_type: LabMetaData
            dims:
              - emission_light_paths
            shape:
              - null
        links:
          - name: microscope
            doc: Link to a Microscope object containing metadata about the device used to acquire this imaging data.
            target_type: Microscope
        groups:
          - neurodata_type_inc: VolumetricImagingSpace
            doc: VolumetricImagingSpace object containing metadata about the region of physical space this imaging data was recorded from.

Response Data
^^^^^^^^^^^

MicroscopyResponseSeries
""""""""""""""""""""""
For extracted ROI responses.

.. code-block:: yaml

    groups:
      - neurodata_type_def: MicroscopyResponseSeries
        neurodata_type_inc: TimeSeries
        doc: ROI response time series.
        datasets:
          - name: data
            dtype: numeric
            dims:
              - frames
              - rois
            shape:
              - null
              - null
            doc: Response data (frames x ROIs).
          - name: table_region
            neurodata_type_inc: DynamicTableRegion
            doc: Reference to segmentation table.
