#!/bin/bash

# This script is used to transform maps with float values. For example average
# t-values maps.

# Invivo group average image that will be transformed to MNI
IMAGE="/path/to/invivo_group_map_with_float_precision.nii.gz"

# Non-linear transformation that will be used with FSL-applywarp
NONLINEAR_TRANSFORMATION="/path/to/step1-invivo_group_bstem-TOmni_icbm152_t1_tal_nlin_sym_09b_hires.nii.gz"
# Linear transformation that will be used with ITK-SNAP
LINEAR_TRANSFORMATION="/path/to/step2-invivo_group_bstem-TO-mni_icbm152_t1_tal_nlin_sym_09b_hires.txt"
# 500 micron to 100 micron
MNI_100MICRON_BSTEM_TRANSFORMATION="/path/to/step3-mni_icbm152_t1_tal_nlin_sym_09b_hires-TO-100um_bstem.txt"

# Nifti that has correct headers for this operation to work
HEADER_MNI_500MICRON="/path/to/header_of_mni_icbm152_tal_nlin_sym_09b_hires.nii.gz"
HEADER_INVIVO_GROUP="/path/to/header_of_invivo_bstem.nii.gz"
HEADER_MNI_100MICRON_BSTEM="/path/to/header_of_MNI_100um_bstem.nii.gz"

# =============================================================================
# Correct header (to be on the safe side)
command="${FSLDIR}/bin/fslmaths "
command+="${HEADER_INVIVO_GROUP} "
command+="-mul 0 -add 1 -mul ${IMAGE} "
command+="${IMAGE}"
${command}

# -----------------------------------------------------------------------------
# Applywarp
command="${FSLDIR}/bin/applywarp "
command+="--in=${IMAGE} "
command+="--ref=${IMAGE} "
command+="--out=${IMAGE%.nii*}_step1.nii.gz "
command+="--warp=${NONLINEAR_TRANSFORMATION} "
command+="--interp=spline "
command+="--datatype=double "
printf "# Step 1:\n"
printf "${command}\n\n"
${command}

# -----------------------------------------------------------------------------
# Apply linear transformation
command="c3d "
command+="-interpolation Linear "
command+="${HEADER_MNI_500MICRON} "  # Target
command+="${IMAGE%.nii*}_step1.nii.gz "  # Moving
command+="-reslice-itk ${LINEAR_TRANSFORMATION} "
command+="-o ${IMAGE%.nii*}_MNI.nii.gz "
printf "# Step 2:\n"
printf "${command}\n\n"
${command}

# -----------------------------------------------------------------------------
# Cleanup
command="rm ${IMAGE%.nii*}_step1.nii.gz"
printf "# Cleaning up intermediates...\n\n"
${command}

# -----------------------------------------------------------------------------
# Apply linear transformation
command="c3d "
command+="-interpolation Linear "
command+="${HEADER_MNI_100MICRON_BSTEM} "  # Target
command+="${IMAGE%.nii*}_MNI.nii.gz "  # Moving
command+="-reslice-itk ${MNI_100MICRON_BSTEM_TRANSFORMATION} "
command+="-o ${IMAGE%.nii*}_MNI_100um_bstem.nii.gz "
printf "# Step 3:\n"
printf "${command}\n\n"
${command}

printf "Finished.\n"
