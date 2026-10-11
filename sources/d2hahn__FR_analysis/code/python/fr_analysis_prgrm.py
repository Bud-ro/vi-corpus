"""
Summary:

Use the following program after using tdms_to_cropped_seperate_csv_prgrm.py to perform OLS fits of the sinewaves
of the cropped data portions that were output as csv files in ./outputs/single_phase_no_droplet/cropped_dataframe_to_csv/.
From the OLS estimation, plots of the estimated input and output waves overlayed with
the experimental data are produced to give a qualitative goodness of fit. The estimated parameters for both input and
output waves for each considered frequency are then tabularized in a dataframe. These estimated parameters are used to
caluclate the estimated magnitude and phase for both the input and output wave, where these are also tabularized in
a dataframe. The estimated magnitude and phase for I/O are then used to calculate the Magnitude and Phase Frequency
Response for each frequency, where this is tabularized in a dataframe as well. The estimate of the error variance and
the estimate of the variance of the estimate of each parameter is also tabularized in respective dataframes.The script then prompts the user to ask
if they want to output the dataframes to csv files in ./python/outputs/' +test+'/estimated_params_csv/ and/or
./python/outputs/' +test+'/mag_and_phase/.

Dependencies:
1. pathlib from Path
2. numpy
3. pandas
4. functions.py (ls_sinewave, sw_mag, sw_phase)
5. math

Notes:
1. Need to change path, p, from which .csv files are extracted for each different test (see line 39 )
2. Will need to add/remove entries from dict_of_frequencies if different frequencies are considered (see line 66)
3. Outputting the tables produced by this program to .csv files SHOULD ONLY BE DONE IF ALL FREQUENCY CASES ARE IN
    THE cropped_dataframe_to_csv SUBFOLDER. (Program erase's/overwrite's .csv files in estimated_params_csv and
    mag_and_phase subfolders). However, it is safe to use this program to rerun OLS fits on reedited graphs as long
    as the .csv files of the non-edited frequency cases in cropped_dataframe_to_csv are not changed/erased.
"""
from pathlib import Path
import math as m
import numpy as np
import pandas as pd
from functions import ls_sinewave, sw_mag, sw_phase


#input path of folder where csv files are stored (change on each run of program)
p = Path('./outputs/e_over_poff_6_3_2024_t2/cropped_dataframe_to_csv/FEP_t2/')

#create list of paths of csv files in the path directory specified in above line
csv_paths = list(p.glob('./*.csv'))

#create empty dictionary to store dataframes
dict_of_df = {}

'''
loop through all csv files and convert them to a dataframe, followed by adding the dataframe to dict_of_df, where the
key to each dataframe is the frequency at which the data was taken. Note original index of values is given in df
loop assumes naming of .csv files follows convention 0pointX.csv and 0pointXY.csv
'''
#set names of columns for dataframe
col_names = ['Original Index', 'P1 [mbar]', 'P2 [mbar]', 't[s]']
size_of_strings=[]
for path in csv_paths:
    str_csv_path = str(path)
    length_str = len(str_csv_path)
    size_of_strings.append(length_str)
    if length_str >= max(size_of_strings):
        dict_of_df[str_csv_path[length_str-12:length_str-4]] = pd.read_csv(path, names = col_names, header=0)
    else:
        dict_of_df[str_csv_path[length_str-11:length_str-4]] = pd.read_csv(path, names = col_names, header=0)


#creating dictionary with the string version of the frequency being the key and the float value being the value in [Hz]
dict_of_frequencies = {'0point01':0.01, '0point02':0.02, '0point03': 0.03, '0point04':0.04, '0point05' : 0.05,
                       '0point06':0.06,  '0point07':0.07, '0point08':0.08, '0point09':0.09, '0point1':0.1,
                        '0point2':0.2, '0point22':0.22, '0point25':0.25, '0point28':0.28, '0point3': 0.3,
                       '0point32': 0.32, '0point35':0.35, '0point38':0.38, '0point4':0.4}

#creating empty dictionaries to hold the estimated parameters for OLS sinewave estimation of input and output waves
input_estimation_dict ={}
output_estimation_dict = {}

est_var_input_dict ={}
est_var_output_dict ={}

param_est_cov_mat_in_dict ={}
param_est_cov_mat_out_dict ={}


"""
Fitting experimentally measured sinewaves to that of a general wave of the form:

u(t) = U*sin(omega*t+phi) + m = U*cos(phi)*sin(omega*t) + U*sin(phi)*cos(omega*t) + m

Where OLS estimation is used to estimate U*cos(phi), U*sin(phi), and m. See ls_sinewave function in functions.py.
When function is called plots of experimental data and fitted data are provided for each frequency specified in
dict_of_df, which contains each .csv file from the folder specified in path variable p. input_estimation_dict and 
output_estimation_dict contain estimated parameters for input and output waves respectivley for each frequency.
Key-value pairs of dictionaries are:

    '0pointXY' : array([U*cos(phi), U*sin(phi), m])
"""

input_estimation_dict, output_estimation_dict, est_var_input_dict, est_var_output_dict, param_est_cov_mat_in_dict, param_est_cov_mat_out_dict = ls_sinewave(dict_of_df,dict_of_frequencies, 'n')

#obtain variance of parameter estimates from covariance mat and store in dictionary (variances are diag of covariance mat)
var_input_param_est_dict ={}
var_output_param_est_dict ={}

for group in param_est_cov_mat_in_dict.keys():
    var_input_param_est_dict[group] = param_est_cov_mat_in_dict[group].diagonal()
    var_output_param_est_dict[group] = param_est_cov_mat_out_dict[group].diagonal()


#convert param est dicts to dfs (each row is a frequency, columns: U*cos(phi), U*sin(phi), m) to be output to .csv file
params =['U*cos(phi)', 'U*sin(phi)', 'm']
input_est_df = pd.DataFrame.from_dict(input_estimation_dict, orient='index', columns=params)
output_est_df = pd.DataFrame.from_dict(output_estimation_dict, orient='index', columns=params)

#store error variance estimates in df
var_est_input_df = pd.DataFrame.from_dict(est_var_input_dict, orient='index', columns=['Estimated Variance'])
var_est_output_df = pd.DataFrame.from_dict(est_var_output_dict, orient='index', columns=['Estimated Variance'])

#store estimated parameter variance estimates in df
var_input_param_est_df = pd.DataFrame.from_dict(var_input_param_est_dict, orient='index', columns=params)
var_output_param_est_df = pd.DataFrame.from_dict(var_output_param_est_dict, orient='index', columns=params)


#calculate magnitude and phase for each frequency (see sw_mag and sw_phase in functions.py)
input_mag_dict = {}
output_mag_dict = {}

input_phase_dict = {}
output_phase_dict ={}

#magnitude calculation
input_mag_dict = sw_mag(input_estimation_dict)
output_mag_dict = sw_mag(output_estimation_dict)


#phase calculation
input_phase_dict = sw_phase(input_estimation_dict, 'y')
output_phase_dict = sw_phase(output_estimation_dict, 'y')

#combine magnitude and phase into one dictionary, for both input and output to be converted to dataframe and output to csv
input_mag_and_phase = {}
output_mag_and_phase ={}

for group in input_mag_dict:
    input_mag_and_phase[group] = [input_mag_dict[group], input_phase_dict[group]]
    output_mag_and_phase[group] = [output_mag_dict[group],output_phase_dict[group]]

#convert input and output mag and phase dicts to dataframes for output to csv file
col_names_mp =['Magnitude [unitless]', 'Phase [deg]']
input_mag_phase_df = pd.DataFrame.from_dict(input_mag_and_phase, orient='index', columns=col_names_mp)
output_mag_phase_df = pd.DataFrame.from_dict(output_mag_and_phase, orient='index', columns=col_names_mp)


#calculate Frequency Response at each frequency (mag(P2)/mag(P1), (phase(P2)-phase(P1))
FR_datframe = pd.DataFrame({'Magnitude [unitless]': output_mag_phase_df['Magnitude [unitless]']/input_mag_phase_df['Magnitude [unitless]'],
                            'Phase [deg]': output_mag_phase_df['Phase [deg]'] - input_mag_phase_df['Phase [deg]']})

#converting magnitude to dB (20*log(FR_mag) = 20*log(Mag(P2)/Mag(P1))
FR_datframe['Magnitude [dB]'] = 20*np.log10(FR_datframe['Magnitude [unitless]'])

#organizing columns [Magnitude [unitless], Magnitude [dB], Phase [deg]]
cols = ['Magnitude [unitless]', 'Magnitude [dB]', 'Phase [deg]']
FR_datframe = FR_datframe[cols]

# creating list of values that are the float versions of the string of form '0pointXY' used as name of df rows
list_of_rows = list(FR_datframe.index)
freq_floats = []
for row in (list_of_rows):
    f = float(row.replace('point','.'))
    freq_floats.append(f)

# adding frequency columns to data frame (Hz and rad/s)
FR_datframe['f [Hz]'] = freq_floats
FR_datframe['f [rad/s]'] = 2*m.pi*FR_datframe['f [Hz]']

#outputting dataframes to csv file (asks user input to specify what to output)
answer = input("Output dataframes to csv file (y/n)?: ")
if answer == "y":
    test = input("Type in output folder (e.g pa_by_poff): ")
    folder = input("Type in test name (e.g. 50_o_12point5_a): ")
    which_files = input("Which data do you want to output?"
                        "\n 1) Estimated parameters from OLS sinewave estimation"
                        "\n 2) Magnitude [unitless] and Phase [deg] of the input and output sinewaves"
                        "\n 3) Magnitude and Phase Frequency Response"
                        "\n 4) 1 and 2"
                        "\n 5) 1 and 3"
                        "\n 6) 2 and 3"
                        "\n 7) Export All"
                        "\n type your answer here (single integer): ")
    if which_files == '1':
        input_est_df.to_csv('./outputs/'+test+'/estimated_params_csv/'+ folder +'/input_est_params.csv')
        output_est_df.to_csv('./outputs/'+test+'/estimated_params_csv/'+ folder +'/output_est_params.csv')
        var_est_input_df.to_csv('./outputs/'+test+'/estimated_params_csv/'+ folder +'/input_var_est.csv')
        var_est_output_df.to_csv('./outputs/'+test+'/estimated_params_csv/'+ folder +'/output_var_est.csv')
        var_input_param_est_df.to_csv('./outputs/'+test+'/estimated_params_csv/'+ folder +'/input_param_est_var_est.csv')
        var_output_param_est_df.to_csv('./outputs/'+test+'/estimated_params_csv/' + folder + '/output_param_est_var_est.csv')
    elif which_files == '2':
        input_mag_phase_df.to_csv('./outputs/'+test+'/mag_and_phase/'+ folder +'/input_mag_phase.csv')
        output_mag_phase_df.to_csv('./outputs/'+test+'/mag_and_phase/'+ folder +'/output_mag_phase.csv')
    elif which_files == '3':
        FR_datframe.to_csv('./outputs/'+test+'/mag_and_phase/'+ folder +'/FR_mag_phase.csv')
    elif which_files == '4':
        input_est_df.to_csv(
            './outputs/'+test+'/estimated_params_csv/' + folder + '/input_est_params.csv')
        output_est_df.to_csv(
            './outputs/'+test+'/estimated_params_csv/' + folder + '/output_est_params.csv')
        var_est_input_df.to_csv(
            './outputs/'+test+'/estimated_params_csv/' + folder + '/input_var_est.csv')
        var_est_output_df.to_csv(
            './outputs/'+test+'/estimated_params_csv/' + folder + '/output_var_est.csv')
        var_input_param_est_df.to_csv(
            './outputs/'+test+'/estimated_params_csv/' + folder + '/input_param_est_var_est.csv')
        var_output_param_est_df.to_csv(
            './outputs/'+test+'/estimated_params_csv/' + folder + '/output_param_est_var_est.csv')
        input_mag_phase_df.to_csv('./outputs/'+test+'/mag_and_phase/' + folder + '/input_mag_phase.csv')
        output_mag_phase_df.to_csv(
            './outputs/'+test+'/mag_and_phase/' + folder + '/output_mag_phase.csv')
    elif which_files == '5':
        input_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/input_est_params.csv')
        output_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/output_est_params.csv')
        var_est_input_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/input_var_est.csv')
        var_est_output_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/output_var_est.csv')
        var_input_param_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/input_param_est_var_est.csv')
        var_output_param_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/output_param_est_var_est.csv')
        FR_datframe.to_csv('./outputs/' +test+'/mag_and_phase/'+ folder +'/FR_mag_phase.csv')
    elif which_files == '6':
        input_mag_phase_df.to_csv('./outputs/' +test+'/mag_and_phase/' + folder + '/input_mag_phase.csv')
        output_mag_phase_df.to_csv(
            './outputs/' +test+'/mag_and_phase/' + folder + '/output_mag_phase.csv')
        FR_datframe.to_csv('./outputs/' +test+'/mag_and_phase/'+ folder +'/FR_mag_phase.csv')
    elif which_files == '7':
        input_est_df.to_csv('./outputs/' +test+'/estimated_params_csv/' + folder + '/input_est_params.csv')
        output_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/output_est_params.csv')
        var_est_input_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/input_var_est.csv')
        var_est_output_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/output_var_est.csv')
        var_input_param_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/input_param_est_var_est.csv')
        var_output_param_est_df.to_csv(
            './outputs/' +test+'/estimated_params_csv/' + folder + '/output_param_est_var_est.csv')
        input_mag_phase_df.to_csv('./outputs/' +test+'/mag_and_phase/' + folder + '/input_mag_phase.csv')
        output_mag_phase_df.to_csv(
            './outputs/' +test+'/mag_and_phase/' + folder + '/output_mag_phase.csv')
        FR_datframe.to_csv('./outputs/' +test+'/mag_and_phase/'+ folder +'/FR_mag_phase.csv')




