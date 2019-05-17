#!/bin/bash

## Crop the data using VTC bounding box information
# Information, from Brainvoyager VTC_Creation_1x1x1.js script
# -----------------------------------------------------------------------------
#docVMR.TargetVTCBoundingBoxXStart = 201;
#docVMR.TargetVTCBoundingBoxXEnd   = 315;
#docVMR.TargetVTCBoundingBoxYStart = 267;
#docVMR.TargetVTCBoundingBoxYEnd   = 338;
#docVMR.TargetVTCBoundingBoxZStart = 214;
#docVMR.TargetVTCBoundingBoxZEnd   = 367;
# -----------------------------------------------------------------------------

declare -a ARR_MAP=(
    "/path/to/S01_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S02_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S03_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S05_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S06_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S07_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S08_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S09_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S10_siT1w_anatomical_TAL.nii.gz"
    "/path/to/S11_siT1w_anatomical_TAL.nii.gz"
    )

# =============================================================================
for i in "${ARR_MAP[@]}"
do
    i_map=${i%.nii}
    command="${FSLDIR}/bin/fslroi "
    command+="$i_map "  # input
    command+="${i_map%.nii*}_roi "  # output
    command+="266 72 "  # BV:Y, FSL:X
    command+="213 154 " # BV:Z, FSL:Y
    command+="200 115 " # BV:X, FSL,Z
    command+="0 -1 "    # Time
    echo "${command}"
    ${command}

done
echo "ROI extraction is done."
