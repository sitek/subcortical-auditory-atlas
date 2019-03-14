"""Modify nifti header to make 100um bstem volume overlay correctly on MNI.

Notes
-----
I have compared nifti headers from MNI 0.5 data (2009b) and our resampled
brainstem-only 100um images. Sform and Qfroms were different. So I have copied
headers from MNI and override sform with a translation-only transformation.
This transformation is computed from ITK-SNAP coregistration of the same MNI
images (T1w) one in original and second resampled and brainstem extracted.

"""

import os
import numpy as np
import nibabel as nb

source = "/path/to/resampled_100um_bstem_image.nii.gz"
target = "/path/to/mni_icbm152_t1_tal_nlin_sym_09b_hires.nii.gz"

# Load niftis
src = nb.load(source)
trg = nb.load(target)

# Assign new affine (coming from ITK-SNAP registration)
new_affine = np.array([[0.1, 0, 0, -38.2284],
                       [0, 0.1, 0, -54.2106],
                       [0, 0, 0.1, -56.1836],
                       [0, 0, 0, 1]])

# Save
out = nb.Nifti1Image(src.get_data(), header=trg.header, affine=new_affine)
basename = source.split(os.extsep, 1)[0]
nb.save(out, "{}_fixHeader.nii.gz".format(basename))
print("Finished.")
