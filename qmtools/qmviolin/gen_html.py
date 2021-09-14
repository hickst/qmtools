# Methods to generate an HTML report to display IMQ violin plots comparing two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/13/2021.
#   Last Modified: Initial creation.
#
from jinja2 import Template

from config.iqms_doc import IQMS_DOC_DICT
from config.mriqc_keywords import (BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS,
                                   STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS)
# import qmtools.qm_utils as qmu


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="IQM Violin Plot Comparisons">
    <link rel="stylesheet" href="main.css" type="text/css">
    <title>QMViolin {{targs.modality}}</title>
  </head>

  <body>
    <div>
      <h1>Comparison of MRIQC IQM datasets ({{targs.modality}} modality)</h1>

      {% for iqm in targs.values() %}
      <div id="{{iqm.name}} class="iqm">
        <table id="iqms" width="500px">
          <tr class="iqm_row" valign="middle">
            <td class="legend" width="60px">
              <img id="" class="legend_img" src="{{iqm.legend_path}}"></img><br/>
            <td>
            <td class="plot">
              <img id="" class="vplot" src="{{iqm.plot_path}}"></img><br/>
              <p>{{iqm.description}}</p>
            <td>
          </tr>
        </table>
      </div>
      {% endfor %}

    </div>
  </body>
"""


def gen_html (modality, args, plot_info, docs=IQMS_DOC_DICT):
  targs = dict()

  for iqm, plot_path in plot_info.items():
    targs[iqm] = {'name': iqm, 'plot_path': plot_path}

  for iqm in plot_info:
    description = docs.get(iqm)
    if (description):
      targs[iqm]['description'] = description
    targs[iqm]['legend_path'] = get_legend_path(iqm)

  template = Template(PAGE_TEMPLATE)
  html_text = template.render(targs=targs)
  return html_text


def get_legend_path (iqm):
  if (iqm in BOLD_LO_GOOD_COLUMNS or (iqm in STRUCT_LO_GOOD_COLUMNS)):
    #  return LO_GOOD_LEGEND_PATH
    return 'LO_GOOD_LEGEND_PATH'
  elif (iqm in BOLD_HI_GOOD_COLUMNS or (iqm in STRUCT_HI_GOOD_COLUMNS)):
    # return HI_GOOD_LEGEND_PATH
    return 'HI_GOOD_LEGEND_PATH'
  else:
    # return NO_LEGEND_PATH
    return 'NO_LEGEND_PATH'
