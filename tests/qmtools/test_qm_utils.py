# Tests of Shared utilities for the QMTools programs.
#   Written by: Tom Hicks and Dianne Patterson. 8/5/2021.
#   Last Modified: Split shared function tests to here.
#
import os
import pandas
import pytest

from tests import TEST_RESOURCES_DIR
from qmtools.qm_utils import load_tsv, validate_modality


class TestQMUtils(object):

  bold_test_fyl  = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  df_cell_count = 855           # size of test dataframe
  df_shape = (19, 45)           # shape of test dataframe


  def test_load_tsv(self):
    qm_df = load_tsv(self.bold_test_fyl)
    print(qm_df)
    assert qm_df is not None
    assert type(qm_df) == pandas.core.frame.DataFrame
    assert qm_df.size == self.df_cell_count
    assert qm_df.shape == self.df_shape


  def test_validate_modality_good(self):
    assert validate_modality('bold') == 'bold'
    assert validate_modality('t1w') == 't1w'
    assert validate_modality('t2w') == 't2w'
    assert validate_modality('Bold') == 'bold'
    assert validate_modality('T1w') == 't1w'
    assert validate_modality('T2w') == 't2w'
    assert validate_modality('BOLD') == 'bold'
    assert validate_modality('T1W') == 't1w'
    assert validate_modality('T2W') == 't2w'
    assert validate_modality('BoLd') == 'bold'


  def test_validate_modality_fail(self):
    with pytest.raises(ValueError, match='Modality argument must be one of'):
      validate_modality('')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      validate_modality('BAD argument')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      validate_modality('T1')

    with pytest.raises(ValueError, match='Modality argument must be one of'):
      validate_modality('t1')
