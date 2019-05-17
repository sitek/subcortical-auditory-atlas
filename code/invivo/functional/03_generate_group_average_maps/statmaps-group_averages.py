"""Average images in same space.

NOTE: This script is also used to generate leave-one-out group maps.
"""

import os
import numpy as np
import nibabel as nb

files = [
    '/path/to/sub-01_map.nii.gz',
    '/path/to/sub-02_map_InCommon.nii.gz',
    '/path/to/sub-03_map_InCommon.nii.gz',
    '/path/to/sub-05_map_InCommon.nii.gz',
    '/path/to/sub-06_map_InCommon.nii.gz',
    '/path/to/sub-07_map_InCommon.nii.gz',
    '/path/to/sub-08_map_InCommon.nii.gz',
    '/path/to/sub-09_map_InCommon.nii.gz',
    '/path/to/sub-10_map_InCommon.nii.gz',
    '/path/to/sub-11_map_InCommon.nii.gz',
    ]

OUT_DIR = "/path/to/group_maps"
OUT_BASENAME = "group_stat_map"

LEAVE1OUT = False
AVERAGE = True

# =============================================================================
# Derivatives
id_subj = [os.path.basename(f)[:3] for f in files]
affine = nb.load(files[1]).affine
header = nb.load(files[1]).header

# -----------------------------------------------------------------------------
# Load all niftis
data = [nb.load(f).get_data() for f in files]
data = np.asarray(data)
nr_subj = len(files)

# =============================================================================
# Big sum with all subjects
group_sum = np.sum(data, axis=0)
# Save
outname = "{}-sum.nii.gz".format(OUT_BASENAME)
outpath = os.path.join(OUT_DIR, outname)
nb.save(nb.Nifti1Image(group_sum, affine=affine, header=header), outpath)

# =============================================================================
if AVERAGE:
    group_avg = np.mean(data, axis=0)
    # Save
    outname = "{}-avg.nii.gz".format(OUT_BASENAME)
    outpath = os.path.join(OUT_DIR, outname)
    nb.save(nb.Nifti1Image(group_avg, affine=affine, header=header), outpath)

# =============================================================================
if LEAVE1OUT:
    # Leave-one-out group maps
    idx = np.arange(0, nr_subj)
    for i in range(nr_subj):
        idx_temp = np.delete(idx, i)
        temp_sum = np.sum(data[idx_temp, ...], axis=0)

        # Save
        outname = "{}-leave_{}_out_sum.nii.gz".format(OUT_BASENAME, id_subj[i])
        outpath = os.path.join(OUT_DIR, outname)
        nb.save(nb.Nifti1Image(temp_sum, affine=affine, header=header), outpath)

print('Finished.')
