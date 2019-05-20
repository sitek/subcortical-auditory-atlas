#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --mem=40G
#SBATCH -c 4

python dipy_atlas_target_life.py
