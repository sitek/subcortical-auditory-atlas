// Preprocessing and SDM creation.
//
// NOTE: Different sessions are processed independently

var bvqx = BrainVoyagerQX;
bvqx.PrintToLog("------");

// Enter the following values:
var MainDataPath = "/path/to/session2/";
var RunPrefix = "RUN_";
var NumberOfRuns = 24;

// Enter fmr file paths
var InFmrList = [
    "/path/to/RUN_1/S01_RUN_01.fmr",
    "/path/to/RUN_2/S01_RUN_02.fmr",
    "/path/to/RUN_3/S01_RUN_03.fmr",
    "/path/to/RUN_4/S01_RUN_04.fmr",
    "/path/to/RUN_5/S01_RUN_05.fmr",
    "/path/to/RUN_6/S01_RUN_06.fmr",
    "/path/to/RUN_7/S01_RUN_07.fmr",
    "/path/to/RUN_8/S01_RUN_08.fmr",
    "/path/to/RUN_9/S01_RUN_09.fmr",
    "/path/to/RUN_10/S01_RUN_10.fmr",
    "/path/to/RUN_11/S01_RUN_11.fmr",
    "/path/to/RUN_12/S01_RUN_12.fmr"]

//Enter the reference fmr volume path.
var TargetVolumeFile = "/path/to/reference_run.fmr"

// ============================================================================
for(count = 1; count <= NumberOfRuns; count++){

    var RunPath = MainDataPath + RunPrefix + String(count) + "/";
    var InFmrPath = InFmrList[count-1];

    // Open the run
    var docFMR = bvqx.OpenDocument(InFmrPath);

    // Slice scan time correction
    docFMR.CorrectSliceTimingUsingTimeTable(2);  // 0: trilinear, 1: cubic spline, 2: windowed sinc
    ResultFileName = docFMR.FileNameOfPreprocessdFMR;
    docFMR.Close();
    docFMR = bvqx.OpenDocument(ResultFileName);

    // Motion Corection
    docFMR.CorrectMotionTargetVolumeInOtherRunEx(
        TargetVolumeFile,
        1, 	// target volume
        2, 	// 0 and 1:trilin./trilin., 2:trilin/sinc, 3:sinc/sinc
        false,  // use full data set(default: false)
        200,  // maximum number of iterations(default: 100)
        false,  // generate movie
        true  // motion estimation parameters in a text file
        );
    ResultFileName = docFMR.FileNameOfPreprocessdFMR;
    docFMR.Close();
    docFMR = bvqx.OpenDocument(ResultFileName);

    // High-pass filtering (note: BV first applies linear trend removal [LTR])
    docFMR.TemporalHighPassFilterGLMFourier(6);
    ResultFileName = docFMR.FileNameOfPreprocessdFMR;
    docFMR.Close();
    docFMR = bvqx.OpenDocument(ResultFileName);

    // Temporal smoothing
    docFMR.TemporalGaussianSmoothing(2, "TR");
    ResultFileName = docFMR.FileNameOfPreprocessdFMR;
    docFMR.Close();
    docFMR = bvqx.OpenDocument(ResultFileName);

    bvqx.PrintToLog(InFmrPath + " finished.");
};

bvqx.PrintToLog("***The_end***.");
