import numpy as np 
import scipy.signal as sig
import scipy.optimize as optimize
import matplotlib.pyplot as plt 
import ROOT as r
from random import choices
import matplotlib
matplotlib.use('Agg')

def create_summary_plot(parameters,name=''):
    #creates one of the summary plots
    fig, ax = plt.subplots()
    im = ax.imshow(parameters.transpose())

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(layer_numbers)))
    ax.set_yticks(np.arange(len(bar_numbers)))
    ax.set_xticklabels(layer_numbers)
    ax.set_yticklabels(bar_numbers)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in layer_numbers:
        for j in bar_numbers:
            if 'size' in name: text = ax.text(i-3, j, int(parameters[i-3, j]),  ha="center", va="center", color="w")
            else: text = ax.text(i-3, j, parameters[i-3, j],  ha="center", va="center", color="w")

    ax.set_title(name+" for each bar")
    fig.tight_layout()
    plt.xlabel('Layer')
    plt.ylabel('Bar number')
    plt.savefig('plots/'+name+'.png', dpi=300)


def get_landau_birk():
    #obtain the Landau-Birk distribution
    idealDistributionFile = r.TFile("extractions/Simulated energy deposits in one specific bar in MIPeq___pure_bars.root","READ")    
    hist=idealDistributionFile.Get('Simulated energy deposits in one specific bar in MIPeq')
    nbins = 600
    Landau_Birk  = np.array([hist.GetBinContent(i) for i in range (1,nbins+1)])
    Landau_Birk_integral = sum(Landau_Birk)
    Landau_Birk_normalised  = Landau_Birk / Landau_Birk_integral 
    return Landau_Birk_normalised



def generate_sample(sample_signal,sample_noise): 
    #if you ever figure out how to do this, this code might be a basis
    #currently, it's mathematically wrong
    sample_size=1000000
    sample_function = np.zeros(len(sample_signal))
    for i in range(sample_size):
            true_deposit = choices(range(len(sample_signal)), sample_signal) [0]
            smeared_deposit = max(0,min(590,true_deposit * choices(range(len(sample_noise))-300, sample_noise) [0] ))
            sample_function[smeared_deposit] += 1
    sample_normalised_function = sample_function / sample_size
    return sample_normalised_function


def gaussian( energy, amplitude, mean, width ): #gaussian function used in this program
    return amplitude * np.exp( -( energy - mean )**2 / ( 2 * width**2 ) )

def landau( energy): #landau function used in this program
    return Landau_Birk_normalised_short

def convolution_function(energy, gauss_amplitude=1, gauss_mean=3, gauss_width=0.1): #Landau-Gauss convolution used in this program
    pure_signal = landau(energy)
    noise = gaussian(energy, gauss_amplitude, gauss_mean, gauss_width)
    detected_signal = sig.convolve(noise, pure_signal)
    return detected_signal


#the main function which finds the landau-gauss convolution for a given SiPM
def analyse_SiPM(layer,strip,end): 
    #define plot
    name = "Layer "+str(layer)+", Strip "+str(strip)+", End "+str(end)
    plt.figure(name)

    #Define x axes.
    resolution = 600 #aka the number of bins
    #energy is the x axis for non-convolved values
    energy = np.linspace( 0, 6, resolution,endpoint=False) # Define energy range in MIP equivalents
    #energy_extended is the x axis for convolved values. It has to be double-1 the bins of the non-convolved values
    energy_extended = np.concatenate( [np.linspace( -3, 0, int(resolution/2),endpoint=False),np.linspace( 0, 6, resolution,endpoint=False),np.linspace( 6, 9, int(resolution/2),endpoint=False)[1:]])
    
    #obtain data for SiPM
    inFile = r.TFile("extractions/Pulse height analysis layer "+str(layer)+', strip '+str(strip)+', end '+str(end)+".root","READ")    
    hist=inFile.Get('cuts')
    sample_size = int(hist.GetEntries())
    sample_as_normalised_function  = []
    sample_error_bars =[]
    for i in range (0,int(resolution/2)):
        sample_as_normalised_function.append(0)
        sample_error_bars.append(0)
    # for i in range (1,resolution+1):
    for i in range (0,resolution):
        sample_as_normalised_function.append(hist.GetBinContent(i))
        sample_error_bars.append(hist.GetBinError(i))
    for i in range (0,int(resolution/2)-1):
        sample_as_normalised_function.append(0)
        sample_error_bars.append(0)

    #attempts to fit the data
    try:
        convolution_fit_parameters, _ = optimize.curve_fit(convolution_function , energy, sample_as_normalised_function, 
        p0=(*toy_gauss_parameters,),  bounds = ((1e-5,0,1e-5),(2,6,2)), maxfev=50 )
    except:
        print('unsuccesful fit')    
        failed_plots.append(name)
        plt.text(2.0, 0.15, 'failed to fit advanced ', fontsize = 15)
        convolution_fit_parameters = [1e-6,-2,1e-6]

    #create fit functions
    convolution_fit = convolution_function( energy, *convolution_fit_parameters )
    deduced_signal = landau( energy )
    deduced_noise = gaussian( energy, *convolution_fit_parameters[0:3] )

    #plot the data
    plt.plot( energy, deduced_signal,  linestyle='solid', color='green',label='Assumed signal', zorder=1 )
    plt.plot( energy-3, deduced_noise,  linestyle='solid', color='lime',label='Deduced r/o response', zorder=1 ) #the -3 may be inexact
    plt.plot( energy_extended, convolution_fit, linestyle='solid', color='cyan', label='Fit of data', zorder=4)
    plt.errorbar( energy_extended, sample_as_normalised_function, yerr=sample_error_bars, linestyle = 'None', marker='_', color='blue', label='Testbeam data', zorder=3) 
    # sample_normalised_function = generate_sample(Landau_Birk_normalised_short,deduced_noise)
    # plt.plot( energy, sample_normalised_function, linestyle = 'None', marker='x', color='red', label='Generated sample', zorder=1)


    #Finish the plot
    plt.xlim(-1,6)
    plt.xlim(-1,4)
    plt.ylim(0,0.06)

    plt.xlabel('Energy response in MIP equivalents')
    plt.ylabel('Number of MIP hits, normalised to data')
    plt.text(1.5, 0.01, name, fontsize = 15)
    plt.annotate('Sample size: '+str(sample_size), xy=(0., 1.05), xycoords='axes fraction')
    plt.legend()
    plt.savefig('plots/deconvolution '+name+'.png', dpi=300)
    plt.close()
    print('Created plot with parameters',convolution_fit_parameters)

    #add data to summary plots
    if end == 0:
        sample_size_ends0[layer-3,strip] = int(sample_size)
        gaussian_amplitudes_ends0[layer-3,strip]= round(convolution_fit_parameters[0]*normalization_to_signal_amplitude_factor,3)
        gaussian_positions_ends0[layer-3,strip]= round(convolution_fit_parameters[1]-3,3)
        gaussian_widths_ends0[layer-3,strip]= round(convolution_fit_parameters[2],3)
    elif end == 1:    
        sample_size_ends1[layer-3,strip] = int(sample_size)
        gaussian_amplitudes_ends1[layer-3,strip]= round(convolution_fit_parameters[0]*normalization_to_signal_amplitude_factor,3)
        gaussian_positions_ends1[layer-3,strip]= round(convolution_fit_parameters[1]-3,3)
        gaussian_widths_ends1[layer-3,strip]= round(convolution_fit_parameters[2],3)


# defines basics of the detector
layer_numbers = range(3,15)
bar_numbers = range(0,8)
layer_count = len(layer_numbers)
bar_count = len(bar_numbers)
toy_gauss_parameters =  [0.3 , 3 , 0.1]


#obtains provided Landau function once for the whole program
Landau_Birk_normalised_short = get_landau_birk()
normalization_to_signal_amplitude_factor = 1/max(Landau_Birk_normalised_short)


#variables for keeping track of analysis
def summary_matrix(): return np.zeros([layer_count,bar_count]) #the matrix in which the data for each type of summary variable is stored
sample_size_ends0 = summary_matrix()
gaussian_amplitudes_ends0 = summary_matrix()
gaussian_positions_ends0 = summary_matrix()
gaussian_widths_ends0 = summary_matrix()
sample_size_ends1 = summary_matrix()
gaussian_amplitudes_ends1 = summary_matrix()
gaussian_positions_ends1 = summary_matrix()
gaussian_widths_ends1 = summary_matrix()
failed_plots=[]
plots_made=0


# Main program loop. Either does a single bar if in single mode or all specified bars if not
single_mode=False
# single_mode=True
if single_mode:
    analyse_SiPM(3,0,0)
else:
    for layer in range(3,15):
        print(layer)
        for strip in range(0,8):
            for end in (0,1):
                analyse_SiPM(layer,strip,end)
                plots_made+=1



#If any plots fail to fit, it displays them
if len(failed_plots) > 0:
    print(str(len(failed_plots))+'/'+str(plots_made)+' failed. These are:')
    for i in failed_plots:
        print(i)
else: print('All plots fitted succesfully')  



#creates summary plots
create_summary_plot(sample_size_ends0,'sample size end 0')
create_summary_plot(gaussian_amplitudes_ends0,'readout response amplitude end 0')
create_summary_plot(gaussian_positions_ends0,'readout response position end 0')
create_summary_plot(gaussian_widths_ends0,'readout response width end 0')

create_summary_plot(sample_size_ends1,'sample size end 1')
create_summary_plot(gaussian_amplitudes_ends1,'readout response amplitude end 1')
create_summary_plot(gaussian_positions_ends1,'readout response position end 1')
create_summary_plot(gaussian_widths_ends1,'readout response width end 1')

#provides summary data
print('amplitude averages end 0', gaussian_amplitudes_ends0.mean())
print('position averages end 0', gaussian_positions_ends0.mean())
print('width averages end 0', gaussian_widths_ends0.mean())

print('amplitude averages end 1', gaussian_amplitudes_ends1.mean())
print('position averages end 1', gaussian_positions_ends1.mean())
print('width averages end 1', gaussian_widths_ends1.mean())

print('amplitude sigmas end 0', gaussian_amplitudes_ends0.std())
print('position sigmas end 0', gaussian_positions_ends0.std())
print('width sigmas end 0', gaussian_widths_ends0.std())

print('amplitude sigmas end 1', gaussian_amplitudes_ends1.std())
print('position sigmas end 1', gaussian_positions_ends1.std())
print('width sigmas end 1', gaussian_widths_ends1.std())



