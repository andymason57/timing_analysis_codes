import psycopg2
from subprocess import call
import os
import sys
import shutil

main_path_NOT_results = "/mnt/4tbdata/xmm_reduce_results/xfast_test_results"
period_results_path = "/mnt/4tbdata/xmm_reduce_results/xfast_test_results_FASPER"



def is_number(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

# set up database table full of results
#conn = psycopg2.connect("dbname=postgres user=postgres host=127.0.0.1 password=YvonneCSutton42")
# cur = conn.cursor()
# obs_listing = os.listdir(main_path_NOT_results)
# for obs in obs_listing:
#     obs = str(obs)
#     cur.execute("INSERT INTO not_reduced (obs_id) VALUES (%s)", (obs,))
#     conn.commit()
# cur.close()
# conn.close()

# Pull obs_id from table and call idl routines 
#pull_obs = conn.cursor()
#pull_obs.execute("SELECT obs_id FROM new_not_obsid;")
#conn.commit()
#results = pull_obs.fetchall()
#pull_obs.close()
#conn.close()
#print "just before main loop"
results = os.listdir(main_path_NOT_results)
for dir_list in results:
    #pull_obs.execute("DELETE FROM not_reduced WHERE obs_id = %s", (dir_list,))
    dir_string = str(dir_list)
    dir_list = dir_string.strip('\'(),')
    move_to_dir = main_path_NOT_results + "/" + dir_list
    sub_dir = os.listdir(move_to_dir)
    for subs in sub_dir:
        if subs == 'processed':
            sub_dir_name = main_path_NOT_results + "/" + dir_list + "/" + subs
            sub_sub_dir = os.listdir(sub_dir_name)
            for subs_subs in sub_sub_dir:
                if subs_subs == 'test': 
                    path_for_test = sub_dir_name + "/" + subs_subs
                    print path_for_test

                    file_listing = os.listdir(path_for_test)
                    lc_files=[] 
                    for files in file_listing: 
                        gti_front_filename, gti_filename_ext = os.path.splitext(files)
                        gti_file = gti_front_filename[0:2]
                
                        if gti_filename_ext == '.txt':
                            text_gti = gti_front_filename + gti_filename_ext
                      
                                          
                        lc_front_filename, lc_filename_ext = os.path.splitext(files)
                        detid = lc_front_filename.split("_")
                        size_of_list = len(detid)
                        if size_of_list > 2:                        
                            convert_detid = detid[2]
                            if convert_detid == 'corrected':
                                lc_files.append(files)
#                        if is_number(convert_detid) == True: 
#                            add_string = ''
#                            length_detid = len(convert_detid)
#                            if length_detid == 3:
#                                add_string = '000'
#                                lc_front_filename = add_string + lc_front_filename
#                            elif length_detid == 4: 
#                                add_string = '00'
#                                lc_front_filename = add_string + lc_front_filename
#                            elif length_detid == 5:
#                                add_string ='0' 
#                                lc_front_filename = add_string + lc_front_filename
                                    
#                        final = convert_detid
#                        print final
#                        if lc_filename_ext == '.fit' and lc_front_filename != gti_filename:
#                            lc_files.append(files)
                      #  run_no = gtis[0:5]
                       # subset_to_use=[]
                        #saved_obs_no=[]
                        #saved_energy_range=[]
                        #counter = 0
                        #for lightcurves in lc_files:
                         #       first_two_chars = lightcurves[6:8]
                         #       print first_two_chars
                          #      if first_two_chars == 'fi':
                          #          obs_no = lightcurves[0:5]
                          #          print obs_no
                          #          if obs_no == run_no:
                          #              subset_to_use.append(lightcurves)
                        
                    for items in lc_files:
                        split_filename, split_ext = os.path.splitext(items)
                        split_up = split_filename.split("_")
                        saved_obs_no = split_up[0] 
                        pass_detid = split_up[1]
                        split_energy_range = split_up[4]
                        saved_energy_range = split_energy_range[0:4]
                        if saved_energy_range == '1000':
                            invoke_period_string = "cd " + path_for_test + " && idl -e FASPER_v2 -args " + path_for_test + "/" + items + " " + path_for_test + "/" + text_gti + " " + period_results_path + "/" + " " + dir_list + " " + "1 1" + " " + saved_energy_range + " " + pass_detid 
                            print invoke_period_string
                            call(invoke_period_string, shell=True, executable='/bin/bash')
                            print "passed idl call"           
                
        
print "########################## Finished #########################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################" 
    