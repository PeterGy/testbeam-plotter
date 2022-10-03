import numpy as np 
import scipy.signal as sig
import scipy.optimize as optimize
import matplotlib.pyplot as plt 
import ROOT as r
# from r.Math import landau_pdf
from random import choices
import matplotlib
matplotlib.use('Agg')


toy_pdf_scaling_factor = 0.4
toy_pdf_push_left = -0

toy_landau_parameters = [0.3*toy_pdf_scaling_factor , 2.15-toy_pdf_push_left , 0.067]
toy_gauss_parameters =  [1  *toy_pdf_scaling_factor , 2.06-toy_pdf_push_left , 0.1]
resolution = 59
nbins = 60



# inFile = r.TFile("extractions/Pulse height analysis layer "+str(5)+', strip '+str(3)+', end '+str(0)+".root","READ")  
inFile = r.TFile("extractions/Pulse height analysis layer "+str(5)+', strip '+str(3)+', end '+str(1)+".root","READ")  
hist=inFile.Get('cuts')

sample_as_normalised_function  = []

for i in range (0,int(nbins/2)):
    sample_as_normalised_function.append(0)
for i in range (1,nbins+1):
    sample_as_normalised_function.append(hist.GetBinContent(i))
for i in range (0,int(nbins/2)-1):
    sample_as_normalised_function.append(0)


# for i in range (1,nbins+1):
#     sample_as_normalised_function.append(hist.GetBinContent(i))
# inFile = r.TFile("extractions/Pulse height analysis layer "+str(layer)+', strip '+str(strip)+', end '+str(end)+".root","READ")    



def convolution_function( energy, landau_amplitude=1, landau_mean=3, landau_width=0.1, gauss_amplitude=1, gauss_mean=3, gauss_width=0.1): 
    # noise = gaussian( energy, 0.2, 5, 0.77 )
    # pure_signal = landau( energy, 1, 3, 0.1 )

    noise = gaussian( energy, gauss_amplitude, gauss_mean, gauss_width )
    pure_signal = landau( energy, landau_amplitude, landau_mean, landau_width )

    detected_signal = sig.convolve(  noise,pure_signal )
    return detected_signal

def gaussian( energy, amplitude, mean, width ): 
    noise = amplitude * np.exp( -( energy - mean )**2 / ( 2 * width**2 ) )
    noise=[max(1e-7,i) for i in noise]  # set noise minimum to prevent deconvolution bug
    return noise

def landau( energy, amplitude, mean, width ):
    return [ amplitude*r.Math.landau_pdf( energy_point, width,mean ) for energy_point in energy ]


energy = np.linspace( 0, 6, resolution+1 ) # Define energy range in MIP equivalents
energy_extended = np.linspace( -3, 12, resolution*2+1 ) # the range of energies for convolved values

noise = gaussian( energy, *toy_gauss_parameters )
pure_signal = landau( energy, *toy_landau_parameters )

detected_signal = sig.convolve(  noise,pure_signal ) #real convolution



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
deconvolved_signal,_ = sig.deconvolve( detected_signal, noise)

# toy_landau_parameters = [1.1,1,0.1]
# toy_gauss_parameters = [0.2,3,0.5]


convolution_fit_parameters, _ = optimize.curve_fit(convolution_function, energy, detected_signal, p0=(*toy_landau_parameters,*toy_gauss_parameters ), maxfev=50000 )
# convolution_fit_parameters, _ = optimize.curve_fit(convolution_function, energy, sample_as_normalised_function, p0=(*toy_landau_parameters,*toy_gauss_parameters ),
# bounds = ((0,0,0,0,0,0),(1,6,1,1,6,1)), maxfev=500 )
convolution_fit_parameters, _ = optimize.curve_fit(convolution_function, energy, sample_as_normalised_function, p0=(*toy_landau_parameters,*toy_gauss_parameters ),
maxfev=500 )
# convolution_fit_parameters, _ = optimize.curve_fit(convolution_function, energy, detected_signal, maxfev=50000 )

print(convolution_fit_parameters)

convolution_fit = convolution_function( energy, *convolution_fit_parameters )
deduced_signal = landau( energy, *convolution_fit_parameters[0:3] )
deduced_noise = gaussian( energy, *convolution_fit_parameters[3:6] )
# deconvolved_data = [i for i in deconvolved_signal]




# deconvolved_data,_ = sig.deconvolve( convolution_fit, noise)
# deconvolved_data,_ = sig.deconvolve( detected_signal, noise)


# plt.ylim(0,3)
plt.ylim(0,0.3)
plt.xlim(0,6)

plt.plot( energy, pure_signal, linestyle='solid', color='black', label='initial guess signal' )
plt.plot( energy, noise, linestyle='solid', color='gray', label='initial guess noise' )
plt.plot( energy_extended, detected_signal, linestyle='solid', color='gainsboro', label='inititial guess convolution' )

plt.plot( energy_extended, sample_as_normalised_function, linestyle = 'None', marker='x', color='blue', label='Data' )

# plt.plot( energy, deconvolved_signal, color='darkgreen', linestyle='dashed', label='Deconvolved signal' )

plt.plot( energy_extended, convolution_fit, color='aqua', linestyle='dotted', label='Fit of data' )

plt.plot( energy, deduced_signal,  linestyle='dashed', color='green', label='Deduced signal' )
plt.plot( energy, deduced_noise,  linestyle='dashed', color='limegreen', label='Deduced noise' )







plt.legend()
plt.savefig('plots/Exploration.png', dpi=300)
plt.close()


