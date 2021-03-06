# Tests of the IMQ Violin plotting modules.
#   Written by: Tom Hicks and Dianne Patterson. 9/7/2021.
#   Last Modified: Move tests due to last refactoring.
#
import os
import pytest
import tempfile

import qmtools.qm_utils as qmu
import qmtools.qmviolin.violin as violin
from qmtools import PLOT_EXT 
from tests import TEST_RESOURCES_DIR


class TestViolin(object):

  bold_test_fyl = f"{TEST_RESOURCES_DIR}/bold_test.tsv"    # group file
  fetch_test_fyl = f"{TEST_RESOURCES_DIR}/manmafmagskyra50.tsv"  # fetched file

  aor_plot_info = { 'aor': os.path.join(TEST_RESOURCES_DIR, 'bold_aor.png') }
  fber_plot_info = { 'fber': os.path.join(TEST_RESOURCES_DIR, 'bold_fber.png') }

  num_auxiliary_files = 4              # 3 png, 1 css copied from resources


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


  def test_make_html_report(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      args = { 'modality': 'bold', 'report_dirpath': tmpdir }
      violin.make_html_report('bold', args, self.aor_plot_info)
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == 1 + self.num_auxiliary_files   # html + aux files
      assert 'violin.html' in files


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


  def test_vplot_badmode(self):
    with pytest.raises(ValueError) as ve:
      violin.vplot('BADMODE', {})
    assert 'Modality argument must be one of' in str(ve)


  def test_vplot_noargs(self):
    with pytest.raises(FileNotFoundError) as fnf:
      violin.vplot('bold', {})
    assert "Required 'fetched_file' filepath not found" in str(fnf)


  def test_vplot_nogrpfyl(self):
    with pytest.raises(FileNotFoundError) as fnf:
      violin.vplot('bold', {'fetched_file': self.fetch_test_fyl})
    assert "Required 'group_file' filepath not found" in str(fnf)


  def test_vplot(self):
    iqms = violin.select_iqms_to_plot('bold')
    with tempfile.TemporaryDirectory() as tmpdir:
      print(f"tmpdir={tmpdir}")
      args = {
       'modality': 'bold', 'report_dirpath': tmpdir,
       'fetched_file': self.fetch_test_fyl, 'group_file': self.bold_test_fyl
      }
      plot_info = violin.vplot('bold', args)
      print(f"PLOT_INFO={plot_info}")

      # check the returned plot information dictionary:
      assert plot_info is not None
      assert len(plot_info) == len(iqms)
      iqms = list(plot_info.keys())
      assert 'aor' in iqms
      assert 'fber' in iqms
      assert 'qi_1' not in iqms

      # now check the plot/reports files
      files = os.listdir(tmpdir)
      print(f"FILES={files}")
      assert files is not None
      assert len(files) == len(iqms)
