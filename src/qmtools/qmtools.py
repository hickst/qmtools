# Top-level landing page for the QMTools suite.
#
#   Written by: Tom Hicks and Dianne Patterson.
#   Last Modified: initial creation.
#
from qmtools.version import VERSION

def main (argv=None):

  print(f"\nWelcome to the QMTools Suite. This is version {VERSION}")

  print("""
Currently, QMTools contains 3 tools:

  qmfetcher - https://github.com/hickst/qmtools-support/blob/main/docs/Fetcher.md

      Queries the MRIQC database server to fetch image quality metrics (IQMs) for images
      previously processed by neuroimaging groups all over the world.


  qmtraffic - https://github.com/hickst/qmtools-support/blob/main/docs/TrafficLight.md

      TrafficLight normalizes a set of MRIQC image quality metrics and creates a tabular HTML report,
      visualizing how much each image's metrics deviate from the mean for all the images in that set.


  qmviolin - https://github.com/hickst/qmtools-support/blob/main/docs/Violin.md

      Violin compares two sets of MRIQC image quality metrics and creates an HTML report,
      using Violin plots to visualize how the two groups compare for each IQM.

We recommend using these tools through the QMTools Support project (https://github.com/hickst/qmtools-support)
which provides sample data, examples, and scripts for running the tools using Docker or Apptainer.

  """)



if __name__ == "__main__":
  main()
