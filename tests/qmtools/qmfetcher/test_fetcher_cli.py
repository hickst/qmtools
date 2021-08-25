# Tests of the MRIQC data fetcher CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 8/4/2021.
#   Last Modified: Minor rename 2 tests.
#
import os
import matplotlib
import numpy
import pandas
import pytest
import sys
import tempfile
from pathlib import Path

from qmtools import ALLOWED_MODALITIES, FETCHED_DIR, NUM_RECS_EXIT_CODE, QUERY_FILE_EXIT_CODE
from qmtools.qmfetcher.fetcher import SERVER_URL
import qmtools.qmfetcher.fetcher_cli as cli
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestFetcherCLI(object):

  bold_test_fyl    = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  struct_test_fyl  = f"{TEST_RESOURCES_DIR}/struct_test.tsv"
  empty_test_fyl   = f"{TEST_RESOURCES_DIR}/empty.txt"
  nosuch_test_fyl = f"{TEST_RESOURCES_DIR}/NO_SUCH.tsv"
  params_query_fyl = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  nosuch_dir = f"{TEST_RESOURCES_DIR}/NO_SUCH_DIR"
  tmp_dir = '/tmp'


  def test_check_query_file_empty(self):
    with pytest.raises(SystemExit) as se:
      cli.check_query_file('')
    assert se.value.code == QUERY_FILE_EXIT_CODE


  def test_check_query_file_bad(self):
    with pytest.raises(SystemExit) as se:
      cli.check_query_file('NOSUCH.qp')
    assert se.value.code == QUERY_FILE_EXIT_CODE


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


  def test_main_urlonly_noqps(self, capsys):
    with pytest.raises(SystemExit) as se:
      sys.argv = [ 'qmtools', '-v', '-m', 'T1w', '-n', '4', '--url-only' ]
      cli.main()
    print(se)
    assert se.value.code == 0
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert SERVER_URL in sysout
    assert '/T1w' in sysout
    assert 'max_results=4' in sysout


  def test_main_urlonly_qps(self, capsys):
    with pytest.raises(SystemExit) as se:
      sys.argv = [ 'qmtools', '-v', '-m', 'bold', '-n', '4',
                   '-q', self.params_query_fyl, '--url-only' ]
      cli.main()
    print(se)
    assert se.value.code == 0
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert SERVER_URL in sysout
    assert '/bold' in sysout
    assert 'max_results=4' in sysout
