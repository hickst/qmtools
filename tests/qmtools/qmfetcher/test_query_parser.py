# Tests of the module to read and parse a query parameters file.
#   Written by: Tom Hicks and Dianne Patterson. 8/17/2021.
# Last Modified: Initial createion.
#
import configparser
import os
import pytest
import sys

from tests import TEST_RESOURCES_DIR
import qmtools.qmfetcher.query_parser as qp

SYSEXIT_ERROR_CODE = 2                 # seems to be error exit code from argparse


class TestQueryParser(object):

  empty_query_fyl = f"{TEST_RESOURCES_DIR}/empty.qp"
  nosec_query_fyl = f"{TEST_RESOURCES_DIR}/nosec.qp"
  noparams_query_fyl = f"{TEST_RESOURCES_DIR}/noparams.qp"
  params_query_fyl = f"{TEST_RESOURCES_DIR}/manmaf.qp"

  def test_parse_query_from_file_nosuch(self):
    with pytest.raises(FileNotFoundError) as fnf:
      qp.parse_query_from_file('NOSUCH_FILE')


  def test_parse_query_from_file_empty(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_query_from_file(self.empty_query_fyl)


  def test_parse_query_from_file_nosec(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_query_from_file(self.nosec_query_fyl)


  def test_parse_query_from_file_noparams(self):
    with pytest.raises(ValueError) as ve:
      qp.parse_query_from_file(self.noparams_query_fyl)


  def test_parse_query_from_file_params(self):
    pd = qp.parse_query_from_file(self.params_query_fyl)
    assert pd is not None
    assert type(pd) is dict
    assert len(pd) == 3
    assert 'dummy_trs' in pd.keys()
    assert 'bids_meta.Manufacturer' in pd.keys()
