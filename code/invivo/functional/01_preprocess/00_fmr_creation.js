// FMR creation
//
// NOTE: Different sessions are processed independently

var bvqx = BrainVoyagerQX;
bvqx.PrintToLog("------");

// Enter the following values:
var MainDataPath = "/path/to/session2/";
var RunPrefix = "RUN_";

// Enter the first dicom file paths per run.
var InDicomList = [
    "/path/to/session2_run01_volume000.dcm",
    "/path/to/session2_run02_volume000.dcm",
    "/path/to/session2_run03_volume000.dcm",
    "/path/to/session2_run04_volume000.dcm",
    "/path/to/session2_run05_volume000.dcm",
    "/path/to/session2_run06_volume000.dcm",
    "/path/to/session2_run07_volume000.dcm",
    "/path/to/session2_run08_volume000.dcm",
    "/path/to/session2_run09_volume000.dcm",
    "/path/to/session2_run10_volume000.dcm",
    "/path/to/session2_run11_volume000.dcm",
    "/path/to/session2_run12_volume000.dcm"];

// Enter the run names.
var RunNameList = [
    "S01_RUN_01",
    "S01_RUN_02",
    "S01_RUN_03",
    "S01_RUN_04",
    "S01_RUN_05",
    "S01_RUN_06",
    "S01_RUN_07",
    "S01_RUN_08",
    "S01_RUN_09",
    "S01_RUN_10",
    "S01_RUN_11"];

var NrVolPerRunList = [
    150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150];

// ============================================================================

var NrOfRuns = InDicomList.length;

for(count = 1; count <= NrOfRuns; count++){

    var RunPath = MainDataPath + RunPrefix + String(count) + "/";
    var RunName = RunNameList[count-1];
    var InDicomPath = InDicomList[count-1];

    // Create FMR Project
    var docFMR = bvqx.CreateProjectMosaicFMR(
        "DICOM", InDicomPath,
        NrVolPerRunList[count-1],  //nr of volumes
        0,          //nr of volumes to skip
        false,      //create AMR
        46,         //nr of slices
        RunName,    //STC prefix
        false,      //swap bytes
        1316, 1316, //dimension of images in volume x, y
        2,          //nr of bytes per pixel, usually 2
        RunPath,    //saving directory
        1,          //number of volumes per file
        188, 188    //dimension of image x, y
        );

    docFMR.SaveAs(RunName);

    bvqx.PrintToLog(RunName + " finished.");
};

bvqx.PrintToLog("***The_end***.");
