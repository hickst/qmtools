# Functional tests of the MRIQC data fetcher code.
#   Written by: Tom Hicks and Dianne Patterson. 8/24/2021.
# Last Modified: Update tests for args dictionary.
#
import os
import pytest
import requests as req
import sys

from qmtools.qmfetcher import SERVER_PAGE_SIZE
import qmtools.qmfetcher.fetcher as fetch
# from qmtools.qmfetcher.fetcher import SERVER_URL
from tests import TEST_RESOURCES_DIR


class TestFetcherMain(object):

  noresult_query = 'https://mriqc.nimh.nih.gov/api/v1/bold?max_records=1&where=bids_meta.Manufacturer%3D%3D"BADCO"'
  query_file = f"{TEST_RESOURCES_DIR}/manmaf.qp"


  def test_do_query_noresults(self):
    rec = fetch.do_query(self.noresult_query)
    assert rec is not None
    assert type(rec) == dict
    assert '_items' in rec
    assert '_meta' in rec
    assert (rec.get('_meta')).get('total') == 0


  def test_get_n_records_norecs(self):
    qparams = { 'dummy_trs': '==999' }
    args = {'num_recs': 2, 'query_params': qparams}
    recs = fetch.get_n_records('bold', args)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 0


  def test_get_n_records_0(self):
    recs = fetch.get_n_records('bold', {'num_recs': 0})
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE


  def test_get_n_records_1(self):
    recs = fetch.get_n_records('bold', {'num_recs': 1})
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 1


  def test_get_n_records_9(self):
    recs = fetch.get_n_records('bold', {'num_recs': 9})
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 9


  def test_get_n_records_pagesize(self):
    recs = fetch.get_n_records('bold', {'num_recs': SERVER_PAGE_SIZE})
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE


  def test_get_n_records_pagesize_plus(self):
    recs = fetch.get_n_records('bold', {'num_recs': SERVER_PAGE_SIZE+4})
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE+4


  def test_get_n_records_pagesize2x(self):
    recs = fetch.get_n_records('bold', {'num_recs': 2 * SERVER_PAGE_SIZE})
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 2 * SERVER_PAGE_SIZE


  def test_query_for_page_default(self):
    query = f"https://mriqc.nimh.nih.gov/api/v1/bold?max_results={SERVER_PAGE_SIZE}"
    recs = fetch.query_for_page(query)
    print(f"LEN(recs)={len(recs)}")
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE


  def test_server_health_check(self):
    try:
      total_recs = fetch.server_status()
      print(f"TOTAL_RECS={total_recs}")
      assert (total_recs > 900000)       # DB has surpassed this number already
    except req.RequestException as re:
      print(str(re))
      status = re.response.status_code
      if (status == 503):
        assert True
      else:
        assert False


  # def test_main_verbose(self, capsys):
  #   with tempfile.TemporaryDirectory() as tmpdir:
  #     os.chdir(tmpdir)
  #     print(f"tmpdir={tmpdir}")
  #     sys.argv = ['qmtools', '-v', '-m', 'bold']
  #     cli.main()
  #     sysout, syserr = capsys.readouterr()
  #     print(f"CAPTURED SYS.ERR:\n{syserr}")
  #     assert "Querying MRIQC server with modality 'bold'" in syserr
  #     assert f"Saved query results to '{FETCHED_DIR}/bold_" in syserr
