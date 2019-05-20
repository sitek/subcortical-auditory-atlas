#!/bin/bash

#SBATCH --mem=20G
#SBATCH --time=1:00:00

data_dir=/om2/user/ksitek/exvivo/data/
#atlas_dir=/om2/user/ksitek/exvivo/atlas/conjunctions/
atlas_dir=/om2/user/ksitek/exvivo/atlas/with_controls/

#input_base=S64520_m0_SLA
#input_base=auditory_brainstem_nuclei_201812_8-structures
#input_base=auditory_brainstem_nuclei_conj_kevin_v2_faruk_v1_100um
input_base=4-control

ref_base=Reg_S64550_nii_b0-slice
#ref_base=Reg_S64550_nii_b0-slice_100um-upsampled

xfm=${data_dir}xfms/diff2anatSLA_ants_Similarity_Affine_MI_16x8x4x20GenericAffine.mat

#--output ${data_dir}xfms/m0_to_diff/${input_base}_to_${ref_base}.nii.gz \
antsApplyTransforms --input ${atlas_dir}${input_base}.nii.gz \
  --reference-image ${data_dir}diff/${ref_base}.nii.gz \
  --output ${atlas_dir}/${input_base}_to_${ref_base}.nii.gz \
  --interpolation MultiLabel \
  --transform [$xfm, 1]
