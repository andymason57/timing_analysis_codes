import psycopg2
from subprocess import call
import os
import sys
import shutil

main_path_NOT_results = "/mnt/4tbdata/xmm_reduce_results/NOT_course_results_tarred"
period_results_path = "/mnt/4tbdata/xmm_reduce_results/NOT_course_results_FASPER"
path_lrzip_unpacked = "/mnt/4tbdata/xmm_reduce_results/NOT_course_results_tarred/mnt/4tbdata/xmm_reduce_results/NOT_course_results/"
end_path_lrzip_unpacked = "/processed/test/"


def is_number(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
"""
code to extract each lrzip archive
"""
lrzipped_results = os.listdir(main_path_NOT_results)
for dir_list in lrzipped_results:
    dir_string = str(dir_list)
    dir_list = dir_string.strip('\'(),')
    untar_via_lrzip = "cd " + main_path_NOT_results + "/" + "&& " + "lrzuntar " + dir_list
    print untar_via_lrzip
    call(untar_via_lrzip, shell=True, executable='/bin/bash')

    """ code to move to unpacked dir """
    obsid,not_needed = dir_list.split('_')
    print obsid
    path_to_move_extract = path_lrzip_unpacked + obsid + end_path_lrzip_unpacked
    print path_to_move_extract


# results = os.listdir(main_path_NOT_results)
# for dir_list in results:
#     #pull_obs.execute("DELETE FROM not_reduced WHERE obs_id = %s", (dir_list,))
#     dir_string = str(dir_list)
#     dir_list = dir_string.strip('\'(),')
#     move_to_dir = main_path_NOT_results + "/" + dir_list
#     sub_dir = os.listdir(move_to_dir)
#     for subs in sub_dir:
#         if subs == 'processed':
#             sub_dir_name = main_path_NOT_results + "/" + dir_list + "/" + subs
#             sub_sub_dir = os.listdir(sub_dir_name)
#             for subs_subs in sub_sub_dir:
#                 if subs_subs == 'test':
#                     path_for_test = sub_dir_name + "/" + subs_subs
#                     print path_for_test

    file_listing = os.listdir(path_to_move_extract)
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


    for items in lc_files:
        split_filename, split_ext = os.path.splitext(items)
        split_up = split_filename.split("_")
        saved_obs_no = split_up[0]
        pass_detid = split_up[1]
        split_energy_range = split_up[4]
        saved_energy_range = split_energy_range[0:4]
        if saved_energy_range == '1000':
            invoke_period_string = "cd " + path_to_move_extract + " && idl -e FASPER_v2 -args " + path_to_move_extract  + items + " " + path_to_move_extract  + text_gti + " " + period_results_path + "/" + " " + obsid + " " + "1 1" + " " + saved_energy_range + " " + pass_detid
            print invoke_period_string
            call(invoke_period_string, shell=True, executable='/bin/bash')
            print "passed idl call"

    """ delete untarred directory """
    invoke_delete = "rm -R " + path_lrzip_unpacked + obsid
    print invoke_delete
    call(invoke_delete, shell=True, executable='/bin/bash')


print "########################## Finished #########################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################"
print "#############################################################################################" 
    