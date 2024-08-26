"""Test roundtrip (write and read back) of the Python API for the ndx-microscopy extension."""

import pytest
from pynwb.testing import TestCase as pynwb_TestCase
from pynwb.testing.mock.file import mock_NWBFile

import pynwb
from ndx_microscopy.testing import (
    mock_EmissionLightPath,
    mock_ExcitationLightPath,
    mock_Microscope,
    mock_MicroscopyPlaneSegmentation,
    mock_MicroscopySegmentations,
    mock_MultiChannelMicroscopyVolume,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
)


class TestPlanarMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for PlanarMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_planar_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        excitation_light_path = mock_ExcitationLightPath(name="ExcitationLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_spacec()

        emission_light_path = mock_EmissionLightPath(name="EmissionLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        planar_microscopy_series = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            imaging_space=imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=planar_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["PlanarImagingSpace"])
            self.assertContainerEqual(emission_light_path, read_nwbfile.lab_meta_data["EmissionLightPath"])

            self.assertContainerEqual(planar_microscopy_series, read_nwbfile.acquisition["PlanarMicroscopySeries"])


class TestVolumetricMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VolumetricMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_volumetric_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        excitation_light_path = mock_ExcitationLightPath(name="ExcitationLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        imaging_space = mock_VolumetricImagingSpace(name="VolumetricImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_spacec()

        emission_light_path = mock_EmissionLightPath(name="EmissionLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        volumetric_microscopy_series = mock_VolumetricMicroscopySeries(
            name="VolumetricMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            imaging_space=imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=volumetric_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["VolumetricImagingSpace"])
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
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        excitation_light_path = mock_ExcitationLightPath(name="ExcitationLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path)

        imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_space()

        emission_light_path = mock_EmissionLightPath(name="EmissionLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path)

        variable_depth_microscopy_series = mock_VariableDepthMicroscopySeries(
            name="VariableDepthMicroscopySeries",
            microscope=microscope,
            excitation_light_path=excitation_light_path,
            imaging_space=imaging_space,
            emission_light_path=emission_light_path,
        )
        nwbfile.add_acquisition(nwbdata=variable_depth_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(excitation_light_path, read_nwbfile.lab_meta_data["ExcitationLightPath"])
            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["PlanarImagingSpace"])
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
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        imaging_space = mock_VolumetricImagingSpace(name="VolumetricImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_space()

        excitation_light_paths = list()
        excitation_light_path_0 = mock_ExcitationLightPath(name="ExcitationLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=excitation_light_path_0)
        excitation_light_paths.append(excitation_light_path_0)

        emission_light_paths = list()
        emission_light_path_0 = mock_EmissionLightPath(name="EmissionLightPath")
        nwbfile.add_lab_meta_data(lab_meta_data=emission_light_path_0)
        emission_light_paths.append(emission_light_path_0)

        # TODO: It might be more convenient in Python to have a custom constructor that takes in a list of
        # light sources and optical channels and does the VectorData wrapping internally
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
            imaging_space=imaging_space,
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
            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["VolumetricImagingSpace"])
            self.assertContainerEqual(emission_light_path_0, read_nwbfile.lab_meta_data["EmissionLightPath"])

            self.assertContainerEqual(
                multi_channel_microscopy_volume, read_nwbfile.acquisition["MultiChannelMicroscopyVolume"]
            )


class TestMicroscopySegmentationsSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MicroscopySegmentations."""

    def setUp(self):
        self.nwbfile_path = "test_microscopy_segmentations_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_space()

        plane_segmentation_1 = mock_MicroscopyPlaneSegmentation(
            imaging_space=imaging_space, name="MicroscopyPlaneSegmentation1"
        )
        plane_segmentation_2 = mock_MicroscopyPlaneSegmentation(
            imaging_space=imaging_space, name="MicroscopyPlaneSegmentation2"
        )
        microscopy_plane_segmentations = [plane_segmentation_1, plane_segmentation_2]

        segmentations = mock_MicroscopySegmentations(
            name="MicroscopySegmentations", microscopy_plane_segmentations=microscopy_plane_segmentations
        )
        processing_module = nwbfile.create_processing_module(name="ophys", description="")
        processing_module.add(segmentations)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["PlanarImagingSpace"])

            self.assertContainerEqual(segmentations, read_nwbfile.processing["ophys"]["MicroscopySegmentations"])


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
