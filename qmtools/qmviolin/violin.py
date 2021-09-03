# Methods to create IMQ violin plots from two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/3/2021.
#   Last Modified: Initial creation of stub.
#
import csv
# import json
import os
import numpy
import pandas
import sys

from config.mriqc_keywords import STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS
from config.mriqc_keywords import BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS
from qmtools import ALLOWED_MODALITIES, STRUCTURAL_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
import qmtools.qm_utils as qmu


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
  group_df = qmu.load_tsv(group_file)

  print('FETCHED DataFrame:\n')
  print(fetch_df)
  print('GROUP DataFrame:\n')
  print(group_df)
