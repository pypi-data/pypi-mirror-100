# Time Series Analysis

This is a MixIn framework to:
   1.  read data (from files, stdin etc.)
   2.  extract one or more event time series 
   3.  run analysis to identify points of interest on the timeline 
   4.  translate the found events in extracted time series back to
   (presumably time) markers in original data
   5.  write finalized output in some format

MixIns for a pipeline are:

* Input
* Analysis Method
* Output
* Logging

## Approaches

Below is a list of currently implemented approaches.

### Kendall Correlation 

Kendall rank correlation coefficient (aka Kendall's τ coefficient) performs
pairwise identification of positive or negative correlation in two
timeseries.

### Time Motifs

Time motifs are repeating patterns which indicate an underlying common cause.  Details on these approaches can be [found here][scrimp paper].

----
[scrimp paper]: https://www.cs.ucr.edu/~eamonn/SCRIMP_ICDM_camera_ready_updated.pdf
