.. _user_guide:

**********
User Guide
**********

This guide provides detailed information about using the ndx-microscopy extension effectively.

Core Concepts
-----------

Device Components
^^^^^^^^^^^^^^^

The primary device component is the Microscope class:

.. code-block:: python

    microscope = Microscope(
        name='2p-scope',
        description='Custom two-photon microscope'
        manufacturer='Company X'
        model='Model Y'
    )
    nwbfile.add_device(microscope)

Other optical components (filters, sources, detectors) are provided by the ndx-ophys-devices extension.

Light Path Configuration
^^^^^^^^^^^^^^^^^^^^^

Light paths define how light travels through the microscope:

1. **ExcitationLightPath**: Defines illumination pathway

   .. code-block:: python

       excitation = ExcitationLightPath(
           name='2p_excitation',
           description='Two-photon excitation path',
           excitation_source=laser,          # from ndx-ophys-devices
           excitation_filter=ex_filter,      # from ndx-ophys-devices
           dichroic_mirror=dichroic         # from ndx-ophys-devices
       )

2. **EmissionLightPath**: Defines collection pathway

   .. code-block:: python

       emission = EmissionLightPath(
           name='gcamp_emission',
           description='GCaMP6f emission path',
           indicator=indicator,              # from ndx-ophys-devices
           photodetector=detector,           # from ndx-ophys-devices
           emission_filter=em_filter,        # from ndx-ophys-devices
           dichroic_mirror=dichroic         # from ndx-ophys-devices
       )

Imaging Space Definition
^^^^^^^^^^^^^^^^^^^^^

Imaging spaces define the physical region being imaged:

1. **PlanarImagingSpace**: For 2D imaging

   .. code-block:: python

       space_2d = PlanarImagingSpace(
           name='cortex_plane',
           description='Layer 2/3 of visual cortex',
           grid_spacing_in_um=[1.0, 1.0],        # x, y spacing
           origin_coordinates=[-1.2, -0.6, -2.0], # relative to bregma
           location='Visual cortex',
           reference_frame='bregma',
           orientation='RAS'                      # Right-Anterior-Superior
       )

2. **VolumetricImagingSpace**: For 3D imaging

   .. code-block:: python

       space_3d = VolumetricImagingSpace(
           name='cortex_volume',
           description='Visual cortex volume',
           grid_spacing_in_um=[1.0, 1.0, 2.0],   # x, y, z spacing
           origin_coordinates=[-1.2, -0.6, -2.0],
           location='Visual cortex',
           reference_frame='bregma',
           orientation='RAS'
       )

Common Workflows
-------------

2D Imaging
^^^^^^^^^

Basic workflow for 2D imaging:

.. code-block:: python

    # 1. Set up imaging space
    planar_imaging_space = PlanarImagingSpace(
        name='cortex_plane',
        description='Layer 2/3 of visual cortex',
        grid_spacing_in_um=[1.0, 1.0],        # x, y spacing
        origin_coordinates=[-1.2, -0.6, -2.0], # relative to bregma
        location='Visual cortex',
        reference_frame='bregma',
        orientation='RAS'                      # Right-Anterior-Superior
    )

    # 2. Create imaging series
    microscopy_series = PlanarMicroscopySeries(
        name='microscopy_series',
        description='Two-photon calcium imaging',
        microscope=microscope,
        excitation_light_path=excitation,
        emission_light_path=emission,
        planar_imaging_space=planar_imaging_space,
        data=data,                # [frames, height, width]
        unit='a.u.',
        rate=30.0,
        starting_time=0.0,
    )
    nwbfile.add_acquisition(microscopy_series)

3D Imaging
^^^^^^^^^

Workflow for volumetric imaging:

.. code-block:: python

    # 1. Set up volumetric space
    volumetric_imaging_space = VolumetricImagingSpace(
        name='cortex_volume',
        description='Visual cortex volume',
        grid_spacing_in_um=[1.0, 1.0, 2.0],   # x, y, z spacing
        origin_coordinates=[-1.2, -0.6, -2.0],
        location='Visual cortex',
        reference_frame='bregma',
        orientation='RAS'
    )

    # 2. Create volumetric series
    volume_series = VolumetricMicroscopySeries(
        name='volume_data',
        microscope=microscope,
        excitation_light_path=excitation,
        emission_light_path=emission,
        volumetric_imaging_space=volumetric_imaging_space,
        data=data,                # [frames, height, width, depths]
        unit='a.u.',
        rate=5.0,
        starting_time=0.0,
    )
    nwbfile.add_acquisition(volume_series)

ROI Segmentation
^^^^^^^^^^^^^

Workflow for ROI segmentation:

.. code-block:: python

    # 1. Create summary images
    mean_image = SummaryImage(
        name='mean',
        description='Mean intensity projection',
        data=np.mean(data, axis=0)
    )

    # 2. Create segmentation
    segmentation = Segmentation2D(
        name='rois',
        description='Manual ROI segmentation',
        planar_imaging_space=imaging_space,
        summary_images=[mean_image]
    )

    # 3. Add ROIs using image masks
    roi_mask = np.zeros((height, width), dtype=bool)
    roi_mask[256:266, 256:266] = True
    segmentation.add_roi(image_mask=roi_mask)

    # 4. Add ROIs using pixel masks
    pixel_mask = [
        [100, 100, 1.0],  # x, y, weight
        [101, 100, 1.0],
        [102, 100, 1.0]
    ]
    segmentation.add_roi(pixel_mask=pixel_mask)

Response Data Storage
^^^^^^^^^^^^^^^^^

Workflow for storing ROI responses:

.. code-block:: python

    # 1. Create ROI region
    roi_region = segmentation.create_roi_table_region(
        description='All ROIs',
        region=list(range(len(segmentation.id)))
    )

    # 2. Create response series
    response_series = MicroscopyResponseSeries(
        name='roi_responses',
        description='Fluorescence responses',
        data=responses,
        rois=roi_region,
        unit='n.a.',
        rate=30.0,
        starting_time=0.0,
    )

Best Practices
-----------

Data Organization
^^^^^^^^^^^^^

1. **Naming Conventions**
   - Use descriptive, consistent names
   - Include relevant metadata in descriptions
   - Document coordinate systems and reference frames

2. **Data Structure**
   - Group related data appropriately
   - Maintain clear relationships between raw and processed data
   - Include all necessary metadata
   
