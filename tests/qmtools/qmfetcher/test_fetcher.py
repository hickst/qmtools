# Tests of the MRIQC data fetcher library code.
#   Written by: Tom Hicks and Dianne Patterson. 8/7/2021.
#   Last Modified: Initial creation.
#
import os
import pandas
import pytest
import sys
import tempfile
from pathlib import Path

from qmtools import ALLOWED_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
import qmtools.qmfetcher.fetcher as fetch
from qmtools.qmfetcher.fetcher import SERVER_URL
from tests import TEST_RESOURCES_DIR

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse

class TestFetcher(object):

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


  def test_query_for_page_bad_modality(self):
    with pytest.raises(ValueError) as ve:
      fetch.query_for_page('BAD_MODE')


  def test_query_for_page_default(self):
    recs = fetch.query_for_page('bold')
    assert recs is not None
    assert recs == []
