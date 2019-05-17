#!/bin/bash

# FNIRT non-linear registration
REFVOL="/path/to/S01_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
declare -a ARR_MAP=(
    "/path/to/S02_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S03_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S05_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S06_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S07_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S08_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S09_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S10_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    "/path/to/S11_siT1w_anatomical_TAL_roi_rangeclipped_normalized.nii.gz"
    )

# =============================================================================
tLen=${#ARR_MAP[@]}
for (( i=0; i<${tLen}; i++ ));
do
    i_map=${ARR_MAP[$i]}
    command="${FSLDIR}/bin/fnirt "
    command+="--ref=$REFVOL "
    command+="--in=$i_map "
    command+="--cout=${i_map%.nii*}_cout.nii "
    command+="--iout=${i_map%.nii*}_iout "
    command+="--fout=${i_map%.nii*}_fout "
    command+="--subsamp=4,2,2,1  "  # Sub-sampling scheme, def 4,2,1,1
    command+="--miter=30,30,20,20 "  # Max # of non-linear iterations, def 5,5,5,5
    command+="--infwhm=1,1,1,1 "  # FWHM (in mm) of gaussian smoothing kernel, def 6,4,2,2
    command+="--reffwhm=1,1,1,1 "  # FWHM (in mm) of gaussian smoothing kernel, def 4,2,0,0
    command+="--lambda=50,25,10,5 "  # Weight of regularisation, def depens on --ssqlambda and --regmod switches. See user documentation.
    command+="--estint=0,0,0,0 "  # Estimate intensity-mapping if set, default 1 (true)
    command+="--warpres=5,5,5 "  # Approx. res. (in mm) of warp basis in x-, y- and z-direction, default 10,10,10
    command+="--interp=linear "  # Spline (slow) or linear (fast)
    command+="--regmod=bending_energy "  # Model for regularisation of warp-field, bending_energy (def) or membrane_energy
    command+="--verbose "
    echo "About to issue FNIRT command: "
    echo "${command}"
    ${command}

    # Create inverse warp coeff. map
    command="${FSLDIR}/bin/invwarp "
    command+="--warp=${i_map%.nii*}_cout.nii "
    command+="--out=${i_map%.nii*}_cout_inv.nii "
    command+="--ref=$REFVOL "
    echo "About to issue invwarp command: "
    echo "${command}"
    ${command}

done
echo "FNIRT is done."
