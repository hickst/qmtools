# Methods to create IMQ violin plots from two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/3/2021.
#   Last Modified: Produce all violin plot files.
#
# import csv
# import os
# import sys

# import numpy as np
import pandas as pd
import seaborn as sb

from config.mriqc_keywords import (BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS,
                                   STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS)
import qmtools.qm_utils as qmu
from qmtools.qmview.traffic_light import write_figure_to_file  # REMOVE LATER
from qmtools import PLOT_EXT, STRUCTURAL_MODALITIES
from qmtools.qmview.traffic_light import write_table_to_tsv  # REMOVE LATER

# Tuple of column name prefix strings which should be removed from fetched data files:
COLUMNS_TO_REMOVE = ('_', 'bids_meta', 'provenance', 'rating')


def vplot (modality, args):
  """
  Plot two MRIQC datasets given the modality and a dictionary of plot arguments.
  Expected arguments include valid, readable filepaths to the datasets and
  optional plot arguments.
  """
  qmu.validate_modality(modality)      # validates or raises ValueError

  fetched_file = args.get('fetched_file')
  if (not fetched_file):
    raise FileNotFoundError("Required 'fetched_file' filepath not found in arguments dictionary")

  group_file = args.get('group_file')
  if (not group_file):
    raise FileNotFoundError("Required 'group_file' filepath not found in arguments dictionary")

  fetch_df = qmu.load_tsv(fetched_file)
  clean_df(fetch_df)
  group_df = qmu.load_tsv(group_file)
  clean_df(group_df)

  # merge fetched and group dataframes, adding 'orig' field to identify the record source
  merged_df = pd.concat([fetch_df.assign(source='fetch'), group_df.assign(source='group')])

  # pivot the merged dataframe to index by bids_name and source
  melted_df = merged_df.melt(id_vars=['bids_name', 'source'], var_name='IQM')

  print('\nMELTED DataFrame:\n')       # REMOVE LATER
  print(melted_df)                     # REMOVE LATER

  do_plots(modality, args, melted_df)


def clean_df (df):
  """
  Renames ID fields to merge them and removes unneeded columns, by side effect!
  Assumes that applying this function to a group file has no effect (because the
  columns to alter don't exist).
  """
  # Rename the fetched records unique ID (_id) so that it merges with the
  # unique ID (bids_name) field of the group file.
  df.rename(columns={'_id': 'bids_name'}, errors='ignore', inplace=True)

  # Remove extra fields from the fetch data records
  del_list = [col for col in list(df.columns) if col.startswith(COLUMNS_TO_REMOVE)]
  df.drop(columns=del_list, errors='ignore', inplace=True)


def do_plots (modality, args, iqms_df, plot_iqms=None):
  """
  Takes a merged and melted MRIQC dataset and an optional list of IQMs to plot
  and plots the given or default IQMs.
  """
  iqms_to_plot = select_iqms_to_plot(modality, plot_iqms)
  print(f"IQMs={iqms_to_plot}")        # REMOVE LATER
  for iqm in iqms_to_plot:
    do_a_plot(modality, args, iqms_df, iqm)


def do_a_plot (modality, args, iqms_df, iqm):
  """
  Select the data for the specified IQM from the given IQMs dataset and plot it.
  """
  plot_df = iqms_df[iqms_df['IQM'] == iqm]
  vplot = sb.catplot(x="IQM", y="value", hue="source", data=plot_df,
                     kind="violin", inner="quartile", split=True, palette="pastel")
  filename = gen_plot_filename(modality, iqm)
  write_figure_to_file(vplot, filename)
  # TODO: gen_html_for_iqm(modality, args, iqm, filename)


def gen_plot_filename (modality, iqm_name, extension=PLOT_EXT):
  """
  Generate and return a default name based on modality, IQM name, and optional extension.
  """
  # time_now = datetime.datetime.now()
  # now_str = time_now.strftime("%Y%m%d_%H%M%S-%f")
  return f"{modality}_{iqm_name}{extension}"


def select_iqms_to_plot (modality, plot_iqms=None):
  """
  Decide which IQMs will be plotted based on modality OR
  check and/or filter a user-provided list of IQMs against modality.
  """
  bold_iqms = sorted(BOLD_HI_GOOD_COLUMNS + BOLD_LO_GOOD_COLUMNS)
  struct_iqms = sorted(STRUCT_HI_GOOD_COLUMNS + STRUCT_LO_GOOD_COLUMNS)

  if (modality in STRUCTURAL_MODALITIES):
    iqms_to_plot = struct_iqms
    if (plot_iqms is not None):
      iqms_to_plot = sorted([iqm for iqm in plot_iqms if iqm in struct_iqms])
  else:
    iqms_to_plot = bold_iqms
    if (plot_iqms is not None):
      iqms_to_plot = sorted([iqm for iqm in plot_iqms if iqm in bold_iqms])

  # return the validated and sorted list of iqms:
  return iqms_to_plot
