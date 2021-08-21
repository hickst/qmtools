#
# Module containing sets of MRIQC schema keywords; to be used for validation.
#   Written by: Tom Hicks. 8/19/2021.
#   Last Modified: Enter first few values to enable tests.
#
BIDS_KEYWORDS = set([
  'bids_meta.subject_id', 'bids_meta.session_id', 'bids_meta.run_id'
])

BOLD_KEYWORDS = set([
  'aor', 'aqi', 'dummy_trs', 'dvars_nstd', 'dvars_std', 'dvars_vstd'
])

STRUCTURAL_KEYWORDS = set([
  'cjv', 'cnr', 'efc', 'fber', 'fwhm_avg', 'fwhm_x', 'fwhm_y', 'fwhm_z'
])