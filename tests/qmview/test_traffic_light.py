# Tests of the traffic-light table code.
#   Written by: Tom Hicks and Dianne Patterson. 7/19/2021.
#   Last Modified: Add/use test constants. Added test for write_table_to_html.
#
import os
import matplotlib
import numpy
import pandas
import pytest
import tempfile
from pathlib import Path

import qmview.traffic_light as traf
from config.settings import REPORTS_DIR
from tests import TEST_RESOURCES_DIR

class TestTrafficLight(object):

  gtest_tstfyl  = f"{TEST_RESOURCES_DIR}/gtest.tsv"
  html_min_size = 100000        # magic number for HTML report file (# bytes)
  legend_min_size = 6000        # magic number for legend (# bytes) in a .png file
  df_cell_count = 855           # size of test zscore dataframe
  df_shape = (19, 45)           # shape of test zscore dataframe


  def test_colorize_by_std_deviations(self):
    df = pandas.DataFrame({'aor':[-4.01, -3.01, -2.01, -1.001, -0.01, 0.0, 0.01, 1.01, 2.01, 3.01, 4.01]})
    styler = traf.colorize_by_std_deviations(df)
    assert styler is not None
    assert type(styler) == pandas.io.formats.style.Styler
    params = styler.export()[0][2]    # get some attributes from styler in a dict
    assert params is not None
    assert params['cmap'] is not None
    assert type(params['cmap']) == matplotlib.colors.LinearSegmentedColormap
    assert params['vmax'] is not None
    assert params['vmax'] == 4.0
    assert params['vmin'] is not None
    assert params['vmin'] == -4.0


  def test_load_tsv(self):
    qm_df = traf.load_tsv(self.gtest_tstfyl)
    print(qm_df)
    assert qm_df is not None
    assert type(qm_df) == pandas.core.frame.DataFrame
    assert qm_df.size == self.df_cell_count
    assert qm_df.shape == self.df_shape


  def test_make_legends_rpts(self):
    traf.make_legends()
    # os.system(f"ls -lH {REPORTS_DIR} >/tmp/DEBUGRPTS")
    files = os.listdir(REPORTS_DIR)
    print(f"FILES={files}")
    assert files is not None
    assert len(files) == 2
    for fyl in files:
      fpath = os.path.join(REPORTS_DIR, fyl)
      assert os.path.getsize(fpath) >= self.legend_min_size


  def test_make_legends(self):
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


  def test_normalize_to_zscores(self):
    qm_df = traf.load_tsv(self.gtest_tstfyl)
    norm_df = traf.normalize_to_zscores(qm_df)
    assert type(norm_df) == pandas.core.frame.DataFrame
    assert norm_df.size == self.df_cell_count
    assert norm_df.shape == self.df_shape
    print(type(norm_df['bids_name'][0]))
    assert type(norm_df['bids_name'][0]) == str
    print(type(norm_df.iloc[0, 1]))
    assert type(norm_df.iloc[0, 1]) == numpy.float64


  def test_write_table_to_html(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      qm_df = traf.load_tsv(self.gtest_tstfyl)
      norm_df = traf.normalize_to_zscores(qm_df)
      styler = traf.colorize_by_std_deviations(norm_df)
      traf.write_table_to_html(styler, "table.html", dirpath=tmpdir)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1
      for fyl in files:
        fpath = os.path.join(tmpdir, fyl)
        assert os.path.getsize(fpath) > self.html_min_size
