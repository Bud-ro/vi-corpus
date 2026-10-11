# FR_analysis
## Summary
Code for obtaining magnitude and phase frequency response (FR) from measured voltage data, followed by transfer function (TF) estimation. Measurement data is digitally stored using TDMS file format, from two sensors using a NI DAQ/LabVIEW experimental setup. Utilizes both Python and MATLAB. Allows user to select portion of time-domain data they want to use for frequency response analysis, and determines magnitude and phase FR at a 95% confidence level in the uncertainty of the calculated values. User can then estimate a TF fit to the data and obtain uncertainty in estimated parameters. Original use of code was for master's thesis work obtaining presure transient transfer function across tubing in a microfluidic system. As such, current code setup converts voltages to pressures, only considers a freqeuncy range from 0.01 to 0.4 Hz, and considers fitting a first-order function, but these can be easily changed to morph the code for general applications. Each code file has its own in depth commenting/description outlining functions of the specific file, and lines that could/need to be changed to enhance/change the output. More work has to be done to make code more general.

## Dependencies
### Python
1. os
2. numpy
3. nptdms
4. pandas
5. pathlib
6. math
7. matplotlib.pyplot
8. matplotlib.widgets (SpanSelector)
9. functions.py

### MATLAB
1. Control Systems Toolbox

## Order of use of code files
1. make_python_output_directories.py (Makes directories for output files from .py files in ./code/python/output folder)
2. make_matlab_output_directories.py (Makes directories for output files from .m files in ./code/matlab/output folder)
3. tdms_to_cropped_seperate_csv_prgrm.py (select region of data from TDMS files to use in fr_analysis_prgrm.py, loops through all frequencies)
4. fr_analysis_prgrm.py (perform OLS fitting of pressure waves to general sinewave model, estimates sinewave model parameters and magnitude and phase FR)
5. fr_uncertainty_analysis.py (perform uncertainty analysis of magnitude and phase FR )
6. bode_plot_prgrm_from_py_w_uncert.m (Plot Magnitude and Phase FR in bode plot format, also estimate TF based off experimental FR and estimate step response)
7. upper_and_lower_uncert_bound_bode_plot_prgrm.m (Determine uncertainty bounds of estimated TF parameters)
8. uncert_tf_params_and_tau_seq_pert.py (Calculate uncertainty of estimated TF parameters and associated transient response characteristic)


