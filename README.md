# Subcortical auditory atlas (work in progress...)
Resources from our human subcortical auditory pathway mapping project.

### Citation
TODO: add link to preprint

## Overview
<img src=flowcharts/overview_of_data_processing.svg>

## Dependencies

### Data
We have used the datasets accessible from the following sources:

| Package                                                  | Used version |
|----------------------------------------------------------|--------------|
| [BigBrain](https://bigbrain.loris.ca/main.php)           | 2015 release |
| [MNI ICBM 152](http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009)| 2009b Nonlin. Sym.|
| [Post mortem (request)](http://www.civm.duhs.duke.edu/SharedData/DataSupplements.htm)                            | ?        |
| [In vivo](TODO: add link)                                | ?        |


Data produced by these analyses are available at [OSF](https://osf.io/hxekn/?view_only=be9ec398304344e8bb694a0658d77ed6).


### Software
These are the software packages we have used to process our data. Not all packages are used in all processes. You can see specifically required packages for each processing step in flowcharts or script docstrings.

| Package                                                  | Used version |
|----------------------------------------------------------|--------------|
| [ITK-SNAP](http://www.itksnap.org/)                      | 3.6.0        |
| [FSL](https://fsl.fmrib.ox.ac.uk/fsl)                    | 5.0.9        |
| [ANTs](http://stnava.github.io/ANTs/)                    | 2.1.0        |
| [DiPy](http://nipy.org/dipy/)                            | 0.14         |
| [NiPype](https://nipype.readthedocs.io)                  | 1.1.8        |
| [NiBabel](http://nipy.org/nibabel/)                      | 2.2.0        |
| [Brainvoyager](https://www.brainvoyager.com/)            | 2.8.4        |
| [Neuroelf](http://neuroelf.net/)                         | 1.1rc2       |
| [Matlab](https://www.mathworks.com/products/matlab.html) | 2016a        |
| [TrackVis](http://www.trackvis.org/)                     | 0.6.1        |

## Support

Please use our GitHub issues page for posting questions or problems.

## License
The project is licensed under [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).
