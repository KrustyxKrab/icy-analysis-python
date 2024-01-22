README File - ICY Analysis python The following codes can be used to analyse and visualise netCDF data of the Arctic region Link to the data used: https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/
Many thanks to the University of Bremen for the free access to the complete data!!

The data is collected by the CryoSat-2 satellite and the amsr2 instrument. More infomation about the satellite and the data: https://earth.esa.int/eogateway/documents/20142/37627/CryoSat-Baseline-D-Product-Handbook.pdf

University of Bremen: https://seaice.uni-bremen.de/start/

DOWNLOAD_DATA_HTTPS.py The code can be used to download from any available server that allows https requests The code was developed for use with NSIDC's Earthdata Databank, but also works for other servers. Each year of data should be in the same directory and labelled by year. Otherwise the analysis programme will not be able to access the years.

DATA_VIEW.py The code can be used to read the netCDF files and view the variables. The variables also contain the variable "polar-stereographic", which is important for the correct map projection

SEA_ICE_CONCENTRATION_ASMR2_VISUALISATION.py This script is the main script for visualisation. The code is with many explanations, but in German. I will change this soon.

IMAGEIO_VIDEO_VISUALISIERUNG.py This script can be used to create a video from hundreds of png files. The animation looks very nice, I think.

Before usage of the scripts, please check wether you have all needed libraries installed.

A exapmle animation (shortened version) is also online in my repository.

I am just in the beginning of my programming. Feel free to comment :D
More details will follow soon.
