%{ 
Summary:

Code intakes magnitude and phase FR data w uncertainties
from .csv files output by fr_uncertainty_analysis.py. This is performed for the
FR data collected for 0.01 Hz to 0.4 Hz from the fluigent pump. Upper and 
lower bound magnitude and phase data is calculated from the experimental FR
and its associated uncertainty. This matrix can be output as a .csv file for
use in quantifying the parameter uncertainty estimate using the
upper_and_lower_uncert_bound_bode_plot_prgrm.m script. 
Magnitude and phase Bode plots are made from both the experimental data (w/ uncertainty),
and a tf model used to fit a model to the experimental FR data, by
adjusting the value of the parameters of the model. Also outputs a step 
response for the fit model, then the user has the option to output the
model parameters and calculated time constant to a .csv file. Where this
output file is to be used in uncert_tf_params_and_tau_seq_pert.py to
calculate the uncertainty in the fit parameters using sequential
perturbation. Program also plots the non-dimensionalized frequency response
based off of the non-deimnsionalized frequency, omega_nd = omega*mu/p_off,
where nu (cSt) and p_off (mbar) are input by the user upon running the
program. Program also calculates the uncertainty associated with the
non-dimensionalized frequency. The bode data for both the
non-dimensionalized and raw data is output to
./outputs/sim_data/bode/test/. The non-dim frequency and uncertainty is
output to ./outputs/uncert_intervals/test/non_dim_freq/. The raw values of 
the parameters are output to ./outputs/params_and_tau/test/. The upper and 
 lower bound of the uncertainty interval for the magnitude and phase is
 output to ./outputs/uncert_intervals/test/mag_and_phase/.

Notes:

1. Will need to change the type_of_test_folder path for different tests
    (see line 82 )

2. Will need to change test_folder path for different tests (see line 83)

3. Will need to change output_folder path depending on tests (see line 111, 123)

4. Current transfer function model based off observed experimental FR from
    single phase tests (50_o_12point5_a , 100_o_25_a, and 200_o_50_a), where
    the model is of the form:

    G(s) = e^(-ds)*(1+as)/(1+bs)
    
    BE CAREFUL TO ALWAYS LOOK AT EXPERIMENTAL FR AND USE SIGNALS AND
    SYSTEMS/CONTROLS KNOWLEDGE TO DETERMINE IF MODEL IS APPROPRIATE
    
    Otherwise, only value of parameters needs to be changed depending on the
    test (see lines )

5. param_output_folder will need to be changed depending on the test
    considered (see lines 343,366, 370 )

%}

%Inputting offset pressure (mbar) and viscosity of oil (cSt) for scaling
%CHANGE OFFSET PRESSURE AND VISCOSITY FOR SCALING
p_off_mbar = input('Input offset pressure in mbar: '); %mbar
p_off_pa = p_off_mbar*100; %Pa

kin_visc  = input("Input kinematic viscosity of silicone oil (5, 10, 20, 50, 100) in cSt: ");

while kin_visc ~= 5 && kin_visc ~=10 && kin_visc ~=20 && kin_visc ~=50 && kin_visc ~=100
    kin_visc = input('Input kinematic viscosity that is 5, 10, 20, 50 , or 100 cSt)');
end 
if kin_visc == 5
    visc = 0.004565;
elseif kin_visc == 10
    visc = 0.009300;
elseif kin_visc == 20
    visc = 0.019000;
elseif kin_visc == 50
    visc = 0.048000;
else 
    visc = 0.096000;
end 

%read .csv files and edit to have columns: [mag [dB], del_u_mag [dB], 
% phase [deg], del_u_phase [deg], omega [rad/s]]

type_of_test_folder = '../python/outputs/pa_by_poff_4_3_2024/mag_and_phase/w_uncertainty/';
test_folder = '25_percent'; %only line you need to change for given test
test_file = '/fr_mag_phase_u.csv';

read_matrix_path = strcat(type_of_test_folder,test_folder,test_file);

%change file name on each run 
m_and_p = readmatrix(read_matrix_path);
m_and_p = [m_and_p(:,4) m_and_p(:,5) m_and_p(:,6) m_and_p(:,7) m_and_p(:,9)];

%calculating non-dimensionalized frequency (omega*visc/p_off_pa)
non_d_freq = m_and_p(:,5)*(visc/p_off_pa);

%calculating uncertainty in non-dimensionalized frequency
del_u_p_off = sqrt((0.0001*p_off_pa)^2+(0.0003*100000)^2);
del_u_non_d_freq = m_and_p(:,5)*(visc/(p_off_pa^2))*del_u_p_off;

%calculating upper and lower bound of confidence interval
upper_bound_mag = m_and_p(:,1)+m_and_p(:,2);
lower_bound_mag = m_and_p(:,1)-m_and_p(:,2);
upper_bound_phase = m_and_p(:,3)+m_and_p(:,4);
lower_bound_phase = m_and_p(:,3)-m_and_p(:,4);

%addding upper and lower bound to matrix [mag_lower mag_upper phase_lower
%phase_upper f[rad/s]]
uncertainty_interval = [lower_bound_mag upper_bound_mag lower_bound_phase upper_bound_phase m_and_p(:,5)];

%creating output folder for upper and lower bound matrix (change depending
%on test)
output_folder_mp = './outputs/uncert_intervals/pa_by_poff_4_3_2024/mag_and_phase/';
type_of_file ='.csv';
output_file_path_mp = strcat(output_folder_mp,test_folder,'_mag_and_phase',type_of_file);

%give user option to write to .csv file
output_upper_lower_bound = input(strcat('Output upper and lower bound to', ' ', output_file_path_mp, '? (y/n): '), 's');
if output_upper_lower_bound =='y'
    writematrix(uncertainty_interval, output_file_path_mp)
else
    else_string = strcat(test_folder, ' Upper and lower bound not output to .csv')
end 

output_folder_non_d_freq = './outputs/uncert_intervals/pa_by_poff_4_3_2024/non_dim_freq/';
output_file_path_non_d_freq = strcat(output_folder_non_d_freq,test_folder,'_non_dim_freq',type_of_file);

%creating matrix of non-dimensionalized frequency with uncertainty (abs and
%rel) [non_d_freq del_u del_u_rel [%]]

uncert_interval_non_d_freq = [non_d_freq del_u_non_d_freq del_u_non_d_freq./non_d_freq*100];

%give user option to write to .csv file
output_uncert_non_d_freq = input(strcat('Output non_d_freq and uncertainty to', ' ', output_file_path_non_d_freq, '? (y/n): '), 's');
if output_uncert_non_d_freq =='y'
    writematrix(uncert_interval_non_d_freq, output_file_path_non_d_freq)
else
    else_string = strcat(test_folder, ' Upper and lower bound not output to .csv')
end 

%{
Below commented section is just for testing and understanding (DO NOT
ACTUALLY APPLY TO DATA THAT IS PRESENTED FOR RESEARCH)
%}

%360 - lead phase for output
% m_and_p(11,2) = -263.047;
% m_and_p(12,2) = -261.3299;
% m_and_p(14,2) = -312.430;
% m_and_p(15,2) = -278.698;
% m_and_p(16,2) = -348.403;
% m_and_p(17,2) = -262.382;

%phase - 180
% m_and_p(1,2) = m_and_p(1,2)-180;
% m_and_p(2,2) = m_and_p(2,2)-180;
% m_and_p(3,2) = m_and_p(3,2)-180;
% m_and_p(4,2) = m_and_p(4,2)-180;
% m_and_p(5,2) = m_and_p(5,2)-180;
% m_and_p(6,2) = m_and_p(6,2)-180;
% m_and_p(7,2) = m_and_p(7,2)-180;
% m_and_p(8,2) = m_and_p(8,2)-180;
% m_and_p(9,2) = m_and_p(9,2)-180;
% m_and_p(10,2) = m_and_p(10,2)-180;
% m_and_p(11,2) = m_and_p(11,2)-180;
% m_and_p(12,2) = m_and_p(12,2)-180;
% m_and_p(13,2) = m_and_p(13,2)-180;
% m_and_p(14,2) = m_and_p(14,2)-180;
% m_and_p(15,2) = m_and_p(15,2)-180;
% m_and_p(16,2) = m_and_p(16,2)-180;
% m_and_p(17,2) = m_and_p(17,2)-180;
% m_and_p(18,2) = m_and_p(18,2)-180;

%{
Determining the frequency response data for a linear model, adjust the a,
b, d parameters below to get an appropriate fit (can also adjust the form
of the model if needed, but this will require further code manipulation.
From the most recent FR experiments it has been determined that the sample
tubing subsystem can be represented as a model of the form:

G(s) = e^(-ds)*(1+as)/(1+bs)

But this should always be checked by looking at experimental FR data points
and using frequency response/bode plot knowledge of general systems
%}

a = 0.2; %vary depending on test
b = 6.6; %vary depending on test
d = .15; %vary depending on test

open_loop_system  = tf(1*[a 1],[b 1], 'InputDelay',d)
omega_td = logspace(-2,1);
[mag_td_data, phase_td_data] = bode(open_loop_system,omega_td);

mag_td_data_sort = zeros(1, length(omega_td));
phase_td_data_sort = zeros(1, length(omega_td));

for i=1:length(omega_td)
    mag_td_data_sort(1,i) = mag_td_data(1,1,i);
    phase_td_data_sort(1,i) = phase_td_data(1,1,i);
end

mag_td_data_sort_dB = 20*log10(mag_td_data_sort);

%TF based off of non-dimensionalized frequency
a_nd = p_off_pa/visc*a; %vary depending on test
b_nd = p_off_pa/visc*b; %vary depending on test
d_nd = p_off_pa/visc*d; %vary depending on test

open_loop_system_nd  = tf(1*[a_nd 1],[b_nd 1], 'InputDelay',d_nd)
omega_td_nd = (visc/p_off_pa)*logspace(-2,1);
[mag_td_data_nd, phase_td_data_nd] = bode(open_loop_system_nd,omega_td_nd);

mag_td_data_sort_nd = zeros(1, length(omega_td_nd));
phase_td_data_sort_nd = zeros(1, length(omega_td_nd));

for i=1:length(omega_td_nd)
    mag_td_data_sort_nd(1,i) = mag_td_data_nd(1,1,i);
    phase_td_data_sort_nd(1,i) = phase_td_data_nd(1,1,i);
end

mag_td_data_sort_dB_nd = 20*log10(mag_td_data_sort_nd);

%bode plot (with dimensions)
% For presentations optimal line size 2, optimal marker size 15
figure(1)
subplot(2,1,1)
semilogx(m_and_p(:,5),m_and_p(:,1), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",5);
set(gca, 'XLim', [10^-2 10^1]);
set(gca, 'YTick', -55:5:5);
set(gca, 'YLim', [-55 5]);
ylabel("Magnitude [dB]")
set(gca,'FontSize',12);
set(gca,'fontname','times');
grid on
hold on
semilogx(omega_td, mag_td_data_sort_dB, "Color","k", "LineStyle","--", "LineWidth",2);
errorbar(m_and_p(:,5),m_and_p(:,1), m_and_p(:,2), m_and_p(:,2),"LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",5, "Color", 'k' );
legend("Experimental Data", "Model Fit")
hold off


subplot(2,1,2)
semilogx(m_and_p(:,5),m_and_p(:,3), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",5);
set(gca, 'XLim', [10^-2 10^1]);
set(gca, 'YLim', [-180 135]);
set(gca, 'YTick', -180:45:135);
xlabel("Freqeuncy [rad/s]")
ylabel("Phase [deg]")
set(gca,'FontSize',12);
set(gca,'fontname','times');
grid on
hold on
semilogx(omega_td, phase_td_data_sort, "Color","k", "LineStyle","--","LineWidth",2);
errorbar(m_and_p(:,5),m_and_p(:,3), m_and_p(:,4), m_and_p(:,4),"LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",5, "Color", 'k' );
hold off

% %bode plot (non-dimensionalized)
% figure(2)
% subplot(2,1,1)
% semilogx(non_d_freq,m_and_p(:,1), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15);
% set(gca, 'XLim', (visc/p_off_pa)*[10^-2 10^1]);
% set(gca, 'YTick', -55:5:5);
% set(gca, 'YLim', [-55 5]);
% ylabel("Magnitude [dB]")
% set(gca,'FontSize',12);
% set(gca,'fontname','times');
% grid on
% hold on
% semilogx(omega_td_nd, mag_td_data_sort_dB_nd, "Color","k", "LineStyle","--", "LineWidth",2);
% errorbar(non_d_freq,m_and_p(:,1), m_and_p(:,2), m_and_p(:,2),"LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15, "Color", 'k' );
% errorbar(non_d_freq,m_and_p(:,1), del_u_non_d_freq, del_u_non_d_freq, 'horizontal', "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15, "Color", 'k')
% legend("Experimental Data", "Model Fit")
% hold off
% 
% 
% subplot(2,1,2)
% semilogx(non_d_freq,m_and_p(:,3), "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15);
% set(gca, 'XLim', (visc/p_off_pa)*[10^-2 10^1]);
% set(gca, 'YLim', [-180 135]);
% set(gca, 'YTick', -180:45:135);
% xlabel('${\it} \frac{\omega \mu}{P_{off}} $','Interpreter','Latex', 'FontName','times')
% ylabel("Phase [deg]")
% set(gca,'FontSize',12);
% set(gca,'fontname','times');
% grid on
% hold on
% semilogx(omega_td_nd, phase_td_data_sort_nd, "Color","k", "LineStyle","--","LineWidth",2);
% errorbar(non_d_freq,m_and_p(:,3), m_and_p(:,4), m_and_p(:,4),"LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15, "Color", 'k' );
% errorbar(non_d_freq, m_and_p(:,3),del_u_non_d_freq, del_u_non_d_freq, 'horizontal', "LineStyle","none", "Marker","*", "MarkerFaceColor","r", "MarkerEdgeColor","r","MarkerSize",15, "Color", 'k')
% hold off

%Outputting magnitude and phase for transfer function models (dim and
%non-dim)
%creating matrices
% [mag [dB] phase [deg] freq [rad/s]]
%and
%[mag_non_dim [dB] phase_non_dim [deg] non_dim_freq = omega*visc/p_off]
sim_mag_and_phase = transpose([mag_td_data_sort_dB; phase_td_data_sort; omega_td]);
sim_mag_and_phase_nd = transpose([mag_td_data_sort_dB_nd; phase_td_data_sort_nd; omega_td_nd]);

output_folder_sim_bode = './outputs/sim_data/bode/pa_by_poff_4_3_2024/';
output_folder_sim_bode_nd = './outputs/sim_data/bode/pa_by_poff_4_3_2024/non_dim/';
type_of_file ='.csv';
output_file_path_sim_bode = strcat(output_folder_sim_bode,test_folder,'_bode_sim',type_of_file);
output_file_path_sim_bode_nd = strcat(output_folder_sim_bode_nd,test_folder,'_bode_sim_nd',type_of_file);

output_sim_bode_data  = input('Output simulated bode data (dim and non-dim)? (y/n): ','s')
if output_sim_bode_data =='y'
    writematrix(sim_mag_and_phase, output_file_path_sim_bode)
    writematrix(sim_mag_and_phase_nd, output_file_path_sim_bode_nd)
else
    else_string = strcat(test_folder, 'simulated bode data not output to .csv')
end 

%step response
% figure(3)
% step(open_loop_system)
[out, tout] = step(open_loop_system);
%obtaining time constant for first order system (time to reach 63% of final
%value). Note that the step info funciton only takes rise time, but to get
%time constant just set the rise time to the time to rise from 0% to 63% of
%steady state value
info = stepinfo(open_loop_system,'RiseTimeLimits',[0 0.63]);
tau = info.RiseTime;
step_data_sim = [tout,out];

%nice plot of step response
% figure(4)
% plot(tout,out, "Color","b")
% hold on
% plot(tout,ones(size(tout)),"LineStyle","--", "Color", "k")
% % plot([0:0.001:tau],0.63*ones(size([0:0.001:tau])),"LineStyle","-", "Color", "r");
% % plot(tau*ones(size([0:0.01:0.63])),[0:0.01:0.63],"LineStyle","-", "Color", "r");
% tau_txt = ['\tau = ' num2str(round(tau,1)) ' s'];
% text(.80*max(tout), 0.1, tau_txt, "FontSize",12, "FontName","times");
% hold off
% set(gca, 'YLim', [0 1.1]);
% set(gca, 'XLim', [0 tout(end)]);
% set(gca,'FontSize',12);
% set(gca,'fontname','times');
% xlabel("Time [s]")
% ylabel("Amplitude")

output_folder_sim_step = './outputs/sim_data/step/pa_by_poff_4_3_2024/';
type_of_file ='.csv';
output_file_path_sim_step = strcat(output_folder_sim_step,test_folder,'_step_sim',type_of_file);

output_sim_step_data = input('Output simulated step data (dim)? (y/n): ','s');
if output_sim_step_data =='y'
    writematrix(step_data_sim, output_file_path_sim_step)
else
    else_string = strcat(test_folder, 'simulated step data not output to .csv')
end 

%write parameters and tau to .csv file
param_and_tau = [a b d tau];
colNames = {'a', 'b', 'd', 'tau'};
param_and_tau_table = array2table(param_and_tau,'VariableNames',colNames);

non_d_params = [a_nd b_nd d_nd];
colNames_nd = {'a_nd', 'b_nd', 'd_nd'};
non_d_param_table = array2table(non_d_params, 'VariableNames',colNames_nd);

%give user option to write to .csv file 
test = input(strcat('output parameter and tau values to .csv file for ', test_folder, ' ? (y/n): '),'s');
if test == 'y'
    param_output_folder = './outputs/params_and_tau/pa_by_poff_4_3_2024/';
    param_output_file_path = strcat(param_output_folder,test_folder,'_params_and_tau',type_of_file);
    writetable(param_and_tau_table, param_output_file_path);

    non_d_param_output_folder = './outputs/params_and_tau/pa_by_poff_4_3_2024/non_dim_params/';
    non_d_param_output_file_path = strcat(non_d_param_output_folder,test_folder,'_non_d_params', type_of_file);
    writetable(non_d_param_table, non_d_param_output_file_path);
else
    else_string = strcat(test_folder, ' parameter and tau values not output to csv')
end

