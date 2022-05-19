import ROOT as r
from numpy import *
# rootColors=[4,2,3,1,6,7,8,9]
# rootColors=[90,95,99]
# rootColors=[4,6,2]
# rootColors=[60,64,68,72,74]
rootColors=[60,70,80,90,99]
rootColors=[60,80,90,99]
rootColors=[60,91,96,99]
# rootColors=[60,65,99,95]

def styleHistogramEnergyResponse(histogram,legend):
    histogram.SetMarkerSize(0.75)    
    legend.SetX1(0.7)               
    legend.SetX2(1)  
    legend.SetY1(0.6)               
    legend.SetY2(0.8)   

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

def labelSiPMResponseRatio(lines):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.048)
    label.SetTextColor(1)
    label.SetNDC()    
    r.gStyle.SetOptStat("")
    binOfInterest=3
    if lines[0].GetBinContent(binOfInterest) != 0:
        ratio = lines[-1].GetBinContent(binOfInterest)/lines[0].GetBinContent(binOfInterest)
        percentage = str(round(ratio*100,6)) + '%'
        label.DrawLatex(0.1,  0.84, "Movement effect: "+percentage+" brightness")
    return label 

def labelLayer(lines):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.SetTextColor(16)
    label.SetNDC()    
    r.gStyle.SetOptStat("")
    binOfInterest=3
    name=lines[0].GetName()
    layer=name[name.find('layer')+6:name.find('bar')-2]
    print(layer)
    label.DrawLatex(0.3,  0.2,  "Layer: "+str(layer))
    return label 

def createContext(fileName,plotName,μ=None,σ=None,χ2=None):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.05)
    label.SetNDC()      
    if '225' in fileName:    particle="e-"; energy = '2'
    if '226' in fileName:    particle="e-"; energy = '1'
    else: particle="#mu-"; energy = '4'
    sample='10'

    # if 'e-' in fileName:    particle="e-"
    # elif 'mu-' in fileName: particle="#mu-"
    # elif 'pi-' in fileName: particle="#pi-"
    # else:                   particle="???"
    # energy = fileName[fileName.find('-')+1:fileName.find('GeV')]
    # sample = fileName[fileName.find('GeV')+3:fileName.find('k')]
    # if 'deg' in fileName: angle = fileName[fileName.find('k')+1:fileName.find('deg')]
    # else: angle = '0'

    # if plotName == 'energy response vs. energy' and "0.5GeV" in fileName :  energy = '0.5 - 8'
    # if plotName == 'energy response vs. energy' and "0.1GeV" in fileName:  energy = '0.1 - 0.5'
    # if plotName == 'energy response vs. angle':  angle = '0 - 40'

    if 'end0' in plotName:    top = 'left side SiPMs'
    # if 'end0' in plotName:    top = 'top SiPMs'
    elif 'end1' in plotName:    top = 'right side SiPMs'
    # elif 'end1' in plotName:    top = 'bottom SiPMs'
    else: top = 'end0=left;end1=right'
    # if σ != None: top += "#sigma: "+str(round(σ,4))
    # if μ != None: top += ", #mu: "+str(round(μ,4))
    # if μ != None and σ != None: top += "Resolution: "+str(round(σ/μ,4))
    

    bottom = "Particle: "+particle+", Energy: "+energy+" GeV, Sample: "+sample+"k"
    # bottom = "Particle: #mu Energy: 4 GeV, Sample: 10k"
    # if χ2 != None: bottom += ", #chi2: "+str(round(χ2,4))
    contextString='#splitline{'+top+'}{'+bottom+'}'

    label.DrawLatex(0,0.038, contextString)


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
    # if str.find("100k")>-1:  
    #     name = str[str.find('-')+1:str.find('GeV')]+' GeV'
    # else:
        name = str[str.find('k')+1:]
        if name.find("deg")>-1: name = name[0:2]+" degrees"
        elif name.find("barsslide")>-1: name = name[-5:-2]+" mm hor. bar disp."
        elif name.find("xpos")>-1: name = name[0:3]+" mm displacement"
        # else: name = name[name.find('-')+1:name.find('GeV')]+" GeV"
        else: name = str[str.find('-')+1:str.find('GeV')]+' GeV'
        return name

def binaryLegendName(str):
    if 'fpga' in str: return 'testbeam'
    if 'GeV' in str: return 'sim'
    else: return '???'

def LegendName2(str):#returns the legend name based on plot type
    name =''
    if 'end0' in str: name+= 'top/left SiPM'
    if 'end1' in str: name+= 'bottom/right SiPM'
    if '(pedestal subtraction)' in str: name+= '; pedestals removed'
    if '(no pedestal subtraction)' in str: name+= '; pedestals kept'
    return name

def LegendName(str): #returns the legend name based on file name 
    if 'fpga0_243' in str: return '#mu 45 cm'
    if 'fpga0_241' in str: return '#mu 60 cm'
    if 'fpga0_235' in str: return '#mu 30 cm'
    if 'fpga0_287' in str: return '#mu 0 cm'
                        
    if 'fpga0_229' in str: return 'e- 0.3 GeV'
    if 'fpga0_228' in str: return 'e- 0.4 GeV'
    if 'fpga0_227' in str: return 'e- 0.5 GeV'
    if 'fpga0_226' in str: return 'e- 1 GeV'
    if 'fpga0_225' in str: return 'e- 2 GeV'

    if 'GeV' in str: return 'sim'
    if 'fpga' in str: return 'testbeam'
    else: return '???'

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
        # plt.title('Fit quality')
        plt.legend()
        plt.grid(visible=True)
        plt.savefig('plots/resolutions '+name+'.png')
        return [[],[]]

    elif len(resolutionList)==10:
        def expected(E,s,p): return p+s*1/sqrt(E)
        plt.figure("Energies")
        energies = (8,4,2,1,0.5)
        # energies = (0.5,0.4,0.3,0.2,0.1)

        xfit=linspace(min(energies),max(energies),50)
        
        plt.errorbar(energies,resolutionList[0:5],xerr=0,yerr=ΔresolutionList[0:5],label='Pions',color='r',marker="_",linestyle='')
        plt.errorbar(energies,resolutionList[5:10],xerr=0,yerr=ΔresolutionList[5:10],label='Electrons',color='b',marker="_",linestyle='')
        
        paramsPion,e_ = optimize.curve_fit(expected,energies,resolutionList[0:5])
        paramsElec,e_ = optimize.curve_fit(expected,energies,resolutionList[5:10])
        yfitPion=[expected(E,paramsPion[0],paramsPion[1]) for E in xfit]
        yfitElec=[expected(E,paramsElec[0],paramsElec[1]) for E in xfit]    
        plt.plot(xfit,yfitPion,"r--",label='Pion 1/√E fit')
        plt.plot(xfit,yfitElec,"b--",label='Electron 1/√E fit')    
        plt.title("Energy resolution")            
        plt.ylabel("Resolution")            
        plt.xlabel("Energy [GeV]")            
        # plt.title('Fit quality')
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
        # plt.title('Fit quality')
        plt.legend()
        plt.grid(visible=True)
        plt.savefig('plots/resEnergies.png')
        return [[],[]]
    return[resolutionList,ΔresolutionList]    