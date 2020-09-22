# calcium-imaging-cultured-cells
Simple calcium imaging analysis pipeline for cultured cells

All scripts written by Thomas Parmentier except scalebar.py from Dan Meliza (https://gist.github.com/dmeliza/3251476)

**SETUP**

These scripts have been written to automate the signal processing and basic analysis of calcium imaging data acquired with Fluo4-AM in cultured cells on a confocal microscope.
Time series should be opened with ImageJ and neurons manually contoured. The first ROI should be of the background (zone without any cell). Mean fluorescence of each neuron is recorded and a matrix is exported in .csv file in T*(N+1) format with T representing the number of frames and N the number of neurons (First column is background).

Make sure to put all scripts and your .csv file in the same folder. Launch pipeline.py in the command line. 
For smoothing, the exponentially weighted moving average with an alpha of 0.5 is used by default but this can be modified in the signalprocess.py file depending on the signal to noise ratio of your recording.
The "Injection Yes or No" prompt refers to if any injection has been performed during the recording to stimulate or inhibit the cell activity. If you answer Yes, the algorithm will use the first 25 seconds of the recording as the baseline fluorescence (this can be modified in signalprocess.py). If you answer No, then the minimum fluorescence of each neuron will be used as the baseline fluorescence for each neuron.
