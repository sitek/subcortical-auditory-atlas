#!/bin/bash
#SBATCH --time=1-00:00:00
#SBATCH --mem=200GB
#SBATCH --cpus-per-task=12

script_dir=/om2/user/ksitek/maastricht/diffusion_faruk/code/
python ${script_dir}dipy_csd_invivo.py
