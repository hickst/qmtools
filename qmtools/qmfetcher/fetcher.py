# Methods to query the MRIQC server and download query result records.
#   Written by: Tom Hicks and Dianne Patterson.
#   Last Modified: Remove unused imports.
#
import csv
import json
import requests as req

from copy import deepcopy

from config.mriqc_keywords import BOLD_KEYWORDS, STRUCTURAL_KEYWORDS
from qmtools import STRUCTURAL_MODALITIES
from qmtools.qmfetcher import REQUEST_TIMEOUT, SERVER_PAGE_SIZE
from qmtools.qm_utils import validate_modality

SERVER_URL = "https://mriqc.nimh.nih.gov/api/v1"


def build_query (modality, args, page_num=1):
  """
  Construct and return a query string given the modality and a dictionary of
  optional query arguments; like maximum results, oldest record flag, and
  dictionary of content query parameter keys and values.
  Returns a single constructed query URL string.
  """
  validate_modality(modality)          # validates or raises ValueError

  # check for a reasonable page number
  if (not page_num or (page_num < 1)):
    page_num = 1

  # use the number of records as the max_results argument
  max_results = get_num_recs_arg(args)

  url_str = f"{SERVER_URL}/{modality}?max_results={max_results}&page={page_num}"

  # if use_oldest flag is not specified, sort the records to use the most recent
  if (not args.get('use_oldest', False)):   # uses most recent by default
    url_str = f"{url_str}&sort=-_created"

  # add any content query parameters in the "special" where clause
  query_params = args.get('query_params')
  if (query_params is not None):
    pairs = [f"{key}{val}" for key, val in query_params.items()]
    qps = '%20and%20'.join(pairs)
    url_str = f"{url_str}&where={qps}"

  return url_str


def clean_records (json_recs, args=None):
  """
  Remove unwanted fields from each record (dictionary) in the given list and
  return the list of cleaned records.
  Arguments:
    json_recs: a list of records, each one representing metrics for a single image.
    args: an optional dictionary of arguments which may contain a list of
          fields to be removed.
  """
  if (args):
    fields_to_remove = args.get('fields_to_remove')
    if (fields_to_remove):
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


def do_query (query_str, timeout=REQUEST_TIMEOUT):
  """
  Query the server with the given query string, waiting for the specified
  or default time, then return the parsed JSON data if successful, otherwise
 raise a RequestException.
  """
  resp = req.get(query_str, timeout=timeout)
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


def get_n_records (modality, args):
  """
  Fetch N records from the server using the given parameters. Query then
  clean, flatten, deduplicate and return a list of fetched image quality
  metrics records (dictionaries).
  Arguments:
    modality: the modality to query on (must be one of {ALLOWED_MODALITIES}).
    args: a dictionary of optional arguments to create/control the query.
  """
  good_records = []
  next_page_num = 1
  chksums_seen = set()

  # loop until we get the number of records requested by the user or we fail to do so:
  num_recs = get_num_recs_arg(args)
  while (len(good_records) < num_recs):
    query = build_query(modality, args, page_num=next_page_num)
    recs = query_for_page(query)
    if (len(recs) < 1):                # if no more records available, then exit
      break
    recs, chksums_seen = deduplicate_records(recs, chksums_seen)
    good_records.extend(recs)
    next_page_num += 1

  # if got more than user asked for, prune off any extra records:
  return good_records[:num_recs] if (len(good_records) > num_recs) else good_records


def get_num_recs_arg (args):
  """
  Extract and check the number of records argument in the given arguments dictionary.
  If the value is missing or not valid, reset it to the default value. Return the
  extracted (or possibly the default) value.
  """
  num_recs = args.get('num_recs', SERVER_PAGE_SIZE)
  if (num_recs < 1):
    num_recs = SERVER_PAGE_SIZE
    args['num_recs'] = num_recs
  return num_recs


def query_for_page (query, args=None):
  """
  Query for the first (or numbered) page of results from
  the MRIQC server, and clean and return the result records.
  Arguments:
    query: pre-built query string to use to fetch a page of results.
    args: a dictionary of arguments to create/control the query, passed to children.
  """
  json_query_result = do_query(query)
  json_recs = extract_records(json_query_result)
  flat_recs = flatten_records(json_recs)
  clean_records(flat_recs, args)
  return flat_recs


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


def server_status (modality='bold', args=None):
  """
  Query the server with the user's current query parameters but only fetch
  one record. This serves as a quick health check.
  Return the total number of records available that satisfy the query with the
  given parameters OR raises a requests.RequestException if the request fails.
  Arguments:
    modality: the modality to query on (must be one of {ALLOWED_MODALITIES}).
    args: a dictionary of arguments to create/control the query, passed to children.
  """
  if (args is None):
    ss_args = {}
  else:
    ss_args = deepcopy(args)
  ss_args['num_recs'] = 1              # reset number of records to fetch to 1
  health_check_query = build_query(modality, ss_args)
  # the GET request will raise an error if not successful:
  json_query_result = do_query(health_check_query)
  meta = json_query_result.get('_meta')
  total_recs = meta.get('total') if meta else 0
  return total_recs
