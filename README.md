# QMTools - Quality Metrics Tools

This is a public code repository of the [Translational Bioimaging Resource–MRI](https://research.arizona.edu/facilities/core-facilities/translational-bioimaging-resource-mri) core group at the [University of Arizona](https://www.arizona.edu/).

**Authors**: [Tom Hicks](https://github.com/hickst) and [Dianne Patterson](https://github.com/dkp)

**About**: This project provides several programs to visualize, compare, and review the image quality metrics (IQMs) produced by the [MRIQC program](https://github.com/poldracklab/mriqc). MRIQC extracts no-reference IQMs from structural (T1w and T2w) and functional (BOLD) MRI data.

## Using QMTools via Docker

The easiest way to use the QMTools is via the publicly available [Docker container](https://hub.docker.com/repository/docker/hickst/qmtools). With this approach, the QMTools, located in the Docker container, are called by auxiliary Bash scripts to process data from input and output directories which the scripts make available to the container. Scripts, examples, and documentation which support and simplify this process are available in the [QMTools Support project on GitHub](https://github.com/hickst/qmtools-support). Since this approach requires only **Docker**, **git** and the **bash shell** to be installed on your local computer, it has a minimal "footprint".

***Note**: For documentation on the individual tools and how to use the tools via Docker, please see the [QMTools Support project](https://github.com/hickst/qmtools-support).*

## Installing with Conda

You can also install the main QMTools project (*not the Support project*) locally on your computer and run the tools from there. Using [Miniconda](https://docs.conda.io/en/latest/miniconda.html), you can easily set up an isolated environment to run the QMTools without interfering with other local software.

## Installing with a Python Virtual Environment

More knowledgable users can install the main QMTools project (*not the Support project*) locally using a Python virtual environment.

## Related Links

The source code for the [QMTools Support project](https://github.com/hickst/qmtools-support) in GitHub.

The QMTools project was inspired by a 2019 Neurohackademy project available [here](https://github.com/elizabethbeard/mriqception).

The [Swagger UI for the MRIQC web API](https://mriqc.nimh.nih.gov). Scroll down to the `Models` section, which documents the database schema (structure and field names) that can be queried with **QMFetcher**.

The source code for the [MRIQC web API](https://github.com/nipreps/mriqcwebapi), which provides the API that **QMFetcher** uses to query the MRIQC database.

Some old [Discussions and Jupyter notebooks](https://www.kaggle.com/chrisfilo/mriqc/code) which utilize the same MRIQC web API that this project uses.

## References

- Esteban O, Blair RW, Nielson DM, Varada JC, Marrett S, Thomas AG et al. (2019). Crowdsourced MRI quality metrics and expert quality annotations for training of humans and machines. Sci Data 6: 30.

- Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ (2017). MRIQC: Advancing the automatic prediction of image quality in MRI from unseen sites. PLoS ONE 12: 9.

## License

This software is licensed under Apache License Version 2.0.

Copyright (c) The University of Arizona, 2021. All rights reserved.
