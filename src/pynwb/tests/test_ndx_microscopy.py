"""Testing suite for ndx-microscopy extension."""

import numpy as np
import pytest
from hdmf.common.table import VectorData
from pynwb.testing import NWBH5IOFlexMixin, TestCase, remove_test_file
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
from pynwb import NWBHDF5IO, NWBFile


def test_constructor_microscope():
    mock_Microscope()


def test_constructor_light_source():
    mock_LightSource()


def test_constructor_microscopy_optical_channel():
    mock_MicroscopyOpticalChannel()


def test_constructor_planar_image_space():
    microscope = mock_Microscope()

    mock_PlanarImagingSpace(microscope=microscope)


def test_constructor_volumetric_image_space():
    microscope = mock_Microscope()

    mock_VolumetricImagingSpace(microscope=microscope)


def test_constructor_planar_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_PlanarMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_variable_depth_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VariableDepthMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


def test_constructor_volumetric_microscopy_series():
    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_VolumetricMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )


@pytest.fixture(scope="module")
def nwbfile_with_microscopy():
    nwbfile = pynwb.testing.mock.mock_NWBFile()

    microscope = mock_Microscope()
    light_source = mock_LightSource()
    imaging_space = mock_PlanarImagingSpace(microscope=microscope)
    optical_channel = mock_MicroscopyOpticalChannel()

    mock_PlanarMicroscopySeries(
        microscope=microscope, light_source=light_source, imaging_space=imaging_space, optical_channel=optical_channel
    )

    return nwbfile


def set_up_nwbfile(nwbfile: NWBFile = None):
    """Create an NWBFile with a Device"""
    nwbfile = nwbfile or mock_NWBFile()
    return nwbfile


class TestPatternedOptogeneticStimulusTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for PatternedOptogeneticStimulusTable."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it to file,
        read the file, and test that the PatternedOptogeneticStimulusTable from the
        file matches the original PatternedOptogeneticStimulusTable.
        """

        start_time = VectorData(name="start_time", description="start time", data=[0.0, 0.0, 0.0])
        stop_time = VectorData(name="stop_time", description="stop time", data=[1.0, 1.0, 1.0])
        power = VectorData(name="power", description="power", data=[0.0, 0.0, 0.0])
        frequency = VectorData(name="frequency", description="frequency", data=[0.0, 0.0, 0.0])
        pulse_width = VectorData(name="pulse_width", description="pulse_width", data=[0.0, 0.0, 0.0])
        stimulus_pattern_s = mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile)
        stimulus_pattern = VectorData(
            name="stimulus_pattern",
            description="stimulus_pattern",
            data=[stimulus_pattern_s, stimulus_pattern_s, stimulus_pattern_s],
        )
        targets_s = mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile)
        targets = VectorData(name="targets", description="targets", data=[targets_s, targets_s, targets_s])
        stimulus_site_s = mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile)
        stimulus_site = VectorData(
            name="stimulus_site", description="stimulus_site", data=[stimulus_site_s, stimulus_site_s, stimulus_site_s]
        )
        columns = [start_time, stop_time, power, frequency, pulse_width, stimulus_pattern, targets, stimulus_site]

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
            columns=columns,
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])

    def test_roundtrip_power_as_array(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it
        to file, read the file, and test that the PatternedOptogeneticStimulusTable
        from the file matches the original PatternedOptogeneticStimulusTable.
        """

        start_time = VectorData(name="start_time", description="start time", data=[0.0, 0.0, 0.0])
        stop_time = VectorData(name="stop_time", description="stop time", data=[1.0, 1.0, 1.0])

        targets_s = mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile)
        targets = VectorData(name="targets", description="targets", data=[targets_s, targets_s, targets_s])

        per_rois = np.ones((len(targets_s.targeted_rois[:])))
        power_per_roi = VectorData(
            name="power_per_roi", description="power_per_roi", data=[per_rois, per_rois, per_rois]
        )
        stimulus_pattern_s = mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile)
        stimulus_pattern = VectorData(
            name="stimulus_pattern",
            description="stimulus_pattern",
            data=[stimulus_pattern_s, stimulus_pattern_s, stimulus_pattern_s],
        )

        stimulus_site_s = mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile)
        stimulus_site = VectorData(
            name="stimulus_site", description="stimulus_site", data=[stimulus_site_s, stimulus_site_s, stimulus_site_s]
        )
        columns = [start_time, stop_time, power_per_roi, stimulus_pattern, targets, stimulus_site]
        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
            columns=columns,
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])

    def test_roundtrip_add_interval(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it to file,
        read the file, and test that the PatternedOptogeneticStimulusTable from the
        file matches the original PatternedOptogeneticStimulusTable.
        """

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        power = 70.0
        frequency = 20.0
        pulse_width = 0.1

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])

    def test_roundtrip_add_interval_power_as_array(self):
        """
        Add a PatternedOptogeneticStimulusTable to an NWBFile, write it
        to file, read the file, and test that the PatternedOptogeneticStimulusTable
        from the file matches the original PatternedOptogeneticStimulusTable.
        """

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        targets = mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile)
        power_per_roi = np.random.uniform(50e-3, 70e-3, targets.targeted_rois.shape[0])
        frequency_per_roi = np.random.uniform(20.0, 100.0, targets.targeted_rois.shape[0])
        pulse_width_per_roi = np.random.uniform(0.1, 0.2, targets.targeted_rois.shape[0])

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power_per_roi=power_per_roi,
            frequency_per_roi=frequency_per_roi,
            pulse_width_per_roi=pulse_width_per_roi,
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=targets,
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(stimulus_table, read_nwbfile.intervals["PatternedOptogeneticStimulusTable"])


class TestPatternedOptogeneticStimulusTableRoundtripPyNWB(NWBH5IOFlexMixin, TestCase):
    """
    Complex, more complete roundtrip test for PatternedOptogeneticStimulusTable
    using pynwb.testing infrastructure.
    """

    def getContainerType(self):
        return "PatternedOptogeneticStimulusTable"

    def addContainer(self):
        set_up_nwbfile(self.nwbfile)

        stimulus_table = PatternedOptogeneticStimulusTable(
            name="PatternedOptogeneticStimulusTable",
            description="description",
        )

        start_time = 0.0
        stop_time = 1.0
        power = 70.0
        frequency = 20.0
        pulse_width = 0.1

        stimulus_table.add_interval(
            start_time=start_time,
            stop_time=stop_time,
            power=power,
            frequency=frequency,
            pulse_width=pulse_width,
            stimulus_pattern=mock_OptogeneticStimulus2DPattern(nwbfile=self.nwbfile),
            targets=mock_OptogeneticStimulusTarget(nwbfile=self.nwbfile),
            stimulus_site=mock_PatternedOptogeneticStimulusSite(nwbfile=self.nwbfile),
        )

        self.nwbfile.add_time_intervals(stimulus_table)

    def getContainer(self, nwbfile: NWBFile):
        return nwbfile.intervals["PatternedOptogeneticStimulusTable"]
