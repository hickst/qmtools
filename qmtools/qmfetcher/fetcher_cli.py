# Author: Tom Hicks and Dianne Patterson.
# Purpose: CLI program to query the MRIQC server and download query result records
#          into a file for further processing.
# Last Modified: Update output file path verbose message.

import argparse
import os
import pandas as pd
import requests as req
import sys

import qmtools.qm_utils as qmu
import qmtools.qmfetcher.fetcher as fetch
from qmtools import ALLOWED_MODALITIES, FETCHED_DIR, NUM_RECS_EXIT_CODE
from qmtools.qmfetcher import SERVER_PAGE_SIZE

PROG_NAME = 'qmfetcher'


def check_num_recs (num_recs):
  if (num_recs < 1):
    err_msg = "({}): ERROR: {} Exiting...".format(PROG_NAME,
      "The total number of records to fetch must be 1 or more.")
    print(err_msg, file=sys.stderr)
    sys.exit(NUM_RECS_EXIT_CODE)


def main (argv=None):
  """
  The main method for the QMView. This method is called from the command line,
  processes the command line arguments and calls into the qmview library to do
  its work.
  This main method takes no arguments so it can be called by setuptools but
  the program expects two arguments from the command line:
    1) the modality of the output file (one of 'bold', 't1w', or 't2w')
    2) optional number of records to fetch (default: {SERVER_PAGE_SIZE})
    3) optional output filename (default: NONE (one will be generated))
    4) path to parameter file (default: query_params.toml)
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
    '-m', '--modality', dest='modality', required=True,
    choices=ALLOWED_MODALITIES,
    help=f"Modality of the MRIQC group output file. Must be one of: {ALLOWED_MODALITIES}"
  )

  parser.add_argument(
    '-n', '--num-recs', dest='num_recs',
    default=SERVER_PAGE_SIZE,
    help='Number of records to fetch (maximum) from a query [default: {SERVER_PAGE_SIZE}]'
  )

  parser.add_argument(
    '-o', '--output-filename', dest='output_filename', metavar='filename',
    default=argparse.SUPPRESS,
    help='Optional name of file to hold query results in fetched directory [default: none].'
  )

  # TODO: Add/check query parameter file argument.

  # actually parse the arguments from the command line
  args = vars(parser.parse_args(argv))

  # check modality for validity: assumes arg parse provides valid value
  modality = qmu.validate_modality(args.get('modality'))

  # check if the fetched directory exists and is writeable or try to create it
  qmu.ensure_fetched_dir(PROG_NAME)

  # if number of records to fetch is specified, check it for validity
  num_recs = args.get('num_recs')      # total number of records to fetch
  check_num_recs(num_recs)             # if check fails exits here, does not return!

  # if output file path given, check the file path for validity
  output_filename = args.get('output_filename')
  if (not output_filename):            # if none provided, generate an output filename
    output_filename = qmu.gen_output_filename(modality)

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Querying MRIQC server with modality '{modality}', for {num_recs} records.",
      file=sys.stderr)

  # test whether the MRIQC server is up, exit out if not
  try:
    fetch.server_health_check()
  except req.RequestException as re:
    status = re.response.status_code
    if (status == 503):
      errMsg = f"({PROG_NAME}): ERROR: MRIQC WebAPI service currently unavailable ({status})."
      print(errMsg, file=sys.stderr)
      sys.exit(status)

  # query the MRIQC server and output or save the results
  try:
    # while more pages:
    #  ?? drop rows with no md5sum ?? 
    #  ?? and duplicate rows ??
    #  concatenate df onto master df

    # url_root = 'https://mriqc.nimh.nih.gov/api/v1/{modality}?{query}'
    # url_root = 'https://mriqc.nimh.nih.gov/api/v1/bold?max_results=100'

    # list of all records gathered so far
    # all_recs = []
    # while True:
    #   jrecs = fetch.query_for_page(modality, start_page)
    #   if (not jrecs):
    #     break
    #   else:
    #     start_page += 1
    #     all_recs.append(jrecs)

    # df = pd.DataFrame(all_recs)
    # write out the dataframe as a TSV file
    print(f"ARGS={args}")              # REMOVE LATER

  except Exception as err:
    errMsg = "({}): ERROR: Processing Error ({}): {}".format(
      PROG_NAME, err.error_code, err.message)
    print(errMsg, file=sys.stderr)
    sys.exit(err.error_code)

  if (args.get('verbose')):
    if (output_filename is not None):
      print(f"({PROG_NAME}): Saved query results to '{FETCHED_DIR}/{output_filename}'.", file=sys.stderr)



if __name__ == "__main__":
  main()