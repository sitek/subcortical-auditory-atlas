#!/bin/bash
# Converts DICOM files to nifti in the BIDS format
# See BIDS specification: https://bids-specification.readthedocs.io/en/stable/
# KRS 2019.05.20

# location of heuristic file used for conversion
heuristic=/om2/user/ksitek/maastricht/atlas_invivo/code/heuristic.py

# create Experiment 1 dicominfo files (but don't convert)
heudiconv -d '/om4/group/gablab/dicoms/auditory_7t/{subject}/{subject}_{session}_DIF/*/*' \
 -s S01 -ss SES01 -c none -o /om2/user/ksitek/maastricht/atlas_invivo/data/ \
 -b -f convertall

# Experiment 1
for ses in SES01 SES02 SES03; do
  heudiconv -d '/om4/group/gablab/dicoms/auditory_7t/{subject}/{subject}_{session}_*/0*/*' \
            -s S01 S02 S03 S05 S06 S07 S08 S09 S10 S11 -ss ${ses} -b -f $heuristic \
            -o /om2/user/ksitek/maastricht/atlas_invivo/data/experiment_1/ \
            -q SLURM --queue-args "--cpus-per-task=10 --mem=16G --time=10:00:00"
done

# create Experiment 2 dicominfo files (but don't convert)
heudiconv -d '/om4/group/gablab/dicoms/auditory_7t/experiment_2/{subject}_{session}/*/*' \
  -s S01 -ss SES1 -c none -o /om2/user/ksitek/maastricht/atlas_invivo/data/experiment_2/ \
  -b -f convertall

# Experiment 2
# S01 S02 S03 S05 S06 S07
for ses in SES1 SES2; do
  heudiconv -d '/om4/group/gablab/dicoms/auditory_7t/experiment_2/{subject}_{session}/0*/*' \
            -s S04 -ss ${ses} -b -f $heuristic \
            -o /om2/user/ksitek/maastricht/atlas_invivo/data/experiment_2/ \
            -q SLURM --queue-args "--cpus-per-task=6 --mem=16G --time=2:00:00"
done
