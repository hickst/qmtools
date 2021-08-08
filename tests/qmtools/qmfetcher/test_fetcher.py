# Tests of the MRIQC data fetcher library code.
#   Written by: Tom Hicks and Dianne Patterson. 8/7/2021.
#   Last Modified: Add tests for clean_records.
#
import json
import os
import pandas
import pytest
import sys
import tempfile
from pathlib import Path

from qmtools import ALLOWED_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
import qmtools.qmfetcher.fetcher as fetch
from qmtools.qmfetcher.fetcher import SERVER_URL, FIELDS_TO_REMOVE
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestFetcher(object):

  empty_results_fyl = f"{TEST_RESOURCES_DIR}/no_results.json"
  page1_results_fyl = f"{TEST_RESOURCES_DIR}/reptime1.json"
  page1_results_cnt = 25

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
    crecs = fetch.clean_records(recs)
    assert crecs is not None
    assert crecs == []


  def test_clean_records_page1(self):
    with open(self.page1_results_fyl) as jfyl:
      results = json.load(jfyl)
    recs = fetch.extract_records(results)
    crecs = fetch.clean_records(recs)
    assert crecs is not None
    assert crecs != []
    assert len(crecs) == self.page1_results_cnt
    for rec in crecs:
      for field in FIELDS_TO_REMOVE:
        assert rec.get(field) is None


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


  def test_query_for_page_bad_modality(self):
    with pytest.raises(ValueError) as ve:
      fetch.query_for_page('BAD_MODE')


  def test_query_for_page_default(self):
    recs = fetch.query_for_page('bold')
    assert recs is not None
    assert recs == []
