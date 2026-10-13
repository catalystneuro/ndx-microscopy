"""Test roundtrip (write and read back) of the Python API for the ndx-microscopy extension."""

import warnings
from datetime import datetime, timezone

import h5py
import numpy as np
import pytest
from hdmf.build.errors import OrphanContainerBuildError
from hdmf.build.warnings import DtypeConversionWarning
from pynwb.image import RGBImage
from pynwb.testing import TestCase as pynwb_TestCase
from pynwb.testing.mock.file import mock_NWBFile

import pynwb
from ndx_ophys_devices import StereotacticPosition
from ndx_ophys_devices.testing import (
    mock_ViralVector,
    mock_ViralVectorInjection,
    mock_Indicator,
)

from ndx_microscopy.testing import (
    mock_full_rig,
    mock_Microscope,
    mock_MicroscopyChannel,
    mock_PlanarSegmentation,
    mock_SegmentationContainer,
    mock_PlanarImagingSpace,
    mock_VolumetricImagingSpace,
    mock_PlanarMicroscopySeries,
    mock_PlanarMicroscopyStaticImage,
    mock_MultiPlaneMicroscopyContainer,
    mock_MultiChannelMicroscopyContainer,
    mock_VolumetricMicroscopySeries,
    mock_VolumetricMicroscopyStaticImage,
    mock_MicroscopyResponseSeries,
)

from ndx_microscopy import MicroscopyExperimentMetadata, MicroscopyResponseSeriesContainer, MicroscopyRig


def add_microscopy_experiment_metadata(nwbfile, indicator_names=("Indicator1",)):
    """Add a full mock rig and one viral vector, injection and indicator(s) to nwbfile."""
    microscopy_rig = mock_full_rig(nwbfile)
    viral_vector = mock_ViralVector(name="ViralVector1")
    viral_vector_injection = mock_ViralVectorInjection(name="ViralVectorInjection1", viral_vector=viral_vector)
    indicators = [mock_Indicator(name=name, viral_vector_injection=viral_vector_injection) for name in indicator_names]
    microscopy_experiment_metadata = MicroscopyExperimentMetadata(
        viral_vectors=[viral_vector],
        viral_vector_injections=[viral_vector_injection],
        indicators=indicators,
        microscopy_rigs=[microscopy_rig],
    )
    nwbfile.add_lab_meta_data(microscopy_experiment_metadata)
    return microscopy_rig, indicators


class TestPlanarMicroscopyStaticImageSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for PlanarMicroscopyStaticImage."""

    def setUp(self):
        self.nwbfile_path = "test_planar_microscopy_static_image_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

        planar_microscopy_static_image = mock_PlanarMicroscopyStaticImage(
            name="PlanarMicroscopyStaticImage",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator),
            planar_imaging_space=mock_PlanarImagingSpace(name="PlanarImagingSpace"),
        )
        nwbfile.add_acquisition(planar_microscopy_static_image)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(
                planar_microscopy_static_image, read_nwbfile.acquisition["PlanarMicroscopyStaticImage"]
            )


class TestVolumetricMicroscopyStaticImageSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VolumetricMicroscopyStaticImage."""

    def setUp(self):
        self.nwbfile_path = "test_volumetric_microscopy_static_image_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

        volumetric_microscopy_static_image = mock_VolumetricMicroscopyStaticImage(
            name="VolumetricMicroscopyStaticImage",
            volumetric_imaging_space=mock_VolumetricImagingSpace(name="VolumetricImagingSpace"),
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator),
        )
        nwbfile.add_acquisition(volumetric_microscopy_static_image)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(
                volumetric_microscopy_static_image, read_nwbfile.acquisition["VolumetricMicroscopyStaticImage"]
            )


class TestPlanarMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for PlanarMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_planar_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

        planar_microscopy_series = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator),
            planar_imaging_space=mock_PlanarImagingSpace(name="PlanarImagingSpace"),
        )
        nwbfile.add_acquisition(planar_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscopy_rig.microscope, read_nwbfile.devices["Microscope"])
            self.assertContainerEqual(microscopy_rig.objective_lens, read_nwbfile.devices["ObjectiveLens"])

            self.assertContainerEqual(planar_microscopy_series, read_nwbfile.acquisition["PlanarMicroscopySeries"])


def test_shared_channel_and_imaging_space_roundtrip(tmp_path):
    """A channel or imaging space passed to several objects is stored once; the other uses are soft links."""
    nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
    microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

    microscopy_channel = mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator)
    planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace")
    for series_name in ("PlanarMicroscopySeries_1", "PlanarMicroscopySeries_2"):
        nwbfile.add_acquisition(
            mock_PlanarMicroscopySeries(
                name=series_name,
                microscopy_rig=microscopy_rig,
                microscopy_channel=microscopy_channel,
                planar_imaging_space=planar_imaging_space,
            )
        )
    planar_segmentation = mock_PlanarSegmentation(name="PlanarSegmentation", planar_imaging_space=planar_imaging_space)
    ophys_module = nwbfile.create_processing_module(name="ophys", description="")
    ophys_module.add(mock_SegmentationContainer(name="SegmentationContainer", segmentations=[planar_segmentation]))

    nwbfile_path = tmp_path / "shared_channel_and_imaging_space.nwb"
    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="w") as io:
        io.write(nwbfile)
    assert pynwb.validate(path=str(nwbfile_path)) == []

    channel_paths = [
        f"acquisition/{name}/MicroscopyChannel" for name in ("PlanarMicroscopySeries_1", "PlanarMicroscopySeries_2")
    ]
    space_paths = [
        "acquisition/PlanarMicroscopySeries_1/PlanarImagingSpace",
        "acquisition/PlanarMicroscopySeries_2/PlanarImagingSpace",
        "processing/ophys/SegmentationContainer/PlanarSegmentation/PlanarImagingSpace",
    ]
    with h5py.File(nwbfile_path, "r") as file:
        channel_links = [type(file.get(path, getlink=True)) for path in channel_paths]
        space_links = [type(file.get(path, getlink=True)) for path in space_paths]
    assert sorted(link.__name__ for link in channel_links) == ["HardLink", "SoftLink"]
    assert sorted(link.__name__ for link in space_links) == ["HardLink", "SoftLink", "SoftLink"]

    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        read_series_1 = read_nwbfile.acquisition["PlanarMicroscopySeries_1"]
        read_series_2 = read_nwbfile.acquisition["PlanarMicroscopySeries_2"]
        read_segmentation = read_nwbfile.processing["ophys"]["SegmentationContainer"]["PlanarSegmentation"]
        assert read_series_2.microscopy_channel is read_series_1.microscopy_channel
        assert read_series_2.planar_imaging_space is read_series_1.planar_imaging_space
        assert read_segmentation.planar_imaging_space is read_series_1.planar_imaging_space


@pytest.mark.parametrize(
    "mock_imaging_space, mock_series, imaging_space_argument",
    [
        (mock_PlanarImagingSpace, mock_PlanarMicroscopySeries, "planar_imaging_space"),
        (mock_VolumetricImagingSpace, mock_VolumetricMicroscopySeries, "volumetric_imaging_space"),
    ],
)
def test_imaging_space_with_fov_center_coordinates_roundtrip(
    tmp_path, mock_imaging_space, mock_series, imaging_space_argument
):
    nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
    microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

    imaging_space = mock_imaging_space(
        name="ImagingSpace",
        fov_center_coordinates=StereotacticPosition(
            name="fov_center_coordinates",
            anatomical_target="Primary visual cortex, layer 2/3",
            origin="bregma (AP, ML); brain surface (DV)",
            orientation="RAS",
            x_in_mm=2.5,
            y_in_mm=-3.8,
            z_in_mm=-0.2,
        ),
    )
    nwbfile.add_acquisition(
        mock_series(
            name="MicroscopySeries",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator),
            **{imaging_space_argument: imaging_space},
        )
    )

    nwbfile_path = tmp_path / "imaging_space_with_fov_center_coordinates.nwb"
    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="w") as io:
        io.write(nwbfile)
    assert pynwb.validate(path=str(nwbfile_path)) == []

    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="r", load_namespaces=True) as io:
        read_imaging_space = getattr(io.read().acquisition["MicroscopySeries"], imaging_space_argument)
        read_coordinates = read_imaging_space.fov_center_coordinates
        assert isinstance(read_coordinates, StereotacticPosition)
        assert read_coordinates.anatomical_target == "Primary visual cortex, layer 2/3"
        assert (read_coordinates.x_in_mm, read_coordinates.y_in_mm, read_coordinates.z_in_mm) == (2.5, -3.8, -0.2)


def test_imaging_space_dimensions_from_python_ints_write_without_dtype_warning(tmp_path):
    """Dimensions are usually given as Python ints, which should not need a dtype conversion on write."""
    nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
    microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)
    microscopy_channel = mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator)
    nwbfile.add_acquisition(
        mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscopy_rig=microscopy_rig,
            microscopy_channel=microscopy_channel,
            planar_imaging_space=mock_PlanarImagingSpace(name="PlanarImagingSpace", dimensions_in_pixels=[5, 5]),
        )
    )
    nwbfile.add_acquisition(
        mock_VolumetricMicroscopySeries(
            name="VolumetricMicroscopySeries",
            microscopy_rig=microscopy_rig,
            microscopy_channel=microscopy_channel,
            volumetric_imaging_space=mock_VolumetricImagingSpace(
                name="VolumetricImagingSpace", dimensions_in_voxels=[5, 5, 3]
            ),
        )
    )

    with warnings.catch_warnings():
        warnings.filterwarnings("error", category=DtypeConversionWarning, message=".*dimensions_in_(pixels|voxels)")
        with pynwb.NWBHDF5IO(path=tmp_path / "imaging_space_dimensions.nwb", mode="w") as io:
            io.write(nwbfile)


def test_microscopy_rig_with_optical_path_scheme_roundtrip(tmp_path):
    nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))

    microscope = mock_Microscope(name="Microscope")
    nwbfile.add_device_model(device_models=microscope.model)
    nwbfile.add_device(devices=microscope)

    optical_path_scheme = RGBImage(
        name="optical_path_scheme",
        data=np.zeros((4, 6, 3), dtype=np.uint8),
        description="Diagram of the optical path.",
    )
    microscopy_rig = MicroscopyRig(
        name="MicroscopyRig",
        description="A rig with an optical path scheme.",
        microscope=microscope,
        optical_path_scheme=optical_path_scheme,
    )
    nwbfile.add_lab_meta_data(MicroscopyExperimentMetadata(microscopy_rigs=[microscopy_rig]))

    nwbfile_path = tmp_path / "microscopy_rig_with_optical_path_scheme.nwb"
    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="w") as io:
        io.write(nwbfile)
    assert pynwb.validate(path=str(nwbfile_path)) == []

    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        read_rig = read_nwbfile.lab_meta_data["microscopy_experiment_metadata"].microscopy_rigs["MicroscopyRig"]
        read_scheme = read_rig.optical_path_scheme
        assert isinstance(read_scheme, RGBImage)
        assert read_scheme.description == "Diagram of the optical path."
        np.testing.assert_array_equal(read_scheme.data[:], optical_path_scheme.data)


def test_microscopy_rig_with_untracked_device(tmp_path):
    """Test that writing a MicroscopyRig with a device that hasn't been added to the NWBFile raises an error."""
    nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))

    microscope = mock_Microscope(name="Microscope")
    nwbfile.add_device_model(device_models=microscope.model)
    # The microscope itself is not added to nwbfile.devices
    microscopy_rig = MicroscopyRig(name="MicroscopyRig", description="A rig.", microscope=microscope)
    nwbfile.add_lab_meta_data(MicroscopyExperimentMetadata(microscopy_rigs=[microscopy_rig]))

    with pytest.raises(OrphanContainerBuildError):
        with pynwb.NWBHDF5IO(path=tmp_path / "untracked_device.nwb", mode="w") as io:
            io.write(nwbfile)


class TestVolumetricMicroscopySeriesSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for VolumetricMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_volumetric_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

        volumetric_microscopy_series = mock_VolumetricMicroscopySeries(
            name="VolumetricMicroscopySeries",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator),
            volumetric_imaging_space=mock_VolumetricImagingSpace(name="VolumetricImagingSpace"),
        )
        nwbfile.add_acquisition(volumetric_microscopy_series)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscopy_rig.microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(
                volumetric_microscopy_series, read_nwbfile.acquisition["VolumetricMicroscopySeries"]
            )


class TestMultiPlaneMicroscopyContainerSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MultiPlaneMicroscopyContainer."""

    def setUp(self):
        self.nwbfile_path = "test_multi_plane_microscopy_container_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

        microscopy_channel = mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator)

        planar_microscopy_series_1 = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries_1",
            microscopy_rig=microscopy_rig,
            microscopy_channel=microscopy_channel,
            planar_imaging_space=mock_PlanarImagingSpace(name="PlanarImagingSpace_1"),
        )
        planar_microscopy_series_2 = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries_2",
            microscopy_rig=microscopy_rig,
            microscopy_channel=microscopy_channel,
            planar_imaging_space=mock_PlanarImagingSpace(name="PlanarImagingSpace_2"),
        )

        multi_plane_microscopy_container = mock_MultiPlaneMicroscopyContainer(
            name="MultiPlaneMicroscopyContainer",
            planar_microscopy_series=[planar_microscopy_series_1, planar_microscopy_series_2],
        )
        nwbfile.add_acquisition(multi_plane_microscopy_container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(microscopy_rig.microscope, read_nwbfile.devices["Microscope"])

            self.assertContainerEqual(
                multi_plane_microscopy_container, read_nwbfile.acquisition["MultiPlaneMicroscopyContainer"]
            )


class TestMultiChannelMicroscopyContainerSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MultiChannelMicroscopyContainer."""

    def setUp(self):
        self.nwbfile_path = "test_multi_channel_microscopy_container_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator_1, indicator_2) = add_microscopy_experiment_metadata(
            nwbfile, indicator_names=("Indicator1", "Indicator2")
        )

        planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace_1")

        planar_microscopy_series_1 = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries_1",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel1", indicator=indicator_1),
            planar_imaging_space=planar_imaging_space,
        )
        planar_microscopy_series_2 = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries_2",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel2", indicator=indicator_2),
            planar_imaging_space=planar_imaging_space,
        )

        multi_channel_microscopy_container = mock_MultiChannelMicroscopyContainer(
            name="MultiChannelMicroscopyContainer",
            microscopy_series=[planar_microscopy_series_1, planar_microscopy_series_2],
        )
        nwbfile.add_acquisition(multi_channel_microscopy_container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(
                multi_channel_microscopy_container, read_nwbfile.acquisition["MultiChannelMicroscopyContainer"]
            )


class TestMultiChannelWithMultiPlaneContainerSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for MultiChannelMicroscopyContainer containing MultiPlaneMicroscopyContainers."""

    def setUp(self):
        self.nwbfile_path = "test_multi_channel_with_multi_plane_container_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator_gcamp, indicator_mcherry) = add_microscopy_experiment_metadata(
            nwbfile, indicator_names=("Indicator_GCaMP", "Indicator_mCherry")
        )

        planar_imaging_space_1 = mock_PlanarImagingSpace(name="PlanarImagingSpace_depth1")
        planar_imaging_space_2 = mock_PlanarImagingSpace(name="PlanarImagingSpace_depth2")

        # Channel 1: functional (GCaMP) — PlanarMicroscopySeries per depth
        gcamp_channel = mock_MicroscopyChannel(name="GCaMPChannel", indicator=indicator_gcamp)
        gcamp_series_1 = mock_PlanarMicroscopySeries(
            name="GCaMP_depth1",
            microscopy_rig=microscopy_rig,
            microscopy_channel=gcamp_channel,
            planar_imaging_space=planar_imaging_space_1,
        )
        gcamp_series_2 = mock_PlanarMicroscopySeries(
            name="GCaMP_depth2",
            microscopy_rig=microscopy_rig,
            microscopy_channel=gcamp_channel,
            planar_imaging_space=planar_imaging_space_2,
        )
        multi_plane_gcamp = mock_MultiPlaneMicroscopyContainer(
            name="GCaMP_planes",
            planar_microscopy_series=[gcamp_series_1, gcamp_series_2],
        )

        # Channel 2: anatomical marker (mCherry) — PlanarMicroscopyStaticImage per depth
        mcherry_channel = mock_MicroscopyChannel(name="mCherryChannel", indicator=indicator_mcherry)
        mcherry_image_1 = mock_PlanarMicroscopyStaticImage(
            name="mCherry_depth1",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mcherry_channel,
            planar_imaging_space=planar_imaging_space_1,
        )
        mcherry_image_2 = mock_PlanarMicroscopyStaticImage(
            name="mCherry_depth2",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mcherry_channel,
            planar_imaging_space=planar_imaging_space_2,
        )
        multi_plane_mcherry = mock_MultiPlaneMicroscopyContainer(
            name="mCherry_planes",
            planar_microscopy_static_images=[mcherry_image_1, mcherry_image_2],
        )

        multi_channel_container = mock_MultiChannelMicroscopyContainer(
            name="MultiChannelMultiPlaneContainer",
            multi_plane_microscopy_containers=[multi_plane_gcamp, multi_plane_mcherry],
        )
        nwbfile.add_acquisition(multi_channel_container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(
                multi_channel_container, read_nwbfile.acquisition["MultiChannelMultiPlaneContainer"]
            )


class TestSegmentationContainerSimpleRoundtrip(pynwb_TestCase):
    """Simple roundtrip test for SegmentationContainer."""

    def setUp(self):
        self.nwbfile_path = "test_segmentation_container_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))

        container = mock_SegmentationContainer(name="SegmentationContainer")
        ophys_module = nwbfile.create_processing_module(name="ophys", description="")
        ophys_module.add(container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

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
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
        microscopy_rig, (indicator,) = add_microscopy_experiment_metadata(nwbfile)

        planar_imaging_space = mock_PlanarImagingSpace(name="PlanarImagingSpace")
        planar_microscopy_series = mock_PlanarMicroscopySeries(
            name="PlanarMicroscopySeries",
            microscopy_rig=microscopy_rig,
            microscopy_channel=mock_MicroscopyChannel(name="MicroscopyChannel", indicator=indicator),
            planar_imaging_space=planar_imaging_space,
        )
        nwbfile.add_acquisition(planar_microscopy_series)

        planar_segmentation = mock_PlanarSegmentation(
            name="PlanarSegmentation", planar_imaging_space=planar_imaging_space
        )

        segmentation_container = mock_SegmentationContainer(
            name="SegmentationContainer", segmentations=[planar_segmentation]
        )
        ophys_module = nwbfile.create_processing_module(name="ophys", description="")
        ophys_module.add(segmentation_container)

        plane_segmentation_region = pynwb.ophys.DynamicTableRegion(
            name="rois",  # Name must be exactly this
            description="",
            data=list(range(len(planar_segmentation))),
            table=planar_segmentation,
        )
        microscopy_response_series = mock_MicroscopyResponseSeries(
            name="MicroscopyResponseSeries",
            rois=plane_segmentation_region,
            microscopy_series=planar_microscopy_series,
        )

        microscopy_response_series_container = MicroscopyResponseSeriesContainer(
            name="MicroscopyResponseSeriesContainer", microscopy_response_series=[microscopy_response_series]
        )
        ophys_module.add(microscopy_response_series_container)

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        self.assertEqual(pynwb.validate(path=self.nwbfile_path), [])

        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(segmentation_container, read_nwbfile.processing["ophys"]["SegmentationContainer"])

            read_container = read_nwbfile.processing["ophys"]["MicroscopyResponseSeriesContainer"]
            self.assertContainerEqual(microscopy_response_series_container, read_container)
            self.assertIs(
                read_container["MicroscopyResponseSeries"].microscopy_series,
                read_nwbfile.acquisition["PlanarMicroscopySeries"],
            )


def test_microscopy_experiment_metadata_without_optional_children_roundtrip(tmp_path):
    nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=timezone.utc))
    nwbfile.add_lab_meta_data(MicroscopyExperimentMetadata())

    nwbfile_path = tmp_path / "empty_microscopy_experiment_metadata.nwb"
    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="w") as io:
        io.write(nwbfile)
    assert pynwb.validate(path=str(nwbfile_path)) == []

    with pynwb.NWBHDF5IO(path=nwbfile_path, mode="r", load_namespaces=True) as io:
        read_metadata = io.read().lab_meta_data["microscopy_experiment_metadata"]
        assert isinstance(read_metadata, MicroscopyExperimentMetadata)
        assert len(read_metadata.microscopy_rigs) == 0
        assert len(read_metadata.viral_vectors) == 0
        assert len(read_metadata.viral_vector_injections) == 0
        assert len(read_metadata.indicators) == 0


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
