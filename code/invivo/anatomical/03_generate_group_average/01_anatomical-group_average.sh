#!/bin/bash

declare -a ARR_MAP=(
    "/path/to/S01_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S02_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S03_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S05_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S06_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S07_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S08_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S09_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S10_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    "/path/to/S11_siT1w_anatomical_TAL_roi_rangeclipped_normalized_iout.nii.gz"
    )

OUTDIR="/path/to/group_average/"

# =============================================================================
command="${FSLDIR}/bin/fslmaths ${ARR_MAP[0]} "

tLen=${#ARR_MAP[@]}
for (( i=1; i<${tLen}; i++ ));
do
    command+="-add ${ARR_MAP[$i]} "
done
command+="-div ${tLen} ${OUTDIR}/ANAT_AVG.nii.gz"
echo ${command}
${command}

echo "Finished."
