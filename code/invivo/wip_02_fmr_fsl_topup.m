% FSL topup wrapper for BV fmr files.
%
% Dependencies
% ------------
% neuroelf
% FSL 5.0.9
%
% NOTE: Dont forget to prepare topup_b0_configuration.cnf and
% topup_acqparams.txt

clc; clear all;
dp = '/media/Data_Drive/ISILON/400_RESTING_STATE/TOPUP/07/';
cd(dp)

% Load AP and PA phase '.fmr'
phaseEncFilename_1 = fullfile(dp, 'AP.fmr');
phaseEncFilename_2 = fullfile(dp, 'PA.fmr');

%% Convert to nii
disp('Converting to nifti...')
phaseEnc1 = xff(phaseEncFilename_1);
phaseEnc1.Write4DNifti([phaseEncFilename_1(1:end-3),'nii']);
phaseEnc1.ClearObject;

phaseEnc2 = xff(phaseEncFilename_2);
phaseEnc2.Write4DNifti([phaseEncFilename_2(1:end-3),'nii']);
phaseEnc2.ClearObject;

%% Merge
disp('Merging files...')
unix(['fslmerge -t up_down_phase ',...
     [phaseEncFilename_1(1:end-3),'nii '],...
     [phaseEncFilename_2(1:end-3),'nii']]);

%% Topup
disp('Topup is running...')
unix(['topup --imain=up_down_phase ',...
      '--datain=acqparams.txt ',...
      '--config=b0_faruk.cnf ',...
      '--out=topup_results'
      ]);
disp('Done (topup computed).')
