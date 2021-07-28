# Tests of the traffic-light CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 7/27/2021.
#   Last Modified: Remove unneeded test of readonly dir.
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
import qmview.traffic_light_cli as cli
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

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
    assert se.value.code == cli.INPUT_FILE_EXIT_CODE


  def test_check_input_file_nosuchfile(self):
    with pytest.raises(SystemExit) as se:
      cli.check_input_file(self.nosuch_test_fyl)
    assert se.value.code == cli.INPUT_FILE_EXIT_CODE


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


  def test_check_reports_dir_noarg(self):
    with pytest.raises(SystemExit) as se:
      cli.check_reports_dir(None)
    assert se.value.code == cli.REPORTS_DIR_EXIT_CODE


  def test_check_reports_dir_nosuchdir(self):
    with pytest.raises(SystemExit) as se:
      cli.check_reports_dir(self.nosuch_dir)
    assert se.value.code == cli.REPORTS_DIR_EXIT_CODE


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
      sys.argv = ['qmview', '-h']
      cli.main()
    assert se.value.code == 0          # help is not an error for parseargs
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    assert f"usage: {cli.PROG_NAME}" in sysout


  def test_main_no_inputfile(self, capsys):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmview', '-m', 'bold']
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: -i/--input-file' in syserr


  def test_main_no_modality(self, capsys):
    with pytest.raises(SystemExit) as se:
      sys.argv = ['qmview', '-i', self.bold_test_fyl]
      cli.main()
    assert se.value.code == SYSEXIT_ERROR_CODE
    sysout, syserr = capsys.readouterr()
    print(f"CAPTURED SYS.ERR:\n{syserr}")
    assert 'the following arguments are required: -m/--modality' in syserr
