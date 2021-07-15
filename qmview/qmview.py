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


TURNIP8_COLORMAP = cm.get_cmap('PiYG', 8)
TURNIP8_COLORMAP_R = cm.get_cmap('PiYG_r', 8)


def colorize_by_std_deviations (norm_df):
  """
  Set the cell backgrounds of the given z-score normalized dataframe,
  divided by standard deviations.
  """
  norm_df.style.background_gradient(cmap=TURNIP8_COLORMAP, axis=None, vmin=-4.0, vmax=4.0)


def normalize_to_zscores (qm_df):
  "Apply Z-score by column to every column except the BIDS name column."
  bids_names = qm_df['bids_name']
  z_df = qm_df.iloc[:, 1:].apply(stats.zscore)
  return pd.concat([bids_names, z_df], axis=1)


def show_pos_good_legend ():
  "Draw a colormap legend for the case where positive values are good."
  # TODO: how to return some legend (subplot?) that can be plotted later
  return plt.imshow([[0, 1, 2, 3, 4, 5, 6, 7]], cmap=TURNIP8_COLORMAP)


def show_pos_bad_legend ():
  "Draw a colormap legend for the case where positive values are bad."
  # TODO: how to return some legend (subplot?) that can be plotted later
  return plt.imshow([[0, 1, 2, 3, 4, 5, 6, 7]], cmap=TURNIP8_COLORMAP_R)


# Argument is: 1) QA file
# Example:  norm_z.py group_T1w.tsv
# qa_file = sys.argv[1]
qa_file = "../../data/gtest.tsv"
# print("qa_file is", qa_file)

qa_df = pd.read_csv(qa_file, sep="\t")
# print("qa_df is a:", type(qa_df))
# print(qa_df)

# try with the data frame itself:
# print("z_df is a:", type(z_df))
# print(z_df)

# print("bids_names is a:", type(bids_names))
# print(bids_names)

print(norm_df)
# print(norm_df[['aor', 'dummy_trs', 'fber', 'fd_num']])

# create our own limited color map
turnip8 = cm.get_cmap('PiYG', 8)

# set cell backgrounds from a colormap based on standard deviations
# plt.imshow(z_df, cmap=turnip8)
# plt.show()
