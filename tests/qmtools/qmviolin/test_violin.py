# Tests of the IMQ Violin plotting modules.
#   Written by: Tom Hicks and Dianne Patterson. 9/7/2021.
#   Last Modified: Initial creation: test_select_iqms_to_plot only.
#
import qmtools.qm_utils as qmu
import qmtools.qmviolin.violin as violin


class TestViolin(object):

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
