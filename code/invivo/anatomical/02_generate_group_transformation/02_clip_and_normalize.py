"""Clip and normalize dynamic range of niftis.

NOTE: I have used range clipping and normalization to 0-100 range to  mitigate
unwanted the effects of extremely bright arteries on the cost calculation
during FNIRT. The intensity clipping ranges that I have used are:
|   | Min| Max|
|S01|  0 | 50 |
|S02|  0 | 40 |
|S03| 10 | 70 |
|S05|  0 | 70 |
|S06|  0 | 60 |
|S07|  0 | 60 |
|S08| 10 | 80 |
|S09| 10 | 80 |
|S10| 15 | 60 |
|S11| 10 | 70 |
"""

import os
import nibabel as nb

FILENAME = "/path/to/S01_siT1w_anatomical_TAL_roi.nii.gz"
THR = 10
UTHR = 70

# -----------------------------------------------------------------------------
nii = nb.load(FILENAME)
data = nii.get_data()
data = data.astype('float')
# Truncate
data[data < THR] = THR
data[data > UTHR] = UTHR

# Normalize
data -= data.min()
data /= data.max()
data *= 100

out = nb.Nifti1Image(data, affine=nii.affine, header=nii.header)
basename, ext = os.path.basename(FILENAME).split(os.extsep, 1)
dirname = os.path.dirname(FILENAME)
outname = "{}_rangeclipped_normalized.nii.gz".format(basename)
outpath = os.path.join(dirname, outname)
nb.save(out, outpath)
print("Finished.")
