# Tests of the MRIQC data fetcher CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 8/4/2021.
#   Last Modified: Update for refactoring shared constants.
#
import os
import matplotlib
import numpy
import pandas
import pytest
import sys
import tempfile
from pathlib import Path

from config.settings import REPORTS_DIR
from qmtools import REPORTS_DIR_EXIT_CODE
import qmtools.qmfetcher.fetcher_cli as cli
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestFetcherCLI(object):

  bold_test_fyl    = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  struct_test_fyl  = f"{TEST_RESOURCES_DIR}/struct_test.tsv"
  empty_test_fyl   = f"{TEST_RESOURCES_DIR}/empty.txt"
  nosuch_test_fyl = f"{TEST_RESOURCES_DIR}/NO_SUCH.tsv"

  nosuch_dir = f"{TEST_RESOURCES_DIR}/NO_SUCH_DIR"
  default_dir = REPORTS_DIR
  tmp_dir = '/tmp'


  def test_check_reports_dir_noarg(self):
    with pytest.raises(SystemExit) as se:
      cli.check_reports_dir(None)
    assert se.value.code == REPORTS_DIR_EXIT_CODE


  def test_check_reports_dir_nosuchdir(self):
    with pytest.raises(SystemExit) as se:
      cli.check_reports_dir(self.nosuch_dir)
    assert se.value.code == REPORTS_DIR_EXIT_CODE


  def test_check_reports_dir_default(self):
    try:
      cli.check_reports_dir(self.default_dir)
    except SystemExit as se:
      assert False, "check_input_file unexpectedly exited when given default reports dir"


  def test_main_noargs(self, capsys):
    with pytest.raises(SystemExit) as se:
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert f"usage: {cli.PROG_NAME}" in syserr


  def test_main_help(self, capsys):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmtools', '-h']
      cli.main()
    assert se.value.code == 0          # help is not an error for parseargs
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    assert f"usage: {cli.PROG_NAME}" in sysout


  def test_main_no_modality(self, capsys):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmtools', '-i', self.bold_test_fyl]
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: -m/--modality' in syserr


  def test_main(self, capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"type(tmpdir)={type(tmpdir)}")
      print(f"tmpdir={tmpdir}")
      sys.argv = ['qmtools', '-m', 'bold', '-r', tmpdir]
      cli.main()
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      # assert len(files) == 6
      # # count how many files of each type written (expect: 2 html, 2 tsv, 2 png)
      # assert 2 == len(list(filter(lambda f: str(f).endswith('.html'),files)))
      # assert 2 == len(list(filter(lambda f: str(f).endswith('.tsv'),files)))
      # assert 2 == len(list(filter(lambda f: str(f).endswith('.png'),files)))


  # def test_main_verbose(self, capsys):
  #   with tempfile.TemporaryDirectory() as tmpdir:
  #     print(f"type(tmpdir)={type(tmpdir)}")
  #     print(f"tmpdir={tmpdir}")
  #     sys.argv = ['qmtools', '-v', '-i', self.bold_test_fyl, '-m', 'bold', '-r', tmpdir]
  #     cli.main()
  #     sysout, syserr = capsys.readouterr()
  #     print(f"CAPTURED SYS.ERR:\n{syserr}")
  #     assert 'Processing MRIQC group file' in syserr
  #     assert 'Produced reports in reports directory' in syserr
