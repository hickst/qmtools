# Author: Dianne Patterson
# Purpose: To convert an mriqc output file to normalized scores for
#          representation in a traffic-light table.

# import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from matplotlib import cm
from matplotlib import pyplot as plt
# import plotly.graph_objects as go

# create our own small color maps for positive good and positive bad
TURNIP8_COLORMAP = cm.get_cmap('PiYG', 8)
TURNIP8_COLORMAP_R = cm.get_cmap('PiYG_r', 8)


def colorize_by_std_deviations (norm_df):
  """
  Set the cell backgrounds of the given z-score normalized dataframe,
  divided by standard deviations.
  """
  norm_df.style.background_gradient(cmap=TURNIP8_COLORMAP, axis=None, vmin=-4.0, vmax=4.0)


def draw_pos_good_legend (pos_ax):
  "Draw a colormap legend for the case where positive values are good."
  make_legend_on_axis(pos_ax, TURNIP8_COLORMAP)


def draw_pos_bad_legend (neg_ax):
  "Draw a colormap legend for the case where positive values are bad."
  make_legend_on_axis(neg_ax, TURNIP8_COLORMAP_R)


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
  "Apply Z-score by column to every column except the BIDS name column."
  bids_names = qm_df['bids_name']
  z_df = qm_df.iloc[:, 1:].apply(stats.zscore)
  return pd.concat([bids_names, z_df], axis=1)


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
