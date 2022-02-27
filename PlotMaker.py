from numpy import *
import ROOT as r
from Histograms import *
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window
import copy
rootColors=[4,2,3,1,6,7,8,9]

colors = {
    'white': 0,
    'black': 1,
    'red': 2,
    'green': 3,
    'blue':4,
    'yellow':5,
    'magenta':6,
    'turqoise':7,
    'gray': 15,
}

def styleHistogramCommon(histogram,histogram2,legend):
    histogram.SetFillColor(colors['white'])
    histogram.SetLineColor(colors['blue'])
    histogram2.SetLineColor(colors['blue'])
    # histogram.SetMarkerColor(colors['black'])
    histogram.SetMarkerSize(0.75)
    histogram.SetMarkerSize(0.75)
    legend.SetX1(0.43)               
    legend.SetX2(0.53)  
    legend.SetY1(0.25)               
    legend.SetY2(0.60)
    legend.Draw()
    
    


def styleHistogram2D(histogram):
    # histogram.SetFillColor(colors['white'])
    # histogram.SetLineColor(colors['black'])
    # histogram.SetMarkerColor(colors['black'])
    histogram.SetMarkerSize(0.75)

def styleHistogramEnergyResponse(histogram,legend):
    # histogram.SetFillColor(colors['white'])
    # histogram.SetLineColor(colors['black'])
    # histogram.SetMarkerColor(colors['black'])
    histogram.SetMarkerSize(0.75)    
    legend.SetX1(0.7)               
    legend.SetX2(1)  
    legend.SetY1(0.6)               
    legend.SetY2(0.9)   

def createLabel(fwhm=None,xpos=0.65):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.05)
    label.SetNDC()    
    if fwhm: label.DrawLatex(xpos,  0.005, "FWHM:  "+str(round(fwhm,6)))
    # if fwhm: label.DrawLatex(xpos,  0.006, "Particle: hepions, Eneregy 11 GeV, Angle: 0 rad, Sample: 12M")
    return label

def label2D():
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.025)
    label.SetNDC()    
    label.DrawLatex(0,  0.95, "Horizontal bars: even; Vertical bars: odd")
    # if fwhm: label.DrawLatex(xpos,  0.006, "Particle: hepions, Eneregy 11 GeV, Angle: 0 rad, Sample: 12M")
    return label

def createContext(fileName,plotName,fwhm=None,μ=None):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.05)
    label.SetNDC()    
    # if fwhm: label.DrawLatex(xpos,  0.005, "FWHM:  "+str(round(fwhm,6)))
    if 'e-' in fileName:    particle="e-"
    elif 'mu-' in fileName: particle="#mu-"
    elif 'pi-' in fileName: particle="#pi-"
    else:                   particle="???"
    energy = fileName[fileName.find('-')+1:fileName.find('GeV')]
    sample = fileName[fileName.find('GeV')+3:fileName.find('k')]
    angle = '0'

    if plotName == 'energy response vs. energy' and "0.5GeV" in fileName :  energy = '0.5 - 8'
    if plotName == 'energy response vs. energy' and "0.1GeV" in fileName:  energy = '0.1 - 0.5'
    if plotName == 'energy response vs. angle':  angle = '0 - 40'

    contextString = "Particle: "+particle+", Energy: "+energy+" GeV, Sample: "+sample+"k, Angle: "+angle+" deg"
    if fwhm != None: contextString += ", Fit fwhm: "+str(round(fwhm,6))
    if μ != None: contextString += ", Fit #mu: "+str(round(μ,6))

    label.DrawLatex(0,0.008, contextString)
    return label


def prepareDualPlots(dualPlotMode,c):
    if dualPlotMode:
        c.SetCanvasSize(1800, 800)
        c.Divide(2,1)
        c.cd(1) 
        c.GetPad(1).SetLeftMargin(0.12)
        c.GetPad(1).SetRightMargin(0.05)
        c.GetPad(2).SetLeftMargin(0.12)
        c.GetPad(2).SetRightMargin(0.05)
        c.GetPad(1).SetBottomMargin(0.14)
        c.GetPad(2).SetBottomMargin(0.14)

def finishDualPlots(dualPlotMode,c,hist):
    if dualPlotMode:
        hist2=copy.deepcopy(hist)
        c.cd(2) 
        c.GetPad(2).SetLogy()
        c.GetPad(2).SetGrid()
        c.GetPad(1).SetGrid()
        hist2.Draw("E")
        c.cd(0)
        # styleHistogramCommon(hist,hist2,legend)

def prettyLegendName(str):
    # if str.find('k') == 0: name='0'
    # else: name = str[str.find('k')+1:]
    name = str[str.find('k')+1:]
    if name.find("deg")>-1: name = name[0:2]+" degrees"
    elif name.find("xpos")>-1: name = name[0:3]+" mm displacement"
    # else: name = name[name.find('-')+1:name.find('GeV')]+" GeV"
    else: 
        name = str[str.find('-')+1:str.find('GeV')]+' GeV'
    # print(name)
    return name

def secondPlotZoom(hist):
    if plotName == 'Distribution of PEs per HCal bar': 
        hist.GetXaxis().SetRangeUser(50,150) 
        hist.SetTitle('Distribution of PEs per HCal bar (MIP range only)')  
    return hist


def main():   
    fwhmList=[]
    fwhmListErrorsBars=[]

    for plot in plotGroups:
        plotName = plot[-1][0]
        fileName = plot[-1][1] 
        
        try: bars = plotDict[plotName]['bars']
        except: bars = [False] 
        for id in bars: 
            extractionName = plotName+"___"+fileName+barName(id)
            dimension = plotDict[plotName]['dimension']
            inFile = r.TFile("extractions/"+extractionName+".root","READ")    
            hist=inFile.Get(plotName+barName(id))
            c=r.TCanvas('t','The canvas of anything', 1100, 900)
            c.cd()
            if dimension == 2:
                # print(c.GetPad(0).GetRightMargin())
                c.SetCanvasSize(1800, 800)
                c.GetPad(0).SetRightMargin(0.121)
                styleHistogram2D(hist)
                hist.Draw("COLZ")
                r.gStyle.SetOptStat("")
                label2D()            
            elif plotName == 'energy response vs. energy' or plotName == 'energy response vs. angle' or plotName == 'energy response vs. position':
                c.SetBottomMargin(0.14)
                lines=[]
                legend = r.TLegend(0.0,0.9,0.18,1)
                for i in range(len(plot)):
                    hist=inFile.Get(plotName+";"+str(i+1))
                    hist.SetLineColor(rootColors[i])  
                    lines.append(copy.deepcopy(hist))
                    legend.AddEntry(lines[-1],prettyLegendName(plot[i][1]),"f")
                for line in lines:
                    line.Draw("same e")    
                    fit = line.Fit('gaus','Sq')
                    fwhm = 2.355*fit.Parameter(2)
                    fwhmError = 2.355*fit.ParError(2)
                    line.GetFunction("gaus").SetLineColor(rootColors[lines.index(line)])
                    label = r.TLatex()
                    label.SetTextFont(42)
                    label.SetTextSize(0.05)
                    label.SetTextColor(rootColors[lines.index(line)])
                    label.SetNDC()    
                    label.DrawLatex(0.6,  0.5 - 0.05*lines.index(line), "#mu = "+str(round(fit.Parameter(1),6)))
                    # label.DrawLatex(0.2,  0.3, "asd")
                    fwhmList.append(fwhm)     
                    fwhmListErrorsBars.append(fwhmError)     
                    r.gStyle.SetOptStat("")
                    print("Average is ",fit.Parameter(1))
                c.SetLogy()   
                c.GetPad(0).SetGrid()                
                styleHistogramEnergyResponse(lines[-1],legend)
                legend.Draw()

            elif dimension == 1:
                c.SetLeftMargin(0.12)   
                dualPlotMode=True
                prepareDualPlots(dualPlotMode,c)   
                r.gStyle.SetOptStat("nerm")                       
                if id != False: hist.SetName(barName(id)) 
                hist.GetRMS()     #this ONE CURSED LINE is somehow the key that makes hist2.GetXaxis().SetRangeUser(50,150) work. Wtf?!?!?!?!             
                if plotName == 'Reconstructed energy for tags': 
                    fit = hist.Fit('gaus','Sq')
                    fwhm = 2.355*fit.Parameter(2)
                    μ = fit.Parameter(1)
                hist.Draw("")                      
                if dualPlotMode:
                    hist2=copy.deepcopy(hist)
                    if plotName == 'Distribution of PEs per HCal bar':                       
                        hist2.GetXaxis().SetRangeUser(50,150) 
                        hist2.SetTitle('Distribution of PEs per HCal bar (MIP range only)') 
                    if plotName == 'TS plots with muons (light yield)':                     
                        hist2.GetXaxis().SetRangeUser(50,100) 
                        hist2.SetTitle('TS plots with muons (light yield) (zoomed in)') 
                        
                        

                    r.gStyle.SetOptStat("nerm")
                    c.cd(2) 
                    
                    c.GetPad(2).SetGrid()
                    c.GetPad(1).SetGrid()
                    hist2.Draw("e")
                    c.GetPad(2).SetLogy()
                    if plotName == 'Distribution of PEs per HCal bar': 
                        
                        fit = hist2.Fit('gaus','Sq')
                        try:
                            fwhm = 2.355*fit.Parameter(2)
                            μ = fit.Parameter(1)    
                        except: pass #sometimes, nothing hits the bar    
                    c.cd(0)
                    # createLabel(fwhm)  

            c.cd()
            if 'fwhm' not in locals(): fwhm = None
            if 'μ' not in locals(): μ = None
            createContext(fileName,plotName,fwhm,μ)
            c.SaveAs("plots/"+extractionName+".png")
            c.Close()
            

        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        if len(fwhmList)==5 and (plotName == 'energy response vs. angle' or plotName == 'energy response vs. position'):
            if plotName == 'energy response vs. angle':
                name="Angles"                
                x=(0,10,20,30,40)
                plt.xlabel("Angle [deg]")
            elif plotName == 'energy response vs. position':
                name="Positions"
                x=(0,100,200,300,400)
                plt.xlabel("Position [mm]")

            plt.figure(name)
            plt.errorbar(x,fwhmList[0:5],xerr=0,yerr=fwhmListErrorsBars,label=name,color='r',marker=",",linestyle='')
            plt.ylabel("Resultion []")            
            plt.title('FWHMs')
            plt.legend()
            plt.grid(visible=True)
            plt.savefig('plots/fwhms'+name+'.png')
            fwhmList=[]   
            fwhmListErrorsBars=[] 

        
        elif len(fwhmList)==10:
            def expected(E,s=1): return s*1/sqrt(E)
            plt.figure("Energies")
            energies = (8,4,2,1,0.5)
            # energies = (0.5,0.4,0.3,0.2,0.1)
            xfit=linspace(min(energies),max(energies),50)
            # plt.plot(energies,fwhmList[0:5],"r*",label='Pions')
            plt.errorbar(energies,fwhmList[0:5],xerr=0,yerr=fwhmListErrorsBars[0:5],label='Pions',color='r',marker=",",linestyle='')
            # plt.plot(energies,fwhmList[5:10],"b*",label='Electrons')
            plt.errorbar(energies,fwhmList[5:10],xerr=0,yerr=fwhmListErrorsBars[5:10],label='Electrons',color='b',marker=",",linestyle='')
            from scipy import optimize
            paramsPion,e_ = optimize.curve_fit(expected,energies,fwhmList[0:5])
            paramsElec,e_ = optimize.curve_fit(expected,energies,fwhmList[5:10])
            yfitPion=[expected(E,s=paramsPion[0]) for E in xfit]
            yfitElec=[expected(E,s=paramsElec[0]) for E in xfit]

            
            plt.plot(xfit,yfitPion,"r-",label='Pion 1/√E fit')
            plt.plot(xfit,yfitElec,"b-",label='Electron 1/√E fit')    

            plt.ylabel("Resultion []")
            plt.xlabel("Energy [GeV]")
            plt.title('FWHMs')
            plt.legend()
            # plt.xscale('log')
            plt.grid(visible=True)
            plt.savefig('plots/fwhmsEnergies.png')
            fwhmList=[]
            fwhmListErrorsBars=[]


main()