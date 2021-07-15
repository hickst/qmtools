**Project**: Test the mriqception package
**Author**: Dianne Patterson,Ph.D.
**Date**: July 8, 2021

# Relevant Links and Reference

- [mriqc web api](https://mriqc.nimh.nih.gov/)
- [Swagger UI for WEB API](https://mriqc.nimh.nih.gov/#/bold/get_bold)
  - Useful for the models it lists with the field names
- [mriqception github](https://github.com/elizabethbeard/mriqception)
- [Jupyter examples](https://www.kaggle.com/chrisfilo/mriqc/kernels)
- Esteban O, Blair RW, Nielson DM, Varada JC, Marrett S, Thomas AG et al. (2019) Crowdsourced MRI quality metrics and expert quality annotations for training of humans and machines. Sci Data 6: 30.

# Set up an environment

- In the years since the project was originally created, plotly and ipywidgets have become incompatible UNLESS you choose very particular ways to install them. The requirements for install are met by the below incantations.
- See **/Volumes/Main/Working/mriqception_test**

`conda create -n mriqception pandas`   
`cact mriqception`   
`conda install -c plotly plotly=5.1.0`   
`conda install "jupyterlab>=3" "ipywidgets>=7.6"`   
`conda install seaborn`   
(seaborn is used in the data_viz_example.ipynb)  

- See /Volumes/Main/Working/mriqception_test

- Check that jupyterlab-plotly 5.1.0 is installed:  
`jupyter labextension list`

# Running the Tool
- Get group_bold.tsv and/or group_T1w.tsv
- `jupyter-lab`
- The notebook now works. Copy it to save it:   
`cp -p Presentation_Notebook.ipynb ~/temp/MRIQception-canned.ipynb`

 
# Data Dump cleanup (if queries don't work)

- Done:
A dump of the database containing a LOT of records (62K for the bold), is available on [FigShare](https://figshare.com/articles/dataset/MRIQC_WebAPI_-_Database_dump/7097879/4). The curated sets have checksums have been matched and data cleaned as per: https://www.kaggle.com/chrisfilo/mriqc-data-cleaning. However, this appears to introduce a lot of complex fields and does not work well with mriqception. 

The non-curated bold data from Figshare is closer, but required the following modifications:

Rename column md5sum to _id
Remove column bids_meta_TaskDescription
Remove provenance_settings
Rename bids_meta_ to bids_meta.
Rename provenance_ to provenance.

The mriqception dataset only preserves these bids_meta fields:
bids_meta.SequenceName	bids_meta.MagneticFieldStrength	bids_meta.ManufacturersModelName	bids_meta.modality	bids_meta.run_id	bids_meta.task_id	bids_meta.TaskName	bids_meta.Manufacturer	bids_meta.FlipAngle	bids_meta.EchoTime	bids_meta.subject_id	bids_meta.RepetitionTime	provenance.md5sum	provenance.settings.fd_thres	provenance.settings.hmc_fsl	provenance.version	provenance.software	_links.self.title	_links.self.href	bids_meta.session_id	bids_meta.ConversionSoftware	bids_meta.EffectiveEchoSpacing	bids_meta.PhaseEncodingDirection	bids_meta.ScanningSequence	bids_meta.CogAtlasID	bids_meta.SliceEncodingDirection	bids_meta.ParallelReductionFactorInPlane	bids_meta.PulseSequenceType	bids_meta.TotalReadoutTime

# Plans
1. Query the WebAPI instead of using canned outputs
  - Example of a retrieval URL: https://mriqc.nimh.nih.gov/api/v1/bold?max_results=100&where=bids_meta.MultibandAccelerationFactor%3E2
  - Convert the JSON returned by the WebAPI into a CSV: 
    - See `get_api_data_convert_2df.ipynb` for hints??
  - Provide the user with the ability to enter criteria from bids_meta (I've bolded the ones I think are most important: e.g. **modality**, **MagneticFieldStrength**, **Manufacturer**, **MultibandAccelerationFactor**, **RepetitionTime**):
  - Ensure that a list of example values is available in the documentation to help the user choose
    - **modality**	string (bold, T1w, T2w)
    - subject_id*	string
    - session_id	string
    - run_id	string
    - acq_id	string
    - task_id	string
    - AccelNumReferenceLines	integer
    - AccelerationFactorPE	integer
    - AcquisitionMatrix	string
    - CogAtlasID	string
    - CogPOID	string
    - CoilCombinationMethod	string
    - ContrastBolusIngredient	string
    - ConversionSoftware	string
    - ConversionSoftwareVersion	string
    - DelayTime	number($float)
    - DeviceSerialNumber	string
    - EchoTime	number($float)
    - EchoTrainLength	integer
    - EffectiveEchoSpacing	number($float)
    - FlipAngle	integer
    - GradientSetType	string
    - HardcopyDeviceSoftwareVersion	string
    - ImagingFrequency	integer
    - InPlanePhaseEncodingDirection	string
    - InstitutionAddress	string
    - InstitutionName	string
    - Instructions	string
    - InversionTime	number($float)
    - MRAcquisitionType	string
    - MRTransmitCoilSequence	string
    - **MagneticFieldStrength	number($float)** e.g., =3
    - **Manufacturer	string** e.g. Siemens
    - ManufacturersModelName	string
    - MatrixCoilMode	string
    - **MultibandAccelerationFactor	number($float)** e.g., <4
    - NumberOfAverages	integer
    - NumberOfPhaseEncodingSteps	integer
    - NumberOfVolumesDiscardedByScanner	number($float)
    - NumberOfVolumesDiscardedByUser	number($float)
    - NumberShots	integer
    - ParallelAcquisitionTechnique	string
    - ParallelReductionFactorInPlane	number($float)
    - PartialFourier	boolean
    - PartialFourierDirection	string
    - PatientPosition	string
    - PercentPhaseFieldOfView	integer
    - PercentSampling	integer
    - PhaseEncodingDirection	string
    - PixelBandwidth	integer
    - ProtocolName	string
    - PulseSequenceDetails	string
    - PulseSequenceType	string
    - ReceiveCoilName	string
    - **RepetitionTime	number($float)** e.g. =2.0
    - ScanOptions	string
    - ScanningSequence	string
    - SequenceName	string
    - SequenceVariant	string
    - SliceEncodingDirection	string
    - SoftwareVersions	string
    - TaskDescription	string
    - TotalReadoutTime	number($float)
    - TotalScanTimeSec	integer
    - TransmitCoilName	string
    - VariableFlipAngleFlag	string
    - TaskName*	string
2. Include a traffic-light table of the User's input (subjects or images in rows and IQMs in columns)
  - Coloring per field is red (bad) to green (good): 
    - See `/Volumes/Main/Working/mriqception_test/iqm_descriptions_and_direction.csv`  
  - Generate normalized data (see norm_z.py)
    - See https://plotly.com/python/table/#cell-color-based-on-variable
  - Display the data in 4 tables using traffic-light coloring for the cells: z-scores from -4 to 4 with 0 at the center and 9 categories:  
    < -3.5, -3.5 to -2.5, -2.5 to < -1.5, -1.5 to < -0.5, -0.5 to 0.5, >0.5 to 1.5, >1.5 to 2.5, >2.5 to 3.5, >3.5
    - anat_hi_good = ['cnr', 'snr_csf', 'snr_gm', 'snr_total', 'snr_wm', 'snrd_csf', 'snrd_gm', 'snrd_total','snrd_wm', 'tpm_overlap_csf', 'tpm_overlap_gm', 'tpm_overlap_wm']
    - anat_low_good = ['cjv', 'rpve_csf', 'rpve_gm', 'rpve_wm', 'fwhm_x', 'fwhm_y', 'fwhm_z', 'inu_med', 'inu_range', 'qi_1', 'qi_2']
    - func_hi_good = ['fber', 'snr', 'tsnr'] 
    - func_low_good = ['aor', 'aqi', 'dummy_trs, 'dvars_nstd', 'dvars_std', 'dvars_vstd', 'efc', 'fd_mean', 'fd_num', 'fd_perc', 'fwhm_avg', 'gcor', 'gsr_x', 'gsr_y]
3. Generate an MRIQC-like report in HTML and/or PDF format: 
  - This should include violin plots for all measures and 
  - a traffic-light table for the user data.
  - Output the z-score normalized tsv file as well.
  - Output the api dataset used for comparison in tsv format.
4. Dockerize the project so the user just has to mount the directory with the group*.tsv, and enter some criteria for the comparison dataset.
