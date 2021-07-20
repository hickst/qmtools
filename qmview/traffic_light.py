# Author: Tom Hicks and Dianne Patterson.
# Purpose: To convert an mriqc output file to normalized scores for
#          representation in a traffic-light table.
# Last Modified: Add methods to load TSV and write HTML file.

import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from matplotlib import cm
from matplotlib import pyplot as plt

from config.settings import REPORTS_DIR

# create our own small color maps for positive good and positive bad
TURNIP8_COLORMAP = cm.get_cmap('PiYG', 8)
TURNIP8_COLORMAP_R = cm.get_cmap('PiYG_r', 8)


def colorize_by_std_deviations (norm_df):
  """
  Set the cell backgrounds of the given z-score normalized dataframe,
  divided by standard deviations.
  Returns a pandas.io.formats.style.Styler object.
  """
  return norm_df.style.background_gradient(cmap=TURNIP8_COLORMAP, axis=None, vmin=-4.0, vmax=4.0)


def draw_pos_good_legend (pos_ax):
  "Draw a colormap legend for the case where positive values are good."
  make_legend_on_axis(pos_ax, TURNIP8_COLORMAP)


def draw_pos_bad_legend (neg_ax):
  "Draw a colormap legend for the case where positive values are bad."
  make_legend_on_axis(neg_ax, TURNIP8_COLORMAP_R)


def load_tsv (tsv_path):
  "Read the specified TSV file and return a Pandas dataframe from it."
  return pd.read_csv(tsv_path, sep='\t')


def make_legends (dirpath=REPORTS_DIR):
  """
  Generate and save a positive-good legend and a positive-bad legend
  as .png files in the reports directory.
  """
  make_a_legend("pos_good.png", TURNIP8_COLORMAP, dirpath)
  make_a_legend("pos_bad.png", TURNIP8_COLORMAP_R, dirpath)


def make_a_legend (filename, colormap, dirpath=REPORTS_DIR):
  """
  Make a legend with the given colormap and save it with the given filename
  in the optionally specified reports directory.
  """
  fig = plt.figure()
  ax = fig.add_axes([0, 0, 1, 1])
  make_legend_on_axis(ax, colormap)
  write_figure_to_file(fig, filename)


def make_legend_on_axis (ax, cmap):
  """
  Draws a legend on the given axis using the given colormap.
  """
  box_rng = np.arange(8)
  ticklabels = ['-4.0', '-3.0', '-2.0', '-1.0', '1.0', '2.0', '3.0', '4.0']
  label_title = 'Green Values are Better'
  im = ax.imshow([box_rng], cmap)
  ax.set_xticks(box_rng)
  ax.set_xticklabels(ticklabels)
  ax.set_yticks([])
  ax.set_yticklabels([])
  ax.set_title(label_title)


def normalize_to_zscores (qm_df):
  """
  Apply Z-score by column to every column except the BIDS name column.
  """
  bids_names = qm_df['bids_name']
  z_df = qm_df.iloc[:, 1:].apply(stats.zscore)
  return pd.concat([bids_names, z_df], axis=1)


def write_figure_to_file (fig, filename, dirpath=REPORTS_DIR):
  """
  Write the given matplotlib figure to a file with the given filename
  in the reports directory. The output format is determined by the file
  extension (.png is the default).
  """
  filepath = os.path.join(dirpath, filename)
  fig.savefig(filepath, bbox_inches='tight')    # .png is default


def write_table_to_html (styler, filepath):
  """
  Render the given pandas.io.formats.style.Styler object as
  HTML and write the HTML to the given filepath.
  """
  with open(filepath, "w") as outfyl:
    outfyl.writelines(styler.render())


# # Argument is: 1) QA file
# # Example:  norm_z.py group_T1w.tsv
# #
# # qm_file = sys.argv[1]
# qm_file = '../test/resources/gtest.tsv'
# qm_df = pd.read_csv(qm_file, sep='\t')
# norm_df = normalize_to_zscores(qm_df)
# # print(norm_df)
# # print(norm_df[['aor', 'dummy_trs', 'fber', 'fd_num']])

# # Plot the legend and the table
# fig, axes = plt.subplots(2, 1)
# legend_ax, table_ax = axes
# draw_pos_good_legend(legend_ax)
# colorize_by_std_deviations(norm_df)
# # table_ax.imshow(norm_df)
# plt.show()
