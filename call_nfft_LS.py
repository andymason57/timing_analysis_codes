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

print n

non_zero_time = np.arange(n, dtype=np.float64)
non_zero_rate = np.arange(n, dtype=np.float64)

timezero = time[0]

counter = 0
while counter < n: 
	non_zero_time[counter] = time[counter] - timezero
	non_zero_rate[counter] = rate[counter]
	counter = counter + 1

hifac = 1.
ofac = 1.  
    
(f,p) = period(non_zero_time,non_zero_rate,ofac,hifac)

maximum = np.ndarray.max(p)
print "max p:", maximum 

#plt.clf()
#plt.plot(f,p)
#plt.loglog()
#plt.show()



new_pow_array = np.empty(n, dtype=np.float64) 

new_pow_array = p[20:n]
new_f = f[20:n]
print p
print "new p: ", new_pow_array
new_maximum = np.ndarray.max(new_pow_array)  
print "new max power p: ", new_maximum

#plt.clf()
#plt.plot(new_f,new_pow_array)
#plt.loglog()

#plt.show()




