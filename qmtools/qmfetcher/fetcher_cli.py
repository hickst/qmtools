# Author: Tom Hicks and Dianne Patterson.
# Purpose: CLI program to query the MRIQC server and download query result records
#          into a file for further processing
# Last Modified: Move allowed modalities constant.

import argparse
import os
import sys
import requests as req

from config.settings import REPORTS_DIR
import qmtools.qmview.traffic_light as traf
from qmtools import ALLOWED_MODALITIES
from qmtools.file_utils import good_file_path, good_dir_path

PROG_NAME = 'qmfetcher'
OUTPUT_FILE_EXIT_CODE = 20
REPORTS_DIR_EXIT_CODE = 11


def check_output_file (output_file):
  """
  If an output file path is given, check that it is a good, writeable path. If not,
  then exit the entire program here with the specified (or default) system exit code.
  """
  output_dir = os.path.dirname(output_file)
  if (output_dir is None or (not good_dir_path(output_dir, writeable=True))):
    errMsg = "({}): ERROR: {} Exiting...".format(PROG_NAME,
      "The directory for the specified output file must be writeable.")
    print(errMsg, file=sys.stderr)
    sys.exit(OUTPUT_FILE_EXIT_CODE)


def check_reports_dir (reports_dir):
  """
  Check that the given output directory path is a valid path. If not, then exit
  the entire program here with the specified (or default) system exit code.
  """
  if (reports_dir is None or (not good_dir_path(reports_dir, writeable=True))):
    helpMsg =  """
      Unless there is a writeable subdirectory called 'reports',
      a path to a writeable reports output directory must be specified.")
      """
    errMsg = "({}): ERROR: {} Exiting...".format(PROG_NAME, helpMsg)
    print(errMsg, file=sys.stderr)
    sys.exit(REPORTS_DIR_EXIT_CODE)


def main (argv=None):
  """
  The main method for the QMView. This method is called from the command line,
  processes the command line arguments and calls into the qmview library to do
  its work.
  This main method takes no arguments so it can be called by setuptools but
  the program expects two arguments from the command line:
    1) the modality of the output file (one of 'bold', 't1w', or 't2w')
    2) number of records to fetch (default: 1000)
    3) path to the output file (default: standard output)
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
    '-n', '--num_recs', dest='num_recs',
    default=1000,
    help='Number of records to fetch (maximum) from a query [default: 1000]'
  )

  parser.add_argument(
    '-o', '--output-file', dest='output_file', metavar='filepath',
    default=argparse.SUPPRESS,
    help='Path to a writeable file in which to store query results [default: (standard output)].'
  )

  parser.add_argument(
    '-r', '--report-dir', dest='reports_dir', metavar='dirpath',
    default=REPORTS_DIR,
    help=f"Path to a writeable directory for reports files [default: {REPORTS_DIR}]"
  )

  # actually parse the arguments from the command line
  args = vars(parser.parse_args(argv))

  # check modality for validity: assumes arg parse provides valid value
  modality = traf.validate_modality(args.get('modality'))

  # if output file path given, check the file path for validity
  output_file = args.get('output_file')
  if (output_file):                    # if user provided an output filepath, check it
    check_output_file(output_file)     # if check fails exits here does not return!

  # if reports directory path given, check the path for validity
  reports_dir = args.get('reports_dir', REPORTS_DIR)
  check_reports_dir(reports_dir)       # if check fails exits here does not return!

  num_recs = args.get('num_recs')      # total number of records to fetch

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Querying MRIQC server with modality '{modality}', for {num_recs} records.",
      file=sys.stderr)

  # query the MRIQC server and output or save the results
  try:
    # TODO: something
    # while more pages:
    #  read each page into df
    #  drop unwanted columns: df.drop('col2', axis=1, inplace=True)
    #  ?? drop rows with no md5sum and duplicate rows ??
    #  ?? other data checking/cleaning ??
    #  concatenate df onto master df
    print(f"ARGS={args}")              # REMOVE LATER
    # url_root = 'https://mriqc.nimh.nih.gov/api/v1/{modality}?{query}'
    # url_root = 'https://mriqc.nimh.nih.gov/api/v1/bold?max_results=100'
    # req.get(url_root)
    

  except Exception as err:
    errMsg = "({}): ERROR: Processing Error ({}): {}".format(
      PROG_NAME, err.error_code, err.message)
    print(errMsg, file=sys.stderr)
    sys.exit(err.error_code)

  if (args.get('verbose')):
    if (output_file is not None):
      print(f"({PROG_NAME}): Saved query results to '{output_file}'.",
        file=sys.stderr)



if __name__ == "__main__":
  main()