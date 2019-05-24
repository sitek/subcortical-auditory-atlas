#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --mem=400GB
#SBATCH --cpus-per-task=10
#SBATCH -p om_bigmem

script_dir=/om2/user/ksitek/exvivo/scripts/dipy/
python ${script_dir}dipy_atlas_target_life.py
