#
# Module containing sets of MRIQC schema keywords; to be used for validation.
# Based on the mriqcwebapi schema file:
#     https://github.com/poldracklab/mriqcwebapi/blob/master/dockereve-master/eve-app/settings.py
#
#   Written by: Tom Hicks. 8/19/2021.
#   Last Modified: Complete the lists.
#
BIDS_KEYWORDS = set([
  'bids_meta.modality',
  'bids_meta.subject_id',
  'bids_meta.session_id',
  'bids_meta.run_id',
  'bids_meta.acq_id',
  'bids_meta.task_id',
  'bids_meta.AccelNumReferenceLines',
  'bids_meta.AccelerationFactorPE',
  'bids_meta.AcquisitionMatrix',
  'bids_meta.CogAtlasID',
  'bids_meta.CogPOID',
  'bids_meta.CoilCombinationMethod',
  'bids_meta.ContrastBolusIngredient',
  'bids_meta.ConversionSoftware',
  'bids_meta.ConversionSoftwareVersion',
  'bids_meta.DelayTime',
  'bids_meta.DeviceSerialNumber',
  'bids_meta.EchoTime',
  'bids_meta.EchoTrainLength',
  'bids_meta.EffectiveEchoSpacing',
  'bids_meta.FlipAngle',
  'bids_meta.GradientSetType',
  'bids_meta.HardcopyDeviceSoftwareVersion',
  'bids_meta.ImagingFrequency',
  'bids_meta.InPlanePhaseEncodingDirection',
  'bids_meta.InstitutionAddress',
  'bids_meta.InstitutionName',
  'bids_meta.Instructions',
  'bids_meta.InversionTime',
  'bids_meta.MRAcquisitionType',
  'bids_meta.MRTransmitCoilSequence',
  'bids_meta.MagneticFieldStrength',
  'bids_meta.Manufacturer',
  'bids_meta.ManufacturersModelName',
  'bids_meta.MatrixCoilMode',
  'bids_meta.MultibandAccelerationFactor',
  'bids_meta.NumberOfAverages',
  'bids_meta.NumberOfPhaseEncodingSteps',
  'bids_meta.NumberOfVolumesDiscardedByScanner',
  'bids_meta.NumberOfVolumesDiscardedByUser',
  'bids_meta.NumberShots',
  'bids_meta.ParallelAcquisitionTechnique',
  'bids_meta.ParallelReductionFactorInPlane',
  'bids_meta.PartialFourier',
  'bids_meta.PartialFourierDirection',
  'bids_meta.PatientPosition',
  'bids_meta.PercentPhaseFieldOfView',
  'bids_meta.PercentSampling',
  'bids_meta.PhaseEncodingDirection',
  'bids_meta.PixelBandwidth',
  'bids_meta.ProtocolName',
  'bids_meta.PulseSequenceDetails',
  'bids_meta.PulseSequenceType',
  'bids_meta.ReceiveCoilName',
  'bids_meta.RepetitionTime',
  'bids_meta.ScanOptions',
  'bids_meta.ScanningSequence',
  'bids_meta.SequenceName',
  'bids_meta.SequenceVariant',
  'bids_meta.SliceEncodingDirection',
  'bids_meta.SoftwareVersions',
  'bids_meta.TaskDescription',
  'bids_meta.TotalReadoutTime',
  'bids_meta.TotalScanTimeSec',
  'bids_meta.TransmitCoilName',
  'bids_meta.VariableFlipAngleFlag'
])

BOLD_KEYWORDS = set([
  '_created',
  '_id',
  '_etag',
  '_updated',
  'aor',
  'aqi',
  'dummy_trs',
  'dvars_nstd',
  'dvars_std',
  'dvars_vstd',
  'efc',
  'fber',
  'fd_mean',
  'fd_num',
  'fd_perc',
  'fwhm_avg',
  'fwhm_x',
  'fwhm_y',
  'fwhm_z',
  'gcor',
  'gsr_x',
  'gsr_y',
  'size_t',
  'size_x',
  'size_y',
  'size_z',
  'snr',
  'spacing_tr',
  'spacing_x',
  'spacing_y',
  'spacing_z',
  'summary_bg_k',
  'summary_bg_mean',
  'summary_bg_median',
  'summary_bg_mad',
  'summary_bg_p05',
  'summary_bg_p95',
  'summary_bg_stdv',
  'summary_bg_n',
  'summary_fg_k',
  'summary_fg_mean',
  'summary_fg_median',
  'summary_fg_mad',
  'summary_fg_p05',
  'summary_fg_p95',
  'summary_fg_stdv',
  'summary_fg_n',
  'tsnr',
  'provenance.version',
  'provenance.md5sum',
  'provenance.software',
  'provenance.settings.fd_thres',
  'provenance.settings.hmc_fsl',
  'provenance.settings.testing',
  'provenance.mriqc_pred',
  'provenance.email',
  'rating.rating',
  'rating.name',
  'rating.comment',
  'rating.md5sum',
  'bids_meta.TaskName'                 # special case: bold modality only
])

STRUCTURAL_KEYWORDS = set([
  '_created',
  '_id',
  '_etag',
  '_updated',
  'cjv',
  'cnr',
  'efc',
  'fber',
  'fwhm_avg',
  'fwhm_x',
  'fwhm_y',
  'fwhm_z',
  'icvs_csf',
  'icvs_gm',
  'icvs_wm',
  'inu_med',
  'inu_range',
  'qi_1',
  'qi_2',
  'rpve_csf',
  'rpve_gm',
  'rpve_wm',
  'size_x',
  'size_y',
  'size_z',
  'snr_csf',
  'snr_gm',
  'snr_total',
  'snr_wm',
  'snrd_csf',
  'snrd_gm',
  'snrd_total',
  'snrd_wm',
  'spacing_x',
  'spacing_y',
  'spacing_z',
  'summary_bg_k',
  'summary_bg_mean',
  'summary_bg_median',
  'summary_bg_mad',
  'summary_bg_p05',
  'summary_bg_p95',
  'summary_bg_stdv',
  'summary_bg_n',
  'summary_csf_k',
  'summary_csf_mean',
  'summary_csf_median',
  'summary_csf_mad',
  'summary_csf_p05',
  'summary_csf_p95',
  'summary_csf_stdv',
  'summary_csf_n',
  'summary_gm_k',
  'summary_gm_mean',
  'summary_gm_median',
  'summary_gm_mad',
  'summary_gm_p05',
  'summary_gm_p95',
  'summary_gm_stdv',
  'summary_gm_n',
  'summary_wm_k',
  'summary_wm_mean',
  'summary_wm_median',
  'summary_wm_mad',
  'summary_wm_p05',
  'summary_wm_p95',
  'summary_wm_stdv',
  'summary_wm_n',
  'tpm_overlap_csf',
  'tpm_overlap_gm',
  'tpm_overlap_wm',
  'wm2max',
  'provenance.version',
  'provenance.md5sum',
  'provenance.software',
  'provenance.settings.fd_thres',
  'provenance.settings.hmc_fsl',
  'provenance.settings.testing',
  'provenance.mriqc_pred',
  'provenance.email'

])