# Shared utilities for the QMTools programs.
#   Written by: Tom Hicks and Dianne Patterson.
#   Last Modified: No default dot in extension. Make header docs consistent.
#
import datetime
import os
import pandas as pd
import sys

from qmtools import ALLOWED_MODALITIES, FETCHED_DIR, FETCHED_DIR_EXIT_CODE
from qmtools import REPORTS_DIR, REPORTS_DIR_EXIT_CODE
from qmtools.file_utils import good_dir_path


def ensure_fetched_dir (program_name):
  """
  Check that the default fetched directory is a writeable directory.
  If not, then attempt to create the subdirectory in the current directory.
  If unable to create the directory, then exit out.
  """
  if (not good_dir_path(FETCHED_DIR, writeable=True)):
    try:
      os.mkdir(FETCHED_DIR, mode=0o775)
    except OSError:
      helpMsg =  """
        There must be a writeable child subdirectory called 'fetched'
        to hold the fetched query results.
        """
      errMsg = "({}): ERROR: {} Exiting...".format(program_name, helpMsg)
      print(errMsg, file=sys.stderr)
      sys.exit(FETCHED_DIR_EXIT_CODE)


def ensure_reports_dir (program_name):
  """
  Check that the default reports directory is a writeable directory.
  If not, then attempt to create the subdirectory in the current directory.
  If unable to create the directory, then exit out.
  """
  if (not good_dir_path(REPORTS_DIR, writeable=True)):
    try:
      os.mkdir(REPORTS_DIR, mode=0o775)
    except OSError:
      helpMsg =  """
        There must be a writeable child subdirectory called 'reports'
        to hold the output reports.
        """
      errMsg = "({}): ERROR: {} Exiting...".format(program_name, helpMsg)
      print(errMsg, file=sys.stderr)
      sys.exit(REPORTS_DIR_EXIT_CODE)


def gen_output_filename (modality, extension='tsv'):
  """
  Generate and return a default name based on modality, timestamp, and optional extension.
  """
  time_now = datetime.datetime.now()
  now_str = time_now.strftime("%Y%m%d_%H%M%S-%f")
  return f"{modality}_{now_str}{extension}"


def load_tsv (tsv_path):
  "Read the specified TSV file and return a Pandas dataframe from it."
  return pd.read_csv(tsv_path, sep='\t')


def validate_modality (modality):
  """
   Check the validity of the given modality string which must be one
   of the elements of the ALLOWED_MODALITIES list.
   Returns the canonicalized modality string or raises ValueError if
   given an invalid modality string.
  """
  if (modality in ALLOWED_MODALITIES):
    return modality
  raise ValueError(f"Modality argument must be one of: {ALLOWED_MODALITIES}")
