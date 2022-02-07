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


# rootColors=[1,2,4,28,7] #a presumably color-blind friendly color palette
# rootColors=[28,2,4] #a three-compare color-blind friendly color palette
# rootColors=[4,2] #a -v+ comparison
rootColors=[4,2,3,1,6,7,8,9] #Colorblind unfriendly for comparing many things
rootMarkers=[4,26,32] #this is getting out of hand


def unabbreviate(str):
    if str == "rec": return "reconstruction"
    elif str == "sim": return "simulation"
    elif str == "e-0.5": return "500 MeV electrons"
    elif str == "e+0.5": return "500 MeV positrons"
    else: return str

             



def createLegend():
    # legend = r.TLegend(0.0,0.95,0.18,1)
    legend = r.TLegend(0.0,0.9,0.18,1)

    # legend = r.TLegend(0.0,0.9,0,1)
    # legend.SetTextSize(0.025)  
    return legend    




# def createLabel(fwhm=None):
#     label = r.TLatex()
#     label.SetTextFont(42)
#     label.SetTextSize(0.03)
#     label.SetNDC()    
#     if fwhm: label.DrawLatex(0,  0.005, "FWHM:  "+str(round(fwhm,6)))
#     return label


def drawLine(plotDimension,line):
    # hist.SetOption("")
        if plotDimension == 1:
            line.Draw("HIST SAME")
            # lines[-1].Draw("SAME E")
        if plotDimension == 2:
            line.Draw("COLZ SAME")  

def drawLines(plotDimension,lines,options=''):
    # hist.SetOption("")
        if plotDimension == 1:
            lines[0].Draw(options)
            for i in range(1,len(lines)):
                lines[i].Draw(options+" SAME")
                # lines[i].Draw("SAME E")
        if plotDimension == 2:
            lines[0].Draw("COLZ") #SAME? 


  
def createHist(plotDict,plotVar,id,fileName='asd'):
    if plotDict[plotVar]['dimension'] == 1:     
        histTitle = plotVar
        histName = plotVar#barName(id)          
        binning = plotDict[plotVar]['binning']                
        if type(binning) == type({}):                     
            hist = r.TH1F(histName,histTitle, binning['nBins'],binning['min'],binning['max']) #name, title, nbins, start, finish          
        elif type(binning) == type([]):
            hist = r.TH1F(histName,histTitle, len(binning)-1, array('f',binning)) #name, title, nbins, binlayout   
        # hist.SetMinimum(0.5)      

    elif plotDict[plotVar]['dimension'] == 2:
        histTitle = plotVar
        # histName = barName(id)    
        histName = plotVar            
        binningX = plotDict[plotVar]['binningX']
        binningY = plotDict[plotVar]['binningY']                           
        if type(binningX) == type({}):
            hist = r.TH2F(histName,histTitle,binningX['nBins'],binningX['min'],binningX['max'] #name, title, nbins, start, finish
            ,binningY['nBins'],binningY['min'],binningY['max']) #nbins, start, finish
        elif type(binningX) == type([]):    
            hist = r.TH2F(histName,histTitle, len(binningX)-1, array('f',binningX) #name, title, nbins, start, finish
            , len(binningY)-1, array('f',binningY)) #nbins, start, finish                    
  
    # elif plotDict[plotVar]['dimension'] == "bar":
    #     binLabelsEvtType = ["Nothing hard","1n","2n","#geq 3n","1#pi","2#pi", "1#pi_{0}", "1#pi 1N", "1p","2N","exotics","multi-body"]
    #     hist.GetXaxis().SetBinLabel(b+1, binLabelsEvtType[b])

    hist.SetYTitle(plotDict[plotVar]['yaxis'])
    hist.SetXTitle(plotDict[plotVar]['xaxis'])
    # hist.SetLineColor(rootColors[len(lines)])
    # hist.SetFillStyle(0);
    # hist.SetMarkerStyle(rootMarkers[len(lines)]) 
    # hist.SetMarkerColor(rootColors[len(lines)])
    # hist.SetMarkerSize(3)    
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

def decoratePlot(filledHist,plotDimension,legend):
    if plotDimension == 1 or 2: legend.Draw();


def main():       
    fwhmList=[]
    for plotNumber in range(len(plotGroups)): #creates a plot
        plotDimension =  getPlotDimension(plotNumber)
        barIDs = getPlotBars(plotNumber)
        extractionName = ""
        for id in barIDs: 
            legend = createLegend()        
            lines=[]     
            c=r.TCanvas('t','Total energy with fits', 1600, 900)
            for j in plotGroups[plotNumber]: #creates a line for each variable in the plot
                plotVar = var  = j[0]
                fileName = j[1]   
                extractionName = plotVar+"___"+fileName+barName(id)
                        

                inFile = r.TFile(fileName+".root","READ")   
                allData = inFile.Get("LDMX_Events")                   
                hist = createHist(plotDict,plotVar,id)         
                if plotVar == 'Energy as a function of the incoming particle angle':
                    angles = [angle for angle in (0,2,10,20,30,40)]
                    inFiles= [r.TFile('e-1GeV'+str(angle)+"deg5k.root","READ")  for angle in angles ]
                    allDatas=[f.Get("LDMX_Events")  for f in inFiles]
                    for i in range(len(angles)): 
                        filledHist = fillHist(hist, plotVar, allDatas[i],angle=angles[i])
                        filledHist.hist.SetMinimum(0.5)                  

                else:
                    beamEnergy=getBeamEnergyFromFileName(fileName)
                    filledHist = fillHist(hist, plotVar, allData, barID=id, beamEnergy=beamEnergy)
                
                filledHist.hist.SetLineColor(rootColors[len(lines)])                                       
                lines.append(copy.deepcopy(filledHist.hist))      
                legend.AddEntry(lines[-1],fileName,"f")            
                
        
            drawLines(plotDimension,lines,options="HIST") 

            decoratePlot(filledHist,plotDimension,legend)
            # canvas.SaveAs("plots/Plot"+str(plotNumber)+"__"+barName(id)+"_linear.png")
            # canvas.SaveAs("plots/Plot"+str(plotNumber)+"__"+barName(id)+"_linear.png")

            file = r.TFile("extractions/"+extractionName+".root", "RECREATE")

            for histos in lines:
                histos.SetDirectory(file)
                histos.Write()
            # legend.SetDirectory(file) 
            legend.Write("legend")
            file.Close()
            print("finished extracting",extractionName)
            c.Close()



            
            
            try:
                del filledHist
            except:pass    






main()