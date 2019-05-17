% FSL applytopup wrapper for BV fmr files.
%
% Dependencies
% ------------
% neuroelf
% FSL 5.0.9

clc; clear all;

% Change directory to topup folder (pathOut)
pathIn    = '/path/to/subject/';
pathTopup = '/path_to/subject/topup';
cd(pathTopup)

epiNames = {
    '/path/to/RUN_2/S01_RUN_02_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_3/S01_RUN_03_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_4/S01_RUN_04_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_5/S01_RUN_05_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_6/S01_RUN_06_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_7/S01_RUN_07_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_8/S01_RUN_08_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_9/S01_RUN_09_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_10/S01_RUN_10_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_11/S01_RUN_11_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr',
    '/path/to/RUN_12/S01_RUN_12_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp.fmr'}

%% Load .fmr time series, convert to nifti
nrEpis=length(epiNames);
disp('Converting to nifti...')
for i=1:nrEpis;
    [inPath, inFileName, ~] = fileparts([pathIn, epiNames{i}]);
    [~, outFileName, ~] = fileparts([pathTopup, epiNames{i}]);
    epi = xff(fullfile(inPath, [inFileName,'.fmr']));
    epi.Write4DNifti(outFileName,'nii');
    epi.ClearObject;
    disp([num2str(i) '/' num2str(nrEpis) ' is converted.'])
end;

%% Apply topup
for i=1:nrEpis;
    [inPath, fmrBaseName, ~] = fileparts([pathIn, epiNames{i}]);
    disp('Changing NaNs to zeros...')
    unix(['fsl5.0-fslmaths ', [fmrBaseName,'.nii '], '-nan ', [fmrBaseName,'.nii.gz ']])
    unix(['rm ', [fmrBaseName, '.nii']]);
    disp('Applying topup...')
    unix(['fsl5.0-applytopup -i ', [fmrBaseName, '.nii.gz'],...
          ' -a acqparams.txt ',...
          '--topup=topup_results ',...
          '--inindex=1 ',... % NOTE: Be sure to have this correct.
          '--method=jac ',...
          '--interp=spline --verbose ',...
          '--out=',[fmrBaseName, '_corrected.nii.gz '],...
          ]);

    unix(['gunzip ', [fmrBaseName, '_corrected.nii.gz']]);
    unix(['rm -rf ', [fmrBaseName, '_corrected.nii.gz']]);
    tempNii=xff([fmrBaseName, '_corrected.nii']);

    % Convert back to .fmr
    tempFmr=tempNii.Dyn3DToFMR;
    fmrProp=xff(fullfile(inPath, [fmrBaseName,'.fmr']));

    % Position information
    fmrProp.Slice.STCData = tempFmr.Slice.STCData;

    % Save with 'TU' suffix
    fmrProp.SaveAs(fullfile(inPath, [fmrBaseName,'_TU.fmr']));
    unix(['rm -rf ', [fmrBaseName, '_corrected.nii']]);
    unix(['rm -rf ', [fmrBaseName, '.nii']]);
    disp([num2str(i) '/' num2str(nrEpis) ' is computed.']);
end;
disp('Done.')
