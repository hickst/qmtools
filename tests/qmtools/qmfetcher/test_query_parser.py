# Tests of the module to read and parse a query parameters file.
#   Written by: Tom Hicks and Dianne Patterson. 8/17/2021.
# Last Modified: Update for rename to load_query_from_file. Add nocolon test for same.
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
  nosec_query_fyl = f"{TEST_RESOURCES_DIR}/nosec.qp"
  params_query_fyl = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  def test_load_query_from_file_nosuch(self):
    with pytest.raises(FileNotFoundError) as fnf:
      qp.load_query_from_file('NOSUCH_FILE', self.TEST_NAME)


  def test_load_query_from_file_empty(self):
    with pytest.raises(ValueError) as ve:
      qp.load_query_from_file(self.empty_query_fyl, self.TEST_NAME)


  def test_load_query_from_file_nosec(self):
    with pytest.raises(ValueError) as ve:
      qp.load_query_from_file(self.nosec_query_fyl, self.TEST_NAME)


  def test_load_query_from_file_noparams(self):
    with pytest.raises(ValueError) as ve:
      qp.load_query_from_file(self.noparams_query_fyl, self.TEST_NAME)


  def test_load_query_from_file_nocolon(self):
    with pytest.raises(ValueError) as ve:
      pd = qp.load_query_from_file(self.nocolon_query_fyl, self.TEST_NAME)
    print(ve)


  def test_load_query_from_file_params(self):
    pd = qp.load_query_from_file(self.params_query_fyl, self.TEST_NAME)
    assert pd is not None
    assert type(pd) is dict
    assert len(pd) == 3
    assert 'dummy_trs' in pd.keys()
    assert 'bids_meta.Manufacturer' in pd.keys()
