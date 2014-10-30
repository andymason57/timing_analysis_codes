from pynfftls import *
import numpy as np
import matplotlib.pyplot as plt
import math
from astropy.io import fits
import numpy as np
import datetime
from subprocess import call


#main directory where LCs are stored
lc_dir = "/home/UTU/andmas/Desktop/"

# open file reading
hdulist = fits.open('/home/UTU/andmas/Desktop/84849_final_src_bkg_and_flare_corrected_LC_1000-10000keV.fit')

tbdata = hdulist[1].data

time = tbdata.field(2)

rate = tbdata.field(0)


######## produce red noise estimates

#mean value of lightcurve
mean_lc = np.mean(rate)
print "mean: ", mean_lc
#std dev of lightcurve 
stdev = np.std(rate)
print "stdev: ", stdev
# power law set 
power_law_slope = -2.0
#bin time of lightcurve  
lc_bin_time = 20
#time length lightcurve 
time_len = np.max(time) - np.min(time)
print "time_len: ", time_len
#set number of bins to simulate LC
num_bins = 1000
#seed value for random number generator


#call rndpwrlc
try: 
	idl_call = "cd " + lc_dir + " && idl -e rndpwrlc,lc_time,lc_rate,nt=1000.,mean=80.,sigma=10.,randomu=1 "
	call(idl_call, shell = True, executable='/bin/bash')
except RuntimeError:
	logger.exception('Some runtime error has occurred in main IDL reduction routine - check IDL console logs for ObsID: ', str_row)



print "finished ################"












































