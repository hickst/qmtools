# Tests of the violin CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 9/18/21.
#   Last Modified: Add test of main with mocks.
#
import os
import pytest
import sys
from pathlib import Path

from qmtools import BIDS_DATA_EXT, INPUT_FILE_EXIT_CODE
from qmtools import REPORTS_DIR_EXIT_CODE, REPORTS_DIR, REPORTS_EXT
import qmtools.qmviolin.violin_cli as cli
import qmtools.qmviolin.violin as violin
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse


@pytest.fixture
def clear_argv():
  sys.argv = []


class MockViolin:
  # mock vplot method to return empty plot_info, which will be ignored
  @staticmethod
  def vplot(modality, args):
    return  {}

  # mock make_html_report to do nothing and succeed
  @staticmethod
  def make_html_report(modality, args, plot_info):
    pass  # normally works by side-effect: so nothing needs to be done


@pytest.fixture
def mock_violin(monkeypatch):
  # return an instance of MockViolin with noop methods
  def violin_mock(*args, **kwargs):
    return MockViolin()

  monkeypatch.setattr(violin, "vplot", violin_mock)
  monkeypatch.setattr(violin, "make_html_report", violin_mock)



class TestViolinCLI(object):

  bold_test_fyl   = f"{TEST_RESOURCES_DIR}/bold_test.tsv"    # group file
  fetch_test_fyl  = f"{TEST_RESOURCES_DIR}/manmafmagskyra50.tsv"  # fetched file
  struct_test_fyl = f"{TEST_RESOURCES_DIR}/struct_test.tsv"  # group file
  empty_test_fyl  = f"{TEST_RESOURCES_DIR}/empty.txt"
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
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert f"usage: {cli.PROG_NAME}" in syserr


  def test_main_help(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmviolin', '-h']
      cli.main()
    assert se.value.code == 0          # help is not an error for parseargs
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert f"usage: {cli.PROG_NAME}" in sysout


  def test_main_no_modality(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmviolin']
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: modality' in syserr


  def test_main_bad_modality(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmviolin', 'fMRI', self.fetch_test_fyl, self.bold_test_fyl ]
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'argument modality: invalid choice' in syserr


  def test_main_no_fetchfile(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmviolin', 'bold']
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: fetched_file' in syserr


  def test_main_no_groupfile(self, capsys, clear_argv):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmviolin', 'bold', self.fetch_test_fyl]
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: group_file' in syserr


  def test_main(self, capsys, clear_argv, mock_violin):
    print(f"TEST_MAIN: in {os.getcwd()}", file=sys.stderr)  # REMOVE LATER
    sys.argv = ['qmviolin', '-v', 'bold', self.fetch_test_fyl, self.bold_test_fyl]
    cli.main()
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert "Comparing MRIQC records with modality 'bold'" in syserr
    assert "Compared group records against fetched records" in syserr
    assert "Produced violin report to 'reports/bold_" in syserr
