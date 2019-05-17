"""Minimum intensity projection over one dimension for a window."""

import os
import numpy as np
from nibabel import load, Nifti1Image, save

# Input 3D nifti
filename = '/path/to/image.nii.gz'
# WindoW on both sides (e.g. W=4 means: 4+1+4)
W = 4

# =============================================================================
nii = load(filename)
data = nii.get_data()
dims = data.shape
# -----------------------------------------------------------------------------
suffix = 'miip_{}_x'.format(W)
temp = np.zeros(dims)
for i in range(W, dims[0]-W):
    temp[i, :, :] = np.min(data[i-W:i+W, :, :], axis=0)

print('Saving x...')
img = Nifti1Image(temp, affine=nii.affine)
temp = None
basename, ext = nii.get_filename().split(os.extsep, 1)
out_name = '{}_{}.{}'.format(basename, suffix, ext)
save(img, out_name)

# -----------------------------------------------------------------------------
suffix = 'miip_{}_y'.format(W)
temp = np.zeros(dims)
for i in range(W, dims[1]-W):
    temp[:, i, :] = np.min(data[:, i-W:i+W, :], axis=1)

print('Saving y...')
img = Nifti1Image(temp, affine=nii.affine)
temp = None
basename, ext = nii.get_filename().split(os.extsep, 1)
out_name = '{}_{}.{}'.format(basename, suffix, ext)
save(img, out_name)

# -----------------------------------------------------------------------------
suffix = 'miip_{}_z'.format(W)
temp = np.zeros(dims)
for i in range(W, dims[2]-W):
    temp[:, :, i] = np.min(data[:, :, i-W:i+W], axis=2)

print('Saving z...')
img = Nifti1Image(temp, affine=nii.affine)
temp = None
basename, ext = nii.get_filename().split(os.extsep, 1)
out_name = '{}_{}.{}'.format(basename, suffix, ext)
save(img, out_name)

print('Finished.')
