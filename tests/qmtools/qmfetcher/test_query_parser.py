# Tests of the module to read and parse a query parameters file.
#   Written by: Tom Hicks and Dianne Patterson. 8/17/2021.
#   Last Modified: Add tests for remaining functions.
#
import pytest

from tests import TEST_RESOURCES_DIR
import qmtools.qmfetcher.query_parser as qp

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestQueryParser(object):

  TEST_NAME = 'TestQueryParser'

  empty_query_fyl = f"{TEST_RESOURCES_DIR}/empty.qp"
  nospace_query_fyl = f"{TEST_RESOURCES_DIR}/nospace.qp"
  justcomment_query_fyl = f"{TEST_RESOURCES_DIR}/justcomment.qp"
  comments_query_fyl = f"{TEST_RESOURCES_DIR}/withcomments.qp"
  multikey_query_fyl = f"{TEST_RESOURCES_DIR}/metrics.qp"
  nosec_query_fyl = f"{TEST_RESOURCES_DIR}/nosec.qp"
  params_query_fyl = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  query_params_list = [
    ['snr', '>  5'],
    ['bids_meta.Manufacturer', '== "Siemens"'],
    ['bids_meta.RepetitionTime', '<= 3']
  ]

  acollection = range(10)

  criteria = [
    'snr  >  5',
    'bids_meta.Manufacturer == "Siemens Inc"',
    'bids_meta.RepetitionTime <= 3'
  ]


  def square_even (self, val):
    "Test function for use with testing keep function."
    return (val * val) if ((val % 2) == 0) else None


  def test_is_criteria_line_blank(self):
    assert qp.is_criteria_line('') is None
    assert qp.is_criteria_line(' ') is None
    assert qp.is_criteria_line('     ') is None
    assert qp.is_criteria_line('\t \t ') is None
    assert qp.is_criteria_line('  \t ') is None
    line = qp.is_criteria_line('  \t keyword')
    assert line is not None
    assert line == 'keyword'


  def test_is_criteria_line_comment(self):
    assert qp.is_criteria_line('#') is None
    assert qp.is_criteria_line('##') is None
    assert qp.is_criteria_line('   # comment') is None
    assert qp.is_criteria_line('\t### ignore this') is None


  def test_keep(self):
    print(self.square_even)
    kept = list(qp.keep(self.square_even, list(range(10))))
    print(kept)
    assert kept is not None
    assert len(kept) == 5
    assert kept == [0, 4, 16, 36, 64]


  def test_keep_empty_lst(self):
    kept = list(qp.keep(self.square_even, []))
    print(kept)
    assert kept is not None
    assert kept == []


  def test_keep_singleton(self):
    kept = list(qp.keep(self.square_even, [12]))
    print(kept)
    assert kept is not None
    assert kept == [144]


  def test_keep_empty_res(self):
    kept = list(qp.keep(self.square_even, [1, 3, 5, 9]))
    print(kept)
    assert kept is not None
    assert kept == []


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


  def test_load_criteria_from_file_justcomment(self):
    pd = qp.load_criteria_from_file(self.justcomment_query_fyl, self.TEST_NAME)
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


  def test_parse_key_and_value_nospace(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_key_and_value('bold', 'aor<4', self.TEST_NAME)
      print(ve)
      assert 'Spaces must separate the parts of a query parameter line' in str(ve)


  def test_parse_key_and_value_badkey(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_key_and_value('bold', 'BADKEY < 4', self.TEST_NAME)
      print(ve)
      assert "Keyword 'BADKEY' is not a valid bold keyword" in str(ve)


  def test_parse_key_and_value(self):
    kv = qp.parse_key_and_value('bold', 'aor <= 4', self.TEST_NAME)
    print(kv)
    assert type(kv) is tuple
    assert kv[0] == 'aor'
    assert kv[1] == '<= 4'


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


  def test_parse_criteria(self):
    params = qp.parse_criteria('bold', self.criteria, self.TEST_NAME)
    print(params)
    assert params is not None
    assert type(params) is list
    assert len(params) == 3
    assert 'snr' in params[0]
    assert 'bids_meta.Manufacturer' in params[1]
    assert 'bids_meta.RepetitionTime' in params[2]
    assert '=="Siemens Inc"' in params[1]


  def test_parse_query_from_file_nospaces(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_query_from_file('bold', self.nospace_query_fyl, self.TEST_NAME)
    print(ve)
    assert 'Spaces must separate the parts of a query parameter line' in str(ve)


  def test_parse_query_from_file(self):
    pd = qp.parse_query_from_file('bold', self.params_query_fyl, self.TEST_NAME)
    assert pd is not None
    assert type(pd) is list
    assert len(pd) == 3
    assert 'dummy_trs' in str(pd)
    assert 'bids_meta.Manufacturer' in str(pd)
    assert 'bids_meta.MultibandAccelerationFactor' in str(pd)
    assert 'snr' not in str(pd)


  def test_parse_query_from_file_multi(self):
    pd = qp.parse_query_from_file('bold', self.multikey_query_fyl, self.TEST_NAME)
    print(pd)
    assert pd is not None
    assert type(pd) is list
    assert len(pd) == 5
    assert 'dummy_trs' in str(pd)
    assert 'size_x' in str(pd)
    assert 'bids_meta.Manufacturer' in str(pd)
    assert 'Siemens' in str(pd)
    assert 'SIEMENS' in str(pd)
    assert 'bids_meta.RepetitionTime' not in str(pd)
