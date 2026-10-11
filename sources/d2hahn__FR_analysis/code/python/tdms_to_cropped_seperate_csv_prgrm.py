"""
Summary:
Purpose of script is to edit TDMS files containing both the transient and steady-state sinusoidal
data such that only the steady-state sinusoidal data is used in the LS fit for frequency response analysis, while also
prepping the data to be used in such an analysis. This script allows the user to select the data of
interest such that an optimal sinewave LS fit is obtained (i.e. the pressure wave of P1 is taken to start at a zero
crossing, where this zero crossing is relabeled as t = 0s.). The parsed and edited data is saved to separate .csv files
for each frequency in:

    ./outputs/single_phase_no_droplet/cropped_dataframe_to_csv/name_of_test.csv (name_of_test edited by user)
    or
    ./outputs/name_of_test/cropped_dataframe_to_csv/name_of_test.csv

Dependencies:
1. numpy
2. nptdms
3. pandas
4. matplotlib (note not needed in current setup, only needed for testing code-body of region_of_interest_fn)
5. functions.py
6. pathlib

Input TDMS files overview:
TDMS files input into this script contain groups of all frequencies tested, where a single TDMS file is for a single
experimental case, with each group in the given file representing one frequency that was tested. (Repeated groups are ok)

Notes:
1. TDMS file to be read into tdms_file must be changed on each code run (see line 55)

2. Calibration curves used are P[mbar] = 201.09*E[V] -1.9532 for P1 (dev1/ai1) and P[mbar] = 200.75*E[V] - 1.3837 for P2
(dev1/ai0), change this if calibration and/or psensors/DAQ change. (see lines 74 and 75)

3. list_of_desired_groups must be edited depending on the data that you want to parse from the specific TDMS file
(see line 93)

4. For region_of_interest function, if you want to edit data over entire frequency range, leave second argument blank
if you want to only edit specific frequency ranges, input a list into the second argument e.g ['0point01', '0point5']
(see line 114)

5. If /name_of_test directory you want to save .csv files to does not exist, must create it before running this code
(see line 145)

"""
import numpy as np
import pandas as pd
import nptdms as tdms
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from functions import region_of_interest
from pathlib import Path

#creates empty dictionary
dict_of_df = {}

#read TDMS file of interest (need to switch each run)
tdms_file = tdms.TdmsFile.read("../../../FR_test_data/main_da_tests/e_over_poff/FEP_t2_6_25_2024.tdms")

#saves all groups as list to variable
all_groups = tdms_file.groups()

#loops through each group
for group in all_groups:

    #obtain group name as string
    group_name = group.name

    #get P1 and P2 data from group as 1D array
    all_channels = group.channels()
    p1_data = all_channels[1]
    p2_data = all_channels[0]
    p1_data_num = p1_data[:]
    p2_data_num = p2_data[:]

    #convert P data from V to mbar from calibration curves (change calibration relationship if needed)
    p1_data_num = 201.09*p1_data_num-1.9532
    p2_data_num = 200.75*p2_data_num-1.3837

    #create 1D array of time using the sample time for the given experiement
    t = np.zeros(p1_data_num.size)
    for i in range(len(t)):
        if i == 0:
            t[i] = 0
        else:
            t[i] = t[i - 1] + p1_data.properties['wf_increment'] #sample time of DAQ from TDMS file properties

    #create pandas dataframe containing pressure measurements and time
    df = pd.DataFrame({'P1 [mbar]': p1_data_num, 'P2 [mbar]': p2_data_num, 't[s]': t})

    # add dataframe to dictionary of dataframes with key being the name of the group from which the channel data was
    # obtained
    dict_of_df[group_name] = df

#creating list of groups that have the experimental data we want to analyze (will need to change for each TDMS file)
list_of_desired_groups = ["0point01", "0point02", "0point03", "0point04", "0point05", "0point06", "0point07",
    "0point08", "0point09", "0point1", "0point2","0point22","0point25","0point28", "0point3", "0point32",
    "0point35","0point38","0point4"]

#creating a dictionary sorted in ascending frequency of the experimental data we want to analyze, omits groups not in
#above list and gets rid of #Z in group name: note requires naming convention 0pointXY in LabVIEW to work
sorted_dict_of_df={}
for group in list_of_desired_groups:
    if len(group) >= 8 and group[7] == ' ':
         sorted_dict_of_df['0point'+group[6]] = dict_of_df[group]
    elif len(group) >=8 and group[7] != ' ':
        sorted_dict_of_df['0point'+group[6:8]] = dict_of_df[group]
    else:
        sorted_dict_of_df[group] = dict_of_df[group]


"""
creating new dict of df's, where the data is parsed using the region_of_interest fn (see functions.py). For the user of
this code: if you want to edit the entire frequency range leave the second argument blank, if you only want to edit data
in specific frequency ranges input a list of the group names in the sorted_dict_of_df you want to edit, note that all
repeat tests, e.g. 0pointXY #Z, from the TDMS file have had their key in the dictionary changed to '0pointXY' (removed
#Z) 
"""

analysis_dict = region_of_interest(sorted_dict_of_df,['0point35', '0point38', '0point4'])

"""
***WARNING**
If writing csv files to a new directory, must make this directory first before running the code.
Be very careful when running following lines, ensure appropriate paths are set and you are not overwriting good data.
User input has been requested at certain lines to try to minimize chance of overwriting good data, all though this is
still possible if someone really wants to.

Purpose of following section is to output the edited data groups to csv files. DO NOT NEED TO EDIT FOR USE (unless you
want to improve functionality in some way). Output to csv done during runtime, with various user input requests to
ensure that only the data the user wants written to a given file is, and the user does not accidently overwrite good data.
"""
#outputting data frames to csv
answer = input("Output to csv file (y/n)?: ")
while answer != 'y' and answer != 'n':
    answer = input("please type in y or n: ")

if answer == "y":
    check = input("are you sure you want to output to csv (y/n)?: ")
    if check == "y":
        print("")
        print("WARNING: IF YOU SPECIFY 'all' ALL GROUPS WILL BE WRITTEN TO CSV FILES EVEN IF THEY WERE NOT EDITED \n")
        dfs_to_csv = input("which groups do you want to export to csv? [enter 'all' or specified groups seperated by '' (whitespace)]: ")
        print("")
        check_2 = input("The group(s) you want to export to separate .csv files are [" + dfs_to_csv + "] is this correct (y/n)? :")
        print("")
        while check_2 =="n":
            print("")
            print("WARNING: IF YOU SPECIFY 'all' ALL GROUPS WILL BE WRITTEN TO CSV FILES EVEN IF THEY WERE NOT EDITED \n")
            dfs_to_csv = input("which groups do you want to export to csv? [enter 'all' or specified groups seperated by '' (whitespace)]: ")
            print("")
            check_2 = input("The group(s) you want to export to separate .csv files are [" + dfs_to_csv + "] is this correct (y/n)? :")
            print("")
        folder_path = input("enter folder path (from present folder i.e. ./subfolder/subsubfolder/) to save to: ")
        if dfs_to_csv == "all":
            for group in analysis_dict.keys():
                filepath = Path(folder_path+group+'.csv')
                analysis_dict[group].to_csv(filepath)
        else:
            groups = dfs_to_csv.split()
            for group in groups:
                filepath = Path(folder_path + group + '.csv')
                analysis_dict[group].to_csv(filepath)




"""
BELOW CODE WAS JUST USED FOR TESTING AND IDEATION, DO NOT NEED TO LOOK THROUGH IF YOU DO NOT WANT
"""
#good code for single group manipulation case and various tests
"""
import numpy as np
import pandas as pd
import nptdms as tdms

tdms_file = tdms.TdmsFile.read("../../../FR_test_data/single_phase_tests/data/raw/tdms_w_group/50_o_12point5_a.tdms")
all_groups = tdms_file.groups()
group = all_groups[0]
print(group.name)
all_group_channels = group.channels()
p2_data = all_group_channels[0]
p1_data = all_group_channels[1]

p1_data = p1_data[:]
p2_data = p2_data[:]

t = np.zeros(p1_data.size)
for i in range(len(t)):
    if i == 0:
        t[i] = 0
    else:
        t[i] = t[i-1] + 0.001

df = pd.DataFrame({'P1 [V]':p1_data, 'P2 [V]':p2_data, 't[s]': t})
print(df)

#test of span selector with single frequency case, used after sorted dictionary
case = sorted_dict_of_df["0point01"]

#set font and fontsize
plt.rc('font',family='Times New Roman')
plt.rcParams.update({'font.size': 12})
#csfont = {'fontname':'Times New Roman',
          #'size': 12}

#creates subplot figure (top is full plot, bottom is cropped plot)
fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

#take the time, P1, and P2 data from the edited dataframe as series
t_plt = case['t[s]']
P1_plt = case['P1 [mbar]']
P2_plt =case['P2 [mbar]']

#plot both the P1 and P2 data wrt time on each plot
line1P1, = ax1.plot(t_plt, P1_plt)
line1P2, =ax1.plot(t_plt, P2_plt)

#add grid to plot
ax1.grid()

#set xlim and ylim for full plot
ax1.set_xlim(t_plt.min(), t_plt.max())
ax1.set_ylim(P1_plt.min(), P1_plt.max())

#instructions on what to do
ax1.set_title('Press left mouse button and drag '
              'to select a region in the top graph')

#setting legend and ylabel for full plot
ax1.set(ylabel = "P [mbar]")
ax1.legend((line1P1, line1P2), ('P1', 'P2'), loc = "upper right")

#creating empty lines for initial output of cropped plot, lists will be filled from onselect() callback fn
line2P1, = ax2.plot([], [])
line2P2, = ax2.plot([], [])

#setting x and y labels of cropped plot and grid
ax2.set(xlabel = "Time [s]", ylabel = "P [mbar]")
ax2.grid()

'''
Callback function onselect() gets called after the SpanSelector function finishes i.e. the region of the graph is
selected. One will note that onselect is called each time the region is selected. In onselect() the time and pressure 
values of the cropped plot are determined from the minimum and maximum indices selected from the full plot. The data and
x and y limits for the cropped plot are then determined.  
'''
def onselect(xmin, xmax):
    '''
    determines the minimum and maximum indices based on the location in the t_plt series
    that the selected min and max t from SpanSelector are located
    '''
    indmin, indmax = np.searchsorted(t_plt, (xmin, xmax))
    indmax = min(len(t_plt) - 1, indmax)

    #determines t, P1, and P@ values of selected region
    region_t = t_plt[indmin:indmax]
    region_P1 = P1_plt[indmin:indmax]
    region_P2 = P2_plt[indmin:indmax]

    #sets the cropped plots data values and limits.
    if len(region_t) >= 2:
        line2P1.set_data(region_t, region_P1)
        line2P2.set_data(region_t, region_P2)
        ax2.set_xlim(region_t.min(), region_t.max())
        ax2.set_ylim(region_P1.min(), region_P1.max())
        fig.canvas.draw_idle()

#funciton that allows us to select data of interest, see matplotlib documentation 
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

"""

#original span_selector code used to develop region_of_interest fn

"""
'''
Below code uses SpanSelector widget to select data we want to do FR analysis on from plot of all transient pressure data
from experiments at a specific frequency. Formulation of code is custom built for our case, but the general idea of the 
code closely resembles that of the SpanSelector example from the matplotlib documentation, which can be found at the 
below link:

    https://matplotlib.org/stable/gallery/widgets/span_selector.html

Note that each frequency case is looped through from the sorted_dict_of_df dictionary where the loop variables come from
the list_of_desired_groups specified on line 72. This will need to be changed for each TDMS file. 
'''

#span selector for all cases

dict_of_analysis_data_dfs = {}

for group in list_of_desired_groups:
    case = sorted_dict_of_df[group]

    #set font and fontsize
    plt.rc('font',family='Times New Roman')
    plt.rcParams.update({'font.size': 12})
    #csfont = {'fontname':'Times New Roman',
            #'size': 12}

    #creates subplot figure (top is full plot, bottom is cropped plot)
    fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

    #take the time, P1, and P2 data from the edited dataframe as series
    t_plt = case['t[s]']
    P1_plt = case['P1 [mbar]']
    P2_plt =case['P2 [mbar]']

    #plot both the P1 and P2 data wrt time on each plot
    line1P1, = ax1.plot(t_plt, P1_plt)
    line1P2, = ax1.plot(t_plt, P2_plt)

    #add grid to plot
    ax1.grid()

    #set xlim and ylim for full plot
    ax1.set_xlim(t_plt.min(), t_plt.max())
    ax1.set_ylim(min(P1_plt.min(), P2_plt.min()), max(P1_plt.max(), P2_plt.max()))

    #instructions on what to do
    ax1.set_title('Press left mouse button and drag '
                'to select a region in the top graph')

    #setting legend and ylabel for full plot
    ax1.set(ylabel = "P [mbar]")
    ax1.legend((line1P1, line1P2), ('P1', 'P2'), loc = "upper right")

    #creating empty lines for initial output of cropped plot, lists will be filled from onselect() callback fn
    line2P1, = ax2.plot([], [])
    line2P2, = ax2.plot([], [])

    #setting x and y labels of cropped plot and grid
    ax2.set(xlabel = "Time [s]", ylabel = "P [mbar]")
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

        #determines t, P1, and P@ values of selected region
        region_t = t_plt[indmin:indmax]
        region_P1 = P1_plt[indmin:indmax]
        region_P2 = P2_plt[indmin:indmax]

        #creates dataframe of region of interest setting initial t to zero
        dataframe = pd.DataFrame({'P1 [mbar]': region_P1, 'P2 [mbar]': region_P2, 't[s]': region_t-region_t.min()})

        #adds dataframe to dictionary
        dict_of_analysis_data_dfs[group] = dataframe

        #sets the cropped plots data values and limits.
        if len(region_t) >= 2:
            line2P1.set_data(region_t, region_P1)
            line2P2.set_data(region_t, region_P2)
            ax2.set_xlim(region_t.min(), region_t.max())
            ax2.set_ylim(min(region_P1.min(), region_P2.min()), max(region_P1.max(), region_P2.max()))
            fig.canvas.draw_idle()

    #funciton that allows us to select data of interest, see matplotlib documentation
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
"""