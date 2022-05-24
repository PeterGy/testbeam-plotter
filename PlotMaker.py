from numpy import *
import ROOT as r
from Histograms import *
from HistogramStyles import *
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window
import copy
import libDetDescr as DD

def main():   
    skipUninterestingPlots=False
    # skipUninterestingPlots=True
    resolutionList=[]
    ΔresolutionList=[]

    for plot in plotGroups:
        plotName = plot[-1][0]
        fileName = plot[-1][1] 
        
        try: bars = plotDict[plotName]['bars']
        except: bars = [False] 
        for id in bars: 
            μ = None
            σ = None
            χ2= None
            extractionName = plotName+"___"+fileName+barName(id)
            dimension = plotDict[plotName]['dimension']
            inFile = r.TFile("extractions/"+extractionName+".root","READ")    
            hist=inFile.Get(plotName+barName(id))
            c=r.TCanvas('t','The canvas of anything', 1100, 900)
            c.cd()
            dualPlotMode=False  
            fittyPlots=['energy response vs. energy','energy response vs. angle','energy response vs. position',
            'energy response vs. bar displacement',
            'Reconstructed energy for tags (absolute energy)','simETot','Reconstructed energy for tags'
            ,'Distribution of signal amplitude for TS bars (individual bars)',
            'total energy deposited FPGA0',
            'total energy deposited FPGA0 horizontal bars',
            'Pulse shape (end0) (no pedestal subtraction)','Pulse shape (end1) (no pedestal subtraction)',
            'Pulse shape (end0) (pedestal subtraction)','Pulse shape (end1) (pedestal subtraction)'
            ]
            if dimension == 2:
                c.SetCanvasSize(900, 800)
                c.GetPad(0).SetRightMargin(0.121)
                hist.GetZaxis().SetRangeUser(0, 8000)
                hist.Draw("COLZ")
                r.gStyle.SetOptStat("")
                label2D()   


            
            # == 'energy response vs. energy' or plotName == 'energy response vs. angle' or plotName == 'energy response vs. position'
            elif plotName in fittyPlots:
                dualPlotMode=False
                prepareDualPlots(dualPlotMode,c)   
                c.SetBottomMargin(0.14)
                lines=[]
                legend = r.TLegend(0.0,0.9,0.18,1)
                for i in range(len(plot)):
                    plotName = plot[i][0]
                    # hist=inFile.Get(plotName+barName(id)+";")
                    hist=inFile.Get(plotName+barName(id)+";"+str(i+1))
                    # print(hist)
                    hist.GetYaxis().SetRangeUser(0, 400)
                    hist.SetLineColor(rootColors[i])  
                    lines.append(copy.deepcopy(hist))
                    legend.AddEntry(lines[-1],LegendName(plot[i][1]),"f")
                    # legend.AddEntry(lines[-1],LegendName2(plot[i][0]),"f")
                for line in lines:
                    line.Draw("same hist e")  
                    # print(line.GetBinContent (3)) 
                    # line.Draw("same hist")    
                    # if len(lines)==1: line.Draw("HIST")  
                    # try:
                    # fit = line.Fit('gaus','Sq')
                    # μ = fit.Parameter(1)
                    # Δμ = fit.ParError(1)
                    # σ = fit.Parameter(2)
                    # Δσ = fit.ParError(2)
                    # resolution=σ/μ
                    # Δresolution=resolution*(Δμ/μ+Δσ/σ)
                    # resolutionList.append(resolution)     
                    # ΔresolutionList.append(Δresolution)     
                    # χ2=fit.Chi2()
                    # line.GetFunction("gaus").SetLineColor(rootColors[lines.index(line)])
                    # if len(plot) ==1: line.GetFunction("gaus").SetLineColor(2)
                    # labelμ(lines,line,fit)
                    # except: pass
                
                # labelSiPMResponseRatio(lines)    
                # labelLayer(lines)    
                # r.gStyle.SetOptStat("nerm")

                # print()    

                    
               
                styleHistogramEnergyResponse(lines[-1],legend)
                if len(lines)>1:
                    # c.SetLogy()   
                    
                    c.GetPad(0).SetGrid() 
                    legend.Draw()

            elif dimension == 1:
                c.SetLeftMargin(0.12)   
                c.SetBottomMargin(0.14)
                r.gStyle.SetOptStat("ne")
                dualPlotMode=False
                prepareDualPlots(dualPlotMode,c)                                       
                if id != False: hist.SetName(barName(id)) 
                hist.GetRMS()     #this ONE CURSED LINE is somehow the key that makes hist2.GetXaxis().SetRangeUser(50,150) work. Wtf?!?!?!?!             
                hist.Draw("HIST")      
                hist.GetYaxis().SetRangeUser(0, 400)

                # c.SetLogy()

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
                    hist2.Draw("E")
                    c.GetPad(2).SetLogy()
                    if plotName == 'Distribution of PEs per HCal bar':   
                        fit = hist2.Fit('landau','Sq')
                        try:
                            σ = fit.Parameter(2)
                            μ = fit.Parameter(1)    
                        except: pass #sometimes, nothing hits the bar    
                    c.cd(0) 

            c.cd()
            # if μ: c.SetBottomMargin(0.15)
            createContext(fileName,plotName,μ,σ,χ2)

            if skipUninterestingPlots:
                # if id in [False,5,402654208+4]:
                if DD.HcalID(id).strip()==2 and DD.HcalID(id).layer()<10:
                    # if DD.HcalID(id).layer()%2==0 :
                # if DD.HcalID(id).strip()==3 and DD.HcalID(id).layer()<10:
                # if DD.HcalID(id).layer()<10:
                        c.SaveAs("plots/"+extractionName+".png")                
            else: c.SaveAs("plots/"+extractionName+".png")
            c.Close()

        # print(resolutionList)
        [resolutionList,ΔresolutionList] = plotResolution(resolutionList,ΔresolutionList,plotName)



main()