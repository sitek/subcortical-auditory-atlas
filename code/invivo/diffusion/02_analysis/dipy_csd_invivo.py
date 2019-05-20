from nipype import config
config.set('execution', 'remove_unnecessary_outputs', 'false')
config.set('execution', 'crashfile_format', 'txt')

#config.enable_provenance()

from nipype import Node, Function, Workflow, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink

import os
from glob import glob

out_prefix = 'fathresh-0.5'
#dirs = '45-dirs'
dirs = ''
num_threads =  12

data_dir = '/om2/user/ksitek/maastricht/diffusion_faruk/data/01_diff_preprocessed'
out_dir = '/om2/user/ksitek/maastricht/diffusion_faruk/analysis/%s/'%(out_prefix)

sids = ['S02']
#sids = ['S%02d' %s for s in range(1,12)]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

work_dir = os.path.abspath('/om2/scratch/ksitek/dipy_csd_invivo/%s_0114/'%(out_prefix))

def dmri_recon(sid, data_dir, out_dir, recon='csd', dirs = '', num_threads=2):
    import tempfile
    #tempfile.tempdir = '/om/scratch/Fri/ksitek/'

    import os
    oldval = None
    if 'MKL_NUM_THREADS' in os.environ:
        oldval = os.environ['MKL_NUM_THREADS']
    os.environ['MKL_NUM_THREADS'] = '%d' % num_threads
    ompoldval = None
    if 'OMP_NUM_THREADS' in os.environ:
        ompoldval = os.environ['OMP_NUM_THREADS']
    os.environ['OMP_NUM_THREADS'] = '%d' % num_threads
    import nibabel as nib
    import numpy as np
    from glob import glob

    filename = 'data.nii.gz'
    fimg = os.path.abspath(glob(os.path.join(data_dir, sid, filename))[0])
    print("dwi file = %s"%fimg)
    fbval = os.path.abspath(glob(os.path.join(data_dir, sid, 'bvals'))[0])
    print("bval file = %s"%fbval)
    fbvec = os.path.abspath(glob(os.path.join(data_dir, sid, 'bvecs'))[0])
    print("bvec file = %s"%fbvec)

    img = nib.load(fimg)
    data = img.get_data()

    affine = img.get_affine()

    prefix = sid

    from dipy.io import read_bvals_bvecs
    bvals, bvecs = read_bvals_bvecs(fbval, fbvec)

    from dipy.core.gradients import gradient_table
    gtab = gradient_table(bvals, bvecs, b0_threshold=100)
    gtab.bvecs.shape == bvecs.shape
    gtab.bvecs
    gtab.bvals.shape == bvals.shape
    gtab.bvals


    from dipy.reconst.csdeconv import auto_response
    response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.5) # 0.7

    '''
    mask_name = 'nodif_brain_mask.nii.gz'
    fmask1 = os.path.join(data_dir, sid, mask_name)
    '''
    mask_dir = os.path.join('/om2/user/ksitek/maastricht/',
                            'diffusion_faruk/data/06_diffusion_space/')
    mask_name = '%s_diff_bstem_mask.nii.gz'%sid
    fmask1 = os.path.join(mask_dir, mask_name)

    print("fmask file = %s"%fmask1)
    mask = nib.load(fmask1).get_data()

    useFA = True
    print("creating model")
    if recon == 'csd':
        from dipy.reconst.csdeconv import ConstrainedSphericalDeconvModel
        model = ConstrainedSphericalDeconvModel(gtab, response)
        useFA = True
    elif recon == 'csa':
        from dipy.reconst.shm import CsaOdfModel, normalize_data
        model = CsaOdfModel(gtab, 4)
        useFA = False
    else:
        raise ValueError('only csd, csa supported currently')
        from dipy.reconst.dsi import (DiffusionSpectrumDeconvModel,
                                      DiffusionSpectrumModel)
        model = DiffusionSpectrumDeconvModel(gtab)
    fit = model.fit(data)

    from dipy.data import get_sphere
    sphere = get_sphere('symmetric724')

    from dipy.reconst.peaks import peaks_from_model
    print("running peaks_from_model")
    peaks = peaks_from_model(model=model,
                             data=data,
                             sphere=sphere,
                             mask=mask,
                             return_sh=True,
                             return_odf=False,
                             normalize_peaks=True,
                             npeaks=5,
                             relative_peak_threshold=.5,
                             min_separation_angle=25,
                             parallel=num_threads > 1,
                             nbr_processes=num_threads)

    from dipy.reconst.dti import TensorModel
    print("running tensor model")
    tenmodel = TensorModel(gtab)
    tenfit = tenmodel.fit(data, mask)

    from dipy.reconst.dti import fractional_anisotropy
    print("running FA")
    FA = fractional_anisotropy(tenfit.evals)
    FA[np.isnan(FA)] = 0
    fa_img = nib.Nifti1Image(FA, img.get_affine())
    tensor_fa_file = os.path.abspath('%s_tensor_fa.nii.gz' % (prefix))
    nib.save(fa_img, tensor_fa_file)

    from dipy.reconst.dti import axial_diffusivity
    print("running AD")
    AD = axial_diffusivity(tenfit.evals)
    AD[np.isnan(AD)] = 0
    ad_img = nib.Nifti1Image(AD, img.get_affine())
    tensor_ad_file = os.path.abspath('%s_tensor_ad.nii.gz' % (prefix))
    nib.save(ad_img, tensor_ad_file)

    from dipy.reconst.dti import radial_diffusivity
    print("running RD")
    RD = radial_diffusivity(tenfit.evals)
    RD[np.isnan(RD)] = 0
    rd_img = nib.Nifti1Image(RD, img.get_affine())
    tensor_rd_file = os.path.abspath('%s_tensor_rd.nii.gz' % (prefix))
    nib.save(rd_img, tensor_rd_file)

    from dipy.reconst.dti import mean_diffusivity
    print("running MD")
    MD = mean_diffusivity(tenfit.evals)
    MD[np.isnan(MD)] = 0
    md_img = nib.Nifti1Image(MD, img.get_affine())
    tensor_md_file = os.path.abspath('%s_tensor_md.nii.gz' % (prefix))
    nib.save(md_img, tensor_md_file)

    evecs = tenfit.evecs
    evec_img = nib.Nifti1Image(evecs, img.get_affine())
    tensor_evec_file = os.path.abspath('%s_tensor_evec.nii.gz' % (prefix))
    nib.save(evec_img, tensor_evec_file)

    shm_coeff = fit.shm_coeff
    shm_coeff_file = os.path.abspath('%s_shm_coeff.nii.gz' % (prefix))
    nib.save(nib.Nifti1Image(shm_coeff, img.get_affine()), shm_coeff_file)

    #from dipy.reconst.dti import quantize_evecs
    #peak_indices = quantize_evecs(tenfit.evecs, sphere.vertices)
    #eu = EuDX(FA, peak_indices, odf_vertices = sphere.vertices,
               #a_low=0.2, seeds=10**6, ang_thr=35)

    fa_img = nib.Nifti1Image(peaks.gfa, img.get_affine())
    model_gfa_file = os.path.abspath('%s_%s_gfa.nii.gz' % (prefix, recon))
    nib.save(fa_img, model_gfa_file)

    from dipy.tracking.eudx import EuDX
    print("reconstructing with EuDX")
    if useFA:
        eu = EuDX(FA, peaks.peak_indices[..., 0],
                  odf_vertices = sphere.vertices,
                  #a_low=0.1,
                  seeds=10**6,
                  ang_thr=45)
    else:
        eu = EuDX(peaks.gfa, peaks.peak_indices[..., 0],
                  odf_vertices = sphere.vertices,
                  #a_low=0.1,
                  seeds=10**6,
                  ang_thr=45)

    sl_fname = os.path.abspath('%s_%s_streamline.trk' % (prefix, recon))
    """
    #import dipy.tracking.metrics as dmetrics
    streamlines = ((sl, None, None) for sl in eu) # if dmetrics.length(sl) > 15)

    hdr = nib.trackvis.empty_header()
    hdr['voxel_size'] = fa_img.get_header().get_zooms()[:3]
    hdr['voxel_order'] = 'RAS' #LAS
    hdr['dim'] = FA.shape[:3]

    nib.trackvis.write(sl_fname, streamlines, hdr, points_space='voxel')
    """
    # trying new dipy.io.streamline module, per email to neuroimaging list
    # 2018.04.05
    from nibabel.streamlines import Field
    from nibabel.orientations import aff2axcodes
    affine = img.get_affine()
    vox_size=fa_img.get_header().get_zooms()[:3]
    fov_shape=FA.shape[:3]

    if vox_size is not None and fov_shape is not None:
        hdr = {}
        hdr[Field.VOXEL_TO_RASMM] = affine.copy()
        hdr[Field.VOXEL_SIZES] = vox_size
        hdr[Field.DIMENSIONS] = fov_shape
        hdr[Field.VOXEL_ORDER] = "".join(aff2axcodes(affine))

    tractogram = nib.streamlines.Tractogram(eu)
    tractogram.affine_to_rasmm = affine
    trk_file = nib.streamlines.TrkFile(tractogram, header=hdr)
    nib.streamlines.save(trk_file, sl_fname)

    if oldval:
        os.environ['MKL_NUM_THREADS'] = oldval
    else:
        del os.environ['MKL_NUM_THREADS']
    if ompoldval:
        os.environ['OMP_NUM_THREADS'] = ompoldval
    else:
        del os.environ['OMP_NUM_THREADS']

    assert tensor_fa_file
    assert tensor_evec_file
    assert model_gfa_file
    assert tensor_ad_file
    assert tensor_rd_file
    assert tensor_md_file
    assert shm_coeff_file
    print('all output files created')

    return tensor_fa_file, tensor_evec_file, model_gfa_file, sl_fname, affine, tensor_ad_file, tensor_rd_file, tensor_md_file, shm_coeff_file

infosource = Node(IdentityInterface(fields=['subject_id']),
                                    name='infosource')
infosource.iterables = ('subject_id', sids)
#infosource.inputs.subject_id = sids[0]

tracker = Node(Function(input_names=['sid', 'data_dir', 'out_dir',
                                     'recon', 'dirs','num_threads'],
                        output_names=['tensor_fa_file',
                                      'tensor_evec_file',
                                      'model_gfa_file',
                                      'model_track_file',
                                      'affine',
                                      'tensor_ad_file',
                                      'tensor_rd_file',
                                      'tensor_md_file',
                                      'shm_coeff_file'],
                        function=dmri_recon), name='tracker')
tracker.inputs.data_dir = data_dir
tracker.inputs.out_dir = out_dir
tracker.inputs.recon = 'csd'
tracker.inputs.dirs = dirs
tracker.inputs.num_threads = num_threads
#tracker.plugin_args = {'sbatch_args': '--time=1-00:00:00 --mem=%dG -N 1 -c %d' % (10 * num_threads, num_threads),
#                       'overwrite': True}

ds = Node(DataSink(parameterization=False), name='sinker')
ds.inputs.base_directory = out_dir
ds.plugin_args = {'overwrite': True}

wf = Workflow(name='streamlines')
wf.config['execution']['crashfile_format'] = 'txt'

wf.connect(infosource, 'subject_id', tracker, 'sid')
wf.connect(infosource, 'subject_id', ds, 'container')

# data sink
wf.connect(tracker, 'tensor_fa_file', ds, 'recon.@fa')
wf.connect(tracker, 'tensor_evec_file', ds, 'recon.@evec')
wf.connect(tracker, 'model_gfa_file', ds, 'recon.@gfa')
wf.connect(tracker, 'model_track_file', ds, 'recon.@track')

wf.connect(tracker, 'tensor_ad_file', ds, 'recon.@ad')
wf.connect(tracker, 'tensor_rd_file', ds, 'recon.@rd')
wf.connect(tracker, 'tensor_md_file', ds, 'recon.@md')
wf.connect(tracker, 'shm_coeff_file', ds, 'recon.@shm_coeff')

wf.base_dir = work_dir

#wf.run(plugin='SLURM', plugin_args={'sbatch_args': '--time=3-00:00:00 --qos=gablab --mem=80G -N1 -c2'})
wf.run(plugin='MultiProc')
