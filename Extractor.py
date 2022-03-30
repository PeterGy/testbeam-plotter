#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is Peter's from-scratch frankenpaste prototype plotter
#naming standard: thisThing

#this program takes many things that end with ".root" and outputs simulation and reconstruction plots into the folder "plots"
#the process name in the config file must be the file's name 
#now available on github


from Histograms import *
from HistogramFiller import *
from numpy import *
import ROOT as r
import pdb
import copy
from array import array
from ROOT import gSystem
from optparse import OptionParser
gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window

parser = OptionParser()
parser.add_option("-e", "--event", default=1, help="For the single event plot, which event you want",)
(options, args) = parser.parse_args()
eventOfInterest=options.event
# print(eventOfInterest)

# rootColors=[1,2,4,28,7] #a presumably color-blind friendly color palette
# rootColors=[28,2,4] #a three-compare color-blind friendly color palette
# rootColors=[4,2] #a -v+ comparison
rootColors=[4,2,3,1,6,7,8,9] #Colorblind unfriendly for comparing many things
rootMarkers=[4,26,32] #this is getting out of hand
  
def createHist(plotDict,plotVar,barIDs,fileName=''):

    if plotDict[plotVar]['dimension'] == 1:     
        hist={}
        for id in barIDs:                                       
            histTitle = plotVar
            histName = plotVar+barName(id)          
            binning = plotDict[plotVar]['binning']                
            if type(binning) == type({}):                     
                hist[id] = r.TH1F(histName,histTitle, binning['nBins'],binning['min'],binning['max']) #name, title, nbins, start, finish          
            elif type(binning) == type([]):
                hist[id] = r.TH1F(histName,histTitle, len(binning)-1, array('f',binning)) #name, title, nbins, binlayout   
            # hist.SetMinimum(0.5)      
            hist[id].SetYTitle(plotDict[plotVar]['yaxis'])
            hist[id].SetXTitle(plotDict[plotVar]['xaxis'])

    elif plotDict[plotVar]['dimension'] == 2:
        hist={}
        for id in barIDs:   
            histTitle = plotVar 
            histName = plotVar            
            binningX = plotDict[plotVar]['binningX']
            binningY = plotDict[plotVar]['binningY']                           
            if type(binningX) == type({}):
                hist[id] = r.TH2F(histName,histTitle,binningX['nBins'],binningX['min'],binningX['max'] #name, title, nbins, start, finish
                ,binningY['nBins'],binningY['min'],binningY['max']) #nbins, start, finish
            elif type(binningX) == type([]):    
                hist[id] = r.TH2F(histName,histTitle, len(binningX)-1, array('f',binningX) #name, title, nbins, start, finish
                , len(binningY)-1, array('f',binningY)) #nbins, start, finish                    
    
            hist[id].SetYTitle(plotDict[plotVar]['yaxis'])
            hist[id].SetXTitle(plotDict[plotVar]['xaxis'])
    return hist

def loadData(fileName): #can't even make it into a function why is ROOT so awful?
    #tried to make this more efficient by only running it once, but such methods are doomed to fail            
    inFile = r.TFile(fileName+".root","READ")  
    allData = inFile.Get("LDMX_Events")
    # allData.Print("toponly")
    return allData

def getPlotDimension(plotNumber):
    plot = plotGroups[plotNumber]
    line = plot[0]
    plotType = line[0]    
    dimension = plotDict[plotType]['dimension']
    return dimension

def getPlotBars(plotNumber):
    plot = plotGroups[plotNumber]
    line = plot[0]
    plotType = line[0]    
    try: bars = plotDict[plotType]['bars']
    except: bars = [False]
    return bars   

def getBeamEnergyFromFileName(fileName):
    try:
        energy=fileName[fileName.find('-')+1:fileName.find('GeV')]
        return (float(energy)*1e3)
    except:
        print('Note: beam energy could not be determined from file name')
        return None    


def main():       
    for plotNumber in range(len(plotGroups)): #creates a plot
        plotDimension =  getPlotDimension(plotNumber)
        barIDs = getPlotBars(plotNumber)
        # barIDs = [2]
        extractionName = ""     
        lines=[]     
        c=r.TCanvas('t','Total energy with fits', 1600, 900)
        for j in plotGroups[plotNumber]: #creates a line for each variable in the plot
            plotVar = var  = j[0]
            fileName = j[1]   
            extractionName = plotVar+"___"+fileName#+barName(id)
            inFile = r.TFile(fileName+".root","READ")   
            allData = inFile.Get("LDMX_Events")                   
            beamEnergy=getBeamEnergyFromFileName(fileName)    
            
            # if barIDs == [False]:
            hist = createHist(plotDict,plotVar,barIDs)  
            hist = fillHist(hist, plotVar, allData, beamEnergy=beamEnergy,eventOfInterest=eventOfInterest)     
            lines.append(copy.deepcopy(hist))          
            #add a line        
            # else:
            #     hists={}
            #     for id in barIDs:                                       
            #         hists[id]=createHist(plotDict,plotVar,id)  
            #     hists = fillHist(hists, plotVar, allData)    
            #     lines.append(copy.deepcopy(hists))t
   
            
        # if barIDs == [False]:
        #     file = r.TFile("extractions/"+extractionName+".root", "RECREATE")
        #     for histos in lines:
        #         histos.SetDirectory(file)
        #         histos.Write()
        #     file.Close()
        #     c.Close()
        #     print("finished extracting",extractionName)
            
        # else:
        for id in barIDs:     
            file = r.TFile("extractions/"+extractionName+barName(id)+".root", "RECREATE")
            for histos in lines:
                histos[id].SetDirectory(file)
                histos[id].Write()
            file.Close()
            c.Close()
        print("finished extracting the plot types ",extractionName)
                

main()