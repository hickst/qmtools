# Author: Tom Hicks and Dianne Patterson.
# Purpose: To convert an mriqc output file to normalized scores for
#          representation in a traffic-light table.
# Last Modified: Move allowed modalities constant.

import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from matplotlib import cm
from matplotlib import pyplot as plt

from config.settings import REPORTS_DIR
from qmtools import ALLOWED_MODALITIES

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


def make_traffic_light_table (tsvfile, modality, dirpath=REPORTS_DIR):
  """
  Given a TSV file of QM metrics, generate and save two traffic light HTML
  tables: one for positive values better and another for negative values better.
  The modality string specifies which columns will be selected and must be
  one of: 'T1w', 'T2w', or 'bold'.
  """
  modality = validate_modality(modality)
  qm_df = load_tsv(tsvfile)
  (pos_good_df, pos_bad_df) = pos_neg_split(qm_df, modality)
  gen_traffic_light_table(pos_good_df, POS_GOOD_FLAG, f"pos_good_{modality}", dirpath)
  gen_traffic_light_table(pos_bad_df, POS_BAD_FLAG, f"pos_bad_{modality}", dirpath)


def gen_traffic_light_table (qm_df, iam_pos_good, outfilename, dirpath=REPORTS_DIR):
  """
  Normalize to Z-scores, stylize, and write the given QM dataframe
  as an HTML table, in the named output file.
  """
  norm_df = normalize_to_zscores(qm_df)
  write_table_to_tsv(norm_df, outfilename, dirpath)
  which_cmap = TURNIP8_COLORMAP if iam_pos_good else TURNIP8_COLORMAP_R
  styler = style_table_by_std_deviations(norm_df, cmap=which_cmap)
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


def style_table_by_std_deviations (norm_df, cmap=TURNIP8_COLORMAP):
  """
  Set the cell backgrounds of the given z-score normalized dataframe
  using the given or default colormap.
  Returns a pandas.io.formats.style.Styler object.
  """
  clean_font = {
    'selector': 'table, table, th, td',
    'props': [
      ('font-family', 'Arial, Helvetica, sans-serif'),
      ('padding', '4px 6px')
    ]
  }
  styler = norm_df.style.background_gradient(cmap=cmap, axis=None, vmin=-4.0, vmax=4.0)
  styler.set_table_styles([clean_font], overwrite=False)
  return styler


def validate_modality (modality):
  """
   Check the validity of the given modality string which must be one
   of the elements of the ALLOWED_MODALITIES list.
   Returns the canonicalized modality string or raises ValueError if
   given an invalid modality string.
  """
  mode = modality.lower()
  if (mode in ALLOWED_MODALITIES):
    return mode
  raise ValueError(f"Modality argument must be one of: {ALLOWED_MODALITIES}")


def write_figure_to_file (fig, filename, dirpath=REPORTS_DIR):
  """
  Write the given matplotlib figure to a file with the given filename
  in the reports directory. The output format is determined by the file
  extension (.png is the default).
  """
  filepath = os.path.join(dirpath, filename)
  fig.savefig(filepath, bbox_inches='tight')    # .png is default


def write_table_to_tsv (norm_df, filename, dirpath=REPORTS_DIR):
  """
  Write the given normalized dataframe into the named TSV file
  in the optionally specified directory.
  """
  filepath = os.path.join(dirpath, f"{filename}.tsv")
  norm_df.to_csv(filepath, index=False, sep='\t')


def write_table_to_html (styler, filename, dirpath=REPORTS_DIR):
  """
  Render the given pandas.io.formats.style.Styler object as
  HTML and write the HTML to the given filepath.
  """
  filepath = os.path.join(dirpath, f"{filename}.html")
  with open(filepath, "w") as outfyl:
    outfyl.writelines(styler.render())
