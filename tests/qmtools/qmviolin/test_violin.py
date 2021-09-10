# Tests of the IMQ Violin plotting modules.
#   Written by: Tom Hicks and Dianne Patterson. 9/7/2021.
#   Last Modified: Add tests for gen_plot_filename.
#
import qmtools.qm_utils as qmu
import qmtools.qmviolin.violin as violin
from qmtools import PLOT_EXT


class TestViolin(object):

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
