# Only these modalities are available for query
ALLOWED_MODALITIES = ['bold', 'T1w', 'T2w']
STRUCTURAL_MODALITIES = ['T1w', 'T2w']

# Name of a subdirectory to hold fetched query results
FETCHED_DIR = 'fetched'

# Name of a subdirectory containing MRIQC group results used as inputs.
INPUTS_DIR = 'inputs'

# Name of the subdirectory which holds output reports.
REPORTS_DIR = 'reports'

# File extensions for report files and BIDS-compliant data files.
BIDS_DATA_EXT = '.tsv'
REPORTS_EXT = '.html'

# Symbolic exit codes for various error exit scenarios
INPUT_FILE_EXIT_CODE = 10
OUTPUT_FILE_EXIT_CODE = 11
QUERY_FILE_EXIT_CODE = 12

FETCHED_DIR_EXIT_CODE = 20
INPUTS_DIR_EXIT_CODE = 21
REPORTS_DIR_EXIT_CODE = 22

NUM_RECS_EXIT_CODE = 30
