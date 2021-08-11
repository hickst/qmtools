# Tests of the MRIQC data fetcher CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 8/4/2021.
#   Last Modified: Update for refactored constants. Comment out main tests.
#                  Remove tests of reports directory.
#
import os
import matplotlib
import numpy
import pandas
import pytest
import sys
import tempfile
from pathlib import Path

from qmtools import ALLOWED_MODALITIES, OUTPUT_FILE_EXIT_CODE, NUM_RECS_EXIT_CODE
import qmtools.qmfetcher.fetcher_cli as cli
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestFetcherCLI(object):

  bold_test_fyl    = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  struct_test_fyl  = f"{TEST_RESOURCES_DIR}/struct_test.tsv"
  empty_test_fyl   = f"{TEST_RESOURCES_DIR}/empty.txt"
  nosuch_test_fyl = f"{TEST_RESOURCES_DIR}/NO_SUCH.tsv"

  nosuch_dir = f"{TEST_RESOURCES_DIR}/NO_SUCH_DIR"
  tmp_dir = '/tmp'


  def test_check_num_recs_zero(self):
    with pytest.raises(SystemExit) as se:
      cli.check_num_recs(0)
    assert se.value.code == NUM_RECS_EXIT_CODE


  def test_check_num_recs_negvalue(self):
    with pytest.raises(SystemExit) as se:
      cli.check_num_recs(-1)
    assert se.value.code == NUM_RECS_EXIT_CODE


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


  # def test_main_verbose(self, capsys):
  #   with tempfile.TemporaryDirectory() as tmpdir:
  #     print(f"type(tmpdir)={type(tmpdir)}")
  #     print(f"tmpdir={tmpdir}")
  #     sys.argv = ['qmtools', '-v', '-m', 'bold', '-o', '/tmp/outfile']
  #     cli.main()
  #     sysout, syserr = capsys.readouterr()
  #     print(f"CAPTURED SYS.ERR:\n{syserr}")
  #     assert "Querying MRIQC server with modality 'bold'" in syserr
  #     assert "Saved query results to '/tmp/outfile'" in syserr
