# Tests of the traffic-light table code.
#   Written by: Tom Hicks and Dianne Patterson. 7/19/2021.
#   Last Modified: Reformatted file. Added test for normalize_to_zscores.
#
import numpy
import pandas
import pytest
from test import TEST_RESOURCES_DIR
import qmview.traffic_light as traf

class TestTrafficLight(object):

  gtest_tstfyl  = f"{TEST_RESOURCES_DIR}/gtest.tsv"

  def test_load_tsv(self):
    qm_df = traf.load_tsv(self.gtest_tstfyl)
    print(qm_df)
    assert qm_df is not None
    assert type(qm_df) == pandas.core.frame.DataFrame
    assert qm_df.size == 855
    assert qm_df.shape == (19, 45)


  def test_normalize_to_zscores(self):
    qm_df = traf.load_tsv(self.gtest_tstfyl)
    norm_df = traf.normalize_to_zscores(qm_df)
    assert type(norm_df) == pandas.core.frame.DataFrame
    assert norm_df.size == 855
    assert norm_df.shape == (19, 45)
    print(type(norm_df['bids_name'][0]))
    assert type(norm_df['bids_name'][0]) == str
    print(type(norm_df.iloc[0, 1]))
    assert type(norm_df.iloc[0, 1]) == numpy.float64


    # hdrs = None
    # with fits.open(self.m13_tstfyl) as hdus:
    #     hdrs = utils.get_header_fields(hdus)
    # print(hdrs)
    # assert hdrs is not None
    # assert len(hdrs) > 0
    # assert len(hdrs) == 18
    # assert 'CTYPE1' in hdrs
    # assert 'SIMPLE' in hdrs
    # assert 'COMMENT' not in hdrs
