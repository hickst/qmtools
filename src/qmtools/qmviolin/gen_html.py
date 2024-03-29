# Methods to generate an HTML report to display IMQ violin plots comparing two MRIQC datasets.
#   Written by: Tom Hicks and Dianne Patterson. 9/13/2021.
#   Last Modified: Major refactor.
#
from jinja2 import Template

from qmtools.iqms_doc import IQMS_DOC_DICT
from qmtools.mriqc_keywords import (BOLD_HI_GOOD_COLUMNS, BOLD_LO_GOOD_COLUMNS,
                                    STRUCT_HI_GOOD_COLUMNS, STRUCT_LO_GOOD_COLUMNS)


# the Jinja template string for generating the HTML page:
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
    <title>QMViolin {{modality}}</title>
  </head>

  <body>
    <div>
      <h1>Comparison of MRIQC IQM datasets (<span class="modality">{{modality}}</span>)</h1>

{% for iqm in iqms.values() %}
      <div id="{{iqm.name}}" class="iqm">
        <table id="iqms" width="100%">
          <tr class="iqm_row">
            <td class="legend">
              <img class="legend_img" src="{{iqm.legend_path}}"></img><br/>
              <p class="hi_lo_text">{{iqm.hi_lo_text}}</p>
            <td>
            <td class="plot">
              <img id="" class="vplot" src="{{iqm.plot_path}}"></img><br/>
              <p class="descrip">{{iqm.description}}</p>
            <td>
          </tr>
        </table>
      </div>
{% endfor %}

    </div>
  </body>
"""


def gen_html (modality, plot_info, docs=IQMS_DOC_DICT):
  """
  From the given plot information and modality, assemble information about the IQMs
  (such as their names, descriptions, hi/lo status) and then render each IQM plot
  and its information into an HTML page (a single string), which is returned.
  """
  iqms = dict()                        # dictionary of IQM properties

  for iqm, plot_path in plot_info.items():
    iqms[iqm] = {'name': iqm, 'plot_path': plot_path}

  for iqm in plot_info:
    description = docs.get(iqm)
    if (description):
      iqms[iqm]['description'] = description
    iqms[iqm]['legend_path'] = get_legend_path(iqm)
    iqms[iqm]['hi_lo_text'] = get_hi_lo_text(iqm)

  # generate the HTML using the Jinja template
  template = Template(PAGE_TEMPLATE)
  html_text = template.render(iqms=iqms, modality=modality)
  return html_text


def get_hi_lo_text (iqm):
  """
  For the given IQM, return a string identifying whether low or high values
  (or neither) are better for the metric.
  """
  if (iqm in BOLD_LO_GOOD_COLUMNS or (iqm in STRUCT_LO_GOOD_COLUMNS)):
    return 'Low values are better'
  elif (iqm in BOLD_HI_GOOD_COLUMNS or (iqm in STRUCT_HI_GOOD_COLUMNS)):
    return 'High values are better'
  else:
    return ''


def get_legend_path (iqm):
  """
  For the given IQM, return an arrow image which shows that low or high values
  (or neither) are better for the metric.
  """
  if (iqm in BOLD_LO_GOOD_COLUMNS or (iqm in STRUCT_LO_GOOD_COLUMNS)):
    return 'down_arrow.png'
  elif (iqm in BOLD_HI_GOOD_COLUMNS or (iqm in STRUCT_HI_GOOD_COLUMNS)):
    return 'up_arrow.png'
  else:
    return 'no_legend.png'
