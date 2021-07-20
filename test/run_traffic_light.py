import sys

from matplotlib import cm
from matplotlib import pyplot as plt

import qmview.traffic_light as traf
from qmview.traffic_light import TURNIP8_COLORMAP, TURNIP8_COLORMAP_R
from config.settings import REPORTS_DIR


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

  # qm_df = traf.load_tsv('test/resources/group_bold.tsv')
  # qm_df = traf.load_tsv('inputs/gtest.tsv')
  # norm_df = traf.normalize_to_zscores(qm_df)
  # styler = traf.colorize_by_std_deviations(norm_df)
  # traf.write_table_to_html(styler, f"{REPORTS_DIR}/table.html")

  # fig, axes = plt.subplots(2, 1)
  # pos_ax, neg_ax = axes
  # traf.make_legend_on_axis(pos_ax, TURNIP8_COLORMAP)
  # traf.make_legend_on_axis(neg_ax, TURNIP8_COLORMAP_R)
  # plt.show()



if __name__ == "__main__":
  main()