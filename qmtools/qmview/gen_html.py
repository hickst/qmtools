# Methods to generate an HTML report to display a table of Z-score normalized IQM data.
#   Written by: Tom Hicks and Dianne Patterson. 10/1/2021.
#   Last Modified: Embed CSS in generated HTML.
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
    <title>QMTraffic {{modality}}</title>
    <style>
      body {
        background-color:#ffffff;
        color:black;
        font-family: Arial, Helvetica, sans-serif;
        font-size:76%;
        margin:0;
      }
      h1 {
        margin-left: 20px;
      }
      img.legend {
        width: 500px;
        height: 100px;
        margin-top: 30px;
        margin-bottom: 40px;
        margin-left: 100px;
        border-style: none;
      }
      iframe.table {
        border-style: none;
        height: 750px;
        width: 100%;
        margin-top: 0;
        margin-bottom: 40px;
        margin-left: 40px;
      }
      .modality {
        color: #9f009f
      }
    </style>
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
