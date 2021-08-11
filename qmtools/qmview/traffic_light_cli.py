# Author: Tom Hicks and Dianne Patterson.
# Purpose: CLI program to convert an MRIQC output file to normalized scores
#          for representation in an HTML "traffic-light" report.
# Last Modified: Update for fixed reports directory (really, this time).

import argparse
import sys

from qmtools import ALLOWED_MODALITIES, INPUT_FILE_EXIT_CODE
from qmtools import REPORTS_DIR, REPORTS_DIR_EXIT_CODE
from qmtools.file_utils import good_file_path, good_dir_path
from qmtools.qm_utils import ensure_reports_dir, validate_modality
import qmtools.qmview.traffic_light as traf

PROG_NAME = 'qmview'


def check_input_file (input_file):
  """
  If an input file path is given, check that it is a good path. If not, then exit
  the entire program here with the specified (or default) system exit code.
  """
  if (input_file is None or (not good_file_path(input_file))):
    errMsg = "({}): ERROR: {} Exiting...".format(PROG_NAME,
      "A readable, MRIQC group output file (.tsv) must be specified.")
    print(errMsg, file=sys.stderr)
    sys.exit(INPUT_FILE_EXIT_CODE)


def main (argv=None):
  """
  The main method for the QMView. This method is called from the command line,
  processes the command line arguments and calls into the qmview library to do
  its work.
  This main method takes no arguments so it can be called by setuptools but
  the program expects two arguments from the command line:
    1) path to the MRIQC group output file in TSV format,
    2) the modality of the input file (one of 'bold', 't1w', or 't2w')
  """
  # the main method takes no arguments so it can be called by setuptools
  if (argv is None):                   # if called by setuptools
    argv = sys.argv[1:]                # then fetch the arguments from the system

  # setup command line argument parsing and add shared arguments
  parser = argparse.ArgumentParser(
    prog=PROG_NAME,
    formatter_class=argparse.RawTextHelpFormatter,
    description='Normalize an MRIQC group output file and produce HTML reports.'
  )

  parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    default=False,
    help='Print informational messages during processing [default: False (non-verbose mode)].'
  )

  parser.add_argument(
    '-i', '--input-file', dest='group_file', required=True, metavar='filepath',
    help='Full path to an MRIQC group output file (.tsv) to process.'
  )

  parser.add_argument(
    '-m', '--modality', dest='modality', required=True,
    choices=ALLOWED_MODALITIES,
    help=f"Modality of the MRIQC group output file. Must be one of: {ALLOWED_MODALITIES}"
  )

  # actually parse the arguments from the command line
  args = vars(parser.parse_args(argv))

  # check modality for validity: assumes arg parse provides valid value
  modality = validate_modality(args.get('modality'))

  # if input file path given, check the file path for validity
  group_file = args.get('group_file')
  check_input_file(group_file)   # if check fails exits here does not return!

  # check if the reports directory exists and is writeable or try to create it
  ensure_reports_dir(PROG_NAME)  # may exit here if unable to create dir

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Processing MRIQC group file '{group_file}' with modality '{modality}'.",
      file=sys.stderr)

  # generate the various files for the traffic light report
  try:
    traf.make_legends()
    traf.make_traffic_light_table(group_file, modality)
  except Exception as err:
    errMsg = "({}): ERROR: Processing Error ({}): {}".format(
      PROG_NAME, err.error_code, err.message)
    print(errMsg, file=sys.stderr)
    sys.exit(err.error_code)

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Produced reports in reports directory '{REPORTS_DIR}'.",
      file=sys.stderr)



if __name__ == "__main__":
  main()