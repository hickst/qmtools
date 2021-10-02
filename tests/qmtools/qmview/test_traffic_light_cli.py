# Tests of the traffic-light CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 7/27/2021.
#   Last Modified: Add and use popdir fixture.
#
import os
import pytest
import sys
import tempfile
from pathlib import Path

from qmtools import BIDS_DATA_EXT, INPUT_FILE_EXIT_CODE
from qmtools import REPORTS_DIR, REPORTS_EXT
import qmtools.qmview.traffic_light_cli as cli
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse


@pytest.fixture
def clear_argv():
  sys.argv = []


@pytest.fixture
def popdir(request):
  yield
  os.chdir(request.config.invocation_dir)


class TestTrafficLightCLI(object):

  bold_test_fyl    = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  struct_test_fyl  = f"{TEST_RESOURCES_DIR}/struct_test.tsv"
  empty_test_fyl   = f"{TEST_RESOURCES_DIR}/empty.txt"
  nosuch_test_fyl = f"{TEST_RESOURCES_DIR}/NO_SUCH.tsv"

  nosuch_dir = f"{TEST_RESOURCES_DIR}/NO_SUCH_DIR"
  default_dir = REPORTS_DIR
  tmp_dir = '/tmp'


  def test_check_input_file_noarg(self):
    with pytest.raises(SystemExit) as se:
      cli.check_input_file(None)
    assert se.value.code == INPUT_FILE_EXIT_CODE


  def test_check_input_file_nosuchfile(self):
    with pytest.raises(SystemExit) as se:
      cli.check_input_file(self.nosuch_test_fyl)
    assert se.value.code == INPUT_FILE_EXIT_CODE


  def test_check_input_file_empty(self):
    try:
      cli.check_input_file(self.empty_test_fyl)
    except SystemExit as se:
      assert False, "check_input_file unexpectedly exited when given empty test file"


  def test_check_input_file_good(self):
    try:
      cli.check_input_file(self.bold_test_fyl)
    except SystemExit as se:
      assert False, "check_input_file unexpectedly exited when given valid bold test file"


  def test_main_noargs(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert f"usage: {cli.PROG_NAME}" in syserr


  def test_main_help(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmtools', '-h']
      cli.main()
    assert se.value.code == 0          # help is not an error for parseargs
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    assert f"usage: {cli.PROG_NAME}" in sysout


  def test_main_no_modality(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmtools']
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: modality' in syserr


  def test_main_no_inputfile(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmtools', 'bold']
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: group_file' in syserr


  def test_main(self, capsys, clear_argv, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      print(f"tmpdir={tmpdir}")
      sys.argv = ['qmtools', 'bold', self.bold_test_fyl]
      cli.main()
      files = os.listdir(os.path.join(tmpdir, REPORTS_DIR))
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 6
      # count how many files of each type written (expect: 2 html, 2 tsv, 2 png)
      assert 2 == len(list(filter(lambda f: str(f).endswith(REPORTS_EXT),files)))
      assert 2 == len(list(filter(lambda f: str(f).endswith(BIDS_DATA_EXT),files)))
      assert 2 == len(list(filter(lambda f: str(f).endswith('.png'),files)))


  def test_main_verbose(self, capsys, clear_argv, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      print(f"tmpdir={tmpdir}")
      sys.argv = ['qmtools', '-v', 'bold', self.bold_test_fyl]
      cli.main()
      sysout, syserr = capsys.readouterr()
      print(f"CAPTURED SYS.ERR:\n{syserr}")
      assert 'Processing MRIQC group file' in syserr
      assert 'Produced reports in reports directory' in syserr
