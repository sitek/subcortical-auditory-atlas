'''
After creating tractography streamlines with dipy_csd.py,
this workflow takes an atlas file and finds connections
between each region in the atlas
KRS 2018.05.04
'''
from nipype import config
config.set('execution', 'remove_unnecessary_outputs', 'false')
config.set('execution', 'crashfile_format', 'txt')

from nipype import Node, Function, Workflow, IdentityInterface, MapNode
from nipype.interfaces.io import SelectFiles, DataSink

import os
from glob import glob

# which data sampling? also used for naming
out_prefix = 'dipy_csd'
atlas_type = 'func-atlas_shift_vox-4_ax-1'

proj_dir = os.path.abspath('/om2/user/ksitek/maastricht/diffusion_faruk/')
data_dir = os.path.join(proj_dir, 'data/01_diff_preprocessed')
out_base = os.path.join(proj_dir, 'analysis/')
out_dir = os.path.join(out_base, '%s_%s/'%(out_prefix, atlas_type))
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

work_dir = os.path.abspath('/om2/scratch/ksitek/%s_%s_0114/'%(out_prefix, atlas_type))

#sids = ['S02']
sids = ['S%02d' %s for s in range(1,12)]

roi_names = ['LH_CN', 'LH_SOC', 'LH_IC', 'LH_MGB',
             'RH_CN', 'RH_SOC', 'RH_IC', 'RH_MGB']
rois = list(range(len(roi_names)))

'''
roi_dir = os.path.join(proj_dir, 'analysis/roi_diff/')
subj_rois = {}
for subj in sids:
    subj_rois[subj] = sorted(glob('%s/%s/%s_roi*_2diff.nii.gz'%(roi_dir, subj, subj)))
print(subj_rois)
'''

roi_dir = os.path.join(proj_dir, 'analysis/roi_diff_shift/')
subj_rois = {}
for subj in sids:
    subj_rois[subj] = sorted(glob('%s/%s/%s_roi*_2diff_shift_vox-4_ax-1.nii.gz'%(roi_dir, subj, subj)))
print(subj_rois)

# create the nipype workflow
wf = Workflow(name='connectivity')
wf.config['execution']['crashfile_format'] = 'txt'

# define inputs to the workflow
infosource = Node(IdentityInterface(fields=['subject_id', 'roi']), name='infosource')
infosource.iterables = [('subject_id', list(subj_rois.keys())),
                        ('roi', rois)]

# grab data
#templates = {'trk': 'analysis/mrtrix/{subject_id}/tracks.trk'}
templates = {'trk': 'analysis/fathresh-0.5/{subject_id}/recon/{subject_id}_csd_streamline.trk'}
grabber = Node(SelectFiles(templates), name='grabber')
grabber.inputs.base_directory = proj_dir
grabber.inputs.sort_filelist = True

wf.connect(infosource, 'subject_id', grabber, 'subject_id')

''' define ROI mask files '''

# get subject-specific list of ROI filenames:
def rois_fetcher(subj_rois, subj):
    return subj_rois[subj], subj
fetch_rois = Node(Function(input_names=['subj_rois', 'subj'],
                           output_names=['target_roi_filenames', 'subj'],
                           function=rois_fetcher),
                  name='fetch_rois')
fetch_rois.inputs.subj_rois = subj_rois
wf.connect(infosource, 'subject_id', fetch_rois, 'subj')

# get single ROI filename for a specific subject:
def roi_fetcher(subj_rois, subj, roi_idx):
    return subj_rois[subj][roi_idx], roi_idx
fetch_roi = Node(Function(input_names=['subj_rois', 'subj', 'roi_idx'],
                           output_names=['seed_roi', 'roi_idx'],
                           function=roi_fetcher),
                 name='fetch_roi')
fetch_roi.inputs.subj_rois = subj_rois
wf.connect(fetch_rois, 'subj', fetch_roi, 'subj')
wf.connect(infosource, 'roi', fetch_roi, 'roi_idx')


''' streamline filtering '''
# filter streamlines by seed region of interest
def sl_filter(streamlines, target_mask):
    from dipy.tracking.utils import target
    #from nilearn.image import resample_img
    import numpy as np
    import os
    import nibabel as nib

    trk_file = nib.streamlines.load(streamlines)
    streams = trk_file.streamlines
    hdr = trk_file.header

    # resample mask to resolution of input data & get data
    #target_resamp = resample_img(target_mask, affine)
    target_mask_img = nib.load(target_mask)
    affine = target_mask_img.affine

    target_mask_bool = np.zeros(target_mask_img.get_data().shape)
    target_mask_bool[target_mask_img.get_data().round()>0]=1 # rounding is key!

    target_sl_generator = target(streams, target_mask_bool, affine, include=True)
    target_streams = list(target_sl_generator)

    # create new filtered streamlines .trk file
    tractogram = nib.streamlines.Tractogram(target_streams)
    tractogram.affine_to_rasmm = np.eye(4)
    trk_file = nib.streamlines.TrkFile(tractogram, header=hdr)

    # get the filename
    import re
    label = re.search(r'(?<=Fix_)\w+',target_mask).group(0)[:-6]

    # save streamlines to filename
    target_streamlines = os.path.abspath('target_streamlines_region_%s.trk'%label)
    nib.streamlines.save(trk_file, target_streamlines)

    return target_streamlines, target_mask, affine, label

filter_streamlines = Node(Function(input_names = ['streamlines', 'target_mask'],
                                   output_names = ['target_streamlines', 'target_mask',
                                                   'affine', 'seed_label'],
                                   function = sl_filter),
                                   name = 'filter_streamlines')
filter_streamlines.inputs.roi_names = roi_names
wf.connect(grabber, 'trk', filter_streamlines, 'streamlines')
wf.connect(fetch_roi, 'seed_roi', filter_streamlines, 'target_mask')

# filter streamlines by target ROI (for each seed ROI)
def sl_filter_target(streamlines, target_mask, affine, seed_label):
    from dipy.tracking.utils import target
    from nilearn.image import resample_img
    import numpy as np
    import os

    import nibabel as nib
    trk_file = nib.streamlines.load(streamlines)
    streams = trk_file.streamlines
    hdr = trk_file.header

    # resample mask to resolution of input data & get data
    #target_resamp = resample_img(target_mask, affine)
    target_mask_img = nib.load(target_mask)
    affine = target_mask_img.affine

    target_mask_bool = np.zeros(target_mask_img.get_data().shape)
    target_mask_bool[target_mask_img.get_data().round()>0]=1 # rounding is key!

    target_sl_generator = target(streams, target_mask_bool, affine, include=True)
    target_streams = list(target_sl_generator)

    # create new filtered streamlines .trk file
    tractogram = nib.streamlines.Tractogram(target_streams)
    tractogram.affine_to_rasmm = np.eye(4)
    trk_file = nib.streamlines.TrkFile(tractogram, header=hdr)

    # get the filename
    import re
    label = re.search(r'(?<=Fix_)\w+',target_mask).group(0)[:-6]

    # save streamlines to filename
    target_streamlines = os.path.abspath('target_streamlines_seed-%s_target-%s.trk'%(seed_label, label))
    nib.streamlines.save(trk_file, target_streamlines)

    return target_streamlines

filter_streamlines_target = MapNode(Function(input_names = ['streamlines', 'target_mask',
                                                            'affine', 'seed_label'],
                                             output_names = ['target_streamlines'],
                                             function = sl_filter_target),
                                    iterfield = ['target_mask'],
                                    name = 'filter_streamlines_target')
wf.connect(fetch_rois, 'target_roi_filenames', filter_streamlines_target, 'target_mask')
wf.connect(filter_streamlines, 'target_streamlines', filter_streamlines_target, 'streamlines')
wf.connect(filter_streamlines, 'affine', filter_streamlines_target, 'affine')
wf.connect(filter_streamlines, 'seed_label', filter_streamlines_target, 'seed_label')

''' workflow '''
# create the output data sink
ds = Node(DataSink(parameterization=False), name='sinker')
ds.inputs.base_directory = out_dir
ds.plugin_args = {'overwrite': True}

wf.connect(infosource, 'subject_id', ds, 'container')

wf.connect(filter_streamlines_target, 'target_streamlines', ds, 'target_streamlines')

# definte the working directory and run the workflow
wf.base_dir = work_dir
wf.run(plugin='MultiProc')
