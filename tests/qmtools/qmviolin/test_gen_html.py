# Tests of the module to generate the HTML violin report.
#   Written by: Tom Hicks and Dianne Patterson. 9/18/2021.
#   Last Modified: Initial creation: test_gen_html only.
#
import os

import qmtools.qmviolin.gen_html as gh

from tests import TEST_RESOURCES_DIR


class TestGenHTML(object):

  aor_docs = { 'aor': 'A FAKE description for testing purposes.' }

  aor_plot_info = { 'aor': os.path.join(TEST_RESOURCES_DIR, 'bold_aor.png') }
  fber_plot_info = { 'fber': os.path.join(TEST_RESOURCES_DIR, 'bold_fber.png') }

  len_template = len(gh.PAGE_TEMPLATE)

  def test_gen_html_bold_lo(self):
    html_text = gh.gen_html('bold', self.aor_plot_info)
    assert html_text is not None
    assert len(html_text) >= self.len_template
    assert 'Comparison of MRIQC IQM datasets' in html_text
    assert 'bold' in html_text
    assert 'bold_aor.png' in html_text
    assert 'id="aor"' in html_text
    assert "AFNI's outlier ratio" in html_text
    assert "Low values are better" in html_text
    assert '{{modality}}' not in html_text
    assert 'cjv' not in html_text


  def test_gen_html_bold_docs(self):
    html_text = gh.gen_html('bold', self.aor_plot_info, docs=self.aor_docs)
    assert html_text is not None
    assert len(html_text) >= self.len_template
    assert 'Comparison of MRIQC IQM datasets' in html_text
    assert 'bold' in html_text
    assert 'bold_aor.png' in html_text
    assert 'id="aor"' in html_text
    assert "Low values are better" in html_text
    assert "AFNI" not in html_text
    assert '{{modality}}' not in html_text
    assert 'cjv' not in html_text


  def test_gen_html_bold_hi(self):
    html_text = gh.gen_html('bold', self.fber_plot_info)
    assert html_text is not None
    assert len(html_text) >= self.len_template
    assert 'Comparison of MRIQC IQM datasets' in html_text
    assert 'bold' in html_text
    assert 'bold_fber.png' in html_text
    assert 'id="fber"' in html_text
    assert "High values are better" in html_text
    assert '{{modality}}' not in html_text
    assert 'cjv' not in html_text
