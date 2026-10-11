"""
Summary:
Purpose of code is to intake parameters and time constant (tau) values from transfer functions used to describe analytical
model from experimental frequency response data from bode_plot_prgrm_from_py_w_uncert.m and upper_and_lower_uncert_bound_bode_plot_
prgrm.m, and calculate the uncertainty of the parameter estimates for the measured data's fit using sequential perturbation.
Program then outputs a .csv file of the parameters for the fit of the measured values and their associated uncertainty
nominal and relative. Form of output .csv file is (./outputs/test/tf_params_tau_uncert/):

[a b d tau [s] del_u_a del_u_b del_u_d del_u_tau [s] rel_del_u_a [%] rel_del_u_b [%] rel_del_u_d [%] rel_del_u_tau [%]]

Where the general form of the transfer function from the fit data is:

G(s) = e^(-ds)*(1+as)/(1+bs)

Code also calculates the non-dimensional parameters, (p_off/mu)*parameter, for the non-dimensionalized FR based of off the
non-dimensionalized frequency, omega_nd = omega*mu/p_off. Program intakes the offset pressure (mbar) and oil kinematic viscosity (cSt)
to calculate the non-dimensionalized parameters and their associated uncertainty. Outputs .csv file in same form as above.

Dependencies:
1. pandas
2. math
3. pathlib from Path

Notes:
   1. Need to change paths at start of code to grab parameters of fits for specific tests (see line 36-38)
   2. Need to change key names for dictionaries depending on names of tests (see line 52,60,65)
"""

import pandas as pd
import math as m
from pathlib import Path


#change paths for different tests
p_ro = Path('../matlab/outputs/params_and_tau/pa_by_poff_4_3_2024/')
p_ub = Path('../matlab/outputs/params_and_tau/pa_by_poff_4_3_2024/ub/')
p_lb = Path('../matlab/outputs/params_and_tau/pa_by_poff_4_3_2024/lb/')

#reading in the parameters and time constants from the models fit to the measured, upper bound uncertainty, and lower
#bound uncertainty data points to dictionaries of data frames
csv_paths_p_ro = list(p_ro.glob('./*.csv'))
csv_paths_p_ub = list(p_ub.glob('./*.csv'))
csv_paths_p_lb = list(p_lb.glob('./*.csv'))

col_names = ['a', 'b', 'd', 'tau']
dict_of_meas = {}

#will need to edit key names for dict_of_meas depending on what tests are considered
for path in csv_paths_p_ro:
    str_path = str(path)
    print(str_path[53:(len(str_path)-19)])
    dict_of_meas[str_path[53:(len(str_path)-19)]] = pd.read_csv(path, names = col_names, header = 0)
dict_of_ub ={}
dict_of_lb ={}

#will need to edit key names for dict_of_ub/lb depending on what tests are considered
for path in csv_paths_p_ub:
    str_path = str(path)
    #print(str_path[56:len(str_path)-21])
    dict_of_ub[str_path[56:len(str_path)-21]] = pd.read_csv(path, names = col_names, header = 0)

for path in csv_paths_p_lb:
    str_path = str(path)
    #print(str_path[49:len(str_path)-7])
    dict_of_lb[str_path[56:len(str_path)-21]] = pd.read_csv(path, names = col_names, header = 0)

dict_of_del_plus ={}
dict_of_del_neg ={}
dict_of_del_avg  ={}

#calculating uncertainty through sequential pertubation
for key in dict_of_ub.keys():
    dict_of_del_plus[key] = dict_of_ub[key] - dict_of_meas[key] # R_plus - R_o
    dict_of_del_neg[key] = dict_of_lb[key] - dict_of_meas[key] #R_neg - R_o
    dict_of_del_avg[key] = (abs(dict_of_del_plus[key]) + abs(dict_of_del_neg[key]))/2 # (abs(del_R_plus) + abs(del_R_neg))/2

#keys list
keys_list = list(dict_of_del_avg.keys())

#calculate uncertainty in non-dimensional parameters
#asking user input for offset pressure (in mbar) and kinematic viscosity (cSt), converting to pressure in Pa and viscosity (Pa-s)
p_off_mbar = int(input('Enter value of pressure offset in mbar: ')) #mbar (must manually enter on each run)
p_off_pa = p_off_mbar*100 #Pa

kin_visc = int(input('Enter value of Si oil kinematic viscosity in cSt: ')) #cSt (must manually enter on each run)

#determining visc from kin_visc value (see laminar_flow_rate_calcs.xlsx in tubing_dynamics/Experimental Materials and Apparatus/Flow Sensors/)
#visc determined from kin_visc and density measurements at @ 25 deg C from sigma aldrich website of 5-100 cSt Si Oil
while kin_visc != 5 and kin_visc != 10 and kin_visc != 20 and kin_visc != 50 and kin_visc != 100:
    kin_visc = int(input('Input kinematic viscosity that is 5, 10, 20, 50 , or 100 cSt): '))
if kin_visc == 5:
    visc = 0.004565
elif kin_visc == 10:
    visc = 0.009300
elif kin_visc == 20:
    visc = 0.019000
elif kin_visc == 50:
    visc = 0.048000
else:
    visc = 0.096000

#calculating uncertainties that do not change on each test
d_pi_d_param = p_off_pa/visc
del_u_p_off = m.sqrt((0.0001*p_off_pa)**2+(0.0003*(100000))**2)

#calculating non-dimensional parameters and uncertainties
dict_of_params = {}
dict_of_non_d ={}
dict_of_non_d_param_w_uncert={}
for key in keys_list:
    #conditional to handle case that ONLY the offset pressure (P_off) is increased for each test case
    if key == '50_mbar' or key== '100_mbar' or key== '150_mbar' or key== '200_mbar' or key== '250_mbar':
        p_off_pa = int(key[0:len(key)-5])*100
        del_u_p_off =m.sqrt((0.0001*p_off_pa)**2+(0.0003*(100000))**2)
        d_pi_d_param = p_off_pa/visc
    else:
        d_pi_d_param = p_off_pa / visc
        del_u_p_off = m.sqrt((0.0001 * p_off_pa) ** 2 + (0.0003 * (100000)) ** 2)
    # #conditional to handle case that ONLY the viscosity is increased for each test case
    if key == '5_cSt' or key == '10_cSt' or key == '20_cSt' or key == '100_cSt':
        if key == '5_cSt':
            visc = 0.004565
        elif key == '10_cSt':
            visc = 0.009300
        elif key == '20_cSt':
            visc = 0.019000
        elif key == '100_cSt':
            visc = 0.096000
        d_pi_d_param = p_off_pa / visc

    dict_of_params[key] = dict_of_meas[key].drop(['tau'], axis=1)
    dict_of_params[key].index=[key]
    dict_of_non_d[key] = dict_of_params[key]*(p_off_pa/visc)

    a = dict_of_params[key]['a'].values[0]
    del_u_a = dict_of_del_avg[key]['a'].values[0]
    d_non_d_a_d_p_off = a/visc
    del_u_non_d_a = m.sqrt((d_non_d_a_d_p_off*del_u_p_off)**2+(d_pi_d_param*del_u_a)**2)

    b = dict_of_params[key]['b'].values[0]
    del_u_b = dict_of_del_avg[key]['b'].values[0]
    d_non_d_b_d_p_off = b/visc
    del_u_non_d_b = m.sqrt((d_non_d_b_d_p_off*del_u_p_off)**2+(d_pi_d_param*del_u_b)**2)

    d = dict_of_params[key]['d'].values[0]
    del_u_d = dict_of_del_avg[key]['d'].values[0]
    d_non_d_d_d_p_off = d/visc
    del_u_non_d_d = m.sqrt((d_non_d_d_d_p_off * del_u_p_off) ** 2 + (d_pi_d_param * del_u_d) ** 2)

    df_non_d_param_uncert = pd.DataFrame({'del_u_non_d_a': [del_u_non_d_a], 'del_u_non_d_b': [del_u_non_d_b],
                                          'del_u_non_d_d': [del_u_non_d_d]})
    df_non_d_param_uncert.index = [key]
    #print(df_non_d_param_uncert)

    dict_of_non_d_param_w_uncert[key] = pd.concat([dict_of_non_d[key], df_non_d_param_uncert], axis=1)
# #print(dict_of_non_d_param_w_uncert)

#automate concatenation based on number of keys in dict_of_del_avg (conditional followed by for loop)
#reorganizing dataframes for output.
df_meas = pd.concat([dict_of_meas[keys_list[0]]])
df_del_avg = pd.concat([dict_of_del_avg[keys_list[0]]])
df_non_d_param_w_uncertainty = pd.concat([dict_of_non_d_param_w_uncert[keys_list[0]]])

if len(keys_list) > 1:
    for i in range(1,len(keys_list)):
        df_meas = pd.concat([df_meas, dict_of_meas[keys_list[i]]])
        df_del_avg = pd.concat([df_del_avg, dict_of_del_avg[keys_list[i]]])
        df_non_d_param_w_uncertainty=pd.concat([df_non_d_param_w_uncertainty, dict_of_non_d_param_w_uncert[keys_list[i]]])
else:
    df_meas = df_meas
    df_del_avg = df_del_avg
    df_non_d_param_w_uncertainty=df_non_d_param_w_uncertainty

df_output = pd.concat([df_meas, df_del_avg], axis=1)
df_output.columns = ['a', 'b', 'd', 'tau', 'del_u_a', 'del_u_b', 'del_u_d', 'del_u_tau']
df_output.index =keys_list

df_non_d_param_w_uncertainty.columns = ['non_d_a', 'non_d_b', 'non_d_d', 'del_u_non_d_a', 'del_u_non_d_b', 'del_u_non_d_d']

#calculation of relative uncertainty
df_output['r_u_a [%]']  = df_output['del_u_a']/df_output['a']*100
df_output['r_u_b [%]']  = df_output['del_u_b']/df_output['b']*100
df_output['r_u_d [%]']  = df_output['del_u_d']/df_output['d']*100
df_output['r_u_tau [%]']  = df_output['del_u_tau']/df_output['tau']*100

df_non_d_param_w_uncertainty['r_u_non_d_a [%]'] = df_non_d_param_w_uncertainty['del_u_non_d_a']/df_non_d_param_w_uncertainty['non_d_a']*100
df_non_d_param_w_uncertainty['r_u_non_d_b [%]'] = df_non_d_param_w_uncertainty['del_u_non_d_b']/df_non_d_param_w_uncertainty['non_d_b']*100
df_non_d_param_w_uncertainty['r_u_non_d_d [%]'] = df_non_d_param_w_uncertainty['del_u_non_d_d']/df_non_d_param_w_uncertainty['non_d_d']*100

#export tables to csv
answer = input('export unceratinty files to .csv? (y/n): ')
if answer == "y":
    folder_out = input("Type in folder for output in ./outputs (e.g single_phase_no_droplet: ")
    df_output.to_csv('./outputs/'+ folder_out + '/tf_params_tau_uncert/tf_params_and_tau_w_uncert_'+folder_out+'.csv')
    df_non_d_param_w_uncertainty.to_csv('./outputs/'+ folder_out + '/tf_params_tau_uncert/non_d_tf_params_w_uncert_'+folder_out+'.csv')
else:
    print('did not output to .csv')
