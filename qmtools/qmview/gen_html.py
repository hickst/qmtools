# Methods to generate an HTML report to display a table of Z-score normalized IQM data.
#   Written by: Tom Hicks and Dianne Patterson. 10/1/2021.
#   Last Modified: Initial creation.
#
from jinja2 import Template

# directory containing style and/or script files used by the generated HTML:
AUX_DIR_PATH = 'qmtools/qmview/static'

# the Jinja template string for generating the HTML page:
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Image Quality Metrics Table Viewer">
    <link rel="stylesheet" href="traffic.css" type="text/css">
    <title>QMTraffic {{modality}}</title>
  </head>

  <body>
    <div>
      <h1>Table of <span class="modality">{{modality}}</span> Z-score Normalized IQMs [Positive values are better]</h1>
      <img id="pos_good_lgnd" class="legend"
           src="pos_good.png"></img><br/>
      <iframe id="pos_good_{{modality}}_tbl" class="table"
              src="pos_good_{{modality}}.html"></iframe><br/>
    </div>
    <div>
      <h1>Table of <span class="modality">{{modality}}</span> Z-score Normalized IQMs [Negative values are better]</h1>
      <img id="pos_bad_lgnd" class="legend"
           src="pos_bad.png"></img><br/>
      <iframe id="pos_bad_{{modality}}_tbl" class="table"
              src="pos_bad_{{modality}}.html"></iframe><br/>
      </div>
    </div>
  </body>
"""


def gen_html (modality):
  """
  Generate HTML for displaying both Z-score normalized tables.
  Returns an HTML page (a single string).
  """
  # generate the HTML using the Jinja template
  template = Template(PAGE_TEMPLATE)
  html_text = template.render(modality=modality)
  return html_text
