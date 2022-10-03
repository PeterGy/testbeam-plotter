#processName is actually protosim on aurora


import ROOT as r
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window

import scipy.signal as sig
from numpy import *
import libDetDescr as DD
import csv
from HCal3Dmodel import *
import numpy as np
from matplotlib.pyplot import *
import scipy.optimize
import matplotlib
import scipy.interpolate
matplotlib.use('Agg')
r.gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?


period = 6
nbins=60
x = np.linspace(0.1,6, nbins)
x = np.linspace(0.1-1,6-1, nbins)



def landau_to_gauss(LA,Lσ,Lμ):
    GA= LA/60.933003910531106
    Gσ = Lσ/16.870424240685622
    Gμ =  Lμ-7.689142543201334

    return [GA,Gμ,Gσ]

def landau(x,LA,Lσ,Lμ):
    x=x*Lσ-Lμ
    p = 1/sqrt(2*pi)*np.exp(-(x+np.exp(-x)/2))*LA
    return p

def gauss(x, GA, Gμ, Gσ):
    return  GA * np.exp(-(x - Gμ) ** 2 / (2 * Gσ ** 2))

def fixed_gauss_component(x,LA,Lσ,Lμ):
    [GA,Gμ,Gσ] = landau_to_gauss(LA,Lσ,Lμ)
    return  GA * np.exp(-(x - Gμ) ** 2 / (2 * Gσ ** 2))    

def landau_gauss(x,LA,Lσ,Lμ, GA,Gμ,Gσ):
    return landau(x,LA,Lσ,Lμ)+gauss(x, GA, Gμ, Gσ)   

def landau_fixed_gauss(x,LA,Lσ,Lμ):
    [GA,Gμ,Gσ] = landau_to_gauss(LA,Lσ,Lμ)
    return landau(x,LA,Lσ,Lμ)+gauss(x, GA, Gμ, Gσ)       


def print_parameters(LA,Lσ,Lμ, GA,Gμ,Gσ):
    print ("{:<20} {:<20} {:<20} {:<20}".format('Amplitudes',LA,GA,LA/GA))
    print ("{:<20} {:<20} {:<20} {:<20}".format('Widths',Lσ,Gσ,Lσ/Gσ))
    print ("{:<20} {:<20} {:<20} {:<20}".format('Positions',Lμ,Gμ,Lμ-Gμ,))



def analyse_bar(layer,strip,end):
    name = "Layer "+str(layer)+", Strip "+str(strip)+", End "+str(end)

    figure(name)
    # nbins=300
    # ylim(-0.02,0.25)
    
    # ylim(-0.05,0.3)
    # ylim(-0.02,0.08)
    # ylim(-0.02,0.02)
    xlabel('Number of MIP equivalents')
    ylabel('Events')
    text(2.5, 0.1, name, fontsize = 15)
    grid(True)

    inFile = r.TFile("extractions/Pulse height analysis layer "+str(layer)+', strip '+str(strip)+', end '+str(end)+".root","READ")    
    c=r.TCanvas('t','The canvas of anything', 1100, 900)
    hist=inFile.Get('cuts')

    x_extended = np.linspace(0.1-3,6+3, nbins*2)
    y = []
    y_extended = []
    for i in range (0,int(nbins/2)):
        y_extended.append(0)
    for i in range (1,nbins+1):
        y.append(hist.GetBinContent(i))
        y_extended.append(hist.GetBinContent(i))
    for i in range (0,int(nbins/2)-1):
        y_extended.append(0)

    y_centered = np.zeros(len(y))
    center = y.index(max(y))
    for i in range(len(y)-20):
        y_centered[i + 19 - center] = y[ i]
    y=y_centered

    landau_min_size = 0.2
    landau_max_size = 1
    gauss_min_size = 0.001
    gauss_max_size = 0.02



    intitial_landau_params,_ = scipy.optimize.curve_fit(landau, x, y, p0=(0.1,0.1,0.1), bounds=((0.01,0,0),(1,10,10)) , maxfev=500 )
    # params2,_ = scipy.optimize.curve_fit(gauss, x, y, p0=(0.05,1,1), bounds=((0.01,0.01,0.01),(0.1,5,5)) , maxfev=500 )
    landau_gauss_params,_ = scipy.optimize.curve_fit(landau_gauss, x, y,p0=(landau_max_size,intitial_landau_params[1],intitial_landau_params[2],gauss_min_size,2,0.1), 
    bounds=((landau_min_size,0,0,gauss_min_size,1.5,0.1),(landau_max_size,10,20,gauss_max_size,2.5,4)) , maxfev=50000 )

    landau_fixed_gauss_params,_ = scipy.optimize.curve_fit(landau_fixed_gauss, x, y, p0=(landau_max_size,intitial_landau_params[1],intitial_landau_params[2]), 
    bounds=((landau_min_size,0,0),(landau_max_size,10,10)) , maxfev=50000 )




    landau_fit = landau(x,*landau_gauss_params[0:3])
    gauss_fit = gauss(x,*landau_gauss_params[3:6])
    # landau_fit = landau(x,*landau_fixed_gauss_params[0:3])
    # gauss_fit = fixed_gauss_component(x,*landau_fixed_gauss_params[0:3])
    # fixed_gauss_fit = gauss(x,*landau_gauss_params[0:3])
    # gauss_fit = gauss(x,0.04,0.94451264,0.20577948)


    landau_gauss_fit = landau_gauss(x,*landau_gauss_params)
    landau_fixed_gauss_fit = landau_fixed_gauss(x,*landau_fixed_gauss_params)
    # the_rest = y-landau_fixed_gauss_fit
    the_rest = y-landau_gauss_fit
    # the_rest = y-landau_fit
    # Δ=zeros(len(y))
    # Δ[int(len(y)/2)] = 1
    # small_gauss = gauss(x,0.1,3.5,0.1)
    # small_convolve =  sig.convolve(landau_fit,small_gauss,'same')


    def f(x):
        return x**1.4 /800
    def triangle():
        shape = [f(x) for x in range(1,20)]
        return shape
    # triangle = [1,0.75,0.5,0.25,0]
    convolve =  sig.convolve(landau_fit,triangle(),'same')

    print(len(convolve))








    # c = sig.convolve(landau_fit,gauss_fit)
    # c2 = sig.convolve(y,gauss_fit)
    # c3 = sig.convolve(y,Δ)




    plot(x,y,'k*', label='Data')
    plot(x,landau_fit,'teal', label='Landau component')
    plot(x,convolve,'red', label='convolution')
    # plot(x,gauss_fit,'green', label='Gauss component')
    # plot(x,fixed_gauss_fit,'green', label='Gauss component')
    # plot(x,landau_gauss_fit,'red', label='Mixed fit')
    # plot(x,landau_fixed_gauss_fit,'yellow', label='Mixed fit 2')
    # plot(x,the_rest,'blue', label='Fit subtracted from data')

    # print('Bar is:',layer,strip,end)
    # print_parameters(*landau_gauss_params)
    # print_parameters(*landau_fixed_gauss_params,*landau_to_gauss(*landau_fixed_gauss_params))


    # plot(x,small_convolve,'b--', label='Convolved a little')
    # plot(x,gauss_fit,'y', label='Gauss')
    # plot(x,landau_gauss_fit,'r', label='Convolved')
    # plot(x_extended[0:-1],c,'r', label='test fit')
    # plot(x_extended[0:-1],c2,'g', label='test data')
    # plot(x_extended[0:-1],c3,'g', label='test data')


    print(len(x))

    legend()
    savefig('plots/subtractive analysis '+name+'.png', dpi=300)
    close()
    return [np.array(landau_fit),np.array(gauss_fit),np.array(the_rest)]
    
landau_sum = np.zeros(nbins)
gauss_sum = np.zeros(nbins)
rest_sum = np.zeros(nbins)
single_mode=False
single_mode=True

analysis=[]

if single_mode:
    analysis.append(analyse_bar(5,5,0))

else:
    for layer in (3,5,7,9):
    # for layer in (5,):
        print(layer)
        for strip in range(0,8):
            for end in (0,1):
                analysis.append(analyse_bar(layer,strip,end))


for i in analysis:
    landau_sum+=i[0]
    gauss_sum+=i[1]
    rest_sum+=i[2]

landau_sum = landau_sum/len(analysis)
gauss_sum = gauss_sum/len(analysis)
rest_sum = rest_sum/len(analysis)
distribution_for_simulation = landau_sum + gauss_sum + rest_sum

ylim(-0.05,0.3)
grid(True)


plot(x,landau_sum,'teal', label='Landau average')
plot(x,gauss_sum,'green', label='Gauss average')
plot(x,rest_sum,'lime', label='Remaining average')
plot(x,distribution_for_simulation ,'blue', label='Proposed probability distribution')
legend()
savefig('plots/sum.png', dpi=300)


