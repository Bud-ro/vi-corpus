%{ 
Summary:
Code is used to estimate the value of the transfer function parameters
for the experimental data at the upper and lower bound of the uncertainty
interval for magnitude and phase. Upper and lower bound values of magnitude
and phase were output by bode_plot_prgrm_from_py_w_uncert.m into
./outputs/uncert_intervals/test/mag_and_phase/. User selects which test
they want to perform the analysis on, and is then prompted to look at
either the upper or lower bound. User can continuously change value of
parameters and rerun code until fit to the upper/lower bound is achieved,
at which point they may output the upper and lower bound parameters to
./outputs/params_and_tau/test/ub and /lb where this output is used in
uncert_tf_params_and_tau_seq_pert.py to calculate the uncertainty in the
raw and non-dimensionalized parameter estimates using sequential
perturbation. 

Notes:
1. Change folder_path (line 28)
2. Change test (line 29)
3. Change output folders (lines 118, 194)
. Change upper and lower bound parameters (lines 50-52, 129-131)



%}

%setting up where folder is being extracted from (change on each run)
folder_path = './outputs/uncert_intervals/e_over_poff_6_3_2024/mag_and_phase/';
test = 'FEP';
type_of_file = '_mag_and_phase.csv';

read_path = strcat(folder_path,test,type_of_file);

%{
reading in matrix of upper and lower bounds for each frequency, matrix
form:

[mag_lb [dB] mag_ub [dB] phase_lb [deg] phase_ub [deg] freq [rad/s]]

%}
bounds_mat = readmatrix(read_path);

upper_or_lower = input(['Do you want to perform fitting for the upper or lower bound of ' ...
    'the experimental data? (u/l): '], 's');

if upper_or_lower == 'l'
    
    plot_lb_string = 'lower bound plotted, Parameter values:'
    %lower bound tf
    a_lb = 0.08
    b_lb = 54 %increase shifts down, decrease shits up (+ del_u_b) determine upper and lower bound by taking average of average relative uncertainty of mag_FR and phase_FR (in frequency range affected by b [0.01-0.1 Hz]) and that is relative uncert in b
    d_lb = .06    
    lb_open_loop_system  = tf(1*[a_lb 1],[b_lb 1], 'InputDelay',d_lb);
    omega_td = logspace(-2,1);
    [lb_mag_td_data, lb_phase_td_data] = bode(lb_open_loop_system,omega_td);
    
    lb_mag_td_data_sort = zeros(1, length(omega_td));
    lb_phase_td_data_sort = zeros(1, length(omega_td));
    
    for i=1:length(omega_td)
        lb_mag_td_data_sort(1,i) = lb_mag_td_data(1,1,i);
        lb_phase_td_data_sort(1,i) = lb_phase_td_data(1,1,i);
    end
    
    lb_mag_td_data_sort_dB = 20*log10(lb_mag_td_data_sort);
    
    %lower bound bode plot
    figure(1)
    subplot(2,1,1)
    semilogx(bounds_mat(:,5),bounds_mat(:,1), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15);
    set(gca, 'XLim', [10^-2 10^1]); %a jostle [0.06 0.7], normal [10^-2 10^0]
    set(gca, 'YTick', -55:5:5); % a jostle : -35:0:5, normal : [-55:5:5]
    set(gca, 'YLim', [-55 5]); % a jostle: [-35 0], normal: [-55 5]
    ylabel("Magnitude [dB]")
    set(gca,'FontSize',12);
    set(gca,'fontname','times');
    grid on
    hold on
    semilogx(omega_td, lb_mag_td_data_sort_dB, "Color","k", "LineStyle","--", "LineWidth",2);
    legend("Experimental Data", "Model Fit")
    hold off
    
    subplot(2,1,2)
    semilogx(bounds_mat(:,5),bounds_mat(:,3), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15);
    set(gca, 'XLim', [10^-2 10^1]); %for  a jostle [0.06 0.7]
    set(gca, 'YLim', [-180 135]);
    set(gca, 'YTick', -180:45:135);
    xlabel("Freqeuncy [rad/s]")
    ylabel("Phase [deg]")
    set(gca,'FontSize',12);
    set(gca,'fontname','times');
    grid on
    hold on
    semilogx(omega_td, lb_phase_td_data_sort, "Color","k", "LineStyle","--","LineWidth",2);
    hold off
    
    %step
    figure(2)
    step(lb_open_loop_system)
    [lb_out, lb_tout] = step(lb_open_loop_system);
    %obtaining time constant for first order system (time to reach 63% of final
    %value). Note that the step info funciton only takes rise time, but to get
    %time constant just set the rise time to the time to rise from 0% to 63% of
    %steady state value
    lb_info = stepinfo(lb_open_loop_system,'RiseTimeLimits',[0 0.63]);
    tau_lb = lb_info.RiseTime
    
    %write parameters and tau to .csv file
    param_and_tau_lb = [a_lb b_lb d_lb tau_lb];
    colNames_lb = {'a_lb', 'b_lb', 'd_lb', 'tau_lb'};
    param_and_tau_table_lb = array2table(param_and_tau_lb,'VariableNames',colNames_lb);
    
    test_lb = input(strcat('output lower bound parameter and tau values to .csv file for ', test, ' ? (y/n): '),'s');
    if test_lb == 'y'
        param_output_folder_lb = './outputs/params_and_tau/e_over_poff_6_3_2024/lb/';
        param_output_file_path_lb = strcat(param_output_folder_lb,test,'_lb',type_of_file);
        writetable(param_and_tau_table_lb, param_output_file_path_lb);
    else
        else_string_lb = strcat(test, '_lb parameter and tau values not output to csv')
    end

elseif upper_or_lower =="u"

    plot_ub_string = 'upper bound plotted, Parameter values:'
    %upper bound tf
    a_ub = 0.20
    b_ub = 50 %increase shifts down, decrease shits up (- del_u_b) determine upper and lower bound by taking average of average relative uncertainty of mag_FR and Phase_FR (in frequency range affected by b [0.01-0.1 Hz]) and that is relative uncert in b
    d_ub = .08
    ub_open_loop_system  = tf(1*[a_ub 1],[b_ub 1], 'InputDelay',d_ub);
    omega_td = logspace(-2,1);
    [ub_mag_td_data, ub_phase_td_data] = bode(ub_open_loop_system,omega_td);
    
    ub_mag_td_data_sort = zeros(1, length(omega_td));
    ub_phase_td_data_sort = zeros(1, length(omega_td));
    
    for i=1:length(omega_td)
        ub_mag_td_data_sort(1,i) = ub_mag_td_data(1,1,i);
        ub_phase_td_data_sort(1,i) = ub_phase_td_data(1,1,i);
    end
    
    ub_mag_td_data_sort_dB = 20*log10(ub_mag_td_data_sort);
    
    %upper bound bode
    figure(1)
    subplot(2,1,1)
    semilogx(bounds_mat(:,5),bounds_mat(:,2), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15);
    set(gca, 'XLim', [10^-2 10^1]);
    set(gca, 'YTick', -55:5:5);
    set(gca, 'YLim', [-55 5]);
    ylabel("Magnitude [dB]")
    set(gca,'FontSize',12);
    set(gca,'fontname','times');
    grid on
    hold on
    semilogx(omega_td, ub_mag_td_data_sort_dB, "Color","k", "LineStyle","--", "LineWidth",2);
    legend("Experimental Data", "Model Fit")
    hold off
    
    subplot(2,1,2)
    semilogx(bounds_mat(:,5),bounds_mat(:,4), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15);
    set(gca, 'XLim', [10^-2 10^1]);
    set(gca, 'YLim', [-180 135]);
    set(gca, 'YTick', -180:45:135);
    xlabel("Freqeuncy [rad/s]")
    ylabel("Phase [deg]")
    set(gca,'FontSize',12);
    set(gca,'fontname','times');
    grid on
    hold on
    semilogx(omega_td, ub_phase_td_data_sort, "Color","k", "LineStyle","--","LineWidth",2);
    hold off
    
    %step
    figure(2)
    step(ub_open_loop_system)
    [ub_out, ub_tout] = step(ub_open_loop_system);
    %obtaining time constant for first order system (time to reach 63% of final
    %value). Note that the step info funciton only takes rise time, but to get
    %time constant just set the rise time to the time to rise from 0% to 63% of
    %steady state value
    ub_info = stepinfo(ub_open_loop_system,'RiseTimeLimits',[0 0.63]);
    tau_ub = ub_info.RiseTime
    
    %write parameters and tau to .csv file
    param_and_tau_ub = [a_ub b_ub d_ub tau_ub];
    colNames_ub = {'a_ub', 'b_ub', 'd_ub', 'tau_ub'};
    param_and_tau_table_ub = array2table(param_and_tau_ub,'VariableNames',colNames_ub);
    
    test_ub = input(strcat('output upper bound parameter and tau values to .csv file for ', test, ' ? (y/n): '),'s');
    if test_ub == 'y'
        param_output_folder_ub = './outputs/params_and_tau/e_over_poff_6_3_2024/ub/';
        param_output_file_path_ub = strcat(param_output_folder_ub,test,'_ub',type_of_file);
        writetable(param_and_tau_table_ub, param_output_file_path_ub);
    else
        else_string_ub = strcat(test, '_ub parameter and tau values not output to csv')
    end
else
    no_plot = 'neither option selected, rerun code'
end

