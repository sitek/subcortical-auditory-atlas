#!/bin/bash

#SBATCH --time=6:00:00
#SBATCH --mem=200G

#data_dir=/om2/user/ksitek/exvivo/data/
#input_base=S64520_m0_SLA_200um
#data_dir=/om2/user/ksitek/exvivo/data/xfms/m0_to_diff/
#input_base=S64520_m0_SLA_to_Reg_S64550_nii_b0-slice_50um-upsampled
#data_dir=/om2/user/ksitek/exvivo/analysis/dipy_csd/fathresh-0.1_0.2mm/recon/
#input_base=Reg_S64550_tensor_md
#data_dir=/om2/user/ksitek/exvivo/atlas/
#input_base=auditory_brainstem_nuclei_201812_8-structures_to_Reg_S64550_nii_b0-slice_100um-upsampled

data_dir=/om2/user/ksitek/exvivo/atlas/conjunctions/
input_base=auditory_brainstem_nuclei_conj_kevin_v2_faruk_v1_100um_to_Reg_S64550_nii_b0-slice

input_image=${data_dir}${input_base}.nii.gz

ref_dir=/om2/user/ksitek/maastricht/brainstem/
reference_base=fnirt_anat_siT1w.2_100um-upsampled
reference_image=${ref_dir}${reference_base}.nii.gz

xfm_dir=/om2/user/ksitek/exvivo/maastricht/ants/
xfm_img=${xfm_dir}maas2exvivo_ants_1InverseWarp.nii.gz
xfm_file=${xfm_dir}maas2exvivo_ants_0GenericAffine.mat

#interp=Linear
interp=MultiLabel

out_dir=${xfm_dir}/atlas_to_maas/
out_base=${input_base}_to_${reference_base}_ants-${interp}
output_image=${out_dir}${out_base}.nii.gz
mkdir -p $out_dir

echo "running antsApplyTransforms"
antsApplyTransforms \
  --input $input_image \
  --reference-image $reference_image \
  --output $output_image \
  --interpolation $interp \
  --transform [$xfm_file, 1] \
  --transform $xfm_img
