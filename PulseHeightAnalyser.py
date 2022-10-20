import numpy as np 
import scipy.signal as sig
import scipy.optimize as optimize
import matplotlib.pyplot as plt 
import ROOT as r
# from r.Math import landau_pdf
from random import choices
import matplotlib
matplotlib.use('Agg')

failed_plots=[]

toy_pdf_scaling_factor = 0.4
toy_landau_parameters = [0.08 , 1 , 0.08]
toy_gauss_parameters =  [0.3 , 3 , 0.1]
signal_wiggle_room_down = 0.5
signal_wiggle_room_up = 1.5
# toy_landau_parameters = [0.17667582  , 1 , 0.0520044]
# toy_gauss_parameters =  [0.32132375 , 3.04389941 , 0.07263753]


    # #obtain the Landau-Birk distribution
idealDistributionFile = r.TFile("extractions/Landau_Birk.root","READ")    
hist=idealDistributionFile.Get('Simulated energy deposits in one specific bar')

nbins = 60
Landau_Birk  = []
for i in range (0,int(nbins/2)):
    Landau_Birk.append(0)
for i in range (1,nbins+1):
    Landau_Birk.append(hist.GetBinContent(i))
for i in range (0,int(nbins/2)-1):
    Landau_Birk.append(0)

Landau_Birk = np.array(Landau_Birk)
Landau_Birk = np.roll(Landau_Birk,-10)
# #normalizes sample to the signal's size
Landau_Birk_integral = sum(Landau_Birk)
Landau_Birk_normalised  = Landau_Birk / Landau_Birk_integral 

Landau_Birk_normalised_short  = Landau_Birk_normalised[30:90]


def convolution_function( energy, landau_amplitude=1, landau_mean=3, landau_width=0.1, gauss_amplitude=1, gauss_mean=3, gauss_width=0.1): 
    # print(landau_amplitude, landau_mean, landau_width, gauss_amplitude, gauss_mean, gauss_width, )
    pure_signal = landau( energy, landau_amplitude, landau_mean, landau_width )
    noise = gaussian( energy, gauss_amplitude, gauss_mean, gauss_width )
    detected_signal = sig.convolve(  noise,pure_signal )
    return detected_signal

def fixed_convolution_function( energy, gauss_amplitude=1, gauss_mean=3, gauss_width=0.1, distortion=1): 
    # print(landau_amplitude, landau_mean, landau_width, gauss_amplitude, gauss_mean, gauss_width, )
    pure_signal = fixed_landau( energy, distortion )
    noise = gaussian( energy, gauss_amplitude, gauss_mean, gauss_width )
    detected_signal = sig.convolve(  noise,pure_signal )
    return detected_signal

def gaussian( energy, amplitude, mean, width ): 
    noise = amplitude * np.exp( -( energy - mean )**2 / ( 2 * width**2 ) )
    # noise=[max(1e-7,i) for i in noise]  # set noise minimum to prevent deconvolution bug
    return noise

def fixed_landau( energy, distortion ):
    return Landau_Birk_normalised_short*distortion


def landau( energy, amplitude, mean, width ):
    return [ amplitude*r.Math.landau_pdf( energy_point, width,mean ) for energy_point in energy ]



def analyse_bar(layer,strip,end):
    #define plot
    name = "Layer "+str(layer)+", Strip "+str(strip)+", End "+str(end)
    plt.figure(name)



    #define x axis
    resolution = 59
    energy = np.linspace( 0, 6, resolution+1 ) # Define energy range in MIP equivalents
    energy_extended = np.linspace( -3, 9, resolution*2+1 ) # the range of energies for convolved values



    inFile = r.TFile("extractions/Pulse height analysis layer "+str(layer)+', strip '+str(strip)+', end '+str(end)+".root","READ")    
    hist=inFile.Get('cuts')
    sample_size = int(hist.GetEntries())
    
    #define y axis
    nbins = 60
    sample_as_normalised_function  = []
    sample_error_bars =[]
    for i in range (0,int(nbins/2)):
        sample_as_normalised_function.append(0)
        sample_error_bars.append(0)
    for i in range (1,nbins+1):
        sample_as_normalised_function.append(hist.GetBinContent(i))
        sample_error_bars.append(hist.GetBinError(i))
    for i in range (0,int(nbins/2)-1):
        sample_as_normalised_function.append(0)
        sample_error_bars.append(0)




    #define initial guesses

    sample_maximum = max(sample_as_normalised_function)
    sample_maximum_index = sample_as_normalised_function.index(sample_maximum)
    sample_landau_average = energy_extended[sample_maximum_index]
    toy_landau_parameters[1] = sample_landau_average


    #create initial guess functions
    initial_guess_pure_signal = landau( energy, *toy_landau_parameters )
    initial_guess_noise = gaussian( energy, *toy_gauss_parameters )
    initial_guess_detected_signal = sig.convolve(initial_guess_noise, initial_guess_pure_signal ) 


    #generate fake sample
    # #samples amount from the detected signal
    # sample_size=100000
    # sample_as_individual_entries = np.array(choices( energy_extended,detected_signal,k=sample_size)) 
    # #converts detected signal into a plottable function
    # sample_as_function = np.zeros(len(energy_extended))
    # for i in sample_as_individual_entries:
    #     index = np.where(energy_extended == i)[0][0]
    #     sample_as_function[index] += 1
    # #normalizes sample to the signal's size
    # signal_pdf_integral = sum(detected_signal)
    # sample_function_integral = sum(sample_as_function) #alos just sample size
    # sample_as_normalised_function  = sample_as_function / sample_function_integral * signal_pdf_integral #/ sample_size *len(energy) # normalizes


    #deconvolve the convolution pdf as a sanity check
    # deconvolved_signal,_ = sig.deconvolve(initial_guess_detected_signal, initial_guess_noise)



    try:
        convolution_fit_parameters, _ = optimize.curve_fit(convolution_function, energy, sample_as_normalised_function, 
        # p0=(*toy_landau_parameters,*toy_gauss_parameters ),
        # bounds = ((0,toy_landau_parameters[1]-0.1,0,1e-5,0,1e-5),(1,toy_landau_parameters[1]+0.3,1,2,6,2)),
        # maxfev=50 )
        p0=(*toy_landau_parameters,*toy_gauss_parameters ),
        bounds = ((toy_landau_parameters[0]*signal_wiggle_room_down,toy_landau_parameters[1]-0.1,toy_landau_parameters[2]*signal_wiggle_room_down,1e-5,0,1e-5),
        (toy_landau_parameters[0]*signal_wiggle_room_up,toy_landau_parameters[1]+0.1,toy_landau_parameters[2]*signal_wiggle_room_up,2,6,2)),
        maxfev=50 )
    except:
        print('unsuccesful fit')    
        failed_plots.append(name)
        plt.text(2.5, 0.15, 'failed to fit', fontsize = 15)
        convolution_fit_parameters = [1e-6,-2,1e-6,1e-6,-2,1e-6, ]

    try:
        fixed_convolution_fit_parameters, _ = optimize.curve_fit(fixed_convolution_function , energy, sample_as_normalised_function, 
        p0=(*toy_gauss_parameters,1),
        bounds = ((1e-5,0,1e-5,0.5),(2,6,2,1.5)),
        maxfev=50 )
    except:
        print('unsuccesful advanced fit')    
        failed_plots.append(name)
        plt.text(2.0, 0.15, 'failed to fit advanced ', fontsize = 15)
        fixed_convolution_fit_parameters = [1e-6,-2,1e-6]




    #create fit functions
    print(convolution_fit_parameters)
    convolution_fit = convolution_function( energy, *convolution_fit_parameters )
    fixed_convolution_fit = fixed_convolution_function( energy, *fixed_convolution_fit_parameters )
    deduced_signal = landau( energy, *convolution_fit_parameters[0:3] )
    deduced_noise = gaussian( energy, *convolution_fit_parameters[3:6] )

    fixed_deduced_signal = fixed_landau( energy, fixed_convolution_fit_parameters[3] )
    fixed_deduced_noise = gaussian( energy, *fixed_convolution_fit_parameters[0:3] )




    #plot the data
    # plt.plot( energy, initial_guess_pure_signal, linestyle='dashed', color='black', label='initial guess signal' )
    # plt.plot( energy-3, initial_guess_noise, linestyle='dashed', color='gray', label='initial guess noise' )

    plt.plot( energy, deduced_signal,  linestyle='dashed', color='black', label='Previous method signal' )
    plt.plot( energy-3, deduced_noise,  linestyle='dashed', color='gray', label='Previous method r/o response' )
    plt.plot( energy_extended, convolution_fit, linestyle='dashed', color='slategray', label='Previous method fit of data', zorder=3)


    plt.plot( energy, fixed_deduced_signal,  linestyle='solid', color='green', label='Improved method signal' )
    plt.plot( energy-3, fixed_deduced_noise,  linestyle='solid', color='lime', label='Improved method r/o response' )
    plt.plot( energy_extended, fixed_convolution_fit, linestyle='solid', color='cyan', label='Improved method fit of data', zorder=3)

    plt.errorbar( energy_extended, sample_as_normalised_function, yerr=sample_error_bars, linestyle = 'None', marker='_', color='blue', label='Data', zorder=4) 

    # plt.plot( energy_extended, Landau_Birk_normalised , color='red', label='Landau Birk', zorder=4) 


    #Finish the plot
    plt.xlim(-1,6)
    plt.ylim(0,0.4)
    plt.xlabel('Energy response in MIP equivalents')
    plt.ylabel('Number of MIP hits, normalised to data')
    plt.text(2.5, 0.1, name, fontsize = 15)
    plt.annotate('Sample size: '+str(sample_size), xy=(0., 1.05), xycoords='axes fraction')
    plt.legend()
    plt.savefig('plots/deconvolution '+name+'.png', dpi=300)
    plt.close()

single_mode=False
# single_mode=True

if single_mode:
    # analyse_bar(5,1,1)
    analyse_bar(13,1,0)

else:
    # for layer in (3,5,7,9):
    for layer in (3,):
        print(layer)
        for strip in range(0,8):
            for end in (0,1):
                # try:
                    analyse_bar(layer,strip,end)
                # except:pass    

toy_landau_parameters[1] = 'varies'


# print('Using initial guesses:')
# print(toy_landau_parameters, toy_gauss_parameters)

# print(str(len(failed_plots))+'/64 failed. These are:')
# for i in failed_plots:
#     print(i)
