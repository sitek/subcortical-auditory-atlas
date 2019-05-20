#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --mem=50G
#SBATCH -c 4

scripts=/om2/user/ksitek/scripts/
#analysis_dir=/om2/user/ksitek/exvivo/analysis/dipy_csd/
#analysis=fathresh-0.1_0.2mm_8-structure_201901_0826-atlas
#analysis=fathresh-0.1_0.2mm_conj_kevin_v2_faruk_v1_dil-500um
#analysis=fathresh-0.1_0.2mm_conj_kevin_v2_faruk_v1_with_controls_dil-500um
analysis_dir=/om2/user/ksitek/exvivo/analysis/dipy/csd/
analysis=alow-0p001_angthr-75_minangle-10_fathresh-50_20190517_0.2mm
atlas=conj_kevin_v2_faruk_v1_with_controls_dil-500um
trk_dir=${analysis_dir}/${analysis}_${atlas}/target_streamlines/
echo "trk dir: ${trk_dir}"

${scripts}dtk/track_merge ${trk_dir}*.trk ${trk_dir}all_atlas_streamlines.trk
