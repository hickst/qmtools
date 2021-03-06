# CLI program to query the MRIQC server and download query result records into
# a file for further processing.
#   Written by: Tom Hicks and Dianne Patterson.
# Last Modified: Minor doc/naming cleanups.
#
import argparse
import os
import sys

import requests as req

import qmtools.qm_utils as qmu
import qmtools.qmfetcher.fetcher as fetch
from qmtools import (ALLOWED_MODALITIES, BIDS_DATA_EXT, FETCHED_DIR,
                     NUM_RECS_EXIT_CODE, QUERY_FILE_EXIT_CODE)
from qmtools.file_utils import good_file_path
from qmtools.qmfetcher import SERVER_PAGE_SIZE
from qmtools.qmfetcher.query_parser import parse_query_from_file

PROG_NAME = 'qmfetcher'


def check_query_file (query_file):
  """
  If a query parameters file path is given, check that it is a good path.
  If not, then exit the entire program here with a specific system exit code.
  """
  if (not good_file_path(query_file)):
    errMsg = "({}): ERROR: {} Exiting...".format(PROG_NAME,
      "The -q flag must specify a valid, readable query parameters file.")
    print(errMsg, file=sys.stderr)
    sys.exit(QUERY_FILE_EXIT_CODE)


def check_num_recs (num_recs):
  """
  Check that the number of records requested is reasonable (i.e. >= 1).
  If not, then exit the entire program here with a specific system exit code.
  """
  if (num_recs < 1):
    err_msg = "({}): ERROR: {} Exiting...".format(PROG_NAME,
      "The total number of records to fetch must be 1 or more.")
    print(err_msg, file=sys.stderr)
    sys.exit(NUM_RECS_EXIT_CODE)


def main (argv=None):
  """
  The main method for the QMView. This method is called from the command line,
  processes the command line arguments and calls into the fetcher module to do
  its work.
  This main method takes no arguments so it can be called by setuptools but
  the program takes arguments from the command line:
    1) required modality of the IQM records to fetch (one of 'bold', 'T1w', or 'T2w')
    2) optional number of records to fetch [default: {SERVER_PAGE_SIZE}]
    3) optional output filename [default: NONE (one will be generated)]
    4) optional path to query parameters file [default: NONE]
    5) optional flag to use the oldest records [default: False (use latest records)]
    6) optional flag to produce query URL only and then exit.
  """
  # the main method takes no arguments so it can be called by setuptools
  if (argv is None):                   # if called by setuptools
    argv = sys.argv[1:]                # then fetch the arguments from the system

  # setup command line argument parsing and add shared arguments
  parser = argparse.ArgumentParser(
    prog=PROG_NAME,
    formatter_class=argparse.RawTextHelpFormatter,
    description='Query the MRIQC server and save query results.'
  )

  parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    default=False,
    help='Print informational messages during processing [default: False (non-verbose mode)].'
  )

  parser.add_argument(
    'modality', choices=ALLOWED_MODALITIES,
    help=f"Modality of the MRIQC IQM records to fetch. Must be one of: {ALLOWED_MODALITIES}"
  )

  parser.add_argument(
    '-n', '--num-recs', dest='num_recs', type=int,
    default=SERVER_PAGE_SIZE,
    help='Number of records to fetch (maximum) from a query [default: {SERVER_PAGE_SIZE}]'
  )

  parser.add_argument(
    '-o', '--output-filename', dest='output_filename', metavar='filename',
    default=argparse.SUPPRESS,
    help='Optional name of file to hold query results in fetched directory [default: none].'
  )

  parser.add_argument(
    '-q', '--query-file', dest='query_file', metavar='filepath',
    default=argparse.SUPPRESS,
    help="Path to a query parameters file in or below the run directory [no default]"
  )

  parser.add_argument(
    '--use-oldest', dest='use_oldest', action='store_true',
    default=False,
    help='Fetch oldest records [default: False (fetches most recent records)].'
  )

  parser.add_argument(
    '--url-only', dest='url_only', action='store_true',
    default=False,
    help='Generate the query URL and exit program [default: False].'
  )

  # actually parse the arguments from the command line
  args = vars(parser.parse_args(argv))

  # check modality for validity: assumes arg parse provides valid value
  modality = qmu.validate_modality(args.get('modality'))

  # check if the fetched directory exists and is writeable or try to create it
  qmu.ensure_fetched_dir(PROG_NAME)

  # if number of records to fetch is specified, check it for validity
  num_recs = args.get('num_recs')      # total number of records to fetch
  check_num_recs(num_recs)             # if check fails exits here, does not return!

  # use output file name given or generate one
  output_filename = args.get('output_filename')
  if (not output_filename):            # if none provided, generate an output filename
    output_filename = qmu.gen_output_name(modality, BIDS_DATA_EXT)
    args['output_filename'] = output_filename

  # ensure output file path has the correct extension
  output_filepath = os.path.join(FETCHED_DIR, output_filename)
  if (not output_filepath.endswith(BIDS_DATA_EXT)):
    output_filepath = output_filepath + BIDS_DATA_EXT
  args['output_filepath'] = output_filepath

  # if query parameters file path given, check the file path for validity
  query_file = args.get('query_file')
  if (query_file):                     # if filepath provided, validate it
    check_query_file(query_file)       # may exit here and not return!
    query_params = parse_query_from_file(modality, query_file, PROG_NAME)
    args['query_params'] = query_params
  else:
    query_params = None

  if (args.get('url_only')):           # if generating URL only
    print(fetch.build_query(modality, args))
    sys.exit(0)                        # all done: exit out now

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Querying MRIQC server with modality '{modality}', for {num_recs} records.",
      file=sys.stderr)

  # Use user's query to test whether the MRIQC server is up, exit out if not:
  try:
    total_recs = fetch.server_status(modality=modality, args=args)
  except req.RequestException as re:
    status = re.response.status_code
    if (status == 503):
      errMsg = f"({PROG_NAME}): ERROR: MRIQC WebAPI service currently unavailable ({status})."
      print(errMsg, file=sys.stderr)
      sys.exit(status)

  # build the query and fetch some records from the MRIQC server:
  recs = fetch.get_n_records(modality, args)

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Fetched {len(recs)} records out of {total_recs}.")

  # save the fetched records into a TSV file:
  fetch.save_to_tsv(modality, recs, output_filepath)

  if (args.get('verbose')):
    if (output_filename is not None):
      print(f"({PROG_NAME}): Saved query results to '{output_filepath}'.", file=sys.stderr)



if __name__ == "__main__":
  main()
