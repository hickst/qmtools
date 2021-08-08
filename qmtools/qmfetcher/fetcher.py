# Author: Tom Hicks and Dianne Patterson.
# Purpose: Methods to query the MRIQC server and download query result records.
# Last Modified: Flesh out and test extract_records.

import os
import pandas as pd
import requests as req

from qmtools import ALLOWED_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
from qmtools.qm_utils import validate_modality

SERVER_URL = "https://mriqc.nimh.nih.gov/api/v1"


def build_query (modality, page_num=None, query_params=None):
  validate_modality(modality)          # validates or raises ValueError
  url_str = f"{SERVER_URL}/{modality}?max_results={SERVER_PAGE_SIZE}"
  if (page_num is not None or query_params is not None):
    if (page_num is not None):
      url_str = f"{url_str}&page={page_num}"
    if (query_params is not None):
      # add the various query parameters
      pass
  return url_str


def clean_records (json_recs):
  # TODO: IMPLEMENT LATER
  return json_recs


def do_query (query_str):
  # TODO: IMPLEMENT LATER
  json_recs = {"_items": []}           # REMOVE LATER
  return json_recs                     # return fake empty query result dictionary


def extract_records (json_query_result):
  return json_query_result['_items']


def query_for_page (modality, page_num=1, query_params=None):
  """
  Query for the first (or numbered) page of results from
  the MRIQC server, and clean and return the result records.
  Arguments:
    modality: the modality to query on (must be one of {ALLOWED_MODALITIES})
    page_num: page number (one offset) for the page to fetch (default: 1)
    query_params: dictionary of additional query parameters (default: None)
  """
  validate_modality(modality)          # validates or raises ValueError
  query = build_query(modality, page_num, query_params)
  json_query_result = do_query(query)
  json_recs = extract_records(json_query_result)
  cleaned = clean_records(json_recs)
  return cleaned