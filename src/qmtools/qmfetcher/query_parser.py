#
# Module with methods to read and parse a query parameters file.
#   Written by: Tom Hicks. 8/17/2021.
#   Last Modified: Major refactor.
#
import sys

from qmtools import STRUCTURAL_MODALITIES
from qmtools.mriqc_keywords import BOLD_KEYWORDS, STRUCTURAL_KEYWORDS


def parse_query_from_file (modality, query_file, prog_name=''):
  """
  Load and validate a set of query parameters from the given query parameters file.
  Return a dictionary of valid query parameters or raise exceptions.
  """
  criteria = load_criteria_from_file(query_file, prog_name)
  query_params = parse_criteria(modality, criteria, prog_name)
  return query_params


def is_criteria_line (line):
  "Strip the given line and return it if it is not empty and not a comment, else return None."
  aline = line.strip()
  if ((not aline) or aline.startswith('#')):  # if empty line or comment line
    return None
  else:
    return aline


def keep (fn, collection):
  """
  Returns a list of the non-None results of (fn item). Note, this means False
  return values will be included. The function should be free of side-effects.
  """
  for val in collection:
    res = fn(val)
    if (res is not None):
      yield res


def load_criteria_from_file (query_file, prog_name=''):
  """
  Load query criteria lines from the given query parameters file.
  Returns a list of non-blank, non-comment lines (i.e., lines assumed to be criteria lines).
  """
  sys.tracebacklimit = 0
  try:
    with open(query_file) as qp:
      return list(keep(is_criteria_line, qp.readlines()))

  except FileNotFoundError as fnf:
    errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
      f"Query parameters file '{query_file}' not found or not readable.")
    raise FileNotFoundError(errMsg)


def parse_criteria (modality, criteria, prog_name=''):
  """
  For each criterion of the query, parse the criterion string into a keyword and a
  comparison part; composed of a valid operator and the value to query for.
  Note that the criteria strings are assumed to have been already stripped (upon reading).
  Return a (possibly empty) list of lists of keywords and comparison strings.
  """
  query_params = []
  for crit in criteria:
    key, value = parse_key_and_value(modality, crit, prog_name)
    comparison = parse_value(value, prog_name)
    query_params.append([key, comparison])
  return query_params


def parse_key_and_value (modality, crit, prog_name):
  """
  Find and validate the keyword which begins the given criterion string.
  Return a tuple containing the keyword and the trimmed, rest of the criterion string.
  May throw a ValueError if the keyword found is not valid.
  """
  sp_pos = crit.find(' ')
  if (sp_pos < 0):
    errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
      f"Spaces must separate the parts of a query parameter line: '{crit}'")
    raise ValueError(errMsg)
  else:                                # must be at least one non-space character
    keyword = (crit[:sp_pos]).strip()
    validate_keyword(modality, keyword, prog_name)

  rest = (crit[sp_pos:]).strip()
  return (keyword, rest)


def parse_value (val, prog_name=''):
  """
  Separate and clean the operator and the value from the given value string.
  Returns the operator and the value reconcatenated, with whitespace stripped.
  """
  ops1 = set(['<', '>'])
  ops2 = set(['==', '<=', '>=', '!='])
  opsall = ops1.union(ops2)

  ch1 = val[:1]
  ch2 = val[:2]
  if (ch2 in ops2):
    value = val[2:].strip()
    if (value):
      return f"{ch2}{value}"
  elif (ch1 in ops1):
    value = val[1:].strip()
    if (value):
      return f"{ch1}{value}"
  else:
    errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
             f"The comparison operator must be one of {opsall}")
    raise ValueError(errMsg)
  # if we reach here there was no non-empty value
  errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
            "The value to be compared must not be empty")
  raise ValueError(errMsg)


def validate_keyword (modality, key, prog_name=''):
  """
  Compare the given keyword to known sets of modality-specific keywords and
  raise a ValueError if the keyword is unknown or not valid for the modality.
  """
  if (modality in STRUCTURAL_MODALITIES):
    if (key in STRUCTURAL_KEYWORDS):
      return True
  else:                                # if modality is not structural (i.e. bold)
    if (key in BOLD_KEYWORDS):
      return True

  errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
           f"Keyword '{key}' is not a valid {modality} keyword.")
  raise ValueError(errMsg)
