# Tests of the traffic-light table code.
#   Written by: Tom Hicks and Dianne Patterson. 7/19/2021.
#   Last Modified: Initial creation.
#
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


    def test_get_header_fields_default(self):
        assert True
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
