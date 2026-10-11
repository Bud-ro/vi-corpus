"""
Summary:

Use code to create directories to store output files from python frequency response analysis programs

Dependencies:
1. os

Notes:
    1. Change test (line 20)
    2. Change cases (line 23)
"""

import os

#first subdirectory (outputs)
sub1 = './outputs'

#test to make directories for
test = '/e_over_poff_6_3_2024_t3'

#cases to make subdirectories for
cases =  ['FEP_t3', 'HPPFA_t3', 'ETFE_t3', 'PEEK_t3']

#creating directories
#test output directory
os.makedirs(sub1+test)

#cropped_dataframe_to_csv directory
os.makedirs(sub1+test+'/cropped_dataframe_to_csv')

#creating subdirectory of cropped dataframes for each case
for case in cases:
    os.makedirs(sub1+test+'/cropped_dataframe_to_csv/'+case)

#estimated_params_csv directory
os.makedirs(sub1+test+'/estimated_params_csv')
os.makedirs(sub1+test+'/estimated_params_csv/w_uncertainty')

#creating subdirectory of cropped dataframes for each case
for case in cases:
    os.makedirs(sub1 + test + '/estimated_params_csv/' + case)
    os.makedirs(sub1 + test + '/estimated_params_csv/w_uncertainty/' + case)

#mag_and_phase directory
os.makedirs(sub1+test+'/mag_and_phase')
os.makedirs(sub1+test+'/mag_and_phase/w_uncertainty')

#creating subdirectory of cropped dataframes for each case
for case in cases:
    os.makedirs(sub1 + test + '/mag_and_phase/' + case)
    os.makedirs(sub1 + test + '/mag_and_phase/w_uncertainty/' + case)

#tf_params_tau_uncert directory
os.makedirs(sub1+test+'/tf_params_tau_uncert')

