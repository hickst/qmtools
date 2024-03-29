# Functional tests of the MRIQC data fetcher code.
#   Written by: Tom Hicks and Dianne Patterson. 8/24/2021.
#   Last Modified: Update test for renamed timeout keyword parameters.
#
import os
import pytest
import requests as req
import sys
import tempfile

from qmtools import FETCHED_DIR
from qmtools.qmfetcher import SERVER_PAGE_SIZE
import qmtools.qmfetcher.fetcher_cli as cli
import qmtools.qmfetcher.fetcher as fetch
from tests import TEST_RESOURCES_DIR


@pytest.fixture
def popdir(request):
  yield
  os.chdir(request.config.invocation_dir)


class TestFetcherMain(object):

  query_file = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  def test_do_query_bad_url(self):
    bad_url = 'https://mriqc.nimh.nih.gov/badjunk?max_records=1'
    with pytest.raises(req.RequestException) as re:
      fetch.do_query(bad_url, connection_timeout=2)
    print(re)


  def test_do_query_noresults(self):
    noresult_query = 'https://mriqc.nimh.nih.gov/api/v1/bold?max_records=1&where=bids_meta.Manufacturer%3D%3D"BADCO"'
    rec = fetch.do_query(noresult_query)
    assert rec is not None
    assert type(rec) == dict
    assert '_items' in rec
    assert '_meta' in rec
    assert (rec.get('_meta')).get('total') == 0


  def test_get_n_records_norecs(self):
    args = {'num_recs': 2, 'query_params': [['dummy_trs', '==999']] }
    recs = fetch.get_n_records('bold', args)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 0


  def test_main_1(self, capsys, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      print(f"tmpdir={tmpdir}")
      sys.argv = ['qmtools', '-v', 'bold', '-n', '1', '-o', 'test']
      cli.main()
      sysout, syserr = capsys.readouterr()
      print(f"CAPTURED SYS.ERR:\n{syserr}")
      print(f"CAPTURED SYS.OUT:\n{sysout}")
      assert "Querying MRIQC server with modality 'bold'" in syserr
      tstfile = f"{FETCHED_DIR}/test.tsv"
      assert f"Saved query results to '{tstfile}'" in syserr
      with open(tstfile) as tstf:
        lines = tstf.readlines()
        print(f"LINES[0]={lines[0]}")
        print(f"LINES[1]={lines[1]}")
      assert len(lines) >= 2
      assert '_id' in lines[0]
      assert '_created' in lines[0]
      assert 'aor' in lines[0]         # bold only


  def test_main_pagesize(self, capsys, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      print(f"tmpdir={tmpdir}")
      print(f"S_P_S={SERVER_PAGE_SIZE}")
      sys.argv = ['qmtools', '-v', 'T2w', '-n', str(SERVER_PAGE_SIZE), '-o', 'test.tsv']
      cli.main()
      sysout, syserr = capsys.readouterr()
      print(f"CAPTURED SYS.ERR:\n{syserr}")
      print(f"CAPTURED SYS.OUT:\n{sysout}")
      assert "Querying MRIQC server with modality 'T2w'" in syserr
      tstfile = f"{FETCHED_DIR}/test.tsv"
      assert f"Saved query results to '{tstfile}'" in syserr
      with open(tstfile) as tstf:
        lines = tstf.readlines()
        print(f"LINES[0]={lines[0]}")
      assert len(lines) >= SERVER_PAGE_SIZE + 1
      assert '_id' in lines[0]
      assert '_created' in lines[0]
      assert 'cnr' in lines[0]         # structural only
      assert 'aor' not in lines[0]     # bold only


  def test_main_pagesize_plus(self, capsys, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      print(f"tmpdir={tmpdir}")
      print(f"S_P_S={SERVER_PAGE_SIZE}")
      sys.argv = ['qmtools', '-v', 'bold', '-n', str(SERVER_PAGE_SIZE + 4), '-o', 'test.tsv']
      cli.main()
      sysout, syserr = capsys.readouterr()
      print(f"CAPTURED SYS.ERR:\n{syserr}")
      print(f"CAPTURED SYS.OUT:\n{sysout}")
      assert "Querying MRIQC server with modality 'bold'" in syserr
      tstfile = f"{FETCHED_DIR}/test.tsv"
      assert f"Saved query results to '{tstfile}'" in syserr
      with open(tstfile) as tstf:
        lines = tstf.readlines()
        print(f"LINES[0]={lines[0]}")
      assert len(lines) >= (SERVER_PAGE_SIZE + 5)
      assert '_id' in lines[0]
      assert '_created' in lines[0]
      assert 'aor' in lines[0]           # bold only


  def test_main_pagesize_2x(self, capsys, popdir):
    with tempfile.TemporaryDirectory() as tmpdir:
      os.chdir(tmpdir)
      print(f"tmpdir={tmpdir}")
      print(f"S_P_S={SERVER_PAGE_SIZE}")
      sys.argv = ['qmtools', '-v', 'bold', '-n', str(2 * SERVER_PAGE_SIZE), '-o', 'test.tsv']
      cli.main()
      sysout, syserr = capsys.readouterr()
      print(f"CAPTURED SYS.ERR:\n{syserr}")
      print(f"CAPTURED SYS.OUT:\n{sysout}")
      assert "Querying MRIQC server with modality 'bold'" in syserr
      tstfile = f"{FETCHED_DIR}/test.tsv"
      assert f"Saved query results to '{tstfile}'" in syserr
      with open(tstfile) as tstf:
        lines = tstf.readlines()
        print(f"LINES[0]={lines[0]}")
      assert len(lines) >= (2 * SERVER_PAGE_SIZE + 1)
      assert '_id' in lines[0]
      assert '_created' in lines[0]
      assert 'aor' in lines[0]           # bold only


  # def test_query_for_page_default(self):
  #   query = f"https://mriqc.nimh.nih.gov/api/v1/bold?max_results={SERVER_PAGE_SIZE}"
  #   recs = fetch.query_for_page(query)
  #   print(f"LEN(recs)={len(recs)}")
  #   assert recs is not None
  #   assert type(recs) == list
  #   assert len(recs) == SERVER_PAGE_SIZE


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
