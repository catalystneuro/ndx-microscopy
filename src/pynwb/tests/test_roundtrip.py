"""Test roundtrip (write and read back) of the Python API for the ndx-microscopy extension."""

from pynwb.testing import TestCase as pynwb_TestCase
from pynwb.testing.mock.file import mock_NWBFile

import pynwb
from ndx_microscopy.testing import (
    mock_LightSource,
    mock_Microscope,
    mock_MicroscopyOpticalChannel,
    mock_PlanarImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_VariableDepthMicroscopySeries,
    mock_VolumetricImagingSpace,
    mock_VolumetricMicroscopySeries,
)


class TestPlanarMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for PlanarMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        light_source = mock_LightSource(name="LightSource")
        nwbfile.add_device(devices=light_source)

        imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_spacec()

        optical_channel = mock_MicroscopyOpticalChannel(name="MicroscopyOpticalChannel")
        nwbfile.add_lab_meta_data(lab_meta_data=optical_channel)

        planar_microscopy_series = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscope=microscope,
            light_source=light_source,
            imaging_space=imaging_space,
            optical_channel=optical_channel,
        )
        nwbfile.add_acquisition(nwbdata=planar_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])
            self.assertContainerEqual(light_source, read_nwbfile.devices["LightSource"])

            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["PlanarImagingSpace"])
            self.assertContainerEqual(optical_channel, read_nwbfile.lab_meta_data["MicroscopyOpticalChannel"])

            self.assertContainerEqual(planar_microscopy_series, read_nwbfile.acquisition["PlanarMicroscopySeries"])


class TestVolumetricMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VolumetricMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        light_source = mock_LightSource(name="LightSource")
        nwbfile.add_device(devices=light_source)

        imaging_space = mock_VolumetricImagingSpace(name="VolumetricImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_spacec()

        optical_channel = mock_MicroscopyOpticalChannel(name="MicroscopyOpticalChannel")
        nwbfile.add_lab_meta_data(lab_meta_data=optical_channel)

        volumetric_microscopy_series = mock_VolumetricMicroscopySeries(
            name="VolumetricMicroscopySeries",
            microscope=microscope,
            light_source=light_source,
            imaging_space=imaging_space,
            optical_channel=optical_channel,
        )
        nwbfile.add_acquisition(nwbdata=volumetric_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])
            self.assertContainerEqual(light_source, read_nwbfile.devices["LightSource"])

            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["VolumetricImagingSpace"])
            self.assertContainerEqual(optical_channel, read_nwbfile.lab_meta_data["MicroscopyOpticalChannel"])

            self.assertContainerEqual(
                volumetric_microscopy_series, read_nwbfile.acquisition["VolumetricMicroscopySeries"]
            )


class TestVariableDepthMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VariableDepthMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        light_source = mock_LightSource(name="LightSource")
        nwbfile.add_device(devices=light_source)

        imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_space()

        optical_channel = mock_MicroscopyOpticalChannel(name="MicroscopyOpticalChannel")
        nwbfile.add_lab_meta_data(lab_meta_data=optical_channel)

        variable_depth_microscopy_series = mock_VariableDepthMicroscopySeries(
            name="VariableDepthMicroscopySeries",
            microscope=microscope,
            light_source=light_source,
            imaging_space=imaging_space,
            optical_channel=optical_channel,
        )
        nwbfile.add_acquisition(nwbdata=variable_depth_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])
            self.assertContainerEqual(light_source, read_nwbfile.devices["LightSource"])

            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["PlanarImagingSpace"])
            self.assertContainerEqual(optical_channel, read_nwbfile.lab_meta_data["MicroscopyOpticalChannel"])

            self.assertContainerEqual(
                variable_depth_microscopy_series, read_nwbfile.acquisition["VariableDepthMicroscopySeries"]
            )


class TestMultiChannelMicroscopyVolumeSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MultiChannelMicroscopyVolume."""

    def setUp(self):
        self.nwbfile_path = "test.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile()

        microscope = mock_Microscope(name="Microscope")
        nwbfile.add_device(devices=microscope)

        light_source = mock_LightSource(name="LightSource")
        nwbfile.add_device(devices=light_source)

        imaging_space = mock_VolumetricImagingSpace(name="VolumetricImagingSpace", microscope=microscope)
        nwbfile.add_lab_meta_data(lab_meta_data=imaging_space)  # Would prefer .add_imaging_space()

        optical_channel = mock_MicroscopyOpticalChannel(name="MicroscopyOpticalChannel")
        nwbfile.add_lab_meta_data(lab_meta_data=optical_channel)

        multi_channel_microscopy_volume = mock_MultiChannelMicroscopyVolume(
            name="MultiChannelMicroscopyVolume",
            microscope=microscope,
            light_source=light_source,
            imaging_space=imaging_space,
            optical_channels=[optical_channel],
        )
        nwbfile.add_acquisition(nwbdata=multi_channel_microscopy_volume)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscope, read_nwbfile.devices["Microscope"])
            self.assertContainerEqual(light_source, read_nwbfile.devices["LightSource"])

            self.assertContainerEqual(imaging_space, read_nwbfile.lab_meta_data["PlanarImagingSpace"])
            self.assertContainerEqual(optical_channel, read_nwbfile.lab_meta_data["MicroscopyOpticalChannel"])

            self.assertContainerEqual(
                multi_channel_microscopy_volume, read_nwbfile.acquisition["MultiChannelMicroscopyVolume"]
            )
