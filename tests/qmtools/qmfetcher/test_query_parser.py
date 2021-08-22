# Tests of the module to read and parse a query parameters file.
#   Written by: Tom Hicks and Dianne Patterson. 8/17/2021.
#   Last Modified: Add tests for parse_query_from_file and validate_query_params.
#
import configparser
import os
import pytest
import sys

from tests import TEST_RESOURCES_DIR
import qmtools.qmfetcher.query_parser as qp

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse


class TestQueryParser(object):

  TEST_NAME = 'TestQueryParser'

  empty_query_fyl = f"{TEST_RESOURCES_DIR}/empty.qp"
  nocolon_query_fyl = f"{TEST_RESOURCES_DIR}/nocolon.qp"
  noparams_query_fyl = f"{TEST_RESOURCES_DIR}/noparams.qp"
  noparamsec_query_fyl = f"{TEST_RESOURCES_DIR}/noparamsec.qp"
  nosec_query_fyl = f"{TEST_RESOURCES_DIR}/nosec.qp"
  params_query_fyl = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  query_params_dict = {
    'snr': '>  5',
    'bids_meta.Manufacturer': '== "Siemens"',
    'bids_meta.RepetitionTime': '<= 3'
  }


  def test_parse_query_from_file(self):
    pd = qp.parse_query_from_file('bold', self.params_query_fyl, self.TEST_NAME)
    assert pd is not None
    assert type(pd) is dict
    assert len(pd) == 3
    assert 'dummy_trs' in pd.keys()
    assert 'bids_meta.Manufacturer' in pd.keys()


  def test_load_query_from_file_nosuch(self):
    with pytest.raises(FileNotFoundError) as fnf:
      qp.load_query_from_file('NOSUCH_FILE', self.TEST_NAME)
    print(fnf)
    assert f"Query parameters file 'NOSUCH_FILE' not found" in str(fnf)


  def test_load_query_from_file_empty(self):
    with pytest.raises(ValueError) as ve:
      qp.load_query_from_file(self.empty_query_fyl, self.TEST_NAME)
    print(ve)
    assert 'No section named' in str(ve)


  def test_load_query_from_file_nosec(self):
    with pytest.raises(ValueError) as ve:
      qp.load_query_from_file(self.nosec_query_fyl, self.TEST_NAME)
    print(ve)
    assert "A 'parameters' section header" in str(ve)


  def test_load_query_from_file_noparamsec(self):
    with pytest.raises(ValueError) as ve:
      qp.load_query_from_file(self.noparamsec_query_fyl, self.TEST_NAME)
    print(ve)
    assert 'No section named' in str(ve)


  def test_load_query_from_file_nocolon(self):
    with pytest.raises(ValueError) as ve:
      pd = qp.load_query_from_file(self.nocolon_query_fyl, self.TEST_NAME)
    print(ve)
    assert 'Source contains parsing errors' in str(ve)
    assert 'line  4' in str(ve)


  def test_load_query_from_file_noparams(self):
    pd = qp.load_query_from_file(self.noparams_query_fyl, self.TEST_NAME)
    assert pd is not None
    assert type(pd) is dict
    assert len(pd) == 0


  def test_load_query_from_file_params(self):
    pd = qp.load_query_from_file(self.params_query_fyl, self.TEST_NAME)
    assert pd is not None
    assert type(pd) is dict
    assert len(pd) == 3
    assert 'dummy_trs' in pd.keys()
    assert 'bids_meta.Manufacturer' in pd.keys()


  def test_parse_value_noop(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_value('', self.TEST_NAME)
    assert 'The comparison operator must be' in str(ve)


  def test_parse_value_badop(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_value('=', self.TEST_NAME)
    assert 'The comparison operator must be' in str(ve)


  def test_parse_value_ee_only(self):
    with pytest.raises(ValueError) as ve:
      comp = qp.parse_value('==', self.TEST_NAME)
    assert 'The value to be compared' in str(ve)


  def test_parse_value_ee(self):
    comp = qp.parse_value('==  x', self.TEST_NAME)
    assert comp is not None
    assert comp == '==x'


  def test_parse_value_lt(self):
    comp = qp.parse_value('<  xyz', self.TEST_NAME)
    assert comp is not None
    assert comp == '<xyz'


  def test_validate_keyword_b_empty(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('bold', '', self.TEST_NAME)
    assert 'is not a valid bold keyword' in str(ve)


  def test_validate_keyword_b_badword(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('bold', 'XXX', self.TEST_NAME)
    assert "'XXX' is not a valid bold keyword" in str(ve)


  def test_validate_keyword_b_badmode(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('bold', 'cnr', self.TEST_NAME)
    assert "'cnr' is not a valid bold keyword" in str(ve)


  def test_validate_keyword_b_good(self):
    assert qp.validate_keyword('bold', 'aor', self.TEST_NAME)
    assert qp.validate_keyword('bold', 'dummy_trs', self.TEST_NAME)
    assert qp.validate_keyword('bold', 'bids_meta.subject_id', self.TEST_NAME)
    assert qp.validate_keyword('bold', 'provenance.md5sum', self.TEST_NAME)
    assert qp.validate_keyword('bold', 'rating.name', self.TEST_NAME)
    assert qp.validate_keyword('bold', 'bids_meta.TaskName', self.TEST_NAME)


  def test_validate_keyword_s_empty(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('T1w', '', self.TEST_NAME)
    assert 'is not a valid T1w keyword' in str(ve)


  def test_validate_keyword_s_badword(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('T1w', 'XXX', self.TEST_NAME)
    assert "'XXX' is not a valid T1w keyword" in str(ve)


  def test_validate_keyword_s_badmode(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('T1w', 'aor', self.TEST_NAME)
    assert "'aor' is not a valid T1w keyword" in str(ve)


  def test_validate_keyword_s_taskname(self):
    with pytest.raises(ValueError) as ve:
      qp.validate_keyword('T1w', 'bids_meta.TaskName', self.TEST_NAME)
    assert "'bids_meta.TaskName' is not a valid T1w keyword" in str(ve)


  def test_validate_keyword_s_good(self):
    assert qp.validate_keyword('T1w', 'cnr', self.TEST_NAME)
    assert qp.validate_keyword('T1w', 'fber', self.TEST_NAME)
    assert qp.validate_keyword('T1w', 'bids_meta.subject_id', self.TEST_NAME)
    assert qp.validate_keyword('T1w', 'provenance.version', self.TEST_NAME)
    assert qp.validate_keyword('T1w', 'wm2max', self.TEST_NAME)


  def test_validate_query_params(self):
    qpd = self.query_params_dict
    qp.validate_query_params('bold', qpd, self.TEST_NAME)
    assert qpd is not None
    assert len(qpd) == 3
    assert 'snr' in qpd
    assert 'bids_meta.Manufacturer' in qpd
    assert 'bids_meta.RepetitionTime' in qpd
    assert 'dummy_trs' not in qpd
