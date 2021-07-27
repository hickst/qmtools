# Tests of the traffic-light CLI code.
#   Written by: Tom Hicks and Dianne Patterson. 7/27/2021.
#   Last Modified: Initial creation.
#
import os
import matplotlib
import numpy
import pandas
import pytest
import tempfile
from pathlib import Path

import qmview.traffic_light_cli as cli
from config.settings import REPORTS_DIR
from tests import TEST_RESOURCES_DIR

class TestTrafficLightCLI(object):

  bold_test_fyl    = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  struct_test_fyl  = f"{TEST_RESOURCES_DIR}/struct_test.tsv"
  empty_test_fyl   = f"{TEST_RESOURCES_DIR}/empty.txt"
  nosuch_test_fyl = f"{TEST_RESOURCES_DIR}/NO_SUCH.tsv"


  def test_check_input_file_noarg(self):
    with pytest.raises(SystemExit) as se:
      cli.check_input_file(None)
    assert se.type == SystemExit
    assert se.value.code != 0          # expecting error exit code


  def test_check_input_file_nosuchfile(self):
    with pytest.raises(SystemExit) as se:
      cli.check_input_file(self.nosuch_test_fyl)
    assert se.type == SystemExit
    assert se.value.code != 0          # expecting error exit code


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
