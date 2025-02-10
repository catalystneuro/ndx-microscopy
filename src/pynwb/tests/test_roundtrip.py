"""Test roundtrip (write and read back) of the Python API for the ndx-microscopy extension."""

from datetime import datetime

from pytz import UTC
import pytest
from pynwb.testing import TestCase as pynwb_TestCase
from pynwb.testing.mock.file import mock_NWBFile

import pynwb
from ndx_ophys_devices.testing import (
    mock_ExcitationSource,
    mock_Photodetector,
    mock_OpticalFilter,
    mock_DichroicMirror,
    mock_Indicator,
)
from ndx_microscopy.testing import (
    mock_EmissionLightPath,
    mock_ExcitationLightPath,
    mock_Microscope,
    mock_Segmentation2D,
    mock_SegmentationContainer,
    mock_PlanarImagingSpace,
    mock_VolumetricImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VolumetricMicroscopySeries,
    mock_MultiChannelMicroscopyVolume,
    mock_MicroscopyResponseSeries,
)
from ndx_microscopy import MicroscopyResponseSeriesContainer


class TestPlanarMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for PlanarMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_planar_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        excitation_source = mock_ExcitationSource()
        nwbfile.add_device(devices=excitation_source)

        excitation_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=excitation_filter)

        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)

        excitation_light_path = mock_ExcitationLightPath(
            name="ExcitationLightPath",
            excitation_source=excitation_source,
            excitation_filter=excitation_filter,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace")

        photodetector = mock_Photodetector()
        nwbfile.add_device(devices=photodetector)

        emission_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=emission_filter)

        emission_light_path = mock_EmissionLightPath(
            name="EmissionLightPath",
            emission_filter=emission_filter,
            photodetector=photodetector,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        planar_microscopy_series = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            planar_imaging_space=planar_imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=planar_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(emission_light_path, read_nwbfile.lab_meta_data["EmissionLightPath"])

            self.assertContainerEqual(planar_microscopy_series, read_nwbfile.acquisition["PlanarMicroscopySeries"])


class TestExcitationLightPathWithUntrackedDevice(pynwb_TestCase):
    """Test that creating an ExcitationLightPath with a device that hasn't been added to the NWBFile raises an error."""

    def setUp(self):
        self.nwbfile_path = "test_excitation_light_path_without_device.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        from hdmf.build.errors import OrphanContainerBuildError

        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        # Create all devices first
        excitation_source = mock_ExcitationSource()
        excitation_filter = mock_OpticalFilter()
        photodetector = mock_Photodetector()
        emission_filter = mock_OpticalFilter()

        # Add all devices except excitation_source to test error handling
        nwbfile.add_device(devices=excitation_filter)
        nwbfile.add_device(devices=photodetector)
        nwbfile.add_device(devices=emission_filter)

        # Create imaging space
        planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace")

        # Create light paths
        emission_light_path = mock_EmissionLightPath(
            name="EmissionLightPath", emission_filter=emission_filter, photodetector=photodetector
        )
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        # Create excitation light path with untracked excitation_source - should fail
        excitation_light_path = mock_ExcitationLightPath(
            name="ExcitationLightPath",
            excitation_source=excitation_source,  # Using device that wasn't added to nwbfile
            excitation_filter=excitation_filter,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        planar_microscopy_series = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            planar_imaging_space=planar_imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=planar_microscopy_series)

        with pytest.raises(OrphanContainerBuildError):
            with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
                io.write(nwbfile)


class TestVolumetricMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VolumetricMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_volumetric_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        excitation_source = mock_ExcitationSource()
        nwbfile.add_device(devices=excitation_source)

        excitation_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=excitation_filter)

        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)

        excitation_light_path = mock_ExcitationLightPath(
            name="ExcitationLightPath",
            excitation_source=excitation_source,
            excitation_filter=excitation_filter,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        volumetric_imaging_space = mock_VolumetricImagingSpace(name="VolumetricImagingSpace")

        photodetector = mock_Photodetector()
        nwbfile.add_device(devices=photodetector)

        emission_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=emission_filter)

        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)

        emission_light_path = mock_EmissionLightPath(
            name="EmissionLightPath",
            emission_filter=emission_filter,
            photodetector=photodetector,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        volumetric_microscopy_series = mock_VolumetricMicroscopySeries(
            name="VolumetricMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            volumetric_imaging_space=volumetric_imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=volumetric_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(emission_light_path, read_nwbfile.lab_meta_data["EmissionLightPath"])

            self.assertContainerEqual(
                volumetric_microscopy_series, read_nwbfile.acquisition["VolumetricMicroscopySeries"]
            )


class TestVariableDepthMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VariableDepthMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_variable_depth_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        excitation_source = mock_ExcitationSource()
        nwbfile.add_device(devices=excitation_source)

        excitation_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=excitation_filter)

        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)

        excitation_light_path = mock_ExcitationLightPath(
            name="ExcitationLightPath",
            excitation_source=excitation_source,
            excitation_filter=excitation_filter,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace")

        photodetector = mock_Photodetector()
        nwbfile.add_device(devices=photodetector)

        emission_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=emission_filter)

        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)

        emission_light_path = mock_EmissionLightPath(
            name="EmissionLightPath",
            emission_filter=emission_filter,
            photodetector=photodetector,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        variable_depth_microscopy_series = mock_VariableDepthMicroscopySeries(
            name="VariableDepthMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            planar_imaging_space=planar_imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=variable_depth_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(emission_light_path, read_nwbfile.lab_meta_data["EmissionLightPath"])

            self.assertContainerEqual(
                variable_depth_microscopy_series, read_nwbfile.acquisition["VariableDepthMicroscopySeries"]
            )


class TestMultiChannelMicroscopyVolumeSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MultiChannelMicroscopyVolume."""

    def setUp(self):
        self.nwbfile_path = "test_multi_channel_microscopy_volume_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        volumetric_imaging_space = mock_VolumetricImagingSpace(name="VolumetricImagingSpace")

        excitation_light_paths = list()
        excitation_source = mock_ExcitationSource()
        nwbfile.add_device(devices=excitation_source)
        excitation_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=excitation_filter)
        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)
        excitation_light_path_0 = mock_ExcitationLightPath(
            name="ExcitationLightPath",
            excitation_source=excitation_source,
            excitation_filter=excitation_filter,
            dichroic_mirror=dichroic_mirror,
        )
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path_0)
        excitation_light_paths.append(excitation_light_path_0)

        emission_light_paths = list()
        photodetector = mock_Photodetector()
        nwbfile.add_device(devices=photodetector)
        emission_filter = mock_OpticalFilter()
        nwbfile.add_device(devices=emission_filter)
        dichroic_mirror = mock_DichroicMirror()
        nwbfile.add_device(devices=dichroic_mirror)
        emission_light_path_0 = mock_EmissionLightPath(
            name="EmissionLightPath",
            photodetector=photodetector,
            emission_filter=emission_filter,
            dichroic_mirror=dichroic_mirror,
            indicator=mock_Indicator(),
        )
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path_0)
        emission_light_paths.append(emission_light_path_0)

        # TODO: It might be more convenient in Python to have a custom constructor that takes in a list of
        # excitation light paths and emission light paths and does the VectorData wrapping internally
        excitation_light_paths_used_by_volume = pynwb.base.VectorData(
            name="excitation_light_paths",
            description="Light sources used by this MultiChannelVolume.",
            data=excitation_light_paths,
        )
        emission_light_paths_used_by_volume = pynwb.base.VectorData(
            name="emission_light_paths",
            description=(
                "Optical channels ordered to correspond to the third axis (e.g., [0, 0, :, 0]) "
                "of the data for this MultiChannelVolume."
            ),
            data=emission_light_paths,
        )
        multi_channel_microscopy_volume = mock_MultiChannelMicroscopyVolume(
            name="MultiChannelMicroscopyVolume",
            microscope=microscope,
            volumetric_imaging_space=volumetric_imaging_space,
            excitation_light_paths=excitation_light_paths_used_by_volume,
            emission_light_paths=emission_light_paths_used_by_volume,
        )
        nwbfile.add_acquisition(nwbdata=multi_channel_microscopy_volume)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path_0, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(emission_light_path_0, read_nwbfile.lab_meta_data["EmissionLightPath"])

            self.assertContainerEqual(
                multi_channel_microscopy_volume, read_nwbfile.acquisition["MultiChannelMicroscopyVolume"]
            )


class TestSegmentationContainerSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for SegmentationContainer."""

    def setUp(self):
        self.nwbfile_path = "test_segmentation_container_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        container = mock_SegmentationContainer(name="SegmentationContainer")
        ophys_module = nwbfile.create_processing_module(name="ophys", description="")
        ophys_module.add(container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(container, read_nwbfile.processing["ophys"]["SegmentationContainer"])


class TestMicroscopyResponseSeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MicroscopyResponseSeries."""

    def setUp(self):
        self.nwbfile_path = "test_microscopy_response_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace")

        segmentation_2D = mock_Segmentation2D(name="Segmentation2D", planar_imaging_space=planar_imaging_space)

        segmentation_container = mock_SegmentationContainer(
            name="SegmentationContainer", segmentations=[segmentation_2D]
        )
        ophys_module = nwbfile.create_processing_module(name="ophys", description="")
        ophys_module.add(segmentation_container)

        number_of_rois = 10
        plane_segmentation_region = pynwb.ophys.DynamicTableRegion(
            name="rois",  # Name must be exactly this
            description="",
            data=[x for x in range(number_of_rois)],
            table=segmentation_2D,
        )
        microscopy_response_series = mock_MicroscopyResponseSeries(
            name="MicroscopyResponseSeries",
            rois=plane_segmentation_region,
        )

        microscopy_response_series_container = MicroscopyResponseSeriesContainer(
            name="MicroscopyResponseSeriesContainer", microscopy_response_series=[microscopy_response_series]
        )
        ophys_module.add(microscopy_response_series_container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])
            self.assertContainerEqual(segmentation_container, read_nwbfile.processing["ophys"]["SegmentationContainer"])

            self.assertContainerEqual(
                microscopy_response_series_container,
                read_nwbfile.processing["ophys"]["MicroscopyResponseSeriesContainer"],
            )


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
