from matplotlib import cm
from matplotlib import pyplot as plt

import qmview.traffic_light as traf
from qmview.traffic_light import TURNIP8_COLORMAP, TURNIP8_COLORMAP_R

# qm_df = traf.load_tsv('test/resources/group_bold.tsv')
qm_df = traf.load_tsv('test/resources/gtest.tsv')
norm_df = traf.normalize_to_zscores(qm_df)
styler = traf.colorize_by_std_deviations(norm_df)
traf.write_table_to_html(styler, "/tmp/table.html")

# fig, axes = plt.subplots(2, 1)
# pos_ax, neg_ax = axes
# traf.make_legend_on_axis(pos_ax, TURNIP8_COLORMAP)
# traf.make_legend_on_axis(neg_ax, TURNIP8_COLORMAP_R)
# plt.show()
