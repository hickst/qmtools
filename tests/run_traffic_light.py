import sys

from matplotlib import cm
from matplotlib import pyplot as plt

import qmview.traffic_light as traf
from qmview.traffic_light import TURNIP8_COLORMAP, TURNIP8_COLORMAP_R
# from config.settings import REPORTS_DIR


def main (argv=None):
  """
  The main method for the tool. This method is called from the command line,
  processes the command line arguments and calls into the ImdTk library to do its work.
  This main method takes no arguments so it can be called by setuptools.
  """

  # the main method takes no arguments so it can be called by setuptools
  if (argv is None):                      # if called by setuptools
      argv = sys.argv[1:]                 # then fetch the arguments from the system

  traf.make_legends()
  traf.make_traffic_light_table('inputs/gtest.tsv', 'bold')



if __name__ == "__main__":
  main()