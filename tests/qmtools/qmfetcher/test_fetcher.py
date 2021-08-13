# Tests of the MRIQC data fetcher library code.
#   Written by: Tom Hicks and Dianne Patterson. 8/7/2021.
#   Last Modified: Add tests for flatten_a_record and flatten_records. Update clean_records test.
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


  def test_build_query_bad_modality(self):
    with pytest.raises(ValueError) as ve:
      fetch.build_query('BAD_MODE')


  def test_build_query_modes(self):
    qstr = fetch.build_query('bold')
    assert qstr == f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}"
    qstr = fetch.build_query('t1w')
    assert qstr == f"{SERVER_URL}/t1w?max_results={SERVER_PAGE_SIZE}"
    qstr = fetch.build_query('t2w')
    assert qstr == f"{SERVER_URL}/t2w?max_results={SERVER_PAGE_SIZE}"


  def test_build_query_pagenum_none(self):
    qstr = fetch.build_query('bold', None)
    assert qstr == f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}"
    qstr = fetch.build_query('bold', 0)
    assert qstr == f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=0"
    qstr = fetch.build_query('bold', 1)
    assert qstr == f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=1"
    qstr = fetch.build_query('bold', 999)
    assert qstr == f"{SERVER_URL}/bold?max_results={SERVER_PAGE_SIZE}&page=999"


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


  def test_do_query_bad_url(self):
    bad_url = 'https://mriqc.nimh.nih.gov/badjunk?max_records=1'
    with pytest.raises(req.RequestException) as re:
      fetch.do_query(bad_url)
    print(re)


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
