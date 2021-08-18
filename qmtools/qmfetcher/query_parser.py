#
# Module with methods to read and parse a query parameters file.
#   Written by: Tom Hicks. 8/17/2021.
#   Last Modified: Fix an error message.
#
import configparser as cp
from configparser import MissingSectionHeaderError, ParsingError
import sys


def parse_query_from_file (query_file, prog_name=''):
    """
    Load and validate a set of query parameters from the given query parameters file.
    Return a dictionary of valid query parameters or raise exceptions.
    """
    qparams = load_query_from_file(query_file, prog_name)
    # TODO: validate_query_params(qparams)
    return qparams


def load_query_from_file (query_file, prog_name=''):
    """
    Load query parameters from the 'parameters' section of the given
    query parameters file. Return those parameters as a dictionary
    or raise exceptions for various loading problems.
    """
    sys.tracebacklimit = 0
    try:
      config = cp.ConfigParser(strict=False, empty_lines_in_values=False)
      config.optionxform = lambda option: option
      config.read_file(open(query_file))
    except FileNotFoundError as fnf:
      errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
        f"Query parameters file '{query_file}' not found or not readable.")
      raise FileNotFoundError(errMsg)
    except MissingSectionHeaderError as mse:
      errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
        "A 'parameters' section header must be included in the query parameters file.")
      raise ValueError(errMsg)
    except ParsingError as pe:
      errMsg = "({}): ERROR: {} Exiting...".format(prog_name, pe)
      raise ValueError(errMsg)

    try:
      qparams = config['parameters']
    except KeyError as ke:
      errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
        "No section named 'parameters' found in query parameters file.")
      raise ValueError(errMsg)

    return dict(qparams)
