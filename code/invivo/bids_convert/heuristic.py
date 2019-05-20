import os

def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    ''' SES01 '''
    t1w_pt7 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
    pdw_pt7 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_PD')
    t2s = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T2star')
    t1ShortInv_pt7 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ShortInv_run-{item:02d}_T1w')

    dwi_ap = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_dir-AP_run-{item:02d}_dwi')
    dwi_pa = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_dir-PA_run-{item:02d}_dwi')

    bold_AP = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-gre_dir-AP_run-{item:02d}_epi')
    bold_PA = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-gre_dir-PA_run-{item:02d}_epi')
    se_AP = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-se_dir-AP_run-{item:02d}_epi')
    se_PA = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-se_dir-PA_run-{item:02d}_epi')

    rs = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_bold')

    ''' SES02 & SES03 '''
    t1w_iso1 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-1mm_T1w')
    pdw_iso1 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-1mm_PD')
    task = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-auditory_run-{item:02d}_bold')

    info = {t1w_pt7:[], pdw_pt7:[], t2s:[], t1ShortInv_pt7:[],
            dwi_ap:[], dwi_pa:[],
            bold_AP:[], bold_PA:[],
            se_AP:[], se_PA:[], rs:[],
            t1w_iso1:[], pdw_iso1:[], task:[]}

    for idx, s in enumerate(seqinfo):
        # anat
        if ('t1_mprage_iso0.6' in s.series_description):
            info[t1w_pt7].append([s.series_id])
        if ('pd_mprage_iso0.6' in s.series_description):
            info[pdw_pt7].append([s.series_id])
        if ('T2s' in s.series_description):
            info[t2s].append([s.series_id])
        if ('t1ShortInv' in s.series_description):
            info[t1ShortInv_pt7].append([s.series_id])
        if ('t1_mprage_iso1' in s.series_description):
            info[t1w_iso1].append([s.series_id])
        if ('pd_mprage_iso1' in s.series_description):
            info[pdw_iso1].append([s.series_id])

        # DWI
        if ('DWI_AP' in s.series_description):
            info[dwi_ap].append([s.series_id])
        if ('DWI_PA' in s.series_description):
            info[dwi_pa].append([s.series_id])

        # functional
        if ('bold_AP' in s.protocol_name):
            if ('run' in s.series_id):
                info[task].append([s.series_id])
            else:
                info[bold_AP].append([s.series_id])
        if ('bold_PA' in s.protocol_name):
            info[bold_PA].append([s.series_id])
        if ('se_AP' in s.protocol_name):
            info[se_AP].append([s.series_id])
        if ('se_PA' in s.protocol_name):
            info[se_PA].append([s.series_id])

    return info
