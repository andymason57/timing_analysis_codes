import psycopg2
import numpy as np
import logging
from astropy.io import fits
from subprocess import call
 

################################ Set up error logging facility ################################################ 

#set logger file destination and time/date format
#logging.basicConfig(filename='/home/andy/disk/data_ssc/reduced_data_errors.log')
#logging.basicConfig(level=logging.WARNING)
#create logger and logging facility
#logger = logging.getLogger('reduce')
#create logging handler
#hdlr = logging.FileHandler('/home/andy/disk/data_ssc/reduced_data_errors.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
#logger.setLevel(logging.WARNING)
#format logging messages

#change this for location of processed files
hard_coded_dir='/home/UTU/andmas/Desktop/test'
source_filename = 'final_product_src_bkg_flare_corrected_343_200-1000keV.fits'

#get time resolution from header of final LC fits file
def get_time_res():
    path_final_lc = hard_coded_dir + '/' + source_filename
    hdulist = fits.open(path_final_lc)
    time_res = hdulist[0].header['timedel'] 
    hdulist.close()
    return time_res
    
# Get total Good time from GTI fits file
def get_total_time():
    path_GTI = hard_coded_dir + '/' + 'GTI_FITS.fits'
    hdulist = fits.open(path_GTI)
    total_time = hdulist[1].header['ontime']
    hdulist.close()
    return total_time


def get_gti_time_intervals():
    path_GTI = hard_coded_dir + '/' + 'GTI_FITS.fits'
    hdulist = fits.open(path_GTI)
    gti_data = hdulist[1].data
    hdulist.close()
    return gti_data
    
# Creates a gti file for each row of the main GTI file so we can run powspec on time range     
def strip_gtis():
    path_GTI = hard_coded_dir + '/' + 'GTI_FITS.fits'
    hdulist = fits.open(path_GTI)
    gti_header = hdulist[0]
     #get individual gti's 
    gtis_to_use = hdulist[1].data
    counter = 0
    for x in gtis_to_use['start']: 
        counter += 1
        #create data column of new fits file
        start_array = np.array([x])
        stop_list = gtis_to_use['stop']
        stop_array = np.array([stop_list[counter-1]])
        
        col1 = fits.Column(name='start', format='E', array=start_array)
        col2 = fits.Column(name='stop', format='E', array=stop_array)
        
        cols = fits.ColDefs([col1,col2])
        tbhdu = fits.new_table(cols)
        thdulist = fits.HDUList([gti_header,tbhdu])  
        print hard_coded_dir + '/' + 'sub_GTI_FITS_' + str(counter) + '.fit'
        thdulist.writeto(hard_coded_dir + '/' + 'sub_GTI_FITS_' + str(counter) + '.fit')
        produce_xron_gti(hard_coded_dir + '/' + 'sub_GTI_FITS_' + str(counter) + '.fit', 
                         hard_coded_dir + '/' + 'sub_GTI_FITS_' + str(counter) + '_xronwin' + '.fit')
    hdulist.close()
        

#################### create ftools formatted GTI file ###############################

def produce_xron_gti(gti,xron_gti):
    try: 
        shell_call='cd ' + hard_coded_dir + ' && gti2xronwin -i ' + gti + ' -o ' + xron_gti
        print shell_call
        call(shell_call, shell=True, executable='/bin/bash')
    except Exception:
#        logger.exception('gti2xronwin failed...')
        print 'gtixronwin failed'
        

################# Run powspec #######################################
# Call like powspec cfile1="input file" window="GTI_file" dtnb (=time res) nbint = total Good time/time res nintfm (=1) gapfill = 4
# rebin (=0) plot (=no) outfile ("-") 

def run_powerspec(source_LC, window_file, dtnb, nbint, nintfm, gapfill, rebin, plot, plotdev, outfile):
        try:
            powspec_call="powspec cfile1=" + source_LC + " window= " + window_file 
            + " dtnb= " + str(dtnb) + " nbint=" + str(nbint) + " nintfm=" + str(nintfm) + " rebin=" + str(rebin) + " plot=" 
            + plot + " outfile=" + outfile
            print powspec_call
            call(powspec_call, shell=True, executable='/bin/bash')
        except Exception:
            logger.exception('some error message') 
            


if __name__ == '__main__':
    gti = 'GTI_FITS.fits'
    xron_gti = 'GTI_FITS_xron.fits'
    strip_gtis()
#    produce_xron_gti(gti,xron_gti)
#    run_powerspec(hard_coded_dir,final_product_src_bkg_flare_corrected_343_200-1000keV.fits, )
    
   




