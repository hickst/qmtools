import io
import numpy as np
import pandas as pd

from matplotlib import cm
from matplotlib import pyplot as plt

# from qmview import qmview as qmv
import qmview.qmview as qmview

TURNIP8_COLORMAP = cm.get_cmap('PiYG', 8)
TURNIP8_COLORMAP_R = cm.get_cmap('PiYG_r', 8)


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


def load_tsv (tsv_path):
  return pd.read_csv(tsv_path, sep='\t')


def write_table_to_html (styler, filepath):
  """
  Render the given pandas.io.formats.style.Styler object as
  HTML and write the HTML to the given filepath.
  """
  with open(filepath, "w") as outfyl:
    outfyl.writelines(styler.render())


qm_df = load_tsv('test/resources/gtest.tsv')
norm_df = qmview.normalize_to_zscores(qm_df)
# the following returns a pandas.io.formats.style.Styler object
styler = norm_df.style.background_gradient(cmap=TURNIP8_COLORMAP, axis=None, vmin=-4.0, vmax=4.0)
write_table_to_html(styler, "/tmp/table.html")

# plt.show()

# qmview.colorize_by_std_deviations(norm_df)
# print(norm_df)

# fig, axes = plt.subplots(2, 1)
# pos_ax, neg_ax = axes
# make_legend_on_axis(pos_ax, TURNIP8_COLORMAP)
# make_legend_on_axis(neg_ax, TURNIP8_COLORMAP_R)
