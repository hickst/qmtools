# Only these modalities are available for query
ALLOWED_MODALITIES = ['bold', 't1w', 't2w']

# Name of a subdirectory to hold fetched query results
FETCHED_DIR = 'fetched'

# Name of a subdirectory containing MRIQC group results used as inputs.
INPUTS_DIR = 'inputs'

# Name of the subdirectory which holds output reports.
REPORTS_DIR = 'reports'

# Symbolic exit codes for various error exit scenarios
INPUT_FILE_EXIT_CODE = 10
OUTPUT_FILE_EXIT_CODE = 11

FETCHED_DIR_EXIT_CODE = 20
INPUTS_DIR_EXIT_CODE = 21
REPORTS_DIR_EXIT_CODE = 22

NUM_RECS_EXIT_CODE = 30
