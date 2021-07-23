# Author: Tom Hicks and Dianne Patterson.
# Purpose: To convert an mriqc output file to normalized scores for
#          representation in a traffic-light table.
# Last Modified: Document call to generate HTML table. Remove dummy trs column.

import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from matplotlib import cm
from matplotlib import pyplot as plt

from config.settings import REPORTS_DIR

# Constants to "mark" a dataframe as having positive good values or positive bad values
POS_GOOD_FLAG = True
POS_BAD_FLAG = False

# create our own small color maps for positive good and positive bad
TURNIP8_COLORMAP = cm.get_cmap('PiYG', 8)
TURNIP8_COLORMAP_R = cm.get_cmap('PiYG_r', 8)

# structural columns whose values are better when positive, or negative
STRUCTURAL_POS_GOOD_COLUMNS = [
  'bids_name', 'cnr', 'snr_csf', 'snr_gm', 'snr_total', 'snr_wm',
  'snrd_csf', 'snrd_gm', 'snrd_total','snrd_wm', 'tpm_overlap_csf',
   'tpm_overlap_gm', 'tpm_overlap_wm'
  ]
STRUCTURAL_POS_BAD_COLUMNS = [
  'bids_name', 'cjv', 'rpve_csf', 'rpve_gm', 'rpve_wm', 'fwhm_x',
  'fwhm_y', 'fwhm_z', 'inu_med', 'inu_range', 'qi_1', 'qi_2'
  ]

# functional columns whose values are better when positive, or negative
BOLD_POS_GOOD_COLUMNS = ['bids_name', 'fber', 'snr', 'tsnr']
BOLD_POS_BAD_COLUMNS = [
  'bids_name', 'aor', 'aqi', 'dvars_nstd', 'dvars_std', 'dvars_vstd',
  'efc', 'fd_mean', 'fd_num', 'fd_perc', 'fwhm_avg', 'gcor', 'gsr_x', 'gsr_y'
]


def colorize_by_std_deviations (norm_df, cmap=TURNIP8_COLORMAP):
  """
  Set the cell backgrounds of the given z-score normalized dataframe
  using the given or default colormap.
  Returns a pandas.io.formats.style.Styler object.
  """
  return norm_df.style.background_gradient(cmap=cmap, axis=None, vmin=-4.0, vmax=4.0)


def gen_traffic_light_table (qm_df, iam_pos_good, outfilename, dirpath=REPORTS_DIR):
  """
  Normalize to Z-scores, stylize, and write the given QM dataframe
  as an HTML table, in the named output file.
  """
  norm_df = normalize_to_zscores(qm_df)
  which_cmap = TURNIP8_COLORMAP if iam_pos_good else TURNIP8_COLORMAP_R
  styler = colorize_by_std_deviations(norm_df, cmap=which_cmap)
  write_table_to_html(styler, outfilename, dirpath)


def load_tsv (tsv_path):
  "Read the specified TSV file and return a Pandas dataframe from it."
  return pd.read_csv(tsv_path, sep='\t')


def make_legends (dirpath=REPORTS_DIR):
  """
  Generate and save a positive-good legend and a positive-bad legend
  as .png files in the reports directory.
  """
  make_a_legend("pos_good.png", TURNIP8_COLORMAP, dirpath)
  make_a_legend("pos_bad.png", TURNIP8_COLORMAP_R, dirpath)


def make_a_legend (filename, colormap, dirpath=REPORTS_DIR):
  """
  Make a legend with the given colormap and save it with the given filename
  in the optionally specified reports directory.
  """
  fig = plt.figure()
  ax = fig.add_axes([0, 0, 1, 1])
  make_legend_on_axis(ax, colormap)
  write_figure_to_file(fig, filename, dirpath)


def make_legend_on_axis (ax, cmap):
  """
  Draws a legend on the given axis using the given colormap.
  """
  box_rng = np.arange(8)
  ticklabels = ['-4.0', '-3.0', '-2.0', '-1.0', '1.0', '2.0', '3.0', '4.0']
  label_title = 'Green Values are Better'
  im = ax.imshow([box_rng], cmap)
  ax.set_xticks(box_rng)
  ax.set_xticklabels(ticklabels)
  ax.set_yticks([])
  ax.set_yticklabels([])
  ax.set_title(label_title)


def make_traffic_light_table (tsvfile, modality, dirpath=REPORTS_DIR):
  """
  Given a TSV file of QM metrics, generate and save two traffic light HTML
  tables: one for positive values better and another for negative values better.
  The modality string specifies which columns will be selected and must be
  one of: 'T1w', 'T2w', or 'bold'.
  """
  qm_df = load_tsv(tsvfile)
  (pos_good_df, pos_bad_df) = pos_neg_split(qm_df, modality)
  gen_traffic_light_table(pos_good_df, POS_GOOD_FLAG, f"pos_good_{modality}.html", dirpath)
  gen_traffic_light_table(pos_bad_df, POS_BAD_FLAG, f"pos_bad_{modality}.html", dirpath)


def normalize_to_zscores (qm_df):
  """
  Normalize every non-string column of the given QM dataframe by Z-score.
  Returns the normalized dataframe.
  """
  bids_names = qm_df['bids_name']
  z_df = qm_df.iloc[:, 1:].apply(stats.zscore)
  return pd.concat([bids_names, z_df], axis=1)


def pos_neg_split (qm_df, modality):
  """
  Split the given QM dataframe into two: one where positive values
  are better and the other where negative values are better.
  Return a tuple of the positive good and positive bad dataframes.
  """
  if (modality.lower() in ['t1w', 't2w', 't1', 't2']):
    pos_good_df = qm_df[STRUCTURAL_POS_GOOD_COLUMNS]
    pos_bad_df = qm_df[STRUCTURAL_POS_BAD_COLUMNS]
  else:
    pos_good_df = qm_df[BOLD_POS_GOOD_COLUMNS]
    pos_bad_df = qm_df[BOLD_POS_BAD_COLUMNS]

  return (pos_good_df, pos_bad_df)


def write_figure_to_file (fig, filename, dirpath=REPORTS_DIR):
  """
  Write the given matplotlib figure to a file with the given filename
  in the reports directory. The output format is determined by the file
  extension (.png is the default).
  """
  filepath = os.path.join(dirpath, filename)
  fig.savefig(filepath, bbox_inches='tight')    # .png is default


def write_table_to_html (styler, filename, dirpath=REPORTS_DIR):
  """
  Render the given pandas.io.formats.style.Styler object as
  HTML and write the HTML to the given filepath.
  """
  filepath = os.path.join(dirpath, filename)
  with open(filepath, "w") as outfyl:
    outfyl.writelines(styler.render())
