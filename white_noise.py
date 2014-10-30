from pynfftls import *
import numpy as np
import matplotlib.pyplot as plt
import math
from astropy.io import fits
import numpy as np
import datetime

# open file reading
hdulist = fits.open('/home/UTU/andmas/Desktop/84849_final_src_bkg_and_flare_corrected_LC_1000-10000keV.fit')

tbdata = hdulist[1].data

time = tbdata.field(2)

rate = tbdata.field(0)


n = np.size(time) 

##### generate random numbers/lightcurves for white noise simulation 

random_flux = np.empty(n, dtype=np.float64)

max_random_power = 0
overall_max_power = 0
print "start time: ", datetime.datetime.now().time()


for x in xrange(1, 10):
	for flux_index in xrange(0,n): 
		a = np.random.randint(0, n-1)
		random_flux[flux_index] = non_zero_rate[a]
	(random_f, random_p) = period(non_zero_time, random_flux, ofac,hifac) 
	max_random_power = np.ndarray.max(random_p)
	#print "max power", max_random_power
	if overall_max_power < max_random_power: 
		overall_max_power = max_random_power
		#print "new max power", overall_max_power

print "end time: ", datetime.datetime.now().time()
print "overall max power: ", overall_max_power






