# To convert an mriqc output file to normalized scores for representation in
# a traffic-light table.
#   Written by: Tom Hicks and Dianne Patterson.
#   Last Modified: Update for move of write_figure_to_file to QM utils.
#
import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from matplotlib import cm
from matplotlib import pyplot as plt

from config.mriqc_keywords import (STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS,
                                   BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS)
from qmtools import BIDS_DATA_EXT, PLOT_EXT, REPORTS_DIR, REPORTS_EXT, STRUCTURAL_MODALITIES
import qmtools.qm_utils as qmu

# create our own small color maps for positive good and positive bad
TURNIP8_COLORMAP = cm.get_cmap('PiYG', 8)
TURNIP8_COLORMAP_R = cm.get_cmap('PiYG_r', 8)


def make_traffic_light_table (tsvfile, modality, dirpath=REPORTS_DIR):
  """
  Given a TSV file of QM metrics, generate and save two traffic light HTML
  tables: one for positive values better and another for negative values better.
  The modality string specifies which columns will be selected and must be
  one of: 'T1w', 'T2w', or 'bold'.
  """
  modality = qmu.validate_modality(modality)
  qm_df = qmu.load_tsv(tsvfile)
  (pos_good_df, pos_bad_df) = pos_neg_split(qm_df, modality)
  gen_traffic_light_table(pos_good_df, True, f"pos_good_{modality}", dirpath)
  gen_traffic_light_table(pos_bad_df, False, f"pos_bad_{modality}", dirpath)


def gen_traffic_light_table (qm_df, iam_hi_good, outfilename, dirpath=REPORTS_DIR):
  """
  Normalize to Z-scores, stylize, and write the given QM dataframe
  as an HTML table, in the named output file.
  """
  norm_df = normalize_to_zscores(qm_df)
  write_table_to_tsv(norm_df, outfilename, dirpath)
  which_cmap = TURNIP8_COLORMAP if iam_hi_good else TURNIP8_COLORMAP_R
  styler = style_table_by_std_deviations(norm_df, cmap=which_cmap)
  write_table_to_html(styler, outfilename, dirpath)


def make_legends (dirpath=REPORTS_DIR):
  """
  Generate and save a positive-good legend and a positive-bad legend
  as plot files (default: PNG) in the reports directory.
  """
  make_a_legend(f"pos_good{PLOT_EXT}", TURNIP8_COLORMAP, dirpath)
  make_a_legend(f"pos_bad{PLOT_EXT}", TURNIP8_COLORMAP_R, dirpath)


def make_a_legend (filename, colormap, dirpath=REPORTS_DIR):
  """
  Make a legend with the given colormap and save it with the given filename
  in the optionally specified reports directory.
  """
  fig = plt.figure()
  ax = fig.add_axes([0, 0, 1, 1])
  make_legend_on_axis(ax, colormap)
  qmu.write_figure_to_file(fig, filename, dirpath)


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
  KEEP_LIST = ['bids_name']
  if (modality in STRUCTURAL_MODALITIES):
    pos_good_df = qm_df[(KEEP_LIST + STRUCT_HI_GOOD_COLUMNS)]
    pos_bad_df = qm_df[(KEEP_LIST + STRUCT_LO_GOOD_COLUMNS)]
  else:
    pos_good_df = qm_df[(KEEP_LIST + BOLD_HI_GOOD_COLUMNS)]
    pos_bad_df = qm_df[(KEEP_LIST + BOLD_LO_GOOD_COLUMNS)]

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


def write_table_to_tsv (norm_df, filename, dirpath=REPORTS_DIR):
  """
  Write the given normalized dataframe into the named TSV file
  in the optionally specified directory.
  """
  filepath = os.path.join(dirpath, f"{filename}{BIDS_DATA_EXT}")
  norm_df.to_csv(filepath, index=False, sep='\t')


def write_table_to_html (styler, filename, dirpath=REPORTS_DIR):
  """
  Render the given pandas.io.formats.style.Styler object as
  HTML and write the HTML to the given filepath.
  """
  filepath = os.path.join(dirpath, f"{filename}{REPORTS_EXT}")
  with open(filepath, "w") as outfyl:
    outfyl.writelines(styler.render())
