# Methods to create IMQ violin plots from two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/3/2021.
#   Last Modified: Add method to clean dataframes before merging.
#
import csv
import os
import numpy as np
import pandas as pd
import sys

from config.mriqc_keywords import STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS
from config.mriqc_keywords import BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS
from qmtools import ALLOWED_MODALITIES, STRUCTURAL_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
import qmtools.qm_utils as qmu
from qmtools.qmview.traffic_light import write_table_to_tsv   # REMOVE LATER

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

  merge_df = pd.concat([fetch_df.assign(orig='fetch'), group_df.assign(orig='group')])
  print('MERGED DataFrame:\n')           # REMOVE LATER
  print(merge_df)                        # REMOVE LATER
  rpt_name = args.get('report_filename', 'mergy')
  write_table_to_tsv(merge_df, rpt_name)  # REMOVE LATER


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
