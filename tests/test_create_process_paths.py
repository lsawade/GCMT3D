"""

Test suite for the creation of processing path_files.

:copyright:
    Lucas Sawade (lsawade@princeton.edu)
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)

Last Update: April 2019

"""


from gcmt3d.utils.io import smart_read_yaml
from gcmt3d.data.management.skeleton import DataBaseSkeleton
from gcmt3d.data.management.create_process_paths import create_process_path_syn
from gcmt3d.data.management.create_process_paths import create_process_path_obs
from gcmt3d.data.management.create_process_paths import create_window_path
from gcmt3d.data.management.create_process_paths import get_processing_list
from gcmt3d.data.management.create_process_paths import get_windowing_list
from gcmt3d.data.management.inversion_dicts \
    import create_full_inversion_dict_list
from gcmt3d.data.management.inversion_dicts import write_inversion_dicts
import tempfile
import inspect
import os
import glob
import unittest


def _upper_level(path, nlevel=4):
    """
    Go the nlevel dir up
    """
    for i in range(nlevel):
        path = os.path.dirname(path)
    return path


# Most generic way to get the data folder path.
TESTBASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(TESTBASE_DIR, "data")


# Recreates bash touch behaviour
def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


class TestCreatePaths(unittest.TestCase):
    """Class that handles testing of the Data Base structure creator"""

    def setUp(self):
        # Create a temporary specfem like directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.specfem_dir = self.test_dir.name
        os.makedirs(os.path.join(self.specfem_dir, "DATA"))
        touch(os.path.join(self.specfem_dir, "DATA", "STATIONS"))
        touch(os.path.join(self.specfem_dir, "DATA", "Par_file"))
        touch(os.path.join(self.specfem_dir, "DATA", "CMTSOLUTION"))
        os.makedirs(os.path.join(self.specfem_dir, "DATABASES_MPI"))
        os.makedirs(os.path.join(self.specfem_dir, "OUTPUT_FILES"))
        os.makedirs(os.path.join(self.specfem_dir, "bin"))

    def tearDown(self):
        # Close the file, the directory will be removed after the tests
        self.test_dir.cleanup()

    def test_IO(self):
        """Testing if strings are set correctly."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=os.path.join(DATA_DIR, "CMTSOLUTION"),
                                  specfem_dir=self.specfem_dir)

            self.assertEqual(DB.specfem_dir, self.specfem_dir)
            self.assertEqual(DB.cmt_fn, os.path.join(DATA_DIR, "CMTSOLUTION"))
            self.assertEqual(DB.basedir, tmp_dir)

    def test__create_process_path_obs(self):
        """Testing the creation of the observed processing yaml file."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Cmtfile path
            cmtfile = os.path.join(DATA_DIR, "CMTSOLUTION")

            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=cmtfile,
                                  specfem_dir=self.specfem_dir)

            # Create database
            DB.create_all()

            # Read the yaml_file which should be created in the CMT directory
            process_dir = os.path.join(DATA_DIR, "ProcessObserved")

            # CMT filename in database
            cmt_filename = os.path.join(DB.Cdirs[0], "C" + DB.Cids[0])

            # Create Processing path files
            create_process_path_obs(cmt_filename, process_dir)

            # Solution output path:
            process_paths = os.path.join(DB.Cdirs[0], "seismograms",
                                         "process_paths")

            # One solution path file:
            process_file = os.path.join(process_paths,
                                        "process_observed.040_100.yml")

            # Solution should be:
            input_asdf = os.path.join(DB.Cdirs[0], "seismograms", "obs",
                                      "raw_observed.h5")
            input_tag = "obs"
            output_asdf = os.path.join(DB.Cdirs[0], "seismograms",
                                       "processed_seismograms",
                                       "processed_observed.040_100.h5")

            output_tag = "040_100_obsd"
            process_param_file = os.path.join(process_dir,
                                              "proc_obsd.40_100.param.yml")

            d = smart_read_yaml(process_file, mpi_mode=False)

            # Assessing correctness of yaml file
            self.assertTrue(d["input_asdf"] == input_asdf)
            self.assertTrue(d["input_tag"] == input_tag)
            self.assertTrue(d["output_asdf"] == output_asdf)
            self.assertTrue(d["output_tag"] == output_tag)
            self.assertTrue(d["process_param_file"] == process_param_file)

    def test__create_process_path_syn(self):
        """Testing the creation of the observed processing yaml file."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Cmtfile path
            cmtfile = os.path.join(DATA_DIR, "CMTSOLUTION")

            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=cmtfile,
                                  specfem_dir=self.specfem_dir)

            # Create database
            DB.create_all()

            # Read the yaml_file which should be created in the CMT directory
            process_dir = os.path.join(DATA_DIR, "ProcessSynthetic")

            # CMT filename in database
            cmt_filename = os.path.join(DB.Cdirs[0], "C" + DB.Cids[0])

            # Create Processing path files
            create_process_path_syn(cmt_filename, process_dir, npar=9)

            # Solution output path:
            process_paths = os.path.join(DB.Cdirs[0], "seismograms",
                                         "process_paths")

            # One solution path file:
            process_file = os.path.join(process_paths,
                                        "process_synthetic_CMT_rp.040_100.yml")

            # Solution should be:
            input_asdf = os.path.join(DB.Cdirs[0], "seismograms", "syn",
                                      "CMT_rp.h5")
            input_tag = "syn"
            output_asdf = os.path.join(DB.Cdirs[0], "seismograms",
                                       "processed_seismograms",
                                       "processed_synthetic_CMT_rp.040_100.h5")
            output_tag = "040_100_synt"
            process_param_file = os.path.join(process_dir,
                                              "proc_synt.40_100.param.yml")

            d = smart_read_yaml(process_file, mpi_mode=False)

            # Assessing correctness of yaml file
            self.assertTrue(d["input_asdf"] == input_asdf)
            self.assertTrue(d["input_tag"] == input_tag)
            self.assertTrue(d["output_asdf"] == output_asdf)
            self.assertTrue(d["output_tag"] == output_tag)
            self.assertTrue(d["process_param_file"] == process_param_file)

    def test__create_window_path(self):
        """Testing the creation of the window path yaml file."""

        with tempfile.TemporaryDirectory() as tmp_dir:

            # Cmtfile path
            cmtfile = os.path.join(DATA_DIR, "CMTSOLUTION")

            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=cmtfile,
                                  specfem_dir=self.specfem_dir)

            # Create database
            DB.create_all()

            # Read the yaml_file which should be created in the CMT directory
            window_process_dir = os.path.join(DATA_DIR, "CreateWindows")

            # CMT filename in database
            cmt_filename = os.path.join(DB.Cdirs[0], "C" + DB.Cids[0])

            # Create Processing path files
            create_window_path(cmt_filename, window_process_dir,
                               figure_mode=True)

            # Outputdir
            cmt_dir = DB.Cdirs[0]

            # Define observed ASDF
            obsd_asdf = os.path.join(cmt_dir, "seismograms",
                                     "processed_seismograms",
                                     "processed_observed.040_100.h5")
            obsd_tag = "040_100_obsd"

            # Synthetic ASDF
            synt_asdf = os.path.join(cmt_dir, "seismograms",
                                     "processed_seismograms",
                                     "processed_synthetic_CMT.040_100.h5")
            synt_tag = "040_100_synt"

            # Output file parameters
            output_file = os.path.join(cmt_dir, "window_data",
                                       "windows.040_100#surface_wave.json")

            figure_dir = os.path.join(cmt_dir, "window_data",
                                      "window_plots.040_100#surface_wave")

            # window paramfile
            window_param_file = os.path.join(window_process_dir,
                                             "window.40_100#surface_wave."
                                             "param.yml")

            # Output path file
            path_file = os.path.join(cmt_dir, "window_data", "window_paths",
                                     "windows.040_100#surface_wave.yml")

            # Read written dictionary
            d = smart_read_yaml(path_file, mpi_mode=False)

            print("Solution: ", synt_asdf)
            print("Loaded: ", d["synt_asdf"])

            # Assessing correctness of yaml file
            self.assertTrue(d["obsd_asdf"] == obsd_asdf)
            self.assertTrue(d["obsd_tag"] == obsd_tag)
            self.assertTrue(d["synt_asdf"] == synt_asdf)
            self.assertTrue(d["synt_tag"] == synt_tag)
            self.assertTrue(d["figure_mode"])
            self.assertTrue(d["figure_dir"] == figure_dir)
            self.assertTrue(d["output_file"] == output_file)
            self.assertTrue(d["window_param_file"] == window_param_file)

    def test_get_processing_list(self):
        """Tests the get_processing_list function in the create_process_paths
        modules. """

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Cmtfile path
            cmtfile = os.path.join(DATA_DIR, "CMTSOLUTION")

            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=cmtfile,
                                  specfem_dir=self.specfem_dir)

            # Create database
            DB.create_all()

            # Outputdir
            cmt_dir = DB.Cdirs[0]
            cmt_file_db = os.path.join(cmt_dir, "C" + DB.Cids[0] + ".cmt")

            # Read the yaml_file which should be created in the CMT directory
            process_syn_dir = os.path.join(DATA_DIR, "ProcessSynthetic")

            # CMT filename in database
            cmt_filename = os.path.join(DB.Cdirs[0], "C" + DB.Cids[0])

            # Create Processing path files
            create_process_path_syn(cmt_filename, process_syn_dir, npar=9)

            # Read the yaml_file which should be created in the CMT directory
            process_obs_dir = os.path.join(DATA_DIR, "ProcessObserved")

            # Create Processing path files
            create_process_path_obs(cmt_filename, process_obs_dir)

            # Solution output path:
            process_paths = os.path.join(DB.Cdirs[0], "seismograms",
                                         "process_paths")

            # Get processing list
            processing_list, obs_list, syn_list = get_processing_list(
                cmt_file_db,
                process_obs_dir,
                process_syn_dir)

            # Files on disk
            solution_list = glob.glob(os.path.join(process_paths, "*"))

            # Check if processing list equals process dir files
            for process_path in processing_list:
                self.assertTrue(process_path in solution_list)

    def test_get_windowing_list(self):
        """Tests the get_processing_list function in the create_process_paths
        modules. """

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Cmtfile path
            cmtfile = os.path.join(DATA_DIR, "CMTSOLUTION")

            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=cmtfile,
                                  specfem_dir=self.specfem_dir)

            # Create database
            DB.create_all()

            # Outputdir
            cmt_dir = DB.Cdirs[0]
            cmt_file_db = os.path.join(cmt_dir, "C" + DB.Cids[0] + ".cmt")

            # Read the yaml_file which should be created in the CMT directory
            window_process_dir = os.path.join(DATA_DIR, "CreateWindows")

            # Create Window path files
            create_window_path(cmt_file_db, window_process_dir,
                               figure_mode=True)

            # Get windowing list
            windowing_list, outputfile_list = get_windowing_list(
                cmt_file_db,
                window_process_dir)

            # Solution output path:
            window_paths = os.path.join(DB.Cdirs[0], "window_data",
                                        "window_paths")

            # Files on disk
            solution_list = glob.glob(os.path.join(window_paths, "*"))

            # Check if processing list equals process dir files
            for window_path, outfile in zip(windowing_list, outputfile_list):
                self.assertTrue(window_path in solution_list)

    def test_create_inversion_dicts(self):
        """Test the inversion dictionary creator."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Cmtfile path
            cmtfile = os.path.join(DATA_DIR, "CMTSOLUTION")

            # Initialize database skeleton class
            DB = DataBaseSkeleton(basedir=tmp_dir,
                                  cmt_fn=cmtfile,
                                  specfem_dir=self.specfem_dir)

            # Create database
            DB.create_all()

            # Outputdir
            cmt_dir = DB.Cdirs[0]
            cmt_file_db = os.path.join(cmt_dir, "C" + DB.Cids[0] + ".cmt")

            # Read the yaml_file which should be created in the CMT directory
            window_process_dir = os.path.join(DATA_DIR, "CreateWindows")

            # Create Window path files
            create_window_path(cmt_file_db, window_process_dir,
                               figure_mode=True)

            # Read the yaml_file which should be created in the CMT directory
            process_syn_dir = os.path.join(DATA_DIR, "ProcessSynthetic")

            # CMT filename in database
            cmt_filename = os.path.join(DB.Cdirs[0], "C" + DB.Cids[0])

            # Create Processing path files
            create_process_path_syn(cmt_filename, process_syn_dir, npar=9)

            # Read the yaml_file which should be created in the CMT directory
            process_obs_dir = os.path.join(DATA_DIR, "ProcessObserved")

            # Create Processing path files
            create_process_path_obs(cmt_filename, process_obs_dir)

            # Create dict list
            inv_dict_list, filenames = create_full_inversion_dict_list(
                cmt_filename,
                process_obs_dir,
                process_syn_dir,
                window_process_dir)

            write_inversion_dicts(inv_dict_list, filenames)

            for inv_dict, filename in zip(inv_dict_list, filenames):
                self.assertTrue(os.path.exists(filename))


if __name__ == "__main__":
    unittest.main()
