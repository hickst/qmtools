# Author: Tom Hicks and Dianne Patterson.
# Purpose: Shared utilities for the QMTools programs.
# Last Modified: Initial creation by refactoring.
#
import pandas as pd

from qmtools import ALLOWED_MODALITIES


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
  mode = modality.lower()
  if (mode in ALLOWED_MODALITIES):
    return mode
  raise ValueError(f"Modality argument must be one of: {ALLOWED_MODALITIES}")
