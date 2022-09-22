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



def landau_to_gauss(a,c,d):
    A= a/60.933003910531106
    x0 =  d-8.360117191318869
    sigma = c/6.126095028799307
    return [A,x0,sigma]

def landau(x,a,c,d):
    x=x*c-d
    # p = 1/sqrt(2*pi)*np.exp(-(x+np.exp(-x)/2))*a +b
    p = 1/sqrt(2*pi)*np.exp(-(x+np.exp(-x)/2))*a
    return p

def gauss(x, A, x0, sigma):
    return  A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def fixed_gauss_component(x,a,c,d):
    [A,x0,sigma] = landau_to_gauss(a,c,d)
    return  A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))    

def landau_gauss(x,a,c,d, A, x0, sigma ):
    return landau(x,a,c,d)+gauss(x, A, x0, sigma)   

def landau_fixed_gauss(x,a,c,d):
    [A,x0,sigma] = landau_to_gauss(a,c,d)
    print('but then it turns into',[a,c,d,A, x0, sigma])
    return landau(x,a,c,d)+gauss(x, A, x0, sigma)       

def landau_gauss_convolusion(x,a,c,d, A, x0, sigma ):
    convolusion = sig.convolve(landau(x,a,c,d),gauss(x, A, x0, sigma),'same')
    return convolusion 


def cn(n,   y,x_axis):
   c = y*np.exp(-1j*2*n*np.pi*x_axis/period)
   return c.sum()/c.size

def taylor(x, Nh,   y, x_axis):
   f = np.array([2*cn(i,y,x_axis)*np.exp(1j*2*i*np.pi*x/period) for i in range(1,Nh+1)])
   return f.sum()


def analyse_bar(layer,strip,end):
    name = "Layer "+str(layer)+", Strip "+str(strip)+", End "+str(end)

    figure(name)
    # nbins=300
    # ylim(-0.02,0.25)
    
    ylim(-0.05,0.3)
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
    the_rest = y-landau_fixed_gauss_fit
    # the_rest = y-landau_gauss_fit
    # the_rest = y-landau_fit
    # Δ=zeros(len(y))
    # Δ[int(len(y)/2)] = 1
    # small_gauss = gauss(x,0.1,3.5,0.1)
    # small_convolve =  sig.convolve(landau_fit,small_gauss,'same')










    # c = sig.convolve(landau_fit,gauss_fit)
    # c2 = sig.convolve(y,gauss_fit)
    # c3 = sig.convolve(y,Δ)




    plot(x,y,'k*', label='Data')
    plot(x,landau_fit,'teal', label='Landau component')
    plot(x,gauss_fit,'green', label='Gauss component')
    # plot(x,fixed_gauss_fit,'green', label='Gauss component')
    plot(x,landau_gauss_fit,'red', label='Mixed fit')
    plot(x,landau_fixed_gauss_fit,'yellow', label='Mixed fit 2')
    plot(x,the_rest,'blue', label='Fit subtracted from data')

    print(layer,strip,end,landau_gauss_params)
    print('Landua/Gauss height ratio',landau_gauss_params[0]/landau_gauss_params[3])
    print('Landua/Gauss width ratio',landau_gauss_params[2]/landau_gauss_params[4])
    print('Landua-gauss position displacement',landau_gauss_params[1]-landau_gauss_params[5])

    # plot(x,small_convolve,'b--', label='Convolved a little')
    # plot(x,gauss_fit,'y', label='Gauss')
    # plot(x,landau_gauss_fit,'r', label='Convolved')
    # plot(x_extended[0:-1],c,'r', label='test fit')
    # plot(x_extended[0:-1],c2,'g', label='test data')
    # plot(x_extended[0:-1],c3,'g', label='test data')


    

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

ylim(-0.05,0.3)


plot(x,landau_sum,'teal', label='Landau average')
plot(x,gauss_sum,'green', label='Gauss average')
plot(x,rest_sum,'red', label='Remaining average')
savefig('plots/sum.png', dpi=300)


# x=time
# y=landau(x,1,1,4)
# yfit=np.array([taylor(t,50).real for t in x])

# # print(y)
# plot(x,y)
# plot(x,yfit)

# savefig('plots/taylor.png', dpi=300)


            
    # the_rest = y-gauss_fit


    # poly = polyfit(x,the_rest,9)
    # the_rest_fit = polyval(poly, x)
    # the_rest_fit = polyval(poly, x)
    # x_fit_range = x[0:30]
    # the_rest_fit=np.array([taylor(t,40,the_rest[0:30],x_fit_range).real for t in x_fit_range])

    # cs = scipy.interpolate.CubicSpline(x, the_rest, axis=0, bc_type='not-a-knot', extrapolate=None)
    # print(hm)

    # gauss_fit = gauss(x, 0.01,1,1)

    # the_rest = y-landau_fit
 # plot(x,y-landau_fit,'r*')
    # plot(x,y-gauss_fit,'g*')
    # plot(x_fit_range,the_rest_fit,'r')
    # plot(x,cs(x,3),'r')




    # scipy.optimize.curve_fit(landau, x, y, p0=None, sigma=None, absolute_sigma=False, check_finite=True, bounds=(- inf, inf), method=None, jac=None, *, full_output=False, **kwargs)

    # params2,_ = scipy.optimize.curve_fit(landau_gauss, x, y, p0=(intitial_landau_params[0],intitial_landau_params[1],intitial_landau_params[2],1,0,0), bounds=((0,0,0,0,0,0),(1,10,10,10,10,10)) , maxfev=5000 )
    # params2,_ = scipy.optimize.curve_fit(landau_gauss, x, y, p0=(0,0,0,1,0,0), bounds=((0,0,0,0,0,0),(1,10,10,10,10,10)) , maxfev=5000 )
    # landau_gauss_params,_ = scipy.optimize.curve_fit(landau_gauss, x, y, p0=(0.1,0,0,1,1,1), bounds=((0.1,0,0,0.01,0.01,0.01),(1,10,10,10,10,10)) , maxfev=5000 )



        # plot(x,gauss_fit,'g', label='Gauss')
    # plot(x,landau_gauss_fit,'b', label='Mixed')
    # plot(x,y-landau_gauss_fit,'b*', label='Data vs fit')

    # convolution = convolve(landau_fit,gauss_fit)

    # try:

    # c = sig.convolve(landau_fit,gauss_fit)
    # print(len(c))
    # d, reeeee = sig.deconvolve(c,gauss_fit)
    # print(len(c))
    # print(len(d))'
    # d, reeeee = sig.deconvolve(c,gauss_fit)


    # figure('wager')
    # noise, reeeee = sig.deconvolve(y_extended,landau_fit)
    # noise, reeeee = sig.deconvolve(y_extended,gauss_fit)
    # print(len(noise))
    # plot(x,y,'k*', label='Data')
    # plot(x,landau_fit,'g', label='Landau')
    # plot(x,noise,'b', label='Noise')
    # ylim(-0.04,0.2)


    # figure('taylor')
    # x_fit_range = x[0:30]
    # y_taylor = np.array([taylor(t,4,y[0:30],x_fit_range).real for t in x_fit_range])
    # # print(y_taylor)
    # # print(y_taylor)
    # y_taylor_extended = concatenate((zeros(30),y_taylor,zeros(59)))
    # plot(x,y,'k*', label='Data')
    # # plot(x,landau_fit,'g', label='Landau')
    # plot(x_fit_range,y_taylor,'k', label='taylor')
    # # plot(x_extended,y_taylor_extended,'k', label='taylor')
    # noise, reeeee = sig.deconvolve(y_taylor_extended,landau_fit)
    # plot(x,noise,'g', label='Noise')
    # ylim(-0.04,0.2)




    # plot(x,y_taylor,'b', label='Noise')


    # e, reeeee = sig.deconvolve(landau_fit,c)
    # plot(x,d,'g', label='Data')
    # figure('the deconvolution')
    # x = [i for i in range (len(c))]
    # plot(x,c)
    # plot(x,e,'b', label='Data')



        # c2 = sig.convolve(gauss_fit,landau_fit)
        # print('attempting')
    # plot(x,y,'r', label='Data')
    # plot(x,landau_fit,'g-', label='Landau')
    
    # d, reeeee = sig.deconvolve(y,landau_fit)
    # y2=[i+0.1 for i in y]
    # d, reeeee = sig.deconvolve(y,y2)
    #     # print(d)
    #     # print(len(c),len(d))
    # plot(x,c,'k', label='')

        # plot(linspace(0,6,119),c,'k', label='')
        # plot(linspace(0,6,119),c2,'y', label='')
    # except: 
    #     print ('bad attempt') 
    # d, reeeee = sig.deconvolve(y,landau_fit)

    # plot(x,d,'k', label='')       