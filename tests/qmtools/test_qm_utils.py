# Tests of Shared utilities for the QMTools programs.
#   Written by: Tom Hicks and Dianne Patterson. 8/5/2021.
# Last Modified: Use dot in explicit file extensions.
#
import os
import pandas
import pytest
import tempfile

from tests import TEST_RESOURCES_DIR
from qmtools import FETCHED_DIR, FETCHED_DIR_EXIT_CODE, REPORTS_DIR, REPORTS_DIR_EXIT_CODE
import qmtools.qm_utils as qmu


@pytest.fixture
def popdir(request):
  yield
  os.chdir(request.config.invocation_dir)


class TestQMUtils(object):

  bold_test_fyl  = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  df_cell_count = 855                  # size of test dataframe
  df_shape = (19, 45)                  # shape of test dataframe


  def test_ensure_fetched_dir(self, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)                 # popdir must restore test dir after test
      print(f"CWD={os.getcwd()}, tmpdir={tmpdir}")
      assert not os.path.isdir(FETCHED_DIR)
      qmu.ensure_fetched_dir('TestQMUtils')
      assert os.path.isdir(FETCHED_DIR)
      assert os.access(FETCHED_DIR, os.W_OK)


  def test_ensure_fetched_dir_fail(self, popdir):
    if (os.environ.get('RUNNING_IN_CONTAINER') is None):
      with pytest.raises(SystemExit) as se:
        os.chdir('/')                  # popdir must restore test dir after test
        print(f"CWD={os.getcwd()}")
        assert not os.path.isdir(FETCHED_DIR)
        qmu.ensure_fetched_dir('TestQMUtils')
      assert se.value.code == FETCHED_DIR_EXIT_CODE
    else:
      assert True


  def test_ensure_reports_dir(self, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)                 # popdir must restore test dir after test
      print(f"CWD={os.getcwd()}, tmpdir={tmpdir}")
      assert not os.path.isdir(REPORTS_DIR)
      qmu.ensure_reports_dir('TestQMUtils')
      assert os.path.isdir(REPORTS_DIR)
      assert os.access(REPORTS_DIR, os.W_OK)


  def test_ensure_reports_dir_fail(self, popdir):
    if (os.environ.get('RUNNING_IN_CONTAINER') is None):
      with pytest.raises(SystemExit) as se:
        os.chdir('/')                  # popdir must restore test dir after test
        print(f"CWD={os.getcwd()}")
        assert not os.path.isdir(REPORTS_DIR)
        qmu.ensure_reports_dir('TestQMUtils')
      assert se.value.code == REPORTS_DIR_EXIT_CODE
    else:
      assert True


  def test_gen_output_filename(self):
    fname = qmu.gen_output_filename('bold')
    print(fname)
    assert 'bold' in fname
    assert '.tsv' in fname


  def test_gen_output_filename_badmode(self):
    fname = qmu.gen_output_filename('BOLDER')
    print(fname)
    assert 'BOLDER' in fname
    assert '.tsv' in fname


  def test_gen_output_filename_ext(self):
    fname = qmu.gen_output_filename('T1w', '.csv')
    print(fname)
    assert 'T1w' in fname
    assert '.csv' in fname


  def test_load_tsv(self):
    qm_df = qmu.load_tsv(self.bold_test_fyl)
    print(qm_df)
    assert qm_df is not None
    assert type(qm_df) == pandas.core.frame.DataFrame
    assert qm_df.size == self.df_cell_count
    assert qm_df.shape == self.df_shape


  def test_validate_modality_good(self):
    assert qmu.validate_modality('bold') == 'bold'
    assert qmu.validate_modality('T1w') == 'T1w'
    assert qmu.validate_modality('T2w') == 'T2w'


  def test_validate_modality_fail(self):
    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('BAD argument')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('t1w')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('t2w')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('Bold')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('t1')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('T1')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('t2')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('T2')
