# Tests of the traffic-light table code.
#   Written by: Tom Hicks and Dianne Patterson. 7/19/2021.
#   Last Modified: Update test for opaque Styler.
#
import os
import tempfile
from pathlib import Path

import matplotlib
import numpy
import pandas

import qmtools.qm_utils as qmu
import qmtools.qmview.traffic_light as traf
from qmtools import BIDS_DATA_EXT, REPORTS_EXT
from tests import TEST_RESOURCES_DIR


class TestTrafficLight(object):

  bold_test_fyl  = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  struct_test_fyl  = f"{TEST_RESOURCES_DIR}/struct_test.tsv"

  html_min_size = 1000          # min bytes for all HTML report files
  legend_min_size = 6000        # min bytes for legend in a .png file
  tsv_min_size = 1700           # min bytes for all TSV report files
  df_cell_count = 855           # size of test zscore dataframe
  df_shape = (19, 45)           # shape of test zscore dataframe

  bold_pos_good_df_cell_count = 19 * (1 + len(traf.BOLD_HI_GOOD_COLUMNS))
  bold_pos_good_df_shape = (19, (1 + len(traf.BOLD_HI_GOOD_COLUMNS)))
  bold_pos_bad_df_cell_count = 19 * (1 + len(traf.BOLD_LO_GOOD_COLUMNS))
  bold_pos_bad_df_shape = (19, (1 + len(traf.BOLD_LO_GOOD_COLUMNS)))

  struct_pos_good_df_cell_count = 19 * (1 + len(traf.STRUCT_HI_GOOD_COLUMNS))
  struct_pos_good_df_shape = (19, (1 + len(traf.STRUCT_HI_GOOD_COLUMNS)))
  struct_pos_bad_df_cell_count = 19 * (1 + len(traf.STRUCT_LO_GOOD_COLUMNS))
  struct_pos_bad_df_shape = (19, (1 + len(traf.STRUCT_LO_GOOD_COLUMNS)))


  def test_make_legends_tmp(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"type(tmpdir)={type(tmpdir)}")
      print(f"tmpdir={tmpdir}")
      traf.make_legends(tmpdir)
      # os.system(f"ls -lH {tmpdir} >/tmp/DEBUG")
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 2
      for fyl in files:
        fpath = os.path.join(tmpdir, fyl)
        assert os.path.getsize(fpath) > self.legend_min_size


  def test_make_traffic_light_table_bold_tmp(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"type(tmpdir)={type(tmpdir)}")
      print(f"tmpdir={tmpdir}")
      traf.make_traffic_light_table('bold', self.bold_test_fyl, tmpdir)
      # os.system(f"ls -lH {tmpdir} >/tmp/DEBUG")
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      # count how many files of each type written (expect: 3 html, 2 tsv, 0 png)
      assert len(files) == 5
      assert 3 == len(list(filter(lambda f: str(f).endswith(REPORTS_EXT),files)))
      assert 2 == len(list(filter(lambda f: str(f).endswith(BIDS_DATA_EXT),files)))
      for fyl in files:
        fpath = os.path.join(tmpdir, fyl)
        print(f"size({fpath})={os.path.getsize(fpath)}")
        if (str(fyl).endswith('html')):
          assert os.path.getsize(fpath) > self.html_min_size
        else:
          assert os.path.getsize(fpath) > self.tsv_min_size


  def test_make_traffic_light_table_struct_tmp(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"type(tmpdir)={type(tmpdir)}")
      print(f"tmpdir={tmpdir}")
      traf.make_traffic_light_table('T1w', self.struct_test_fyl, tmpdir)
      # os.system(f"ls -lH {tmpdir} >/tmp/DEBUG")
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      # count how many files of each type written (expect: 3 html, 2 tsv, 0 png)
      assert len(files) == 5
      assert 3 == len(list(filter(lambda f: str(f).endswith(REPORTS_EXT),files)))
      assert 2 == len(list(filter(lambda f: str(f).endswith(BIDS_DATA_EXT),files)))
      for fyl in files:
        fpath = os.path.join(tmpdir, fyl)
        if (str(fyl).endswith('html')):
          assert os.path.getsize(fpath) > self.html_min_size
        else:
          assert os.path.getsize(fpath) > self.tsv_min_size

  def test_normalize_to_zscores(self):
    qm_df = qmu.load_tsv(self.bold_test_fyl)
    norm_df = traf.normalize_to_zscores(qm_df)
    assert type(norm_df) == pandas.core.frame.DataFrame
    assert norm_df.size == self.df_cell_count
    assert norm_df.shape == self.df_shape
    print(type(norm_df['bids_name'][0]))
    assert type(norm_df['bids_name'][0]) == str
    print(type(norm_df.iloc[0, 1]))
    assert type(norm_df.iloc[0, 1]) == numpy.float64


  def test_pos_neg_split_bold(self):
    qm_df = qmu.load_tsv(self.bold_test_fyl)
    (pos_good_df, pos_bad_df) = traf.pos_neg_split(qm_df, 'bold')
    print(f"POS_GOOD.columns={pos_good_df.columns}")
    print(f"POS_BAD.columns={pos_bad_df.columns}")

    assert pos_good_df is not None
    assert type(pos_good_df) == pandas.core.frame.DataFrame
    assert pos_good_df.size == self.bold_pos_good_df_cell_count
    assert pos_good_df.shape == self.bold_pos_good_df_shape

    assert pos_bad_df is not None
    assert type(pos_bad_df) == pandas.core.frame.DataFrame
    assert pos_bad_df.size == self.bold_pos_bad_df_cell_count
    assert pos_bad_df.shape == self.bold_pos_bad_df_shape


  def test_pos_neg_split_struct(self):
    qm_df = qmu.load_tsv(self.struct_test_fyl)
    (pos_good_df, pos_bad_df) = traf.pos_neg_split(qm_df, 'T1w')
    print(f"POS_GOOD.columns={pos_good_df.columns}")
    print(f"POS_BAD.columns={pos_bad_df.columns}")

    assert pos_good_df is not None
    assert type(pos_good_df) == pandas.core.frame.DataFrame
    assert pos_good_df.size == self.struct_pos_good_df_cell_count
    assert pos_good_df.shape == self.struct_pos_good_df_shape

    assert pos_bad_df is not None
    assert type(pos_bad_df) == pandas.core.frame.DataFrame
    assert pos_bad_df.size == self.struct_pos_bad_df_cell_count
    assert pos_bad_df.shape == self.struct_pos_bad_df_shape



  def test_style_table_by_std_deviations(self):
    df = pandas.DataFrame({'aor':[-4.01, -3.01, -2.01, -1.001, -0.01, 0.0, 0.01, 1.01, 2.01, 3.01, 4.01]})
    styler = traf.style_table_by_std_deviations(df)
    assert styler is not None
    assert type(styler) == pandas.io.formats.style.Styler



  def test_write_table_to_tsv(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      qm_df = qmu.load_tsv(self.bold_test_fyl)
      norm_df = traf.normalize_to_zscores(qm_df)
      traf.write_table_to_tsv(norm_df, "table", report_dirpath=tmpdir)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1
      for fyl in files:
        assert str(fyl).endswith(BIDS_DATA_EXT)
        fpath = os.path.join(tmpdir, fyl)
        assert os.path.getsize(fpath) > self.tsv_min_size


  def test_write_table_to_html(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      qm_df = qmu.load_tsv(self.bold_test_fyl)
      norm_df = traf.normalize_to_zscores(qm_df)
      styler = traf.style_table_by_std_deviations(norm_df)
      traf.write_table_to_html(styler, "table", report_dirpath=tmpdir)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1
      for fyl in files:
        assert str(fyl).endswith(REPORTS_EXT)
        fpath = os.path.join(tmpdir, fyl)
        assert os.path.getsize(fpath) > self.html_min_size
