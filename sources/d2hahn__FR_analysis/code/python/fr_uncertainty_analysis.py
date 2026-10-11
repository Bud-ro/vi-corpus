"""
Summary:
Purpose of this script is to intake the estimated parameters, the estimated variance of the estimated parameters
and the estimated magnitude and phase frequency response output from fr_analysis_prgrm.py. From these inputs, the script
calculates the uncertainty in the parameter estimates and in the magnitude and phase frequency response, as well as the
relative uncertainty. 4 seperate dataframes are output: 1) input estimated parameters and uncertainties, 2) output
estimated parameters and uncertainties, 3) mag and phase FR and uncertainties 4) mag and phase FR w/ uncertainties and
relative uncertainties

Dependencies:
1. Path from pathlib
2. math
3. numpy
4. pandas
5. ls_sw_mag_uncert, ls_sw_phase_uncert, mag_fr_uncert, mag_fr_uncert_db, phase_fr_uncert, relative_uncertainty from functions.py

Notes:
Will need to change folder for different cases for the paths (i.e. single_phase_no_droplet)
"""


from pathlib import Path
import math as m
import numpy as np
import pandas as pd
from functions import ls_sw_mag_uncert, ls_sw_phase_uncert, mag_fr_uncert, mag_fr_uncert_db, phase_fr_uncert, relative_uncertainty

#input path of folder where csv files are stored (change on each run of program)
test = input('Input name of folder for output (e.g. pa_by_poff_4_3_2024): ')
folder = input("Which test do you want to perform uncertainty analysis for? (e.g. 50_o_12point5_a):")

#intaking input and output estimated parameters paths from fr_analysis_prgrm.py
input_est_params_path = Path('./outputs/' +test+'/estimated_params_csv/'+folder+'/input_est_params.csv')
output_est_params_path = Path('./outputs/' +test+'/estimated_params_csv/'+folder+'/output_est_params.csv')

#intaking input and output estimated variances of estimated parameters paths from fr_analysis_prgrm.py
input_est_params_est_var_path = Path('./outputs/' +test+'/estimated_params_csv/'+folder+'/input_param_est_var_est.csv')
output_est_params_est_var_path = Path('./outputs/' +test+'/estimated_params_csv/'+folder+'/output_param_est_var_est.csv')

#intaking input and output mag and phase [deg] path from fr_analysis_prgrm.py
in_mag_phase_path = Path('./outputs/' +test+'/mag_and_phase/'+folder+'/input_mag_phase.csv')
out_mag_phase_path = Path('./outputs/' +test+'/mag_and_phase/'+folder+'/output_mag_phase.csv')

#intaking FR mag and phase folder path from fr_analysis_prgrm.py output
mag_and_phase_folder_path = Path('./outputs/' +test+'/mag_and_phase/'+folder+'/FR_mag_phase.csv')

#intaking input and output estimated parameters and converting to dataframes
input_est_params = pd.read_csv(input_est_params_path, index_col=0)
output_est_params = pd.read_csv(output_est_params_path, index_col=0)

#intaking input and output mag and phase [deg] and converting to dataframes
in_mag_phase = pd.read_csv(in_mag_phase_path, index_col=0)
out_mag_phase = pd.read_csv(out_mag_phase_path, index_col=0)

#intaking input and output estimated variances of estimated parameters and converting to dataframes
input_est_var = pd.read_csv(input_est_params_est_var_path, index_col=0)
output_est_var = pd.read_csv(output_est_params_est_var_path, index_col=0)


#calculating est_std_dev of estimated parameters from estimated variance for each parameter
input_est_std_dev = input_est_var.apply(np.sqrt)
output_est_std_dev = output_est_var.apply(np.sqrt)

#calcualting estimate of uncertainty of each parameter estimate for 95% confidence
input_est_uncert = input_est_std_dev.mul(1.96)
output_est_uncert = output_est_std_dev.mul(1.96)


#intaking FR mag and phase
fr_mag_phase = pd.read_csv(mag_and_phase_folder_path, index_col=0)


#creating dataframe for input estimated params w uncertainty of form [param param_uncertainty (repeated for each param)]
input_est_params.insert(1,"del_u_A",input_est_uncert['U*cos(phi)'])
input_est_params.insert(3,"del_u_B",input_est_uncert['U*sin(phi)'])
input_est_params.insert(5,"del_u_m",input_est_uncert['m'])



#creating dataframe for output estimated params w uncertainty of form [param param_uncertainty (repeated for each param)]
output_est_params.insert(1,"del_u_A",output_est_uncert['U*cos(phi)'])
output_est_params.insert(3,"del_u_B",output_est_uncert['U*sin(phi)'])
output_est_params.insert(5,"del_u_m",output_est_uncert['m'])


#adding frequencies to input and output estimamted parameter dataframes
# creating list of values that are the float versions of the string of form '0pointXY' used as name of df rows
list_of_rows = list(fr_mag_phase.index)
freq_floats = []
for row in (list_of_rows):
    f = float(row.replace('point','.'))
    freq_floats.append(f)

# adding frequency columns to dataframes (Hz and rad/s)
input_est_params['f [Hz]'] = freq_floats
input_est_params['f [rad/s]'] = 2*m.pi*input_est_params['f [Hz]']
output_est_params['f [Hz]'] = freq_floats
output_est_params['f [rad/s]'] = 2*m.pi*input_est_params['f [Hz]']


#calculate magnitude uncertainty for I/O
in_mag_del_u = ls_sw_mag_uncert(input_est_params)
out_mag_del_u = ls_sw_mag_uncert(output_est_params)

#calculate phase uncertainty [rad] for I/O
in_phase_del_u = ls_sw_phase_uncert(input_est_params)
out_phase_del_u = ls_sw_phase_uncert(output_est_params)

#calculating FR_mag uncertainty [unitless]
del_u_mag_fr = mag_fr_uncert(in_mag_phase, out_mag_phase, in_mag_del_u, out_mag_del_u)

#calculating FR_mag_uncertainty [dB]
del_u_mag_fr_db = mag_fr_uncert_db(fr_mag_phase,del_u_mag_fr)


#calculating FR_phase uncertainty
del_u_phase_fr = phase_fr_uncert(in_phase_del_u, out_phase_del_u)
#convert phase uncertainty from [rad] to [deg]
del_u_phase_fr_deg = del_u_phase_fr*(180/np.pi)

#add mag and phase fr uncertatinty to fr_mag_phase dataframe
fr_mag_phase.insert(1,"del_u_mag [unitless]",del_u_mag_fr)
fr_mag_phase.insert(3,"del_u_mag [dB]",del_u_mag_fr_db)
fr_mag_phase.insert(5,"del_u_phase [deg]",del_u_phase_fr_deg)

#compute relative uncertainty for mag and phase (using relative_uncertainty fn from funcitons.py)
rel_u_fr = relative_uncertainty(fr_mag_phase)

#export tables to csv
answer = input('export unceratinty files to .csv? (y/n): ')
if answer == "y":
    input_est_params.to_csv('./outputs/' +test+'/estimated_params_csv/w_uncertainty/'+ folder + '/input_est_params_u.csv')
    output_est_params.to_csv('./outputs/' +test+'/estimated_params_csv/w_uncertainty/' + folder + '/output_est_params_u.csv')
    fr_mag_phase.to_csv('./outputs/' +test+'/mag_and_phase/w_uncertainty/' + folder + '/fr_mag_phase_u.csv')
    rel_u_fr.to_csv('./outputs/' +test+'/mag_and_phase/w_uncertainty/' + folder + '/rel_u_fr.csv')
#test of functions
# A = input_est_params['U*cos(phi)'].values
# B = input_est_params['U*sin(phi)'].values
# del_u_A = input_est_params['del_u_A'].values
# del_u_B = input_est_params['del_u_B'].values
#
#
# d_mag_d_A = np.multiply(A,np.reciprocal(np.sqrt((np.square(A)+np.square(B)))))
# d_mag_d_B = np.multiply(B,np.reciprocal(np.sqrt((np.square(A)+np.square(B)))))
#
# del_u_mag = np.sqrt(np.square(np.multiply(d_mag_d_A,del_u_A))+np.square(np.multiply(d_mag_d_B,del_u_B)))
#
# d_phase_d_A = -1*np.multiply(B,np.reciprocal(np.square(A)+np.square(B)))
# d_phase_d_B = np.multiply(A,np.reciprocal(np.square(A)+np.square(B)))
#
# del_u_phase = np.sqrt(np.square(np.multiply(d_phase_d_A,del_u_A))+np.square(np.multiply(d_phase_d_B,del_u_B)))

