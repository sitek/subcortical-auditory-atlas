#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --mem=450GB
#SBATCH --cpus-per-task=4
#SBATCH --qos=gablab

script_dir=/om2/user/ksitek/exvivo/scripts/dipy/
python ${script_dir}dipy_csd.py
