// Spatial smoothing for vtc files.
// 1x1x1 subcortical vtc with bounding box.

var bvqx = BrainVoyagerQX;
bvqx.PrintToLog("------");

// Enter the following values:
var NumberOfRuns = 24;
var AnatomicalData = "/path/to/anatomical_in_talairach_0pt5.vmr";

//Output Talairach vtc file names
var VTCNameList =  [
    "/path/to/S01_run1_sc.vtc",
    "/path/to/S01_run2_sc.vtc",
    "/path/to/S01_run3_sc.vtc",
    "/path/to/S01_run4_sc.vtc",
    "/path/to/S01_run5_sc.vtc",
    "/path/to/S01_run6_sc.vtc",
    "/path/to/S01_run7_sc.vtc",
    "/path/to/S01_run8_sc.vtc",
    "/path/to/S01_run9_sc.vtc",
    "/path/to/S01_run10_sc.vtc",
    "/path/to/S01_run11_sc.vtc",
    "/path/to/S01_run12_sc.vtc",
    "/path/to/S01_run13_sc.vtc",
    "/path/to/S01_run14_sc.vtc",
    "/path/to/S01_run15_sc.vtc",
    "/path/to/S01_run16_sc.vtc",
    "/path/to/S01_run17_sc.vtc",
    "/path/to/S01_run18_sc.vtc",
    "/path/to/S01_run19_sc.vtc",
    "/path/to/S01_run20_sc.vtc",
    "/path/to/S01_run21_sc.vtc",
    "/path/to/S01_run22_sc.vtc",
    "/path/to/S01_run23_sc.vtc",
    "/path/to/S01_run24_sc.vtc"];

// ============================================================================
// Open an anatomical data
var docVMR = bvqx.OpenDocument(AnatomicalData);

for(count = 1; count <= NumberOfRuns; count++){
    // Link VTC to Anatomical
    docVMR.LinkVTC(VTCNameList[count-1]);

    // Spatial smoothing on vtc
    docVMR.SpatialGaussianSmoothing(3, "vx");  // FWHM value and unit ("mm" or "vx")
    BrainVoyagerQX.PrintToLog("Name of spatially smoothed VTC file: " + docVMR.FileNameOfCurrentVTC);

    // // Save VTC
    // docVMR.SaveVTC("")

    bvqx.PrintToLog(VTCNameList[count-1] + " finished.");
};

bvqx.PrintToLog("***The_end***.");
