# Methods to create IQM violin plots from two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/3/2021.
#   Last Modified: Remove args argument in gen_html call.
#
import os

import pandas as pd
import seaborn as sb

from config.mriqc_keywords import (BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS,
                                   STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS)
from qmtools import PLOT_EXT, REPORTS_DIR, STRUCTURAL_MODALITIES
from qmtools.file_utils import copy_tree
import qmtools.qm_utils as qmu
import qmtools.qmviolin.gen_html as genh


# Tuple of column name prefix strings which should be removed from fetched data files:
COLUMNS_TO_REMOVE = ('_', 'bids_meta', 'provenance', 'rating')

DEFAULT_HTML_FILENAME = 'violin.html'


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

  return do_plots(modality, args, melted_df)


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
  and plots the given, or default, IQMs, returning a dictionary of IQM names
  and plot filenames.
  """
  plot_info = dict()
  iqms_to_plot = select_iqms_to_plot(modality, plot_iqms)
  report_dirpath = args.get('report_dirpath', REPORTS_DIR)
  for iqm in iqms_to_plot:
    filename = do_a_plot(modality, iqms_df, iqm, report_dirpath=report_dirpath)
    plot_info[iqm] = filename
  return plot_info


def do_a_plot (modality, iqms_df, iqm, report_dirpath=REPORTS_DIR):
  """
  Select the data for the specified IQM from the given IQMs dataset and plot it.
  Return the filename where the plot is saved.
  """
  plot_df = iqms_df[iqms_df['IQM'] == iqm]
  vplot = sb.catplot(x="IQM", y="value", hue="source", data=plot_df,
                     kind="violin", inner="quartile", split=True, palette="pastel")
  filename = gen_plot_filename(modality, iqm)
  qmu.write_figure_to_file(vplot, filename, dirpath=report_dirpath)
  return filename                      # return the name of the generated plot file


def gen_plot_filename (modality, iqm_name, extension=PLOT_EXT):
  """
  Generate and return a default name based on modality, IQM name, and optional extension.
  """
  return f"{modality}_{iqm_name}{extension}"


def make_html_report (modality, args, plot_info):
  """
  Generate HTML text for the given modality and plot information and write it to
  the reports directory named in args. Also, copy all needed support files to the
  same reports directory.
  """
  report_dirpath = args.get('report_dirpath')
  if (not report_dirpath):
    raise FileNotFoundError("Required reports directory path not found in arguments dictionary")

  # generate the HTML and write it to a file in the current report directory
  html_text = genh.gen_html(modality, plot_info)
  write_html(html_text, report_dirpath)

  # copy the required report support files to the current report directory
  copy_tree(genh.AUX_DIR_PATH, report_dirpath)


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


def write_html (html_text, dirpath, filename=DEFAULT_HTML_FILENAME):
  """
  Write the given html text string to the named file in the given directory path.
  """
  filepath = os.path.join(dirpath, filename)
  with open(filepath, 'w', newline='') as htmlfile:
    written = htmlfile.write(html_text)
  return written