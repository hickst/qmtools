# CLI program to convert an MRIQC file to normalized scores
# for representation in an HTML "traffic-light" report.
#   Written by: Tom Hicks and Dianne Patterson.
# Last Modified: Minor error message change.
#
import argparse
import os
import sys

from qmtools import ( ALLOWED_MODALITIES, BIDS_DATA_EXT, INPUT_FILE_EXIT_CODE,
                      REPORTS_DIR, REPORTS_EXT )
from qmtools.file_utils import good_file_path
import qmtools.qm_utils as qmu
import qmtools.qmview.traffic_light as traf

PROG_NAME = 'qmtraffic'


def check_input_file (input_file):
  """
  If an input file path is given, check that it is a good path. If not, then exit
  the entire program here with the specified (or default) system exit code.
  """
  if (input_file is None or (not good_file_path(input_file))):
    errMsg = "({}): ERROR: {} Exiting...".format(PROG_NAME,
      f"A path to a readable, MRIQC group file ({BIDS_DATA_EXT}) must be specified.")
    print(errMsg, file=sys.stderr)
    sys.exit(INPUT_FILE_EXIT_CODE)


def main (argv=None):
  """
  The main method for the QMView. This method is called from the command line,
  processes the command line arguments and calls into the traffic_light module to do
  its work.
  This main method takes no arguments so it can be called by setuptools but
  the program expects two arguments from the command line:
    1) required modality of the MRIQC group file (one of 'bold', 'T1w', or 'T2w')
    2) required path to the MRIQC group file (in TSV format) to visualize.
    3) optional name of output report file in the reports directory.
  """
  # the main method takes no arguments so it can be called by setuptools
  if (argv is None):                   # if called by setuptools
    argv = sys.argv[1:]                # then fetch the arguments from the system

  # setup command line argument parsing and add shared arguments
  parser = argparse.ArgumentParser(
    prog=PROG_NAME,
    formatter_class=argparse.RawTextHelpFormatter,
    description='Normalize an MRIQC group file and produce HTML reports.'
  )

  parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    default=False,
    help='Print informational messages during processing [default: False (non-verbose mode)].'
  )

  parser.add_argument(
    'modality', choices=ALLOWED_MODALITIES,
    help=f"Modality of the MRIQC group file. Must be one of: {ALLOWED_MODALITIES}"
  )

  parser.add_argument(
    'group_file',
    help=f"Path to an MRIQC group file ({BIDS_DATA_EXT}) to visualize."
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

  # if input file path given, check the file path for validity
  group_file = args.get('group_file')
  check_input_file(group_file)   # if check fails exits here does not return!

  # check if the reports directory exists and is writeable or try to create it
  qmu.ensure_reports_dir(PROG_NAME)  # may exit here if unable to create dir

  # use given output subdirectory name or generate one
  report_dir = args.get('report_dir')
  if (not report_dir):            # if none provided, generate an output dirname
    report_dir = qmu.gen_output_name(modality)
    args['report_dir'] = report_dir

  # create the path to the report subdirectory in the main reports directory
  report_dirpath = os.path.join(REPORTS_DIR, report_dir)
  args['report_dirpath'] = report_dirpath

  # check if the reports directory exists and is writeable or try to create it
  qmu.ensure_reports_dir(PROG_NAME, report_dirpath)  # may exit here if unable to create dir

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Processing MRIQC group file '{group_file}' with modality '{modality}'.",
      file=sys.stderr)

  # generate the various files for the traffic light report
  traf.make_legends(report_dirpath)
  traf.make_traffic_light_table(modality, group_file, report_dirpath)

  if (args.get('verbose')):
    print(f"({PROG_NAME}): Produced reports in reports directory '{report_dirpath}'.",
      file=sys.stderr)
    print(f"({PROG_NAME}): To see the report: open '{report_dirpath}/{modality}{REPORTS_EXT}' in a browser.",
      file=sys.stderr)



if __name__ == "__main__":
  main()
