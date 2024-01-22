This script can take several files used to consruct Krona plots and merge them into a single taxonomy table.

The desired level of taxonomic classification can be adjusted with command line arguments. Currently 1-7 is supported with 1 being kingdom level only and 7 being species level taxonomy. If one of the samples does not contain one of the taxonomic labels a score of 0 is attributed to that sample.

Note: For linux one can use the standard way of running a python script, following the instructions provided in the script itself.

For windows users the following steps have to be taken to run the script.

1. Install python; this can be done by going to the following link (Note that this script was designed for python 3.12.1) https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe . When installing python, it is important to include python in the program path, this option is given during the installation of python. Adding something to the path implies that it can be found through the command line.

2. Test the python installation; Press the windows button and type "cmd" then press enter. The command prompt should now open. Then type "python --version". If python is installed correctly the version of python should be printed to the command prompt.

3. If python is installed correctly the script can be run, in order to run the script type "python3 scriptpath inputpath outputpath depth"

scriptpath = location were the script is stored (example: C:\Users\Me\Scripts\script.py).
inputpath = location were the krona files are located (Note; the script expects that there are ONLY krona files in this directory!)
outputpath = path to the location were the output files are to be stored (example: C:\Users\Me\Data\).
depth = number between 1-7 were 1 is kingdom level and 7 is species level.

This script produces 2 output files, this includes the merged krona file and the taxonomy table in TSV format.
