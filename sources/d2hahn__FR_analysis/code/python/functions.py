import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m
from matplotlib.widgets import SpanSelector

'''
Title: region_of_interest (dict_of_df, specified_groups)

Below function uses SpanSelector widget to select data we want to do FR analysis on from plot of all transient pressure data
from experiments at a specific frequency. Formulation of code is custom built for our case, but the general idea of the 
code closely resembles that of the SpanSelector example from the matplotlib documentation, which can be found at the 
below link:

    https://matplotlib.org/stable/gallery/widgets/span_selector.html

Summary: 
Inputs: 
1) a dictionary of dataframes where each key in the dictionary represents data from TDMS file at a specific frequency, dict_of_df
2) a list of keys/groups in the dictionary we want to analyze (optional), specified_groups = [list], if nothing specified
    automatically loops through all keys in the input dictionary

Outputs:
If no specific groups are specified, function loops through each group in the input dictionary and allows the user 
to use the span selector to select the data they want to use in the FR analysis. The function then returns a new
dictionary, which has the same group names as the input dictionary, only the data in each group is that selected from 
the graph using the span selector for the specific group, and the value of the first time [s] in the new group is set to be 
equal to zero, with all other time points incremented according to the sample time from the original dataset.

If a list of specified groups is given, fn only loops through the groups in the specified_groups list for use in the 
SpanSelector, outputs new dictionary whose only difference with the input dictionary is that the specified groups in 
specified_groups = [list] are cropped to the users selection.

Function also prints out the names of all edited groups
'''

def region_of_interest(dict_of_df, specified_groups = []):
    if specified_groups == []:
        dict_of_analysis_data_dfs = {}
        modified_groups =[]
        for group in dict_of_df.keys():
            case = dict_of_df[group]

            # set font and fontsize
            plt.rc('font', family='Times New Roman')
            plt.rcParams.update({'font.size': 12})
            # csfont = {'fontname':'Times New Roman',
            # 'size': 12}

            # creates subplot figure (top is full plot, bottom is cropped plot)
            fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

            # take the time, P1, and P2 data from the edited dataframe as series
            t_plt = case['t[s]']
            P1_plt = case['P1 [mbar]']
            P2_plt = case['P2 [mbar]']

            # plot both the P1 and P2 data wrt time on each plot
            line1P2, = ax1.plot(t_plt, P2_plt, color = 'blue')
            line1P1, = ax1.plot(t_plt, P1_plt, color = 'red')

            # add grid to plot
            ax1.grid()

            # set xlim and ylim for full plot
            ax1.set_xlim(t_plt.min(), t_plt.max())
            ax1.set_ylim(min(P1_plt.min(), P2_plt.min()), max(P1_plt.max(), P2_plt.max()))

            # instructions on what to do
            ax1.set_title('Press left mouse button and drag '
                          'to select a region in the top graph')

            # setting legend and ylabel for full plot
            ax1.set(ylabel="P [mbar]")
            ax1.legend((line1P1, line1P2), ('P1', 'P2'), loc="upper right")

            # creating empty lines for initial output of cropped plot, lists will be filled from onselect() callback fn
            line2P2, = ax2.plot([], [], color = 'blue')
            line2P1, = ax2.plot([], [], color = 'red')

            # setting x and y labels of cropped plot and grid
            ax2.set(xlabel="Time [s]", ylabel="P [mbar]")
            ax2.grid()

            '''
            Callback function onselect() gets called after the SpanSelector function finishes i.e. the region of the graph is
            selected. One will note that onselect is called each time the region is selected. In onselect() the time and pressure 
            values of the cropped plot are determined from the minimum and maximum indices selected from the full plot. The data and
            x and y limits for the cropped plot are then determined. Following this, the selected  t, P1, and P2 data is stored
            in a dataframe in the same structure as in line 65, where this dataframe is added to dict_of_analysis_data_dfs  
            with a key = to the current group being looped through. The value of the first t in the dataframe is set to zero for
            use in FR analysis through least squares fitting.  
            '''

            def onselect(xmin, xmax):
                '''
                determines the minimum and maximum indices based on the location in the t_plt series
                that the selected min and max t from SpanSelector are located
                '''
                indmin, indmax = np.searchsorted(t_plt, (xmin, xmax))
                indmax = min(len(t_plt) - 1, indmax)

                # determines t, P1, and P@ values of selected region
                region_t = t_plt[indmin:indmax]
                region_P1 = P1_plt[indmin:indmax]
                region_P2 = P2_plt[indmin:indmax]

                # creates dataframe of region of interest setting initial t to zero
                dataframe = pd.DataFrame(
                    {'P1 [mbar]': region_P1, 'P2 [mbar]': region_P2, 't[s]': region_t - region_t.min()})
                # adds dataframe to dictionary
                dict_of_analysis_data_dfs[group] = dataframe
                modified_groups.append(group)


                # sets the cropped plots data values and limits.
                if len(region_t) >= 2:
                    line2P1.set_data(region_t, region_P1)
                    line2P2.set_data(region_t, region_P2)
                    ax2.set_xlim(region_t.min(), region_t.max())
                    ax2.set_ylim(min(region_P1.min(), region_P2.min()), max(region_P1.max(), region_P2.max()))
                    fig.canvas.draw_idle()

            # funciton that allows us to select data of interest, see matplotlib documentation
            span = SpanSelector(
                ax1,
                onselect,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:blue"),
                interactive=True,
                drag_from_anywhere=True
            )
            # Set useblit=True on most backends for enhanced performance.
            # ax2.legend((line2P1, line2P2), ('P1', 'P2'), loc = "upper right")
            plt.show()
        print('specified groups:')
        print(modified_groups)
        return dict_of_analysis_data_dfs

    else:
        dict_of_analysis_data_dfs = {}

        #for loop to copy input dictionary key-value pairs to new dictionary note that if we set dict1=dict2 any change
        #to dict2 would also result in a change to dict1, hence the need for the first for loop
        for group in dict_of_df.keys():
            dict_of_analysis_data_dfs[group] = dict_of_df[group]

        modified_groups = []

        for group in specified_groups:
            case = dict_of_analysis_data_dfs[group]

            # set font and fontsize
            plt.rc('font', family='Times New Roman')
            plt.rcParams.update({'font.size': 12})
            # csfont = {'fontname':'Times New Roman',
            # 'size': 12}

            # creates subplot figure (top is full plot, bottom is cropped plot)
            fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

            # take the time, P1, and P2 data from the edited dataframe as series
            t_plt = case['t[s]']
            P1_plt = case['P1 [mbar]']
            P2_plt = case['P2 [mbar]']

            # plot both the P1 and P2 data wrt time on each plot
            line1P2, = ax1.plot(t_plt, P2_plt, color = "blue")
            line1P1, = ax1.plot(t_plt, P1_plt, color = "red")


            # add grid to plot
            ax1.grid()

            # set xlim and ylim for full plot
            ax1.set_xlim(t_plt.min(), t_plt.max())
            ax1.set_ylim(min(P1_plt.min(), P2_plt.min()), max(P1_plt.max(), P2_plt.max()))

            # instructions on what to do
            ax1.set_title('Press left mouse button and drag '
                          'to select a region in the top graph')

            # setting legend and ylabel for full plot
            ax1.set(ylabel="P [mbar]")
            ax1.legend((line1P1, line1P2), ('P1', 'P2'), loc="upper right")

            # creating empty lines for initial output of cropped plot, lists will be filled from onselect() callback fn
            line2P2, = ax2.plot([], [], color ='blue')
            line2P1, = ax2.plot([], [], color ='red')

            # setting x and y labels of cropped plot and grid
            ax2.set(xlabel="Time [s]", ylabel="P [mbar]")
            ax2.grid()

            '''
            Callback function onselect() gets called after the SpanSelector function finishes i.e. the region of the graph is
            selected. One will note that onselect is called each time the region is selected. In onselect() the time and pressure 
            values of the cropped plot are determined from the minimum and maximum indices selected from the full plot. The data and
            x and y limits for the cropped plot are then determined. Following this, the selected  t, P1, and P2 data is stored
            in a dataframe in the same structure as in line 65, where this dataframe is added to dict_of_analysis_data_dfs  
            with a key = to the current group being looped through. The value of the first t in the dataframe is set to zero for
            use in FR analysis through least squares fitting.  
            '''

            def onselect(xmin, xmax):
                '''
                determines the minimum and maximum indices based on the location in the t_plt series
                that the selected min and max t from SpanSelector are located
                '''
                indmin, indmax = np.searchsorted(t_plt, (xmin, xmax))
                indmax = min(len(t_plt) - 1, indmax)

                # determines t, P1, and P@ values of selected region
                region_t = t_plt[indmin:indmax]
                region_P1 = P1_plt[indmin:indmax]
                region_P2 = P2_plt[indmin:indmax]

                # creates dataframe of region of interest setting initial t to zero
                dataframe = pd.DataFrame(
                    {'P1 [mbar]': region_P1, 'P2 [mbar]': region_P2, 't[s]': region_t - region_t.min()})

                # replaces dataframe in dictionary
                dict_of_analysis_data_dfs[group] = dataframe
                modified_groups.append(group)

                # sets the cropped plots data values and limits.
                if len(region_t) >= 2:
                    line2P1.set_data(region_t, region_P1)
                    line2P2.set_data(region_t, region_P2)
                    ax2.set_xlim(region_t.min(), region_t.max())
                    ax2.set_ylim(min(region_P1.min(), region_P2.min()), max(region_P1.max(), region_P2.max()))
                    fig.canvas.draw_idle()

            # function that allows us to select data of interest, see matplotlib documentation
            span = SpanSelector(
                ax1,
                onselect,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:blue"),
                interactive=True,
                drag_from_anywhere=True
            )
            # Set useblit=True on most backends for enhanced performance.
            # ax2.legend((line2P1, line2P2), ('P1', 'P2'), loc = "upper right")
            plt.show()
        print('specified groups:')
        print(modified_groups)
        return dict_of_analysis_data_dfs

"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: var_est_gmm(y_vec,P_x)

Function calculates the estimate of the variance of the error of a Gauss Markov Model (GMM) of the form 

y_vec = X_mat*Beta_vec + e_vec

Where the mathematical formula is

sigma^2 = (y_vec^T*(I-P_x))*y_vec)/(n-r) = SSE/(n-r) = sum((y_i - y_hat_i)^2)/(n-r)

Where

P_x = X*(X^T*X)^-1*X^T (orthogonal projection matrix)
n = number of rows in y_vec (Nx1 vector)
r = rank(X_mat) = rank(P_x)

Summary:
Inputs:
1) a vector of obersvations/responses, y_vec
2) a vector of the estimated responses, E_y_hat_vec
3) a matrix of inputs, X_mat

Outputs:
1) estimate of the variance of the error of each observation 

"""

def var_est_gmm(y_vec, E_y_hat_vec, X_mat):
    y_vec_shape = np.shape(y_vec) #obtain shape of the observation vector (N,1) (Nx1)
    num_rows = y_vec_shape[0] #obtain value of N
    rank_X = np.linalg.matrix_rank(X_mat) #calculate the rank of the input matrix
    residuals = y_vec - E_y_hat_vec #calculate the residuals (difference between actual and estimated response)
    squared_residuals = np.square(residuals) #square each residual
    sse = np.sum(squared_residuals) #sum the residuals
    var_est = sse/(num_rows-rank_X) #calculate the estimate of the variance
    return var_est

'''
Title: ls_sinewave(dict_of_df, dict_of_freq)

Function performs ordinary least squares (OLS) estimation of sinewaves assuming a Gauss Markov Model with Normal Errors 
(GMMNE) General Linear Model (GLM) of the form:
 
 y = XB + e ; e~N(0,sigma^2)

Where in terms of sinewaves one can consider a general sinewave of the form:

 u(t) = U*sin(omega*t+phi) + m = U*cos(phi)*sin(omega*t) + U*sin(phi)*cos(omega*t) + m
 
If written in the form of a GLM, knowing that U, cos(phi), sin(phi), and m are constant:

  (y)                  (X)                    (B)
 u(t) = [sin(omega*t) cos(omega*t) 1]*[U*cos(phi) U*sin(phi) m]^T + e 

The Best Linear Unbiased Estimator for this model is:

    B_hat = X*(X^T*X)^-1*X^T*y

The error variance, sigma^2, can be estimated with var_est_gmm fn which calculates

sigma^2_hat = (y^T*(I-P_x)*y)/(n-r)= SSE/(n-r) = sum((y_i - y_hat_i)^2)/(n-r)

Where

P_x = X*(X^T*X)^-1*X^T (orthogonal projection matrix)
n = number of rows in y_vec (Nx1 vector)
r = rank(X_mat) = rank(P_x)

The estimate of the covariance matrix of the estimated parameters is then calculated with 

cov_hat(B_hat) = sigma^2_hat*(X^T*X)^-1 

Where the variance of each parameter is the diagonal of the covariance matrix

Summary: 
Inputs: 
1) a dictionary of dataframes where each key in the dictionary represents data from csv file at a specific frequency, dict_of_df
    data must have a 'P1 [mbar]', 'P2 [mbar], and 't[s]' column currently, although this can easily be changed for a general case 
2) a dictionary of the frequencies tested where key-values pairs are of the form 0pointXY : 0.XY, dict_of_freq

Outputs:
Plots actual data used and the fit from the estimation for both the input and output sinusoid for all frequencies. Returns 6 dictionaries:
1) the estimated parameters of the input wave, input_est_dict
2) the estimated parameters of the output wave, output_est_dict 
        (see general sinewave in GLM from above for reference to the parameters). Output in key-value form:
        
            0pointXY : [U*cos(phi), U*sin(phi), m] ~numpy array
            
3) estimation of error variance for input wave, var_est_input_dict 
4) estimation of error variance for output wave, var_est_output_dict 

Output in key-value form:
        
            0pointXY : [est_var] 


5) estimation of variance of estimated parameters for input wave, param_cov_mat_in_dict
6) estimation of variance of estimated parameters for output wave, param_cov_mat_out_dict

Output in key-value form:
        
            0pointXY : [U*cos(phi), U*sin(phi), m] ~numpy array
'''

def ls_sinewave(dict_of_dfs, dict_of_freq, plot='n'):
    input_est_dict ={}
    output_est_dict ={}
    var_est_input_dict = {}
    var_est_output_dict = {}
    param_cov_mat_in_dict = {}
    param_cov_mat_out_dict = {}
    for group in dict_of_dfs:
        ls_test_case = dict_of_dfs[group]
        f = dict_of_freq[group]

        P1_ls = ls_test_case["P1 [mbar]"].values  # gives Nx1 np array
        P2_ls = ls_test_case["P2 [mbar]"].values  # gives Nx1 np array
        t_ls = ls_test_case["t[s]"].values  # gives Nx1 np array

        omega = 2 * np.pi * f  # calculating frequency in rad/s (omega = 2*pi*f)
        X_t = np.array([np.sin(omega * t_ls), np.cos(omega * t_ls), np.ones(len(t_ls))])  # creating X_transpose
        X = np.transpose(X_t)  # creating X matrix
        Xt_mult_X = np.matmul(X_t, X)  # Xt*X
        inv_Xt_mult_X = np.linalg.inv(Xt_mult_X)  # (Xt*X)^-1
        inv_Xt_mult_X_mult_Xt = np.matmul(inv_Xt_mult_X, X_t)  # (Xt*X)^-1*X_t


        in_est_params = np.matmul(inv_Xt_mult_X_mult_Xt, P1_ls)  # (Xt*X)^-1*X_t*y = beta_hat calculating param est for input wave
        out_est_params = np.matmul(inv_Xt_mult_X_mult_Xt, P2_ls)  # (Xt*X)^-1*X_t*y = beta_hat calculating param est for output wave

        input_est_dict[group] = in_est_params
        output_est_dict[group] = out_est_params

        # calculating the estimate of the output from the estimated parameters
        E_y_in_hat = np.matmul(X, in_est_params)  # E(y_hat) = X*beta_hat = X*(Xt*X)^-1*X_t*y
        E_y_out_hat = np.matmul(X, out_est_params)  # E(y_hat) = X*beta_hat = X*(Xt*X)^-1*X_t*y

        #calculating the estimate of the variance of the error in the responses using var_est_gmm fn
        est_var_P1 = var_est_gmm(P1_ls,E_y_in_hat,X)
        est_var_P2 = var_est_gmm(P2_ls,E_y_out_hat,X)

        #adding variance estimate for given freq to dictionary
        var_est_input_dict[group] = est_var_P1
        var_est_output_dict[group] = est_var_P2

        #calculating the estimate of the covariance matrix of the estimated parameters
        cov_in_param_est = est_var_P1*inv_Xt_mult_X
        cov_out_param_est = est_var_P2*inv_Xt_mult_X

        #adding covariance estimate for given freq to dictionary
        param_cov_mat_in_dict[group] = cov_in_param_est
        param_cov_mat_out_dict[group] = cov_out_param_est
        if plot != 'n':
            # testing the validity of the estimate through plotting experimental and estimated data
            plt.rc('font', family='Times New Roman')
            plt.rcParams.update({'font.size': 12})

            fig, (ax1, ax2) = plt.subplots(2)

            ax1.grid()
            ax2.grid()

            #setting title of each plot to be specific frequency
            ax1.set(ylabel="P [mbar]")
            ax2.set(ylabel="P [mbar]", xlabel="Time [s]")
            if len(group) >= 8:
               ax1.set_title('f = 0.' + group[6:8] + "[Hz]")
            else:
               ax1.set_title('f = 0.' + group[6] + "[Hz]")

            #plotting experimental data and line of estimate
            data_line_in, = ax1.plot(t_ls, P1_ls, color = 'red')
            est_line_in, = ax1.plot(t_ls, E_y_in_hat, color = 'black')
            ax1.plot(t_ls, in_est_params[2] * np.ones(len(t_ls)), color='grey', linestyle='dashed')
            ax1.set_xlim(min(t_ls), max(t_ls))
            data_line_out, = ax2.plot(t_ls, P2_ls, color = 'blue')
            ax2.plot(t_ls, E_y_out_hat, color = 'black')
            ax2.plot(t_ls, out_est_params[2] * np.ones(len(t_ls)), color='grey', linestyle='dashed')
            ax2.set_xlim(min(t_ls), max(t_ls))

            ax1.legend((data_line_in, data_line_out, est_line_in), ('Input','Output', 'Estimate'), loc="upper right")

            plt.show()
    return input_est_dict, output_est_dict, var_est_input_dict, var_est_output_dict, param_cov_mat_in_dict, param_cov_mat_out_dict
"""
**********************************************END OF FUNCTION***********************************************************
"""


"""
Title: sw_mag(dict_of_params)

Summary:
Intakes dictionary of estimated sinewave parameters for different frequencies and outputs a dictionary of magnitudes of
the sinewaves for each frequency. Where the magnitude of a general sinusoid of the form

u(t) = U*sin(omega*t+phi) + m = U*cos(phi)*sin(omega*t) + U*sin(phi)*cos(omega*t) + m

If written in the form of a GLM, knowing that U, cos(phi), sin(phi), and m are constant:

  (y)                  (X)                    (B)
 u(t) = [sin(omega*t) cos(omega*t) 1]*[U*cos(phi) U*sin(phi) m]^T + e
 
 Magnitude is given by:
 
    U = sqrt((U*cos(phi))^2 + (U*sin(phi))^2)
 
Inputs:
1) Dictionary of estimated parameters, dict_of_params, with key-value pair:
    
    '0pointXY': array([U*cos(phi), U*sin(phi), m])
    
Outputs:
1) dictionary of the magnitudes for the different frequency cases, key-value pair:
    
    '0pointXY': float(magnitude)
"""

def sw_mag(dict_of_params):
    dict_of_mag={}
    for group in dict_of_params.keys():
        est_params = dict_of_params[group]
        dict_of_mag[group] = m.sqrt(est_params[0]**2+est_params[1]**2)
    return dict_of_mag

"""
**********************************************END OF FUNCTION***********************************************************
"""


"""
Title: sw_phase(dict_of_params, deg)

Summary:
Intakes dictionary of estimated sinewave parameters for different frequencies and outputs a dictionary of the phases of
the sinewaves for each frequency. Where the phase of a general sinusoid of the form

u(t) = U*sin(omega*t+phi) + m = U*cos(phi)*sin(omega*t) + U*sin(phi)*cos(omega*t) + m

If written in the form of a GLM, knowing that U, cos(phi), sin(phi), and m are constant:

  (y)                  (X)                    (B)
 u(t) = [sin(omega*t) cos(omega*t) 1]*[U*cos(phi) U*sin(phi) m]^T + e

 phase is given by:

    phi = atan(U*sin(phi)/U*cos(phi))

Inputs:
1) Dictionary of estimated parameters, dict_of_params, with key-value pair:

    '0pointXY': array([U*cos(phi), U*sin(phi), m])
2) string deg == 'y' or 'n'

Outputs:
1) dictionary of the phase for the different frequency cases, key-value pair:

    '0pointXY': float(phase)
if deg =='y' outputs phase in degrees instead of radians, defaulted to 'n'
"""

def sw_phase(dict_of_params, deg ="n"):
    dict_of_phase ={}
    for group in dict_of_params.keys():
        est_params = dict_of_params[group]
        dict_of_phase[group] = m.atan(est_params[1]/est_params[0])
        if deg == "y":
            dict_of_phase[group] = (dict_of_phase[group]*180)/m.pi
    return dict_of_phase
"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: ls_sw_mag_uncert(df_est_p_and_u)

Summary:
Intakes dataframe of estimated parameters and their uncertainties 
from OLS sinewave fitting for different frequencies and calculates the 95%
confident uncertainty value for the magnitude calculation. Where 

del_u_mag_hat = +- sqrt((d_mag_hat/d_A_hat*del_u_A_hat)^2+(d_mag_hat/d_B_hat*del_u_B_hat)^2)

d_mag/d_A_hat = A_hat/sqrt(A_hat^2+B_hat^2)
del_u_A_hat = 1.96(sigma_A_hat) *sigma_A_hat is in input dataframe
d_mag/d_B_hat = -B_hat/sqrt(A_hat^2+B_hat^2)
del_u_B_hat = 1.96(sigma_B_hat)  *sigma_B_hat is in input dataframe

Inputs:
1)  df_est_p_and_u, Dataframe of estimated parameters with uncertainties in form:
    [U*cos(phi) del_u_A U*sin(phi) del_u_B m del_u_m]

Outputs:
1) 1XN numpy array of estimated magnitude uncertainty for each estimated magnitude


"""
def ls_sw_mag_uncert(df_est_p_and_u):
    A = df_est_p_and_u['U*cos(phi)'].values
    B = df_est_p_and_u['U*sin(phi)'].values
    del_u_A = df_est_p_and_u['del_u_A'].values
    del_u_B = df_est_p_and_u['del_u_B'].values

    d_mag_d_A = np.multiply(A, np.reciprocal(np.sqrt((np.square(A) + np.square(B)))))
    d_mag_d_B = np.multiply(B, np.reciprocal(np.sqrt((np.square(A) + np.square(B)))))

    del_u_mag = np.sqrt(np.square(np.multiply(d_mag_d_A, del_u_A)) + np.square(np.multiply(d_mag_d_B, del_u_B)))
    return del_u_mag

"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: ls_sw_phase_uncert(df_est_p_and_u)

Summary:
Intakes dataframe of estimated parameters and their uncertainties 
from OLS sinewave fitting for different frequencies and calculates the 95%
confident uncertainty value for the phase calculation in rads. Where 

del_u_phase_hat = +- sqrt((d_phase_hat/d_A_hat*del_u_A_hat)^2+(d_phase_hat/d_B_hat*del_u_B_hat)^2)

d_phase_hat/d_A_hat = -B_hat/(A_hat^2+B_hat^2)
del_u_A_hat = 1.96(sigma_A_hat) *sigma_A_hat is in input dataframe
d_phase_hat/d_B_hat = A_hat/(A_hat^2+B_hat^2)
del_u_B_hat = 1.96(sigma_B_hat)  *sigma_B_hat is in input dataframe

Inputs:
1) df_est_p_and_u, Dataframe of estimated parameters with uncertainties in form:
    [U*cos(phi) del_u_A U*sin(phi) del_u_B m del_u_m]

Outputs:
1) 1XN numpy array of estimated phase [rad] uncertainty for each estimated phase [rad]


"""
def ls_sw_phase_uncert(df_est_p_and_u):
    A = df_est_p_and_u['U*cos(phi)'].values
    B = df_est_p_and_u['U*sin(phi)'].values
    del_u_A = df_est_p_and_u['del_u_A'].values
    del_u_B = df_est_p_and_u['del_u_B'].values

    d_phase_d_A = -1 * np.multiply(B, np.reciprocal(np.square(A) + np.square(B)))
    d_phase_d_B = np.multiply(A, np.reciprocal(np.square(A) + np.square(B)))

    del_u_phase_rad = np.sqrt(np.square(np.multiply(d_phase_d_A, del_u_A)) + np.square(np.multiply(d_phase_d_B, del_u_B)))
    #del_u_phase_deg = del_u_phase_rad*(180/np.pi)
    return del_u_phase_rad

"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: mag_fr_uncert(in_mag_phase_df, out_mag_phase_df, del_u_mag_in, del_u_mag_out)

Summary:
Intakes dataframes of input and output magnitude and phase calculations from OLS estimation of the sinewaves, as well as
1xN numpy arrays of the calculated uncertainty in the input magnitude and output magnitude from OLS estimation. Outputs 
1xN numpy array representing the uncertainty in the unitless FR_magnitude calculations for each frequency. 

del_u_FR_mag_hat = +- sqrt((d_FR_mag_hat/d_Mi_hat*del_u_Mi_hat)^2+(d_FR_mag_hat/d_Mo_hat*del_u_Mo_hat)^2)

d_FR_mag_hat/d_Mi_hat = -Mo_hat/(Mi_hat^2)
del_u_Mi_hat = del_u_mag_in *del_u_Mi_hat is in input dataframe del_u_mag_in, needs to be calculated from ls_sw_mag_uncert fn
d_FR_mag_hat/d_Mo_hat = 1/Mi_hat
del_u_Mo_hat = del_u_mag_out *del_u_Mo_hat is in input dataframe del_u_mag_out, needs to be calculated from ls_sw_mag_uncert fn

Inputs:
1) in_mag_phase_df, dataframe of input magnitudes and phase calculated from OLS sinewave estimation in fr_analysis_prgrm.py, of form:
    [Magnitude [unitless] Phase [deg]]
    
2) out_mag_phase_df, dataframe of output magnitudes and phase calculated from OLS sinewave estimation in fr_analysis_prgrm.py, of form:
    [Magnitude [unitless] Phase [deg]]
    
3) del_u_mag_in, 1xN numpy array of the uncertainties associated with each magnitude calculation from the estimated parameters
    of the input sinewave, obtained from ls_sw_mag_uncert_fn
    
4) del_u_mag_out, 1xN numpy array of the uncertainties associated with each magnitude calculation from the estimated parameters
    of the output sinewave, obtained from ls_sw_mag_uncert_fn

Outputs:
1) 1XN numpy array of estimated FR magnitude uncertainty for each frequency
"""

def mag_fr_uncert(in_mag_phase_df,out_mag_phase_df,del_u_mag_in, del_u_mag_out):
    mag_in = in_mag_phase_df['Magnitude [unitless]'].values
    mag_out = out_mag_phase_df['Magnitude [unitless]'].values

    d_mag_fr_d_mag_out = np.reciprocal(mag_in)
    d_mag_fr_d_mag_in = -1*np.multiply(mag_out,np.reciprocal(np.square(mag_in)))

    del_u_mag_fr = np.sqrt(np.square(np.multiply(d_mag_fr_d_mag_out,del_u_mag_out))+np.square(np.multiply(d_mag_fr_d_mag_in,del_u_mag_in)))
    return del_u_mag_fr

"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: mag_fr_uncert_dB(fr_df, del_u_mag_fr)

Summary:
Intakes dataframe of magnitude and phase frequency response calculated from fr_analysis_prgrm.py along with a 1xN numpy 
array of estimated uncertainties in the magnitude calculations, calculated from mag_fr_uncert_fn. Outputs a 1xN numpy 
array of the calculated uncertainty associated with scaling the magnitude in the dB scale. Where 

del_u_FR_mag_dB_hat = +- d_FR_mag_dB_hat/d_FR_mag_hat*del_u_FR_mag_hat

d_FR_mag_dB_hat/d_FR_mag_hat = 20/(M*ln(10))
del_u_FR_mag_hat = del_u_mag_fr *del_u_FR_mag_hat is in input dataframe del_u_mag_fr, needs to be calculated from mag_fr_uncert fn

Inputs:
1) fr_df, dataframe of FR magnitudes and phase calculated from OLS sinewave estimation of parameters in fr_analysis_prgrm.py, of form:
    [Magnitude [unitless] Magnitude [dB] Phase [deg] f[Hz] f[rad/s]]

2) del_u_mag_fr, 1xN numpy array calculated from mag_fr_uncert fn


Outputs:
1) 1XN numpy array of estimated FR magnitude uncertainty in dB for each frequency
"""

def mag_fr_uncert_db(fr_df, del_u_mag_fr):
    m = fr_df['Magnitude [unitless]'].values
    d_mdb_d_m = 20*np.reciprocal(np.log(10)*m)
    del_u_mag_fr_db = np.multiply(d_mdb_d_m,del_u_mag_fr)
    return del_u_mag_fr_db

"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: phase_fr_uncert_dB(del_u_phase_rad_in,del_u_phase_rad_out)

Summary:
Intakes input and output 1xN numpy arrays of the estimated unceratinty in the estimate of phase [rad] calculated from
ls_sw_phase_uncert_fn. Outputs 1xN numpy array of estimated uncertainty in estimate of phase FR calculated from
fr_analysis_prgrm.py. Where:

del_u_FR_phase_hat = sqrt((del_u_in_phase_hat)^2 +(del_u_out_phase_hat)^2)

del_u_in_phase_hat = del_u_phase_rad_in, calculated from ls_sw_phase_uncert_fn
del_u_out_phase_hat = del_u_phase_rad_out, calculated from ls_sw_phase_uncert_fn

Inputs:
1) del_u_phase_rad_in, 1xN numpy array calculated from ls_sw_phase_uncert fn in [rad] (uncertainty in input phase estimation)

2) del_u_phase_rad_out, 1xN numpy array calculated from ls_sw_phase_uncert fn in [rad] (uncertainty in output phase estimation)


Outputs:
1) 1XN numpy array of estimated FR phase uncertainty in [rad] for each frequency
"""

def phase_fr_uncert(del_u_phase_rad_in,del_u_phase_rad_out):
    del_u_phase_fr_rad = np.sqrt(np.square(del_u_phase_rad_in)+np.square(del_u_phase_rad_out))
    return del_u_phase_fr_rad

"""
**********************************************END OF FUNCTION***********************************************************
"""

"""
Title: relative_uncertainty(fr_mag_phase_df)

Summary:
intakes datafframe of mag and phase FR with uncertainties and calculates the relative uncertainties and appends these 
to the dataframe, outputs the new dataframe. Note that relative uncertainty is given by:

del_u/U*100 ; U is the measured value

Inputs:
1) dataframe of mag and phase FR values with ucnertainties of form:

[Magnitude [unitless] del_u_mag [unitless] Magnitude [dB] del_u_mag [dB] Phase [deg] del_u_phase [deg]]

Outputs:
1) dataframe of form 

[Magnitude [unitless] del_u_mag [unitless] rel_del_u_mag [%] Magnitude [dB] del_u_mag [dB] rel_del_u_mag_db [%] Phase [deg] del_u_phase [deg] rel_del_u_phase [%]]

"""
def relative_uncertainty(fr_mag_phase_df):
    row_names = list(fr_mag_phase_df.index)
    del_u_mag = fr_mag_phase_df['del_u_mag [unitless]'].values
    del_u_mag_db = fr_mag_phase_df['del_u_mag [dB]'].values
    del_u_phase = fr_mag_phase_df['del_u_phase [deg]'].values
    mag = fr_mag_phase_df['Magnitude [unitless]'].values
    mag_db = fr_mag_phase_df['Magnitude [dB]'].values
    phase = fr_mag_phase_df['Phase [deg]'].values
    rel_u_mag = abs(100*np.multiply(del_u_mag,np.reciprocal(mag)))
    rel_u_mag_dB = abs(100*np.multiply(del_u_mag_db,np.reciprocal(mag_db)))
    rel_u_phase = abs(100*np.multiply(del_u_phase,np.reciprocal(phase)))
    rel_u_df = pd.DataFrame({'Magnitude [unitless]': mag, 'del_u_mag [unitless]': del_u_mag,'rel_del_u_mag [%]': rel_u_mag,
                             'Magnitude [dB]': mag_db,'del_u_mag_dB [dB]': del_u_mag_db, 'rel_del_u_mag_db [%]': rel_u_mag_dB,
                             'Phase [deg]': phase, 'del_u_phase [deg]': del_u_phase,
                             'rel_del_u_phase [%]': rel_u_phase }, index=row_names)
    return rel_u_df

"""
**********************************************END OF FUNCTION***********************************************************
"""