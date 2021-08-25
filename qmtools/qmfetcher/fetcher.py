# Author: Tom Hicks and Dianne Patterson.
# Purpose: Methods to query the MRIQC server and download query result records.
# Last Modified: Enhance server status to return total records available for current query.
#
import csv
import json
import os
import requests as req
import sys

from config.mriqc_keywords import BOLD_KEYWORDS, STRUCTURAL_KEYWORDS
from qmtools import ALLOWED_MODALITIES, STRUCTURAL_MODALITIES
from qmtools.qmfetcher import DEFAULT_RESULTS_SIZE, SERVER_PAGE_SIZE
from qmtools.qm_utils import validate_modality

SERVER_URL = "https://mriqc.nimh.nih.gov/api/v1"
DEFAULT_FIELDS_TO_REMOVE = ['_etag', 'bids_meta.Instructions',
                            '_links.self.title', '_links.self.href']


def build_query (modality, latest=True, max_results=SERVER_PAGE_SIZE,
                 page_num=1, query_params=None):
  """
  Construct and return a query string given the modality, starting page number,
  optional maximum results, most recent records flag, and
  optional dictionary of query parameter keys and values.
  Returns a single constructed query URL string.
  """
  validate_modality(modality)          # validates or raises ValueError

  # check for a reasonable page number and max results
  if (not page_num or (page_num < 1)):
    page_num = 1
  if (not max_results or (max_results < 1)):
    max_results = SERVER_PAGE_SIZE

  url_str = f"{SERVER_URL}/{modality}?max_results={max_results}&page={page_num}"

  # if latest flag specified, use the most recent records
  if (latest):                         # uses most recent by default
    url_str = f"{url_str}&sort=-_created"

  if (query_params is not None):
    pairs = [f"{key}{val}" for key, val in query_params.items()]
    qps = '%20and%20'.join(pairs)
    url_str = f"{url_str}&where={qps}"

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
     records: list of records (dictionaries) to be deduplicated.
     chksums: SET of previously seen checksums; used to identify duplicate records.
  """
  # omit records w/ no checksum or checksum is in list of checksums already seen
  return ([rec for rec in records if is_not_duplicate(rec, chksums)], chksums)


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
  return json_query_result.get('_items', [])


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


def get_n_records (modality, num_recs, query_params=None,
                   fields_to_remove=DEFAULT_FIELDS_TO_REMOVE):
  """
  Fetch N records from the server using the given parameters. Query then
  clean, flatten, deduplicate and return a list of fetched image quality
  metrics records (dictionaries).
  Arguments:
    modality: the modality to query on (must be one of {ALLOWED_MODALITIES}).
    num_recs: number of records the user would like returned.
    query_params: dictionary of additional query parameters (default: None).
    fields_to_remove: a list of field names to remove when cleaning records.
  """
  good_records = []
  next_page_num = 1
  chksums_seen = set()

  # loop until we get the number of records requested by the user or we fail to do so:
  while (len(good_records) < num_recs):
    query = build_query(modality, page_num=next_page_num, query_params=query_params)
    recs = query_for_page(query, fields_to_remove=fields_to_remove)
    if (len(recs) < 1):                # if no more records available, then exit
      break
    recs, chksums_seen = deduplicate_records(recs, chksums_seen)
    good_records.extend(recs)
    next_page_num += 1

  # if got more than user asked for, prune off any extra records:
  return good_records[:num_recs] if (len(good_records) > num_recs) else good_records


def query_for_page (query, fields_to_remove=DEFAULT_FIELDS_TO_REMOVE):
  """
  Query for the first (or numbered) page of results from
  the MRIQC server, and clean and return the result records.
  Arguments:
    query: pre-built query string to use to fetch a page of results.
    fields_to_remove: a list of field names to remove when cleaning records.
  """
  json_query_result = do_query(query)
  json_recs = extract_records(json_query_result)
  flat_recs = flatten_records(json_recs)
  return clean_records(flat_recs, fields_to_remove=fields_to_remove)


def save_to_tsv (modality, records, filepath):
  """
  Save the given image metric records (list of dictionaries) to the
  file at the given filepath (default standard output).
  """
  if (records):
    if (modality in STRUCTURAL_MODALITIES):
      fields = sorted(list(STRUCTURAL_KEYWORDS))
    else:
      fields = sorted(list(BOLD_KEYWORDS))
    with open(filepath, 'w', newline='') as tsvfile:
      writer = csv.DictWriter(tsvfile, fieldnames=fields, delimiter='\t', extrasaction='ignore')
      writer.writeheader()
      for rec in records:
        writer.writerow(rec)


def server_status (modality='bold', query_params=None):
  """
  Query the server with the user's current query parameters but only fetch
  one record. This serves as a quick health check.
  Return the total number of records available that satisfy the query with the
  given parameters OR raises a requests.RequestException if the request fails.
  """
  health_check_query = build_query(modality=modality, max_results=1, query_params=query_params)
  # the GET request will raise an error if not successful:
  json_query_result = do_query(health_check_query)
  meta = json_query_result.get('_meta')
  total_recs = meta.get('total') if meta else 0
  return total_recs
