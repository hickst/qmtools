#
# Module with methods to read and parse a query parameters file.
#   Written by: Tom Hicks. 8/17/2021.
#   Last Modified: Fix indentation. Add methods to parse and validate the query parameters.
#
import sys
import configparser as cp
from configparser import MissingSectionHeaderError, ParsingError
from qmtools import STRUCTURAL_MODALITIES
from config.mriqc_keywords import BIDS_KEYWORDS, BOLD_KEYWORDS, STRUCTURAL_KEYWORDS


def parse_query_from_file (modality, query_file, prog_name=''):
  """
  Load and validate a set of query parameters from the given query parameters file.
  Return a dictionary of valid query parameters or raise exceptions.
  """
  query_params = load_query_from_file(query_file, prog_name)
  validate_query_params(modality, query_params, prog_name)
  return query_params


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


def parse_value (val, prog_name=''):
  """
  Separate and clean the operator and the value from the given value string.
  Returns the operator and the value reconcatenated, with whitespace stripped.
  """
  ops1 = set(['<', '>'])
  ops2 = set(['==', '<=', '>=', '!='])
  opsall = ops1.union(ops2)
  ch1 = val[:2]
  ch2 = val[:1]
  if (ch2 in ops2):
    return f"{ch2}{val[2:].strip()}"
  elif (ch1 in ops1):
    return f"{ch1}{val[1:].strip()}"
  else:
    errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
             f"The comparison operator must be one of {opsall}")
    raise ValueError(errMsg)


def validate_keyword (modality, key, prog_name=''):
  """
  Compare the given keyword to known sets of modality-specific keywords and
  raise a ValueError if the keyword is unknown or not valid for the modality.
  """
  if (key in BIDS_KEYWORDS):
    return True

  if (modality in STRUCTURAL_MODALITIES):
    if (key in STRUCTURAL_KEYWORDS):
      return True
  else:                                # if modality is not structural (i.e. bold)
    if (key in BOLD_KEYWORDS):
      return True

  errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
           f"Keyword '{key}' is not a valid {modality} keyword.")
  raise ValueError(errMsg)


def validate_query_params (modality, query_params, prog_name=''):
  """
  For each query parameter: validate the keyword by modality, validate
  the comparison operator, and then clean the comparison value. Concatenate
  the cleaned and validated comparison operator and value and re-store it
  back into the query_params dictionary under the validated key.
  Raises ValueError if any validation step fails.
  """
  for key, value in query_params:
    validate_keyword(modality, key, prog_name)
    comparison = parse_value(value, prog_name)
    query_params[key] = comparison
