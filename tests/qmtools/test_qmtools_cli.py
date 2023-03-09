# Tests of the top-level QMTools default page.
#   Written by: Tom Hicks and Dianne Patterson. 3/9/2023.
#   Last Modified: Initial creation.
#
import os
import pytest
import sys

from qmtools.version import VERSION
import qmtools.qmtools as cli


@pytest.fixture
def clear_argv():
  sys.argv = []


class TestQMTools(object):

  def test_main(self, capsys, clear_argv):
    sys.argv = ['qmtools']
    cli.main()
    sysout, _ = capsys.readouterr()
    print(f"CAPTURED SYS.OUT:\n{sysout}")
    assert 'QMTools contains' in sysout
    assert VERSION in sysout
    assert 'qmfetcher' in sysout
    assert 'qmtraffic' in sysout
    assert 'qmviolin' in sysout
    assert 'which provides sample data' in sysout
