// VTC creation. Native to ACPC to Talairach space (0.5 mm iso.)
// 1x1x1 subcortical vtc with bounding box.
//
// NOTE: Both sessions are processed together. Which means that at this stage
// session3 functional should be aligned to session2 reference volume.
// If this was not done, process different sessions separately by using IA and
// FA transformation files that align those sessions to main anatomical image.

var bvqx = BrainVoyagerQX;
bvqx.PrintToLog("------");

// Enter the following values:
var OutDataPath = "/media/Data_Drive/S11_SES2_PREP/VTC/";
var NumberOfRuns = 25;
var AnatomicalData = "/media/Data_Drive/ISILON/002_ANAT/11/T1_512/S11_SES1_T1_pt5_divPD_IIHC_TAL.vmr";

var IA_TRFList = ["/path/to/S11_RUN_01-TO-SES2_T1_IA.trf"];
var FA_TRFList = ["/path/to/S11_RUN_01-TO-SES2_T1_FA.trf"];
var ACPC_TRFList = ["/path/to/S11_SES2_T1-TO-SES1_T1_ACPC.trf"];
var TAL_List = ["/path/to/S11_SES1_T1_pt5_ACPC.tal"];

var InFmrList = [
    "path/to/session2/S01_RUN_01_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_01_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_02_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_03_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_04_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_05_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_06_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_07_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_08_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_09_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_10_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_11_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session2/S01_RUN_12_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_01_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",  // session 3 fmr's are assumed to be registered to session 2 at this point
    "path/to/session3/S01_RUN_02_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_03_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_04_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_05_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_06_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_07_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_08_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_09_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_10_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_11_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",
    "path/to/session3/S01_RUN_12_SCSTBL_3DMCTS_LTR_THPGLMF6c_TDTS2.0dp_TU.fmr",];

//Output Talairach vtc file names
var OutVTCNameList = [
    "delete_this_file.vtc",  // Because BV creates the first extended TAL vtc incorrectly
    "S11_run1_sc.vtc",
    "S11_run2_sc.vtc",
    "S11_run3_sc.vtc",
    "S11_run4_sc.vtc",
    "S11_run5_sc.vtc",
    "S11_run6_sc.vtc",
    "S11_run7_sc.vtc",
    "S11_run8_sc.vtc",
    "S11_run9_sc.vtc",
    "S11_run10_sc.vtc",
    "S11_run11_sc.vtc",
    "S11_run12_sc.vtc",
    "S11_run13_sc.vtc",
    "S11_run14_sc.vtc",
    "S11_run15_sc.vtc",
    "S11_run16_sc.vtc",
    "S11_run17_sc.vtc",
    "S11_run18_sc.vtc",
    "S11_run19_sc.vtc",
    "S11_run20_sc.vtc",
    "S11_run21_sc.vtc",
    "S11_run22_sc.vtc",
    "S11_run23_sc.vtc",
    "S11_run24_sc.vtc"];

// ============================================================================
// Open an anatomical data
var docVMR = bvqx.OpenDocument(AnatomicalData);

// Specify bounding box for target VTC
docVMR.ExtendedTALSpaceForVTCCreation = true;
docVMR.UseBoundingBoxForVTCCreation = true;
docVMR.TargetVTCBoundingBoxXStart = 201;
docVMR.TargetVTCBoundingBoxXEnd   = 315;
docVMR.TargetVTCBoundingBoxYStart = 267;
docVMR.TargetVTCBoundingBoxYEnd   = 338;
docVMR.TargetVTCBoundingBoxZStart = 214;
docVMR.TargetVTCBoundingBoxZEnd   = 367;

for(count = 1; count <= NumberOfRuns; count++){
    var InFmrPath = InFmrList[count-1];
    var OutVTCName = OutDataPath + OutVTCNameList[count-1];
    var IA_Path = IA_TRFList[0];
    var FA_Path = FA_TRFList[0];

    bvqx.PrintToLog(docVMR.TargetVTCBoundingBoxXStart);
    bvqx.PrintToLog(docVMR.TargetVTCBoundingBoxXEnd);
    bvqx.PrintToLog(docVMR.TargetVTCBoundingBoxYStart);
    bvqx.PrintToLog(docVMR.TargetVTCBoundingBoxYEnd);
    bvqx.PrintToLog(docVMR.TargetVTCBoundingBoxZStart);
    bvqx.PrintToLog(docVMR.TargetVTCBoundingBoxZEnd);

    // Create VTC in TAL Space
    docVMR.CreateVTCInTALSpace(InFmrPath,
                                IA_Path,  // IA.trf
                                FA_Path,  // FA.trf
                                ACPC_TRFList[0],  // *_ACPC.trf
                                TAL_List[0],  // *.tal
                                OutVTCName,  // output name
                                2,   // datatype integer 2-byte format:1 or float format:2
                                1,   // target resolution 1x1x1:1 or 2x2x2:2 or 3x3x3:3
                                2,   // nearest neighbour:0 or trilinear:1 or sinc:2
                                100  // threshold(Default value:100)
                                );

    bvqx.PrintToLog(OutVTCName + " finished.");
};

bvqx.PrintToLog("***The_end***.");
