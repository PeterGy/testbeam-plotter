#processName is actually protosim on aurora
import ROOT as r
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window

from numpy import *
import libDetDescr as DD
import csv
from HCal3Dmodel import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import scipy.optimize
import matplotlib
matplotlib.use('Agg')
r.gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?

def labelLayer(text):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.SetTextColor(1)
    label.SetNDC()    
    # r.gStyle.SetOptStat("")
    # label.DrawLatex(0.5,  0.85,  'Just raw ADC sums')
    label.DrawLatex(0.3,  0.85,  'After track-like cut on layers 1 & 15')
    label.DrawLatex(0.4,  0.8,  'MIPeq >= 0.9')
    label.DrawLatex(0.4,  0.75,  text)
    return label     

def label_fit(μ,σ):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.SetTextColor(1)
    label.SetNDC()    
    # r.gStyle.SetOptStat("")
    # label.DrawLatex(0.5,  0.85,  'Just raw ADC sums')
    # label.DrawLatex(0.3,  0.85,  'After track-like cut on layers 1 & 11')
    label.DrawLatex(0.5,  0.5,  '#mu: '+str(round(μ,4)))
    label.DrawLatex(0.5,  0.45, '#sigma: '+str(round(σ,4)))
    return label  

class BarData:
    pass

def analyse_bar(layer,strip,end):
            x = BarData()
            x.location = (layer,strip,end)
            inFile = r.TFile("extractions/Strict Pulse height analysis layer "+str(layer)+', strip '+str(strip)+', end '+str(end)+".root","READ")    
            c=r.TCanvas('t','The canvas of anything', 1100, 900)
            hist=inFile.Get('cuts')
            hist.GetYaxis().SetRangeUser(0, 0.27)

            fit = hist.Fit('landau','Sq')
            # fit = hist.Fit('landau','S')
            # fit = hist.Fit('pol6','Sq')
            # fit = hist.Fit('gaus','Sq')
            # print(fit.GetMaximum())

            try:
                x.σ = fit.Parameter(2)
                x.μ = fit.Parameter(1) 
            except: pass 
            # averages.append(μ)



            hist.Draw('e')
            label_fit(x.μ,x.σ)   
            label = "Layer: "+str(layer)+", Strip: "+str(strip)+", End: "+str(end)
            labelLayer(label)
            c.SaveAs("plots/Strict Pulse Height Fit layer "+str(layer)+', strip '+str(strip)+', end '+str(end)+".png")
            c.Close()
            return x

# averages = []
# c=r.TCanvas('t','The canvas of anything', 1100, 900)
analysis=[]
for layer in (3,5,7,9):
    for strip in range(0,8):
        for end in (0,1):
            analysis.append(analyse_bar(layer,strip,end))
            # analysis.append(data)
            
def μmap(end):            
    c=r.TCanvas('t','The canvas of anything', 1100, 900)
    hist = r.TH2F('Average SiPM response end '+str(end),'Average SiPM response end '+str(end),11,0.5,11.5,8,-0.5,7.5)


    for SiPM in analysis:
        if SiPM.location[2] == end:
            hist.Fill(SiPM.location[0],SiPM.location[1],SiPM.μ)

    r.gStyle.SetOptStat("")
    hist.GetZaxis().SetRangeUser(0.9, 1.1)
    hist.SetYTitle('Strip')
    hist.SetXTitle('Layer')

    hist.Draw('COLZ')
    c.SaveAs("plots/averages"+str(end)+".png")
    c.Close()

μmap(0)  
μmap(1)  

# print(max(averages))
# print(min(averages))
# print(min(μ))
