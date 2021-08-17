# Tests of the MRIQC data fetcher library code.
#   Written by: Tom Hicks and Dianne Patterson. 8/7/2021.
#   Last Modified: Added tests for get_n_records and do_query w/ no results.
#
import json
import os
import pandas
import pytest
import requests as req
import sys
import tempfile
from pathlib import Path

from qmtools import ALLOWED_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
import qmtools.qmfetcher.fetcher as fetch
from qmtools.qmfetcher.fetcher import SERVER_URL, DEFAULT_FIELDS_TO_REMOVE
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestFetcher(object):

  noresult_query = 'https://mriqc.nimh.nih.gov/api/v1/bold?max_records=1&where=bids_meta.Manufacturer%3D%3D"BADCO"'

  empty_results_fyl = f"{TEST_RESOURCES_DIR}/no_results.json"
  page1_results_fyl = f"{TEST_RESOURCES_DIR}/reptime1.json"
  page1_results_cnt = 25

  arec_len = 23
  arec = {
    '_id': '59cfad7f265d200019380537',
    'fber': 3165.384765625,
    'dummy_trs': 0,
    'bids_meta': {
      'RepetitionTime': 2.0,
      'subject_id': '6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918',
      'MagneticFieldStrength': 3,
      'modality': 'bold',
      'Manufacturer': 'Siemens',
      'EchoTime': 0.026
    },
    'gcor': 0.00348879,
    'fwhm_x': 2.266005,
    '_created': 'Sat, 30 Sep 2017 14:43:11 GMT',
    'provenance': {
      'md5sum': 'af34ecc2a49a550d49216f5b5b5b22d7',
      'settings': {
        'fd_thres': 0.2,
        'hmc_fsl': False
      },
      'version': '0.9.6',
      'software': 'mriqc'
    },
    'snr': 5.489635677064641,
    '_updated': 'Sat, 30 Sep 2017 14:43:11 GMT',
    '_etag': 'c93ade3cea8db90a9d1f6f1d4433effe5ce7192c',
    'spacing_z': 1.9999998807907104,
    '_links': {
      'self': {
        'title': 'bold',
        'href': 'bold/59cfad7f265d200019380537'
      }
    }
  }

  flrec = {
    '_id': '59cfad7f265d200019380537',
    'fber': 3165.384765625,
    'dummy_trs': 0,
    'bids_meta.RepetitionTime': 2.0,
    'bids_meta.modality': 'bold',
    'bids_meta.Manufacturer': 'Siemens',
    'bids_meta.EchoTime': 0.026,
    'gcor': 0.00348879,
    'fwhm_x': 2.266005,
    '_created': 'Sat, 30 Sep 2017 14:43:11 GMT',
    'provenance.md5sum': 'af34ecc2a49a550d49216f5b5b5b22d7',
    'provenance.settings.fd_thres': 0.2,
    'provenance.settings.hmc_fsl': False,
    'snr': 5.489635677064641,
    '_updated': 'Sat, 30 Sep 2017 14:43:11 GMT',
    '_etag': 'c93ade3cea8db90a9d1f6f1d4433effe5ce7192c',
    'spacing_z': 1.9999998807907104,
    '_links.self.title': 'bold',
    '_links.self.href': 'bold/59cfad7f265d200019380537'
  }

  for_dedup_recs = [
    {
      '_id': '1',
      'provenance.md5sum': '19cf39e8895fcf98e46f6017caebbbf1',
      'dummy_data': 111,
    },
    {
      '_id': '2',
      'provenance.md5sum': '42febfb2ff72767655b0901dbde42ecb',
      'dummy_data': 222,
    },
    {
      '_id': '999',
      'dummy_data': 'BAD RECORD',
    },
    {
      '_id': '3',
      'provenance.md5sum': 'af34ecc2a49a550d49216f5b5b5b22d7',
      'dummy_data': 333,
    }
  ]


  def test_build_query_bad_modality(self):
    with pytest.raises(ValueError) as ve:
      fetch.build_query('BAD_MODE')


  def test_build_query_modes_default(self):
    qstr = fetch.build_query('bold')
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1" in qstr
    qstr = fetch.build_query('t1w')
    assert f"{SERVER_URL}/t1w?max_results={SERVER_PAGE_SIZE}&page=1" in qstr
    qstr = fetch.build_query('t2w')
    assert f"{SERVER_URL}/t2w?max_results={SERVER_PAGE_SIZE}&page=1" in qstr


  def test_build_query_pagenum_nums(self):
    qstr = fetch.build_query('bold', None)
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1" in qstr
    qstr = fetch.build_query('bold', 0)
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1" in qstr
    qstr = fetch.build_query('bold', 1)
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1" in qstr
    qstr = fetch.build_query('bold', 999)
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=999" in qstr


  def test_build_query_latest(self):
    qstr = fetch.build_query('bold')
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1&sort=-_created" in qstr
    qstr = fetch.build_query('bold', latest=False)
    assert f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1" in qstr
    assert 'sort=' not in qstr
    assert '_created' not in qstr


  def test_clean_records_empty(self):
    with open(self.empty_results_fyl) as jfyl:
      results = json.load(jfyl)
    print(results)
    recs = fetch.extract_records(results)
    flrecs = fetch.flatten_records(recs)
    crecs = fetch.clean_records(flrecs)
    assert crecs is not None
    assert crecs == []


  def test_clean_records(self):
    crecs = fetch.clean_records([self.flrec])
    assert crecs is not None
    assert crecs != []
    assert len(crecs) == 1
    for rec in crecs:
      for field in DEFAULT_FIELDS_TO_REMOVE:
        assert rec.get(field) is None
      for field in ['bids_meta', '_links', 'provenance']:
        assert rec.get(field) is None


  def test_deduplicate_records(self):
    # Also tests is_not_duplicate
    recs = fetch.deduplicate_records(self.for_dedup_recs,set())
    assert recs is not None
    assert len(recs) == 3

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set(['8f56e0168c25e7bd919572669c2e43be'])) # not in set: has no effect
    assert recs is not None
    assert len(recs) == 3

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set(['42febfb2ff72767655b0901dbde42ecb']))      # should remove 1 record
    assert recs is not None
    assert len(recs) == 2

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set(['42febfb2ff72767655b0901dbde42ecb',       # should remove record w/ this key
       '8f56e0168c25e7bd919572669c2e43be']))
    assert recs is not None
    assert len(recs) == 2

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set(['42febfb2ff72767655b0901dbde42ecb',       # should remove this record
       '19cf39e8895fcf98e46f6017caebbbf1']))      # should remove this record
    assert recs is not None
    assert len(recs) == 1

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set([ '69b0e488119a656f70d881e6112a41cd',
        '42febfb2ff72767655b0901dbde42ecb',       # should remove this record
        '19cf39e8895fcf98e46f6017caebbbf1',       # should remove this record
        'c54e9578f22a0efebe32128291e1c947']))
    assert recs is not None
    assert len(recs) == 1

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set([ '42febfb2ff72767655b0901dbde42ecb',       # should remove these records
        '19cf39e8895fcf98e46f6017caebbbf1',
        'af34ecc2a49a550d49216f5b5b5b22d7']))
    assert recs is not None
    assert len(recs) == 0

    recs = fetch.deduplicate_records(self.for_dedup_recs,
      set([ 'cb948823526737aa29f11e3acd1c8dd2',
        '42febfb2ff72767655b0901dbde42ecb',       # should remove this record
        '5805b03d4ea8cfd577bff761e321f0b9',
        '69b0e488119a656f70d881e6112a41cd',
        '19cf39e8895fcf98e46f6017caebbbf1',       # should remove this record
        'af34ecc2a49a550d49216f5b5b5b22d7',       # should remove this record
        'cb948823526737aa29f11e3acd1c8dd2']))
    assert recs is not None
    assert len(recs) == 0


  def test_do_query_bad_url(self):
    bad_url = 'https://mriqc.nimh.nih.gov/badjunk?max_records=1'
    with pytest.raises(req.RequestException) as re:
      fetch.do_query(bad_url)
    print(re)


  def test_do_query_noresults(self):
    recs = fetch.do_query(self.noresult_query)
    assert recs is not None
    assert recs == []


  def test_extract_records_empty(self):
    with open(self.empty_results_fyl) as jfyl:
      results = json.load(jfyl)
    print(results)
    recs = fetch.extract_records(results)
    assert recs is not None
    assert recs == []


  def test_extract_records_page1(self):
    with open(self.page1_results_fyl) as jfyl:
      results = json.load(jfyl)
    print(results)
    recs = fetch.extract_records(results)
    assert recs is not None
    assert recs != []
    assert len(recs) == self.page1_results_cnt


  def test_flatten_a_record(self):
    tups = fetch.flatten_a_record(self.arec)
    print(f"TUPS[{len(tups)}]={tups}")
    assert tups is not None
    assert len(tups) == self.arec_len
    d = dict(tups)
    assert '_id' in d
    assert 'bids_meta.modality' in d
    assert 'bids_meta.EchoTime' in d
    assert '_created' in d
    assert 'provenance.md5sum' in d
    assert 'provenance.settings.fd_thres' in d
    assert '_etag' in d
    assert '_links.self.title' in d

    assert 'bids_meta' not in d
    assert 'provenance' not in d
    assert '_links' not in d
    assert '_links.self' not in d
    assert 'aqi' not in d


  def test_flatten_records(self):
    flist = fetch.flatten_records([self.arec, self.arec])
    assert flist is not None
    assert len(flist) == 2
    assert type(flist[0]) == dict
    d = flist[0]
    assert len(d) == self.arec_len
    assert '_id' in d
    assert 'bids_meta.modality' in d
    assert 'bids_meta.EchoTime' in d
    assert '_created' in d
    assert 'provenance.md5sum' in d
    assert 'provenance.settings.fd_thres' in d
    assert '_etag' in d
    assert '_links.self.title' in d

    assert 'bids_meta' not in d
    assert 'provenance' not in d
    assert '_links' not in d
    assert '_links.self' not in d
    assert 'aqi' not in d


  def test_get_n_records_bad_modality(self):
    with pytest.raises(ValueError) as ve:
      fetch.get_n_records('BAD_MODE')


  def test_get_n_records_0(self):
    recs = fetch.get_n_records('bold', 0)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 0


  def test_get_n_records_1(self):
    recs = fetch.get_n_records('bold', 1)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 1


  def test_get_n_records_9(self):
    recs = fetch.get_n_records('bold', 9)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 9


  def test_get_n_records_pagesize(self):
    recs = fetch.get_n_records('bold', SERVER_PAGE_SIZE)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE


  def test_get_n_records_pagesize_plus(self):
    recs = fetch.get_n_records('bold', SERVER_PAGE_SIZE+4)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE+4


  def test_get_n_records_pagesize2x(self):
    recs = fetch.get_n_records('bold', 2 * SERVER_PAGE_SIZE)
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == 2 * SERVER_PAGE_SIZE


  def test_query_for_page_bad_modality(self):
    with pytest.raises(ValueError) as ve:
      fetch.query_for_page('BAD_MODE')


  def test_query_for_page_default(self):
    recs = fetch.query_for_page('bold')
    print(recs)
    assert recs is not None
    assert type(recs) == list
    assert len(recs) == SERVER_PAGE_SIZE


  def test_server_health_check(self):
    "No test assertion: just calls code which always returns status code"
    status = fetch.server_health_check()
    assert (status == 200 or status == 503)
