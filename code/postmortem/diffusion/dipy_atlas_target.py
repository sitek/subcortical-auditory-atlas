'''
After creating tractography streamlines with dipy_csd.py,
this workflow takes an atlas file and finds connections
between each region in the atlas
KRS 2018.05.04
'''
from nipype import config
config.set('execution', 'remove_unnecessary_outputs', 'false')
config.set('execution', 'crashfile_format', 'txt')

#config.enable_provenance()

from nipype import Node, Function, Workflow, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink

import os
from glob import glob

# which data sampling? also used for naming
resolution = '1.05mm'
analysis_prefix = 'alow-0p001_angthr-75_minangle-10_' \
                  'fathresh-50_20190523_%s'%resolution

atlas_type = 'conj_kevin_v2_faruk_v1'
#atlas_type = 'conj_kevin_v2_faruk_v1_dil-500um'

data_dir = os.path.abspath('/om2/user/ksitek/exvivo/data')
analysis_base = os.path.join('/om2/user/ksitek/exvivo/analysis/dipy/', 'csd')
out_dir = os.path.join(analysis_base, '%s_%s/'%(analysis_prefix,
                                                atlas_type))
analysis_dir = os.path.join(analysis_base, analysis_prefix)

sids = ['Reg_S64550']

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

work_dir = os.path.join('/om2/scratch/ksitek/dipy_csd/',
                        '%s_%s/'%(analysis_prefix,
                                  atlas_type))

# filter tractography streamlines from specific regions of interest
if atlas_type == 'func-atlas':
    atlas_file = os.path.join('/om2/user/ksitek/exvivo/maastricht/',
                              'atlas/maas-atlas2exvivo_ants_Linear.nii.gz')
    atlas_labels = [x+1 for x in range(8)] # labels 1-8
else:
    atlas_file = os.path.join('/om2/user/ksitek/exvivo/atlas/',
                              #'archive_segs',
                              #'auditory_brainstem_8-structures_0826_atlas2diff_Similarity_Affine_MI_16x8x4x2_MultiLabel.nii.gz')
                              #'segs_201812',
                              #'auditory_brainstem_nuclei_201812_8-structures_to_Reg_S64550_nii_b0-slice_dilD-sphere-0.5.nii.gz')
                              'conjunctions',
                              #'auditory_brainstem_nuclei_conj_kevin_v2_faruk_v1_100um_to_Reg_S64550_nii_b0-slice.nii.gz')
                              'auditory_brainstem_nuclei_conj_' \
                              'kevin_v1_faruk_v1_100um_' \
                              'to_Reg_S64550_nii_b0-slice' \
                              #'_dilD-sphere-500um.nii.gz'
                              '.nii.gz'
                              )

    #atlas_labels = [x+1 for x in range(8)] # labels in current anatomical atlas
    atlas_labels = [x+1 for x in range(12)] # labels in current anatomical atlas

# grab input data - from dipy_csd.dmri_recon()
if resolution == '0.2mm':
    filename = 'Reg_S64550_nii4d.nii'
    fimg = os.path.abspath(glob(os.path.join(data_dir, 'diff', filename))[0])
else:
    filename = 'Reg_S64550_nii4d_resamp-%s.nii.gz'%(resolution)
    fimg = os.path.abspath(glob(os.path.join(data_dir,'diff',
                                             'resample',
                                             filename))[0])
print("dwi file = %s"%fimg)
fbvec = os.path.abspath(glob(os.path.join(data_dir, 'diff', 'bvecs',
                                          'camino_120_RAS_flipped-xy.bvecs'))[0])
print("bvec file = %s"%fbvec)
fbval = os.path.abspath(glob(os.path.join(data_dir, 'diff', 'bvecs',
                                          'camino_120_RAS.bvals'))[0])
print("bval file = %s"%fbval)

all_streamlines = os.path.join(analysis_dir, 'recon',
                               'Reg_S64550_csd_det_streamline.trk')
fa_file = os.path.join(analysis_dir, 'recon',
                       'Reg_S64550_tensor_fa.nii.gz')

# iterate through the labels
iden = Node(IdentityInterface(fields=['label']), name="identity")
iden.iterables = [("label", atlas_labels)]

# extract the seed ROI from an atlas file
def extract_region(atlas_file, label):
    from nipype.interfaces.base import CommandLine
    from nipype.pipeline.engine import Node
    import os
    from glob import glob
    node = Node(CommandLine('fslmaths %s -thr %s -uthr %s ' \
                            'region_%s.nii.gz'%(atlas_file, label,
                                                label, label)),
                name='extract_roi')
    cwd = os.getcwd()
    print("cwd = ", cwd)
    node.base_dir = cwd
    node.config = {'execution': {'keep_unnecessary_outputs': 'true'}}
    node.run()
    single_region = os.path.realpath(os.path.join(cwd, 'extract_roi',
                                                  'region_%s.nii.gz'%label))

    print('single region mask file: ', single_region)
    assert os.path.exists(single_region)
    return single_region, label, atlas_file

region_extracter = Node(Function(input_names = ['atlas_file','label'],
                                 output_names = ['single_region',
                                                 'label',
                                                 'atlas_file'],
                                 function = extract_region),
                                 name = 'region_extracter')
region_extracter.config = {'execution': {'keep_unnecessary_outputs': 'true'}}

# filter streamlines by seed region of interest
def sl_filter(streamlines, target_mask, affine, label):
    from dipy.tracking.utils import target
    from nilearn.image import resample_img
    import numpy as np
    import os

    import nibabel as nib
    trk_file = nib.streamlines.load(streamlines)
    streams = trk_file.streamlines
    hdr = trk_file.header

    # resample mask to resolution of input data & get data
    target_resamp = resample_img(target_mask, affine)
    target_mask_bool = np.zeros(target_resamp.shape)
    target_mask_bool[target_resamp.get_data().round()>0]=1 # rounding is key!

    target_sl_generator = target(streams, target_mask_bool,
                                 affine, include=True)
    target_streams = list(target_sl_generator)

    # create new filtered streamlines .trk file
    tractogram = nib.streamlines.Tractogram(target_streams)
    tractogram.affine_to_rasmm = np.eye(4)
    trk_file = nib.streamlines.TrkFile(tractogram, header=hdr)

    target_streamlines = os.path.abspath('target_streamlines_region_%d.trk'%label)
    nib.streamlines.save(trk_file, target_streamlines)

    return target_streamlines, label, target_mask

filter_streamlines = Node(Function(input_names = ['streamlines', 'target_mask',
                                                  'affine', 'label'],
                                   output_names = ['target_streamlines',
                                                   'label', 'target_mask'],
                                   function = sl_filter),
                                   name = 'filter_streamlines')
filter_streamlines.inputs.streamlines = all_streamlines

import nibabel as nib
fa_img = nib.load(fa_file)
affine = fa_img.affine
filter_streamlines.inputs.affine = affine

# filter streamlines AGAIN - did it for each seed, also filter for each target
iden_target = Node(IdentityInterface(fields=['target_label']),
                   name="identity_target")
iden_target.iterables = [("target_label", atlas_labels)]

# extract target ROI
def extract_region_target(atlas_file, label):
    from nipype.interfaces.base import CommandLine
    from nipype.pipeline.engine import Node
    import os
    from glob import glob
    node = Node(CommandLine('fslmaths %s -thr %s -uthr %s region_%s.nii.gz'%(atlas_file,
                                                                             label,
                                                                             label,
                                                                             label)),
                name='extract_roi')
    cwd = os.getcwd()
    print("cwd = ", cwd)
    node.base_dir = cwd
    node.config = {'execution': {'keep_unnecessary_outputs': 'true'}}
    node.run()
    single_region = os.path.realpath(os.path.join(cwd, 'extract_roi',
                                                  'region_%s.nii.gz'%label))

    print('single region mask file: ', single_region)
    assert os.path.exists(single_region)
    return single_region, label

region_extracter_target = Node(Function(input_names = ['atlas_file','label'],
                                 output_names = ['single_region', 'label'],
                                 function = extract_region_target),
                                 name = 'region_extracter_target')
region_extracter_target.config = {'execution':{'keep_unnecessary_outputs':'true'}}

# filter streamlines by target ROI (for each seed ROI)
def sl_filter_target(streamlines, target_mask, affine, seed_label, target_label):
    from dipy.tracking.utils import target
    from nilearn.image import resample_img
    import numpy as np
    import os

    import nibabel as nib
    trk_file = nib.streamlines.load(streamlines)
    streams = trk_file.streamlines
    hdr = trk_file.header

    # resample mask to resolution of input data & get data
    target_resamp = resample_img(target_mask, affine)
    target_mask_bool = np.zeros(target_resamp.shape)
    target_mask_bool[target_resamp.get_data().round()>0]=1 # rounding is key!

    target_sl_generator = target(streams, target_mask_bool, affine, include=True)
    target_streams = list(target_sl_generator)

    # create new filtered streamlines .trk file
    tractogram = nib.streamlines.Tractogram(target_streams)
    tractogram.affine_to_rasmm = np.eye(4)
    trk_file = nib.streamlines.TrkFile(tractogram, header=hdr)

    target_streamlines = os.path.abspath('target_streamlines_' \
                                         'seed-%d_target-%d.trk'%(seed_label,
                                                                  target_label))
    nib.streamlines.save(trk_file, target_streamlines)

    return target_streamlines, seed_label, target_label

filter_streamlines_target = Node(Function(input_names=['streamlines',
                                                       'target_mask',
                                                       'affine',
                                                       'seed_label',
                                                       'target_label'],
                                   output_names = ['target_streamlines',
                                                   'seed_label',
                                                   'target_label'],
                                   function = sl_filter_target),
                                   name = 'filter_streamlines_target')
filter_streamlines_target.inputs.affine = affine

# reduce unlikely streamlines with linear fascicle evaluation
def life(streamline_file, data_file, bvals, bvecs, seed_label, target_label):
    import numpy as np
    import nibabel as nib
    import os
    import dipy.tracking.life as life
    from dipy.core.gradients import gradient_table

    trk_file = nib.streamlines.load(streamline_file)
    streams = trk_file.streamlines
    hdr = trk_file.header

    data_img = nib.load(data_file)
    data = data_img.get_data()

    gtab = gradient_table(bvals, bvecs)
    fiber_model = life.FiberModel(gtab)
    fiber_fit = fiber_model.fit(data, streams, affine=np.eye(4))

    optimized_sl = list(np.array(streams)[np.where(fiber_fit.beta>0)[0]])

    tractogram = nib.streamlines.Tractogram(optimized_sl)
    tractogram.affine_to_rasmm = data_img.affine
    life_streams = nib.streamlines.TrkFile(tractogram, header=hdr)

    life_trk = os.path.abspath('life_seed-%d_target-%d.trk'%(seed_label,
                                                             target_label))
    nib.streamlines.save(life_streams, life_trk)

    return streamline_file, life_trk
'''
life = Node(Function(input_names = ['streamline_file', 'data_file',
                                    'bvals', 'bvecs',
                                    'seed_label', 'target_label'],
                     output_names = ['streamline_file', 'life_trk'],
                     function = life),
                     name = 'life')
life.inputs.data_file = fimg
life.inputs.bvals = fbval
life.inputs.bvecs = fbvec
'''
# define inputs to the workflow
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'atlas_file',
                                            ]),
                                    name='infosource')
infosource.inputs.subject_id = sids[0]
infosource.inputs.atlas_file = atlas_file

# create the output data sink
ds = Node(DataSink(parameterization=False), name='sinker')
ds.inputs.base_directory = out_dir
ds.plugin_args = {'overwrite': True}

# create the nipype workflow and connect nodes' inputs/outputs
wf = Workflow(name='exvivo')
wf.config['execution']['crashfile_format'] = 'txt'

wf.connect(infosource, 'atlas_file', region_extracter, 'atlas_file')
wf.connect(iden, 'label', region_extracter, 'label')

wf.connect(region_extracter, 'single_region', filter_streamlines, 'target_mask')
wf.connect(region_extracter, 'label', filter_streamlines, 'label')

wf.connect(iden_target, 'target_label', region_extracter_target, 'label')
wf.connect(region_extracter, 'atlas_file',
           region_extracter_target, 'atlas_file')

wf.connect(filter_streamlines, 'target_streamlines',
           filter_streamlines_target, 'streamlines')
wf.connect(filter_streamlines, 'label',
           filter_streamlines_target, 'seed_label')

wf.connect(region_extracter_target, 'single_region',
           filter_streamlines_target, 'target_mask')
wf.connect(region_extracter_target, 'label',
           filter_streamlines_target, 'target_label')

"""wf.connect(filter_streamlines_target, 'target_streamlines',
              life, 'streamline_file')
wf.connect(filter_streamlines_target, 'seed_label', life, 'seed_label')
wf.connect(filter_streamlines_target, 'target_label', life, 'target_label')
"""
# output data to the data sink
wf.connect(filter_streamlines_target, 'target_streamlines',
           ds, 'target_streamlines')
"""
wf.connect(life, 'streamline_file', ds, 'target_streamlines')
wf.connect(life, 'life_trk', ds, 'life')
"""
# definte the working directory and run the workflow
wf.base_dir = work_dir
wf.run(plugin='MultiProc', plugin_args={'n_procs' : 10})
