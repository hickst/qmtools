# Tests of Shared utilities for the QMTools programs.
#   Written by: Tom Hicks and Dianne Patterson. 8/5/2021.
#   Last Modified: Move tests due to last refactoring.
#
import os
import pandas
import pytest
import tempfile
import seaborn as sb

from tests import TEST_RESOURCES_DIR
from qmtools import (BIDS_DATA_EXT, FETCHED_DIR, FETCHED_DIR_EXIT_CODE,
                     PLOT_EXT, REPORTS_DIR, REPORTS_DIR_EXIT_CODE, REPORTS_EXT)
import qmtools.qm_utils as qmu


@pytest.fixture
def popdir(request):
  yield
  os.chdir(request.config.invocation_dir)


class TestQMUtils(object):

  bold_test_fyl  = f"{TEST_RESOURCES_DIR}/bold_test.tsv"
  df_cell_count = 855                  # size of test dataframe
  df_shape = (19, 45)                  # shape of test dataframe
  fig_min_size = 20000                 # min bytes for our test figure in a .png file

  html_text = '<html><head></head><body></body></html>'


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


  def test_ensure_reports_dirs(self, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)                 # popdir must restore test dir after test
      print(f"CWD={os.getcwd()}, tmpdir={tmpdir}")
      dpath = f"{REPORTS_DIR}/child/newdir"
      assert not os.path.isdir(dpath)
      qmu.ensure_reports_dir('TestQMUtils', dir_path=dpath)
      assert os.path.isdir(dpath)
      assert os.access(dpath, os.W_OK)


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


  def test_gen_output_name(self):
    fname = qmu.gen_output_name('bold', BIDS_DATA_EXT)
    print(fname)
    assert 'bold' in fname
    assert '.tsv' in fname


  def test_gen_output_name_badmode(self):
    fname = qmu.gen_output_name('BOLDER', BIDS_DATA_EXT)
    print(fname)
    assert 'BOLDER' in fname
    assert '.tsv' in fname


  def test_gen_output_name_ext(self):
    fname = qmu.gen_output_name('T1w', '.csv')
    print(fname)
    assert 'T1w' in fname
    assert '.csv' in fname


  def test_gen_output_name_noext(self):
    fname = qmu.gen_output_name('aDir')
    print(fname)
    assert 'aDir' in fname
    assert '.csv' not in fname
    assert '.tsv' not in fname


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


  def make_fig(self):
    tips = sb.load_dataset("tips")
    return sb.catplot(x="smoker", y="tip", order=["No", "Yes"], data=tips)


  def test_write_figure_to_file(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      fig = self.make_fig()
      qmu.write_figure_to_file(fig, "figure", dirpath=tmpdir)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1
      for fyl in files:
        assert str(fyl).endswith(PLOT_EXT)
        fpath = os.path.join(tmpdir, fyl)
        fsize = os.path.getsize(fpath)
        print(f"FSIZE={fsize}")
        assert fsize > self.fig_min_size


  def test_write_html_to_file_default(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      qmu.write_html_to_file(self.html_text, 'BOLD_OUT.html', tmpdir)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1
      for fyl in files:
        assert str(fyl).endswith(REPORTS_EXT)
        fpath = os.path.join(tmpdir, fyl)
        fsize = os.path.getsize(fpath)
        print(f"FSIZE={fsize}")
        assert fsize >= len(self.html_text)


  def test_write_html_to_file_filename(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      qmu.write_html_to_file(self.html_text, 'happy.html', tmpdir)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1
      for fyl in files:
        assert 'happy' in str(fyl)
        assert str(fyl).endswith(REPORTS_EXT)
        fpath = os.path.join(tmpdir, fyl)
        fsize = os.path.getsize(fpath)
        print(f"FSIZE={fsize}")
        assert fsize >= len(self.html_text)
