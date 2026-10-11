"""
Summary:

Use code to create directories to store output files from matlab frequency response analysis programs

Dependencies:
1. os

Notes:
    1. Change test (line 19)
"""

import os
#first subdirectory (outputs)
matlab_outputs = '../matlab/outputs/'

#test to make directories for
test = 'e_over_poff_6_3_2024_t3'

#params_and_tau_directory
os.makedirs(matlab_outputs + 'params_and_tau/' + test)
os.makedirs(matlab_outputs + 'params_and_tau/' + test+ '/ub')
os.makedirs(matlab_outputs + 'params_and_tau/' + test+ '/lb')
os.makedirs(matlab_outputs + 'params_and_tau/' + test+ '/non_dim_params')

#sim_data_directory
os.makedirs(matlab_outputs + 'sim_data/bode/'+test)
os.makedirs(matlab_outputs + 'sim_data/bode/'+test+'/non_dim')
os.makedirs(matlab_outputs + 'sim_data/step/'+test)

#uncert_intervals_directory
os.makedirs(matlab_outputs + 'uncert_intervals/' + test)
os.makedirs(matlab_outputs + 'uncert_intervals/' + test+ '/mag_and_phase')
os.makedirs(matlab_outputs + 'uncert_intervals/' + test+ '/non_dim_freq')
