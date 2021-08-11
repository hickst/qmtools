# Tests of Shared utilities for the QMTools programs.
#   Written by: Tom Hicks and Dianne Patterson. 8/5/2021.
#   Last Modified: Added tests for gen_output_filename, ensure_fetched_dir.
#
import os
import pandas
import pytest
import tempfile

from tests import TEST_RESOURCES_DIR
from qmtools import FETCHED_DIR, FETCHED_DIR_EXIT_CODE
import qmtools.qm_utils as qmu


class TestQMUtils(object):

  bold_test_fyl  = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  df_cell_count = 855           # size of test dataframe
  df_shape = (19, 45)           # shape of test dataframe


  def test_ensure_fetched_dir(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      assert not os.path.isdir(FETCHED_DIR)
      qmu.ensure_fetched_dir('TestQMUtils')
      assert os.path.isdir(FETCHED_DIR)
      assert os.access(FETCHED_DIR, os.W_OK)


  def test_ensure_fetched_dir_fail(self):
    if (os.environ.get('RUNNING_IN_CONTAINER') is None):
      with pytest.raises(SystemExit) as se:
        os.chdir('/')
        assert not os.path.isdir(FETCHED_DIR)
        qmu.ensure_fetched_dir('TestQMUtils')
      assert se.value.code == FETCHED_DIR_EXIT_CODE
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
    fname = qmu.gen_output_filename('t1w', 'csv')
    print(fname)
    assert 't1w' in fname
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
    assert qmu.validate_modality('t1w') == 't1w'
    assert qmu.validate_modality('t2w') == 't2w'
    assert qmu.validate_modality('Bold') == 'bold'
    assert qmu.validate_modality('T1w') == 't1w'
    assert qmu.validate_modality('T2w') == 't2w'
    assert qmu.validate_modality('BOLD') == 'bold'
    assert qmu.validate_modality('T1W') == 't1w'
    assert qmu.validate_modality('T2W') == 't2w'
    assert qmu.validate_modality('BoLd') == 'bold'


  def test_validate_modality_fail(self):
    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('BAD argument')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('T1')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      qmu.validate_modality('t1')
