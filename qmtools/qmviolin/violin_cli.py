# CLI program to produce a report with violin plots comparing two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/1/2021.
#   Last Modified: Begin HTML report generation.
#
import argparse
import os
import sys

import qmtools.qm_utils as qmu
from qmtools import (ALLOWED_MODALITIES, BIDS_DATA_EXT,
                     INPUT_FILE_EXIT_CODE, REPORTS_DIR)
from qmtools.file_utils import good_file_path
from qmtools.qmviolin import violin

PROG_NAME = 'qmviolin'


def check_input_file (input_file, msg='A readable input file must be specified.'):
  """
  If an input file path is given, check that it is a good path. If not, then exit
  the entire program here with the specified (or default) system exit code.
  """
  if (input_file is None or (not good_file_path(input_file))):
    errMsg = "({}): ERROR: {} Exiting...".format(PROG_NAME, msg)
    print(errMsg, file=sys.stderr)
    sys.exit(INPUT_FILE_EXIT_CODE)


def main (argv=None):
  """
  The main method for the QMViolin. This method is called from the command line,
  processes the command line arguments and calls into the qmview library to do
  its work.
  This main method takes no arguments so it can be called by setuptools but
  the program expects various arguments from the command line:
    1) required modality of the MRIQC group file (one of 'bold', 'T1w', or 'T2w')
    2) required path to the MRIQC downloaded/fetched file (in TSV format) to compare against.
    3) required path to the MRIQC group file (in TSV format) to process.
    4) optional name of output report file in the reports directory.
  """
  # the main method takes no arguments so it can be called by setuptools
  if (argv is None):                   # if called by setuptools
    argv = sys.argv[1:]                # then fetch the arguments from the system

  # setup command line argument parsing and add shared arguments
  parser = argparse.ArgumentParser(
    prog=PROG_NAME,
    formatter_class=argparse.RawTextHelpFormatter,
    description='Produce a report with violin plots comparing two MRIQC datasets.'
  )

  parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    default=False,
    help='Print informational messages during processing [default: False (non-verbose mode)].'
  )

  parser.add_argument(
    'modality', choices=ALLOWED_MODALITIES,
    help=f"Modality of the MRIQC files. Must be one of: {ALLOWED_MODALITIES}"
  )

  parser.add_argument(
    'fetched_file',
    help=f"Path to an MRIQC downloaded/fetched file ({BIDS_DATA_EXT}) to compare against."
  )

  parser.add_argument(
    'group_file',
    help=f"Path to the MRIQC group file ({BIDS_DATA_EXT}) to process."
  )

  parser.add_argument(
    '-r', '--report-dir', dest='report_dir',
    default=argparse.SUPPRESS,
    help='Optional name of report subdirectory in main reports directory [default: none].'
  )

  # actually parse the arguments from the command line
  args = vars(parser.parse_args(argv))

  # check modality for validity: assumes arg parse provides valid value
  modality = qmu.validate_modality(args.get('modality'))

  # check if the reports directory exists and is writeable or try to create it
  qmu.ensure_reports_dir(PROG_NAME)    # may exit here if unable to create dir

  # use given output directory name or generate one
  report_dir = args.get('report_dir')
  if (not report_dir):            # if none provided, generate an output filename
    report_dir = qmu.gen_output_name(modality)
    args['report_dir'] = report_dir

  # create the path to the report subdirectory in the main reports directory
  report_dirpath = os.path.join(REPORTS_DIR, report_dir)
  args['report_dirpath'] = report_dirpath

  # if MRIQC fetched input file path given, check the file path for validity and
  # exit if the file path is not valid!
  fetched_file = args.get('fetched_file')
  check_input_file(fetched_file, f"A readable, MRIQC fetched data file ({BIDS_DATA_EXT}) must be specified.")

  # if user's input group file path given, check the file path for validity and
  # exit if the file path is not valid!
  group_file = args.get('group_file')
  check_input_file(group_file, f"A readable, MRIQC group file ({BIDS_DATA_EXT}) must be specified.")

  # check if the reports directory exists and is writeable or try to create it
  qmu.ensure_reports_dir(PROG_NAME, report_dirpath)  # may exit here if unable to create dir

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Comparing MRIQC records with modality '{modality}'.",
          file=sys.stderr)

  # query the MRIQC server and output or save the results
  try:
    # print(f"ARGS={args}", file=sys.stderr)  # REMOVE LATER

    # read data, merge records, and create the violin plots:
    plot_info = violin.vplot(modality, args)

    # generate the HTML report into the reports directory:
    # TODO: IMPLEMENT HTML generation
    violin.make_html_report(modality, args, plot_info)

    if (args.get('verbose')):
      print(f"({PROG_NAME}): Compared group records against fetched records.",
            file=sys.stderr)

  except Exception as err:
    errMsg = "({}): ERROR: Processing Error: {}".format(PROG_NAME, str(err))
    print(errMsg, file=sys.stderr)
    sys.exit(1)

  if (args.get('verbose')):
    if (report_dir is not None):
      print(f"({PROG_NAME}): Produced violin report to '{report_dirpath}'.",
            file=sys.stderr)



if __name__ == "__main__":
  main()
