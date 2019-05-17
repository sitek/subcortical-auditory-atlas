#!/bin/bash
set -e
echo -e "\n START: eddy_postproc"

#Hard-Coded filename. Flag from eddy to indicate that the jac method has been used for resampling
EddyJacFlag="JacobianResampling" 

workingdir='workingdir'
GdCoeffs="NONE"  #Coefficients for gradient nonlinearity distortion correction. If "NONE" this corrections is turned off #Faruk: I have deleted the corresponding lines of code for now since "NONE".
CombineDataFlag=1
globalscriptsdir='workingdir/scripts'

eddydir=${workingdir}/eddy
datadir=${workingdir}/data

#Prepare for next eddy Release
#if [ ! -e ${eddydir}/${EddyJacFlag} ]; then 
#    echo "LSR resampling has been used. Eddy Output has already been combined."
#    cp ${eddydir}/Pos.bval ${datadir}/bvals
#    cp ${eddydir}/Pos.bvec ${datadir}/bvecs
#    $FSLDIR/bin/imcp ${eddydir}/eddy_unwarped_images ${datadir}/data
#else
    if [ ${CombineDataFlag} -eq 2 ]; then
	${FSLDIR}/bin/imcp  ${eddydir}/eddy_unwarped_images ${datadir}/data
	cp ${eddydir}/Pos_Neg.bvals ${datadir}/bvals
	cp ${eddydir}/Pos_Neg.bvecs ${datadir}/bvecs
    else
	echo "JAC resampling has been used. Eddy Output is now combined."
	PosVols=`wc ${eddydir}/Pos.bval | awk {'print $2'}`
	NegVols=`wc ${eddydir}/Neg.bval | awk {'print $2'}`    #Split Pos and Neg Volumes
	${FSLDIR}/bin/fslroi ${eddydir}/eddy_unwarped_images ${eddydir}/eddy_unwarped_Pos 0 ${PosVols}
	${FSLDIR}/bin/fslroi ${eddydir}/eddy_unwarped_images ${eddydir}/eddy_unwarped_Neg ${PosVols} ${NegVols}
	${FSLDIR}/bin/eddy_combine ${eddydir}/eddy_unwarped_Pos ${eddydir}/Pos.bval ${eddydir}/Pos.bvec ${eddydir}/Pos_SeriesVolNum.txt \
                                        ${eddydir}/eddy_unwarped_Neg ${eddydir}/Neg.bval ${eddydir}/Neg.bvec ${eddydir}/Neg_SeriesVolNum.txt ${datadir} ${CombineDataFlag}

	${FSLDIR}/bin/imrm ${eddydir}/eddy_unwarped_Pos
	${FSLDIR}/bin/imrm ${eddydir}/eddy_unwarped_Neg
	#rm ${eddydir}/Pos.bv*
	#rm ${eddydir}/Neg.bv*
    fi
#fi

#Remove negative intensity values (caused by spline interpolation) from final data
${FSLDIR}/bin/fslmaths ${datadir}/data -thr 0 ${datadir}/data
${FSLDIR}/bin/bet ${datadir}/data ${datadir}/nodif_brain -m -f 0.1
$FSLDIR/bin/fslroi ${datadir}/data ${datadir}/nodif 0 1

echo -e "\n END: eddy_postproc"

