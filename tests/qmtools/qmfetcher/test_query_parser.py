# Tests of the module to read and parse a query parameters file.
#   Written by: Tom Hicks and Dianne Patterson. 8/17/2021.
#   Last Modified: Begin to redo for rewritten query parsing.
#
import pytest

from tests import TEST_RESOURCES_DIR
import qmtools.qmfetcher.query_parser as qp

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestQueryParser(object):

  TEST_NAME = 'TestQueryParser'

  empty_query_fyl = f"{TEST_RESOURCES_DIR}/empty.qp"
  nospace_query_fyl = f"{TEST_RESOURCES_DIR}/nospace.qp"
  noparams_query_fyl = f"{TEST_RESOURCES_DIR}/noparams.qp"
  comments_query_fyl = f"{TEST_RESOURCES_DIR}/withcomments.qp"
  nosec_query_fyl = f"{TEST_RESOURCES_DIR}/nosec.qp"
  params_query_fyl = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  query_params_list = [
    ['snr', '>  5'],
    ['bids_meta.Manufacturer', '== "Siemens"'],
    ['bids_meta.RepetitionTime', '<= 3']
  ]

  def test_parse_query_from_file(self):
    pd = qp.parse_query_from_file('bold', self.params_query_fyl, self.TEST_NAME)
    print(pd)
    assert pd is not None
    assert type(pd) is list
    assert len(pd) == 3
    assert 'dummy_trs' in str(pd)
    assert 'bids_meta.Manufacturer' in str(pd)


  def test_load_criteria_from_file_nosuch(self):
    with pytest.raises(FileNotFoundError) as fnf:
      qp.load_criteria_from_file('NOSUCH_FILE', self.TEST_NAME)
    print(fnf)
    assert f"Query parameters file 'NOSUCH_FILE' not found" in str(fnf)


  def test_load_criteria_from_file_empty(self):
    pd = qp.load_criteria_from_file(self.empty_query_fyl, self.TEST_NAME)
    print(pd)
    assert pd is not None
    assert len(pd) == 0


  def test_load_criteria_from_file_nospace(self):
    pd = qp.load_criteria_from_file(self.nospace_query_fyl, self.TEST_NAME)
    print(pd)
    assert pd is not None
    assert type(pd) is list
    assert len(pd) == 4
    assert 'dummy_trs' in str(pd)
    assert 'bids_meta.Manufacturer' in str(pd)
    assert 'size_x' in str(pd)


  def test_load_criteria_from_file_noparams(self):
    pd = qp.load_criteria_from_file(self.noparams_query_fyl, self.TEST_NAME)
    print(pd)
    assert pd is not None
    assert type(pd) is list
    assert len(pd) == 0


  def test_load_criteria_from_file_params(self):
    pd = qp.load_criteria_from_file(self.params_query_fyl, self.TEST_NAME)
    print(pd)
    assert pd is not None
    assert type(pd) is list
    assert len(pd) == 3
    assert 'dummy_trs' in str(pd)
    assert 'bids_meta.Manufacturer' in str(pd)


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
    print(comp)
    assert comp is not None
    assert comp == '==x'


  def test_parse_value_lt(self):
    comp = qp.parse_value('<  xyz', self.TEST_NAME)
    print(comp)
    assert comp is not None
    assert comp == '<xyz'


  def test_parse_query_from_file_nospaces(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_query_from_file('bold', self.nospace_query_fyl, self.TEST_NAME)
    print(ve)
    assert 'Spaces must separate the parts of a query parameter line' in str(ve)


  def test_parse_query_from_file(self):
    qpd = qp.parse_query_from_file('bold', self.params_query_fyl, self.TEST_NAME)
    assert qpd is not None
    assert type(qpd) is list
    assert len(qpd) == 3
    assert 'dummy_trs' in str(qpd)
    assert 'bids_meta.Manufacturer' in str(qpd)
    assert 'bids_meta.MultibandAccelerationFactor' in str(qpd)
    assert 'snr' not in str(qpd)


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
