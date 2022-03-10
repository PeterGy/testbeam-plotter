from numpy import *
import ROOT as r
from Histograms import *
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window
import copy
rootColors=[4,2,3,1,6,7,8,9]

# colors = {
#     'white': 0,
#     'black': 1,
#     'red': 2,
#     'green': 3,
#     'blue':4,
#     'yellow':5,
#     'magenta':6,
#     'turqoise':7,
#     'gray': 15,
# }

# def styleHistogramCommon(histogram,histogram2,legend):
#     histogram.SetFillColor(colors['white'])
#     histogram.SetLineColor(colors['blue'])
#     histogram2.SetLineColor(colors['blue'])
#     # histogram.SetMarkerColor(colors['black'])
#     histogram.SetMarkerSize(0.75)
#     histogram.SetMarkerSize(0.75)
#     legend.SetX1(0.43)               
#     legend.SetX2(0.53)  
#     legend.SetY1(0.25)               
#     legend.SetY2(0.60)
#     legend.Draw()
    
    


# def styleHistogram2D(histogram):
#     # histogram.SetFillColor(colors['white'])
#     # histogram.SetLineColor(colors['black'])
#     # histogram.SetMarkerColor(colors['black'])
#     histogram.SetMarkerSize(0.75)

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
    label.DrawLatex(0,  0.92, "Odd layers: horizontal bars; Even layers: vertical bars")
    # if fwhm: label.DrawLatex(xpos,  0.006, "Particle: hepions, Eneregy 11 GeV, Angle: 0 rad, Sample: 12M")
    return label

def createContext(fileName,plotName,fwhm=None,μ=None,σ=None,stacked=False):
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
    if 'deg' in fileName: angle = fileName[fileName.find('k')+1:fileName.find('deg')]
    else: angle = '0'

    if plotName == 'energy response vs. energy' and "0.5GeV" in fileName :  energy = '0.5 - 8'
    if plotName == 'energy response vs. energy' and "0.1GeV" in fileName:  energy = '0.1 - 0.5'
    if plotName == 'energy response vs. angle':  angle = '0 - 40'

    if stacked:
        label2 = r.TLatex()
        label2.SetTextFont(42)
        label2.SetTextSize(0.05)
        label2.SetNDC()  
        contextString = "Particle: "+particle+", Energy: "+energy+" GeV, Sample: "+sample+"k, Angle: "+angle+" deg"
        contextString2 = "Fit fwhm: "+str(round(fwhm,6))+", Fit #mu: "+str(round(μ,6))
        label.DrawLatex(0,0.008, contextString)
        label.DrawLatex(0,0.068, contextString2)
    elif not stacked:
        contextString = "Particle: "+particle+", Energy: "+energy+" GeV, Sample: "+sample+"k, Angle: "+angle+" deg"
        ##if fwhm != None: contextString += "; Fit fwhm: "+str(round(fwhm,6))
        if σ != None: contextString += "; Fit #sigma: "+str(round(σ,4))
        if μ != None: contextString += ", Fit #mu: "+str(round(μ,4))
        if μ != None and σ != None: contextString += ", Resolution: "+str(round(σ/μ,4))
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
    if str.find("100k")>-1:  
        name = str[str.find('-')+1:str.find('GeV')]+' GeV'
    else:
        name = str[str.find('k')+1:]
        if name.find("deg")>-1: name = name[0:2]+" degrees"
        elif name.find("xpos")>-1: name = str[0:3]+" particle"
        # elif name.find("xpos")>-1: name = name[0:3]+" mm displacement"
        # else: name = name[name.find('-')+1:name.find('GeV')]+" GeV"
        else: name = str[str.find('-')+1:str.find('GeV')]+' GeV'
    return name


def main():   
    fwhmList=[]
    fwhmListErrorsBars=[]
    resolutionList=[]
    ΔresolutionList=[]

    for plot in plotGroups:
        plotName = plot[-1][0]
        fileName = plot[-1][1] 
        
        try: bars = plotDict[plotName]['bars']
        except: bars = [False] 
        for id in bars: 
            fwhm = None
            μ = None
            extractionName = plotName+"___"+fileName+barName(id)
            dimension = plotDict[plotName]['dimension']
            inFile = r.TFile("extractions/"+extractionName+".root","READ")    
            hist=inFile.Get(plotName+barName(id))
            c=r.TCanvas('t','The canvas of anything', 1100, 900)
            c.cd()
            if dimension == 2:
                # print(c.GetPad(0).GetRightMargin())
                # hist.SetTitle('Simulated deposits') 
                c.SetCanvasSize(1800, 800)
                c.GetPad(0).SetRightMargin(0.121)
                # styleHistogram2D(hist)
                hist.Draw("COLZ")
                r.gStyle.SetOptStat("")
                label2D()            
            elif plotName == 'energy response vs. energy' or plotName == 'energy response vs. angle' or plotName == 'energy response vs. position':
                dualPlotMode=False
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
                    fwhmList.append(fwhm)     
                    fwhmListErrorsBars.append(fwhmError) 


                    μ = fit.Parameter(1)
                    Δμ = fit.ParError(1)
                    σ = fit.Parameter(2)
                    Δσ = fit.ParError(2)
                    resolution=σ/μ
                    Δresolution=resolution*(Δμ/μ+Δσ/σ)
                    resolutionList.append(resolution)     
                    ΔresolutionList.append(Δresolution)     



                    line.GetFunction("gaus").SetLineColor(rootColors[lines.index(line)])
                    label = r.TLatex()
                    label.SetTextFont(42)
                    label.SetTextSize(0.05)
                    label.SetTextColor(rootColors[lines.index(line)])
                    label.SetNDC()    
                    label.DrawLatex(0.6,  0.5 - 0.05*lines.index(line), "#mu = "+str(round(fit.Parameter(1),6)))
                    # label.DrawLatex(0.2,  0.3, "asd")

                    r.gStyle.SetOptStat("")
                c.SetLogy()   
                c.GetPad(0).SetGrid()                
                styleHistogramEnergyResponse(lines[-1],legend)
                legend.Draw()

            # elif plotName == 'Reconstructed energy for tags (absolute energy)'  or plotName == 'Total number of hits per event':
            elif plotName == 'Reconstructed energy for tags (absolute energy)':
                c.SetBottomMargin(0.14)
                lines=[]
                legend = r.TLegend(0.0,0.9,0.18,1)
                for i in range(len(plot)):
                    hist=inFile.Get(plotName+";"+str(i+1))
                    hist.SetLineColor(rootColors[i])  
                    lines.append(copy.deepcopy(hist))
                    legend.AddEntry(lines[-1],prettyLegendName(plot[i][1]),"f")
                for line in lines:
                    line.Draw("same")    
                    label = r.TLatex()
                    label.SetTextFont(42)
                    label.SetTextSize(0.05)
                    label.SetTextColor(rootColors[lines.index(line)])
                    label.SetNDC()     
                    r.gStyle.SetOptStat("")           
                styleHistogramEnergyResponse(lines[-1],legend)
                legend.Draw()

            elif dimension == 1:
                c.SetLeftMargin(0.12)   
                c.SetBottomMargin(0.14)
                r.gStyle.SetOptStat("ne")
                dualPlotMode=True
                # r.gStyle.SetOptStat("nerm") 
                # if not dualPlotMode: 
                    
                prepareDualPlots(dualPlotMode,c)   
                                      
                if id != False: hist.SetName(barName(id)) 
                hist.GetRMS()     #this ONE CURSED LINE is somehow the key that makes hist2.GetXaxis().SetRangeUser(50,150) work. Wtf?!?!?!?!             
                if plotName == 'Reconstructed energy for tags': 
                    fit = hist.Fit('gaus','Sq')
                    fwhm = 2.355*fit.Parameter(2)
                    fwhmError = 2.355*fit.ParError(2)
                    fwhmList.append(fwhm)     
                    fwhmListErrorsBars.append(fwhmError)   
                    μ = fit.Parameter(1)
                    σ = fit.Parameter(2)
                hist.Draw("")                      
                if dualPlotMode:
                    hist2=copy.deepcopy(hist)
                    if plotName == 'Distribution of PEs per HCal bar':                       
                        hist2.GetXaxis().SetRangeUser(50,150) 
                        hist2.SetTitle('Distribution of PEs per HCal bar (MIP range only)') 
                    elif plotName == 'TS plots with muons (light yield)':                     
                        hist2.GetXaxis().SetRangeUser(50,100) 
                        hist2.SetTitle('TS plots with muons (light yield) (zoomed in)') 
                    else:
                        hist2.SetTitle(hist2.GetTitle()+' (log plot)')     
                        
                        

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
                            σ = fit.Parameter(2)
                            μ = fit.Parameter(1)    
                        except: pass #sometimes, nothing hits the bar    
                    c.cd(0)
                    # createLabel(fwhm)  

            c.cd()
            # if 'fwhm' not in locals(): fwhm = None
            # if 'μ' not in locals(): μ = None
            
            
            if μ and not dualPlotMode: 
                c.SetBottomMargin(0.15)
                createContext(fileName,plotName,fwhm,μ,stacked=True)
            elif μ: createContext(fileName,plotName,fwhm,μ,σ)
            else: createContext(fileName,plotName)

            skipUninterestingPlots=False
            # skipUninterestingPlots=True
            if skipUninterestingPlots:
                if id in [False,5,402654208+4]:
                    c.SaveAs("plots/"+extractionName+".png")                
            else: c.SaveAs("plots/"+extractionName+".png")
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
            plt.errorbar(x,resolutionList,xerr=0,yerr=ΔresolutionList,label=name,color='r',marker=",",linestyle='')
            plt.ylabel("Resolution")            
            plt.title('Fit quality')
            plt.legend()
            plt.grid(visible=True)
            plt.savefig('plots/resolutions '+name+'.png')
            resolutionList=[]   
            ΔresolutionList=[] 

    
        elif len(resolutionList)==10:
            def expected(E,s=1): return s*1/sqrt(E)
            plt.figure("Energies")
            # energies = (8,4,2,1,0.5)
            energies = (0.5,0.4,0.3,0.2,0.1)
            xfit=linspace(min(energies),max(energies),50)
            
            plt.errorbar(energies,resolutionList[0:5],xerr=0,yerr=ΔresolutionList[0:5],label='Pions',color='r',marker="_",linestyle='')
            # plt.plot(energies,fwhmList[5:10],"b*",label='Electrons')
            plt.errorbar(energies,resolutionList[5:10],xerr=0,yerr=ΔresolutionList[5:10],label='Electrons',color='b',marker="_",linestyle='')
            from scipy import optimize
            paramsPion,e_ = optimize.curve_fit(expected,energies,resolutionList[0:5])
            paramsElec,e_ = optimize.curve_fit(expected,energies,resolutionList[5:10])
            yfitPion=[expected(E,s=paramsPion[0]) for E in xfit]
            yfitElec=[expected(E,s=paramsElec[0]) for E in xfit]

            
            plt.plot(xfit,yfitPion,"r--",label='Pion 1/√E fit')
            plt.plot(xfit,yfitElec,"b--",label='Electron 1/√E fit')    

            plt.ylabel("Resolution")
            plt.xlabel("Energy [GeV]")
            plt.title('Fit quality')
            plt.legend()
            # plt.xscale('log')
            plt.grid(visible=True)
            plt.savefig('plots/resolutionEnergies.png')
            resolutionList=[]
            resolutionListErrorsBars=[]

        elif len(fwhmList)==4 and (plotName == 'Reconstructed energy for tags'):
            plt.figure("Energies")
            energies = (1,2)
            plt.errorbar(energies,fwhmList[0:2],xerr=0,yerr=fwhmListErrorsBars[0:2],label='Electrons',color='b',marker="_",linestyle='')
            # plt.plot(energies,fwhmList[5:10],"b*",label='Electrons')
            plt.errorbar(energies,fwhmList[2:4],xerr=0,yerr=fwhmListErrorsBars[2:4],label='Pions',color='r',marker="_",linestyle='') 

            plt.ylabel("FWHM")
            plt.xlabel("Energy [GeV]")
            plt.title('Fit quality')
            plt.legend()
            # plt.xscale('log')
            plt.grid(visible=True)
            plt.savefig('plots/fwhmsEnergies.png')
            fwhmList=[]
            fwhmListErrorsBars=[]


main()