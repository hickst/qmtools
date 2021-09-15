# Descriptions strings for the various Image Quality Metrics, accessible as a dictionary.
#   Written by: Tom Hicks and Dianne Patterson. 9/13/2021.
#   Last Modified: Removed "are better" statements.
#
IQMS_DOC_DICT = {
  "aor": "AFNI's outlier ratio is the mean fraction of outliers per volume from AFNI’s 3dToutcount.",
  "aqi": "AFNI's quality index calculates a quality index for each volume using AFNI’s 3dTqual. MRIqc reports the mean of these values.",
  "cjv": "Coefficient of Joint Variation between WM and GM. Higher values indicate more head motion and/or INU (bias-field) artifacts. Ganzetti, 2016.",
  "cnr": "Contrast-to-Noise Ratio (Mean GM intensity - Mean WM intensity) / (SD of air background). CNR reflects separation of GM and WM. Magnotta, 2006.",
  "dummy_trs": "Dummy scans are the number of volumes at the beginning of the fMRI series identified as non-steady state.",
  "dvars_nstd": "Derivatives of variance (std, vstd, and nstd) indexes the rate of whole-brain BOLD signal change between each pair of consecutive volumes in an fMRI series. DVARS is scaled to make comparisons across scanning protocols possible. Slices with high values indicate more noise (e.g., motion or spiking), and should be excluded/replaced. D = temporal derivative of timecourses. VARS = RMS variance over voxels. See Afyouni, 2018.",
  "dvars_std": "Derivatives of variance (std, vstd, and nstd) indexes the rate of whole-brain BOLD signal change between each pair of consecutive volumes in an fMRI series. DVARS is scaled to make comparisons across scanning protocols possible. Slices with high values indicate more noise (e.g., motion or spiking), and should be excluded/replaced. D = temporal derivative of timecourses. VARS = RMS variance over voxels. See Afyouni, 2018.",
  "dvars_vstd": "Derivatives of variance (std, vstd, and nstd) indexes the rate of whole-brain BOLD signal change between each pair of consecutive volumes in an fMRI series. DVARS is scaled to make comparisons across scanning protocols possible. Slices with high values indicate more noise (e.g., motion or spiking), and should be excluded/replaced. D = temporal derivative of timecourses. VARS = RMS variance over voxels. See Afyouni, 2018.",
  "efc": "Shannon Entropy-focus criterion is the the Shannon entropy of voxel intensities proportional to the maximum possible entropy for a similarly sized image. Higher values indicate more ghosting and/or head motion induced blurring. Atkinson, 1997.",
  "fber": "Foreground-background energy ratio is the energy inside the head relative to the air background. Shehzad, 2015.",
  "fd_mean": "The mean Framewise displacement is a measure of instantaneous subject head motion. It compares motion in consecutive volumes by summing displacement and rotation in all three axes. Power, 2012.",
  "fd_num": "Framewise displacement_number lists the # of volumes with framewise displacement greater than 0.2mm. Power, 2012. This is a measure of subject head motion. Power, 2012.",
  "fd_perc": "Framewise displacement_percent lists the percent of volumes with framewise displacement greater than 0.2mm. Power, 2012. This is a measure of subject head motion. Power, 2012.",
  "fwhm_avg": "Full-Width Half-Maximum (mean, x,y,z) is the image blurriness (smoothness). Higher values indicate blurrier image. Forman, 1995.",
  "fwhm_x": "Full-Width Half-Maximum (mean, x,y,z) is the image blurriness (smoothness). Higher values indicate blurrier image. Forman, 1995.",
  "fwhm_y": "Full-Width Half-Maximum (mean, x,y,z) is the image blurriness (smoothness). Higher values indicate blurrier image. Forman, 1995.",
  "fwhm_z": "Full-Width Half-Maximum (mean, x,y,z) is the image blurriness (smoothness). Higher values indicate blurrier image. Forman, 1995.",
  "gcor": "Global correlation is the average correlation of all pairs of voxel time series inside of the brain. GCOR identifies differences between data due to motion, physiological noise and-or imaging artifacts. Saad, 2013.",
  "gsr_x": "Ghost-to-signal ratio (x and y) along the x or y encoding axes. Gianelli, 2010.",
  "gsr_y": "Ghost-to-signal ratio (x and y) along the x or y encoding axes. Gianelli, 2010.",
  "icvs": "Intracranial Volume fraction is a summary statistic for CSF, GM, and WM. Beware of outliers.",
  "inu_med": "Intensity Non-Uniformity (a.k.a. Bias Field) is slow nonanatomic intensity variation in the same tissue over the image. It can result from problems with scanner gradient coils. We collect median and range. A larger range indicates greater RF field inhomogeneity. A small range with a median ~1 is better. Tustison, 2010.",
  "inu_range": "Intensity Non-Uniformity (a.k.a. Bias Field) is slow nonanatomic intensity variation in the same tissue over the image. It can result from problems with scanner gradient coils. We collect median and range. A larger range indicates greater RF field inhomogeneity. A small range with a median ~1 is better. Tustison, 2010.",
  "qi_1": "Mortamet’s Quality Index 1 identifies the proportion of voxels in the air background with artifacts compared to the total number of voxels in the air background of T1w images. Mortamet, 2009.",
  "qi_2": "Mortamet’s Quality Index 2 identifies artifacts and artifact clusters in the air background of T1w images (collected without parallel imaging or pre-scan normalization). QI2 reliably identifies very poor quality images. Mortamet, 2009.",
  "rpve_csf": "Residual partial voluming error is a tissue-wise sum of partial volumes that fall in the range [5%-95%] of the total volume of a voxel, computed from FSL FAST partial volume map for CSF, WM and GM.",
  "rpve_gm": "Residual partial voluming error is a tissue-wise sum of partial volumes that fall in the range [5%-95%] of the total volume of a voxel, computed from FSL FAST partial volume map for CSF, WM and GM.",
  "rpve_wm": "Residual partial voluming error is a tissue-wise sum of partial volumes that fall in the range [5%-95%] of the total volume of a voxel, computed from FSL FAST partial volume map for CSF, WM and GM.",
  "snr": "Signal-to-noise ratio is the mean intensity in each tissue (CSF, GM, WM, and total) signal divided by SD of the air background (noise). SNR is important for estimating the statistical power. A higher value indicates a more stable signal over repeated measurements, thus higher reliability of the measure.",
  "snr_csf": "Signal-to-noise ratio is the mean intensity in each tissue (CSF, GM, WM, and total) signal divided by SD of the air background (noise). SNR is important for estimating the statistical power. A higher value indicates a more stable signal over repeated measurements, thus higher reliability of the measure.",
  "snr_gm": "Signal-to-noise ratio is the mean intensity in each tissue (CSF, GM, WM, and total) signal divided by SD of the air background (noise). SNR is important for estimating the statistical power. A higher value indicates a more stable signal over repeated measurements, thus higher reliability of the measure.",
  "snr_total": "Signal-to-noise ratio is the mean intensity in each tissue (CSF, GM, WM, and total) signal divided by SD of the air background (noise). SNR is important for estimating the statistical power. A higher value indicates a more stable signal over repeated measurements, thus higher reliability of the measure.",
  "snr_wm": "Signal-to-noise ratio is the mean intensity in each tissue (CSF, GM, WM, and total) signal divided by SD of the air background (noise). SNR is important for estimating the statistical power. A higher value indicates a more stable signal over repeated measurements, thus higher reliability of the measure.",
  "snrd_csf": "Dietrich’s Signal to Noise ratio (for CSF, GM, WM, and total) is more robust than conventional SNR for MRI: especially for filtered, multi-channel, and parallel images. Dietrich, 2007.",
  "snrd_gm": "Dietrich’s Signal to Noise ratio (for CSF, GM, WM, and total) is more robust than conventional SNR for MRI: especially for filtered, multi-channel, and parallel images. Dietrich, 2007.",
  "snrd_total": "Dietrich’s Signal to Noise ratio (for CSF, GM, WM, and total) is more robust than conventional SNR for MRI: especially for filtered, multi-channel, and parallel images. Dietrich, 2007.",
  "snrd_wm": "Dietrich’s Signal to Noise ratio (for CSF, GM, WM, and total) is more robust than conventional SNR for MRI: especially for filtered, multi-channel, and parallel images. Dietrich, 2007.",
  "summary_stats": "K (kurtosis), M, SD, 5% , and 95% for average intensities in air background, CSF, GM, and WM. Larger differences represent better tissue contrast.",
  "tpm_overlap_csf": "Overlap of tissue probability maps indicates how well the native Tissue Probability Maps (TPMS) overlap with the MNI ICBM 2009 template. Higher values indicate better quality spatial normalization.",
  "tpm_overlap_gm": "Overlap of tissue probability maps indicates how well the native Tissue Probability Maps (TPMS) overlap with the MNI ICBM 2009 template. Higher values indicate better quality spatial normalization.",
  "tpm_overlap_wm": "Overlap of tissue probability maps indicates how well the native Tissue Probability Maps (TPMS) overlap with the MNI ICBM 2009 template. Higher values indicate better quality spatial normalization.",
  "tsnr": "Temporal signal-to-noise ratio is the median SNR over time and is adversely affected by subject motion. Low tSNR may bias the data. Kruger, 2001.",
  "wm2max": "White Matter-to-MAXimum intensity ratio is the median intensity in the WM mask over the 95% percentile of the full intensity distribution. This captures skewed distributions in the WM mask, caused by fat & hyperintensities. Ideal values fall within the interval [0.6, 0.8]."
}