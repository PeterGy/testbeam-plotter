import ROOT as r
from numpy import *
rootColors=[4,2,3,1,6,7,8,9]

def styleHistogramEnergyResponse(histogram,legend):
    histogram.SetMarkerSize(0.75)    
    legend.SetX1(0.7)               
    legend.SetX2(1)  
    legend.SetY1(0.6)               
    legend.SetY2(0.9)   

def label2D():
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.025)
    label.SetNDC()    
    label.DrawLatex(0,  0.92, "Odd layers: horizontal bars; Even layers: vertical bars")
    return label

def labelμ(lines,line,fit):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.05)
    label.SetTextColor(rootColors[lines.index(line)])
    label.SetNDC()    
    r.gStyle.SetOptStat("")
    label.DrawLatex(0.6,  0.5 - 0.05*lines.index(line), "#mu = "+str(round(fit.Parameter(1),6)))
    return label    

def createContext(fileName,plotName,μ=None,σ=None,stacked=False):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.05)
    label.SetNDC()      
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

    
    top = ''
    if σ != None: top += "#sigma: "+str(round(σ,4))
    if μ != None: top += ", #mu: "+str(round(μ,4))
    if μ != None and σ != None: top += ", res: "+str(round(σ/μ,4))

    bottom = "Particle: "+particle+", Energy: "+energy+" GeV, Sample: "+sample+"k, Angle: "+angle+" deg"
    contextString='#splitline{'+top+'}{'+bottom+'}'

    label.DrawLatex(0,0.038, contextString)

    # if stacked:
    #     label2 = r.TLatex()
    #     label2.SetTextFont(42)
    #     label2.SetTextSize(0.05)
    #     label2.SetNDC()  
    #     contextString = "Particle: "+particle+", E nergy: "+energy+" GeV, Sample: "+sample+"k, Angle: "+angle+" deg"
    #     contextString2 = "Fit #splitline{#sigma: "+str(round(σ,6))+", }{Fit} #mu: "+str(round(μ,6))
    #     label.DrawLatex(0,0.008, contextString)
    #     label.DrawLatex(0,0.068, contextString2)
    # elif not stacked:
    #     contextString = "Particle: "+particle+", Ene \\ rgy: "+energy+" GeV, Sample: "+sample+"k, Angle: "+angle+" deg"
    #     if σ != None: contextString += "; Fit #sigma: "+str(round(σ,4))
    #     if μ != None: contextString += ", Fit #mu: "+str(round(μ,4))
    #     if μ != None and σ != None: contextString += ", Resolution: "+str(round(σ/μ,4))
    #     label.DrawLatex(0,0.008, contextString)
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

def plotResolution(resolutionList,ΔresolutionList,plotName):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from scipy import optimize


    if len(resolutionList)==5 and (plotName == 'energy response vs. angle' or plotName == 'energy response vs. position'):
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
        plt.savefig('plots/resolutions '+name+'.png')
        plt.ylabel("Resolution")            
        plt.title('Fit quality')
        plt.legend()
        plt.grid(visible=True)
        plt.savefig('plots/resolutions '+name+'.png')
        return [[],[]]

    elif len(resolutionList)==10:
        def expected(E,s=1): return s*1/sqrt(E)
        plt.figure("Energies")
        # energies = (8,4,2,1,0.5)
        energies = (0.5,0.4,0.3,0.2,0.1)
        xfit=linspace(min(energies),max(energies),50)
        
        plt.errorbar(energies,resolutionList[0:5],xerr=0,yerr=ΔresolutionList[0:5],label='Pions',color='r',marker="_",linestyle='')
        plt.errorbar(energies,resolutionList[5:10],xerr=0,yerr=ΔresolutionList[5:10],label='Electrons',color='b',marker="_",linestyle='')
        
        paramsPion,e_ = optimize.curve_fit(expected,energies,resolutionList[0:5])
        paramsElec,e_ = optimize.curve_fit(expected,energies,resolutionList[5:10])
        yfitPion=[expected(E,s=paramsPion[0]) for E in xfit]
        yfitElec=[expected(E,s=paramsElec[0]) for E in xfit]    
        plt.plot(xfit,yfitPion,"r--",label='Pion 1/√E fit')
        plt.plot(xfit,yfitElec,"b--",label='Electron 1/√E fit')    
        plt.ylabel("Resolution")            
        plt.title('Fit quality')
        plt.legend()
        plt.grid(visible=True)
        plt.savefig('plots/resolutionEnergies.png')

        return [[],[]]

    elif len(resolutionList)==4 and (plotName == 'Reconstructed energy for tags'):
        plt.figure("Energies")
        energies = (1,2)
        plt.errorbar(energies,resolutionList[0:2],xerr=0,yerr=ΔresolutionList[0:2],label='Electrons',color='b',marker="_",linestyle='')
        plt.errorbar(energies,resolutionList[2:4],xerr=0,yerr=ΔresolutionList[2:4],label='Pions',color='r',marker="_",linestyle='') 
        
        plt.ylabel("Resolution")            
        plt.title('Fit quality')
        plt.legend()
        plt.grid(visible=True)
        plt.savefig('plots/resEnergies.png')
        return [[],[]]
    return[resolutionList,ΔresolutionList]    