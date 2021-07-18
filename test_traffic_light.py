from matplotlib import cm
from matplotlib import pyplot as plt

import qmview.qmview as qmv
from qmview.qmview import TURNIP8_COLORMAP, TURNIP8_COLORMAP_R

# qm_df = qmv.load_tsv('test/resources/group_bold.tsv')
qm_df = qmv.load_tsv('test/resources/gtest.tsv')
norm_df = qmv.normalize_to_zscores(qm_df)
styler = qmv.colorize_by_std_deviations(norm_df)
qmv.write_table_to_html(styler, "/tmp/table.html")

# fig, axes = plt.subplots(2, 1)
# pos_ax, neg_ax = axes
# qmv.make_legend_on_axis(pos_ax, TURNIP8_COLORMAP)
# qmv.make_legend_on_axis(neg_ax, TURNIP8_COLORMAP_R)
# plt.show()
