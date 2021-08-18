#
# Module with methods to read and parse a query parameters file.
#   Written by: Tom Hicks. 8/17/2021.
#   Last Modified: Initial creation
#
import configparser as cp


def parse_query_from_file (query_file, prog_name=''):
    """
    Load and parse a set of query parameters from the given query parameters file.
    """
    try:
      config = cp.ConfigParser(strict=False, empty_lines_in_values=False)
      config.optionxform = lambda option: option
      config.read_file(open(query_file))
    except FileNotFoundError:
      errMsg = "({}): ERROR: {} Exiting...".format(prog_name,
        "Query parameters file '{query_file}' not found or not readable.")
      raise FileNotFoundError(errMsg)
    except cp.MissingSectionHeaderError:
      errMsg = "A 'parameters' section header must be included in the query parameters file '{query_file}'."
      raise ValueError(errMsg)

    try:
      qparams = config['parameters']
    except KeyError:
      errMsg = "No section named 'parameters' found in query parameters file '{query_file}'."
      raise ValueError(errMsg)

    return dict(qparams)
