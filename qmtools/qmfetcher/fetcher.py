# Author: Tom Hicks and Dianne Patterson.
# Purpose: Methods to query the MRIQC server and download query result records.
# Last Modified: Add doc string for deduplicate_records.
#
import json
import os
import pandas as pd
import requests as req

from qmtools import ALLOWED_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
from qmtools.qm_utils import validate_modality

SERVER_URL = "https://mriqc.nimh.nih.gov/api/v1"
DEFAULT_FIELDS_TO_REMOVE = ['_etag', 'bids_meta.Instructions',
                            '_links.self.title', '_links.self.href']


def build_query (modality, page_num=1, query_params=None, latest=True):
  """
  Construct and return a query string given the modality, starting page number,
  and optional dictionary of query parameter keys and values.
  """
  validate_modality(modality)          # validates or raises ValueError

  # check for reasonable page number
  if (not page_num or (page_num < 1)):
    page_num = 1

  url_str = f"{SERVER_URL}/{modality}?max_results={SERVER_PAGE_SIZE}&page={page_num}"
  if (latest):                         # by default use the latest records
    url_str = f"{url_str}&sort=-_created"

  if (query_params is not None):
    # TODO: add the various query parameters
    pass
  return url_str


def clean_records (json_recs, fields_to_remove=DEFAULT_FIELDS_TO_REMOVE):
  """
  Remove unwanted fields from each record (dictionary) in the given list and
  return the list of cleaned records.
  Arguments:
    json_recs: a list of records, each one representing metrics for a single image.
    fields_to_remove: a list of field names to remove when cleaning records.
  """
  for rec in json_recs:
    for field in fields_to_remove:
      if (field in rec):
        rec.pop(field)
  return json_recs


def deduplicate_records (records, chksums=set()):
  """
  Use the given set of previously gathered checksums to identify and
  remove duplicate records from the given list.
  Arguments:
     records: list of records (dictionaries) to be deduplicated
     chksums: SET of previously seen checksums; used to identify duplicate records.
  """
  # omit records w/ no checksum or checksum is in list of checksums already seen
  return [rec for rec in records if is_not_duplicate(rec, chksums)]


def is_not_duplicate (record, chksums):
  """
  Return False for records w/ no checksum or with a checksum in the list of
  checksums already seen. Returns True if record checksum has not been seen AND
  adds the checksum to the given set of checksums, by side effect!
  Arguments:
    record: a record (dictionary) of image information.
    chksums: a SET of previously seen md5sums.
  """
  recsum = record.get('provenance.md5sum')
  if (recsum is None or (recsum in chksums)):
    return False
  else:
    chksums.add(recsum)
    return True


def do_query (query_str):
  """
  Query the server with the given query string, return the parsed JSON data
  if successful, otherwise raise a RequestException.
  """
  resp = req.get(query_str)
  if (resp.status_code == req.codes.ok):
    json_query_result = json.loads(resp.text)
    return json_query_result
  else:
    resp.raise_for_status()


def extract_records (json_query_result):
  """
  Extract and return a list of records (dictionaries) from the given
  query result dictionary.
  """
  return json_query_result['_items']


def flatten_a_record (rec, prefix='', sep='.'):
  """
  Flatten the given record (dictionary) into a list of key/value tuples and
  return the tuple list.
  Arguments:
    rec: the dictionary to be flattened.
    prefix: the prefix key "path" at this level of flattening. If provided, must
            already include the separator as a suffix.
    sep: the string to use to separate the levels in the prefix key "path".
  """
  entries = []
  for key, val in rec.items():
    if (isinstance(val, dict)):
      new_prefix = f"{prefix}{key}{sep}"
      entries.extend(flatten_a_record(val, prefix=new_prefix, sep=sep))
    else:
      top_key = f"{prefix}{key}"
      entries.append((top_key, val))
  return entries


def flatten_records (json_recs):
  """
  Given a list of records (dictionaries), return a list of flattened dictionaries.
  Arguments:
    json_recs: a list of records (dictionaries), each one representing metrics for a single image.
  """
  return [dict(flatten_a_record(rec)) for rec in json_recs]


def query_for_page (modality, page_num=1, query_params=None,
                    fields_to_remove=DEFAULT_FIELDS_TO_REMOVE):
  """
  Query for the first (or numbered) page of results from
  the MRIQC server, and clean and return the result records.
  Arguments:
    modality: the modality to query on (must be one of {ALLOWED_MODALITIES}).
    page_num: page number (one offset) for the page to fetch (default: 1).
    query_params: dictionary of additional query parameters (default: None).
    fields_to_remove: a list of field names to remove when cleaning records.
  """
  validate_modality(modality)          # validates or raises ValueError
  query = build_query(modality, page_num, query_params)
  json_query_result = do_query(query)
  json_recs = extract_records(json_query_result)
  flat_recs = flatten_records(json_recs)
  return clean_records(flat_recs, fields_to_remove)


def server_health_check ():
  """
  Send a minimal request to the server as a health check.
  Return True is server responds with HTTP 200, else False.
  """
  health_check_url = f"{SERVER_URL}/bold?max_results=1"
  resp = req.get(health_check_url)
  # resp.raise_for_status()
  return resp.status_code
