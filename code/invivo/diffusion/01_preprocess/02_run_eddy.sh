#!/bin/bash

# Main processing - Run eddy#######################################

workingdir='workingdir/eddy'
topupdir='workingdir/topup'

${FSLDIR}/bin/imcp ${topupdir}/nodif_brain_mask ${workingdir}/

eddy_command="${FSLDIR}/bin/eddy " #standart eddy
eddy_command+="--imain=${workingdir}/Pos_Neg "
eddy_command+="--mask=${workingdir}/nodif_brain_mask "
eddy_command+="--index=${workingdir}/series_index.txt "
eddy_command+="--acqp=${workingdir}/acqparams.txt "
eddy_command+="--bvecs=${workingdir}/Pos_Neg.bvecs "
eddy_command+="--bvals=${workingdir}/Pos_Neg.bvals "
eddy_command+="--fwhm=0 "
eddy_command+="--topup=${topupdir}/topup_Pos_Neg_b0 "
eddy_command+="--out=${workingdir}/eddy_unwarped_images "
eddy_command+="--flm=quadratic "
eddy_command+="--very_verbose "

echo "About to issue the following eddy command: "
echo "${eddy_command}"
${eddy_command}
eddyReturnValue=$?

echo "Completed with return value: ${eddyReturnValue}"

