'''
unit tests for the specplot_gallery module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2019, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import json
import logging
import os
import shutil
import sys
import tempfile
import time
import unittest


_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import specplot_gallery

import tests.common


class SpecPlotGallery(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.join(_path, 'spec2nexus')
        self.datapath = os.path.join(self.basepath, 'data')
        self.tempdir = tempfile.mkdtemp()
        sys.argv = [sys.argv[0],]
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        if os.path.exists(self.tempdir):
            logging.shutdown()
            shutil.rmtree(self.tempdir)
            self.tempdir = None
        logging.disable(logging.NOTSET)

#     def testName(self):
#         pass
    
    def abs_data_fname(self, fname):
        return os.path.join(self.datapath, fname)
    
    def test_command_line_NeXus_writer_1_3(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('writer_1_3.h5'))
        specplot_gallery.main()
        # this is HDF5 file, not SPEC, so not much content
        children = os.listdir(self.tempdir)
        self.assertEqual(len(children), 0)
        # self.assertEqual(children[0], 'specplot_files_processing.log')
    
    def test_command_line_spec_data_file_33bm_spec(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('33bm_spec.dat'))
        specplot_gallery.main()
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, specplot_gallery.MTIME_CACHE_FILE)))
        # TODO: test contents of mtime_cache.txt?

        plotDir = os.path.join(self.tempdir, '2010', '06', '33bm_spec')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '33bm_spec.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: #69: look for handling of scan 15
    
    def test_command_line_spec_data_file_user6idd(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('user6idd.dat'))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, specplot_gallery.MTIME_CACHE_FILE)))
 
        # S1 aborted, S2 all X,Y are 0,0
        plotDir = os.path.join(self.tempdir, '2013', '10', 'user6idd')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'user6idd.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: #69: look for handling of scan 1
 
    def test_command_line_spec_data_file_03_06_JanTest(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('03_06_JanTest.dat'))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, specplot_gallery.MTIME_CACHE_FILE)))
 
        # S1 aborted, S2 all X,Y are 0,0
        plotDir = os.path.join(self.tempdir, '2014', '03', '03_06_JanTest')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '03_06_JanTest.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 's00001' + specplot_gallery.PLOT_TYPE)))
        # TODO: #69: look for handling of scan 1
        self.assertFalse(os.path.exists(os.path.join(plotDir, 's1' + specplot_gallery.PLOT_TYPE)))
        # TODO: look for that scan in index.html?
     
    def test_command_line_spec_data_file_02_03_setup(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('02_03_setup.dat'))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, specplot_gallery.MTIME_CACHE_FILE)))
 
        plotDir = os.path.join(self.tempdir, '2016', '02', '02_03_setup')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '02_03_setup.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: #69: look for handling of scan 5
     
    def test_command_line_spec_data_file_list(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        for item in 'user6idd.dat APS_spec_data.dat 02_03_setup.dat'.split():
            sys.argv.append(self.abs_data_fname(item))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, specplot_gallery.MTIME_CACHE_FILE)))
 
        plotDir = os.path.join(self.tempdir, '2010', '11', 'APS_spec_data')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'APS_spec_data.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
 
        plotDir = os.path.join(self.tempdir, '2013', '10', 'user6idd')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'user6idd.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
 
        plotDir = os.path.join(self.tempdir, '2016', '02', '02_03_setup')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '02_03_setup.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
     
    def test_command_line_spec_data_file_list_reversed_chronological_issue_79(self):
        sys.argv.append('-r')
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('APS_spec_data.dat'))
        specplot_gallery.main()

        plotDir = os.path.join(self.tempdir, '2010', '11', 'APS_spec_data')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'APS_spec_data.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))

    def test_command_line_specified_directory_not_found_issue_98(self):
        sys.argv.append('-d')
        sys.argv.append("Goofball-directory_does_not_exist")
        sys.argv.append(self.abs_data_fname('APS_spec_data.dat'))
        self.assertRaises(specplot_gallery.DirectoryNotFoundError, specplot_gallery.main)

    def test_command_line_specified_directory_fails_isdir_issue_98(self):
        text_file_name = os.path.join(self.tempdir, 'goofball.txt')
        outp = open(text_file_name, 'w')
        outp.write('goofball text is not a directory')
        outp.close()
        sys.argv.append('-d')
        sys.argv.append(text_file_name)
        sys.argv.append(self.abs_data_fname('APS_spec_data.dat'))
        self.assertRaises(specplot_gallery.PathIsNotDirectoryError, specplot_gallery.main)


class TestFileRefresh(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.tempdir, "data")
        self.data_file = os.path.join(self.data_dir, "specdata.txt")
        self.gallery = os.path.join(self.tempdir, "gallery")

        os.mkdir(self.data_dir)
        os.mkdir(self.gallery)
        src = os.path.join(_test_path, "tests", "data", "refresh1.txt")
        shutil.copy(src, self.data_file)
        
        logging.disable(logging.CRITICAL)

    def addMoreScans(self, append_scan=True):
        path = os.path.join(_test_path, "tests", "data")
        if append_scan:
            file2 = os.path.join(path, "refresh2.txt")
        else:
            file2 = os.path.join(path, "refresh3.txt")
        with open(file2, "r") as fp:
            text = fp.read()
        with open(self.data_file, "a") as fp:
            fp.write(text)

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
        logging.disable(logging.NOTSET)
    
    def test_refresh(self):
        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.gallery, 
                    specplot_gallery.MTIME_CACHE_FILE)))

        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        plotdir = os.path.join(self.gallery, "2010", "11", "specdata")
        children = [
            k
            for k in sorted(os.listdir(plotdir))
            if k.endswith(specplot_gallery.PLOT_TYPE)
            ]
        self.assertEqual(len(children), 3)
        mtimes = {
            k: os.path.getmtime(os.path.join(plotdir, k))
            for k in children
            }
        self.assertEqual(len(mtimes), 3)
        
        # update the file with more data
        self.addMoreScans()
        time.sleep(0.1)

        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        k = children[-1]
        self.assertNotEqual(
            os.path.getmtime(os.path.join(plotdir, k)), 
            mtimes[k], 
            k)
        for k in children[:-1]:
            # should pass all but the latest (#S 3)
            self.assertEqual(
                os.path.getmtime(os.path.join(plotdir, k)), 
                mtimes[k], 
                k)
        children = [
            k
            for k in sorted(os.listdir(plotdir))
            if k.endswith(specplot_gallery.PLOT_TYPE)
            ]
        mtimes = {
            k: os.path.getmtime(os.path.join(plotdir, k))
            for k in children
            }
        self.assertEqual(len(children), 5)
        
        # update the file with another scan
        self.addMoreScans(False)
        time.sleep(0.1)

        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        children = [
            k
            for k in sorted(os.listdir(plotdir))
            if k.endswith(specplot_gallery.PLOT_TYPE)
            ]
        self.assertEqual(len(children), 6)
        for k in children[:-1]:
            # should pass all but newest scan
            self.assertEqual(
                os.path.getmtime(os.path.join(plotdir, k)), 
                mtimes[k], 
                k)

        # restart file with first set of scans, should trigger replot all
        t0 = time.time()
        time.sleep(0.1)
        src = os.path.join(_test_path, "tests", "data", "refresh1.txt")
        shutil.copy(src, self.data_file)

        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        children = [
            k
            for k in sorted(os.listdir(plotdir))
            if k.endswith(specplot_gallery.PLOT_TYPE)
            ]
        self.assertEqual(len(children), 3)
        for k in children:
            # should pass all
            self.assertGreater(
                os.path.getmtime(os.path.join(plotdir, k)), 
                t0, 
                k)

        self.addMoreScans()
        time.sleep(0.1)
        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)

        # restart file again, use reversed chronological order
        t0 = time.time()
        time.sleep(0.1)
        src = os.path.join(_test_path, "tests", "data", "refresh1.txt")
        shutil.copy(src, self.data_file)

        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery,
            reverse_chronological=True)
        self.assertEqual(len(children), 3)
        self.addMoreScans()
        time.sleep(0.1)
        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        children = [
            k
            for k in sorted(os.listdir(plotdir))
            if k.endswith(specplot_gallery.PLOT_TYPE)
            ]
        
        # issue #206 here
        # edit mtime_cache.json
        mtime_file = os.path.join(self.gallery, "mtime_cache.json")
        self.assertTrue(os.path.exists(mtime_file))
        with open(mtime_file, "r") as fp:
            mtimes = json.loads(fp.read())
        # edit mtimes
        mtimes[self.data_file]["mtime"] = 1
        mtimes[self.data_file]["size"] = 1
        with open(mtime_file, "w") as fp:
            fp.write(json.dumps(mtimes, indent=4))
        # reprocess
        specplot_gallery.PlotSpecFileScans(
            [self.data_file], self.gallery)
        # look at the index.html file
        # TODO: learn YYY/mm/file subdir
        plot_dir = os.path.join(self.gallery, "2010", "11", "specdata")
        index_file = os.path.join(plot_dir, "index.html")
        with open(index_file, "r") as fp:
            html = fp.read()
        for line in html.splitlines():
            if (line.find(".svg") > 0 
                and line.find("href=") < 0 
                and line.startswith("s")
                ):
                self.assertFalse(
                    os.path.exists(
                        os.path.join(plot_dir, line)
                        ),
                    f"plot {line} is not linked in `index.html`"
                    )
        


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        TestFileRefresh,
        SpecPlotGallery,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
