# Tests of the IMQ Violin plotting modules.
#   Written by: Tom Hicks and Dianne Patterson. 9/7/2021.
#   Last Modified: Add tests for write_html.
#
import os
import pytest
import tempfile

import qmtools.qmviolin.violin as violin
from qmtools import PLOT_EXT, REPORTS_EXT
from tests import TEST_RESOURCES_DIR


class TestViolin(object):

  bold_test_fyl = f"{TEST_RESOURCES_DIR}/bold_test.tsv"    # group file
  fetch_test_fyl = f"{TEST_RESOURCES_DIR}/manmafmagskyra50.tsv"  # fetched file

  html_text = '<html><head></head><body></body></html>'

  def test_vplot_badmode(self):
    with pytest.raises(ValueError) as ve:
      violin.vplot('BADMODE', {})
    assert 'Modality argument must be one of' in str(ve)


  def test_vplot_noargs(self, capsys):
    with pytest.raises(FileNotFoundError) as fnf:
      violin.vplot('bold', {})
    assert "Required 'fetched_file' filepath not found" in str(fnf)


  def test_vplot_nogrpfyl(self, capsys):
    with pytest.raises(FileNotFoundError) as fnf:
      violin.vplot('bold', {'fetched_file': self.fetch_test_fyl})
    assert "Required 'group_file' filepath not found" in str(fnf)


  def test_gen_plot_filename(self):
    fname = violin.gen_plot_filename('bold', 'aor')
    print(fname)
    assert 'bold' in fname
    assert 'aor' in fname
    assert PLOT_EXT in fname


  def test_gen_plot_filename_ext(self):
    fname = violin.gen_plot_filename('T1w', 'cjv', extension='.plot')
    print(fname)
    assert 'T1w' in fname
    assert 'cjv' in fname
    assert '.plot' in fname
    assert PLOT_EXT not in fname


  def test_gen_plot_filename_fake(self):
    "NB: this test will succeed since no semantic checking is done."
    fname = violin.gen_plot_filename('BOLDER', 'NOSUCH', extension='.crazy')
    print(fname)
    assert 'BOLDER' in fname
    assert 'NOSUCH' in fname
    assert '.crazy' in fname


  def test_make_html_report_nodirpath(self):
    with pytest.raises(FileNotFoundError) as fnf:
      violin.make_html_report('bold', {}, {})
    assert 'Required reports directory path not found' in str(fnf)


  def test_select_iqms_to_plot_bold(self):
    iqms = violin.select_iqms_to_plot('bold')
    assert iqms is not None
    assert len(iqms) > 0
    assert 'aor' in iqms
    assert 'fber' in iqms
    assert 'snr' in iqms
    assert 'bids_name' not in iqms
    assert 'cjv' not in iqms


  def test_select_iqms_to_plot_struct(self):
    iqms = violin.select_iqms_to_plot('T1w')
    assert iqms is not None
    assert len(iqms) > 0
    assert 'cjv' in iqms
    assert 'fber' in iqms
    assert 'bids_name' not in iqms
    assert 'aor' not in iqms


  def test_select_iqms_to_plot_userB(self):
    kws = [ 'aor', 'cjv', 'fber', 'bids_name', 'snr', 'YUCK' ]
    iqms = violin.select_iqms_to_plot('bold', plot_iqms=kws)
    assert iqms is not None
    assert len(iqms) > 0
    assert 'aor' in iqms
    assert 'fber' in iqms
    assert 'snr' in iqms
    assert 'cjv' not in iqms
    assert 'qi_1' not in iqms
    assert 'bids_name' not in iqms
    assert 'YUCK' not in iqms


  def test_select_iqms_to_plot_userS(self):
    kws = [ 'aor', 'cjv', 'fber', 'bids_name', 'qi_1', 'YUCK' ]
    iqms = violin.select_iqms_to_plot('T2w', plot_iqms=kws)
    assert iqms is not None
    assert len(iqms) > 0
    assert 'cjv' in iqms
    assert 'fber' in iqms
    assert 'qi_1' in iqms
    assert 'aor' not in iqms
    assert 'snr' not in iqms
    assert 'bids_name' not in iqms
    assert 'YUCK' not in iqms


  def test_write_html_default(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      violin.write_html(self.html_text, tmpdir)
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


  def test_write_html_filename(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      violin.write_html(self.html_text, tmpdir, filename='happy.html')
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
