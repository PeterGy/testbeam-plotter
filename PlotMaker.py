from numpy import *
import ROOT as r
from Histograms import *
from HistogramStyles import *
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window
import copy
#import libDetDescr as DD

def main():   
    skipUninterestingPlots=False
    skipUninterestingPlots=True
    resolutionList=[]
    ΔresolutionList=[]
    EresponseList=[]
    ΔEresponseList=[]

    for plot in plotGroups:
        plotName = plot[-1][0]
        fileName = plot[-1][1] 
        
        try: bars = plotDict[plotName]['bars']
        except: bars = [False] 
        IDcounter=0
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

            # if id != False: hist.SetName(barName(id)) 
            # hist.SetName(barName(id)) 
            # hist.SetName('come on') 
            if dimension == 2:
                c.SetCanvasSize(1600, 800)
                # c.SetCanvasSize(900, 800)
                # c.GetPad(0).SetRightMargin(0.121)
                c.GetPad(0).SetLeftMargin(0.16)
                c.GetPad(0).SetBottomMargin(0.25)
                # hist.GetZaxis().SetRangeUser(0, 8000)
                hist.GetYaxis().SetTitleOffset(0.6)
                hist.Draw("COLZ")
                c.cd(1)
                # axis = r.TGaxis(c.GetPad(0).GetUxmin(),c.GetPad(0).GetUymax(),c.GetPad(0).GetUxmax(),c.GetPad(0).GetUymax(),1,120,510,"+L")
                # axis = r.TGaxis(0,0,0,12,0,12,80506,"+L")
                axis = r.TGaxis(0.5,-2,19.5,-2,0,19*45,21,'')
                axis.SetTitle("Distance along beamline [mm]")
                axis.Draw()
                axis2 = r.TGaxis(-1.5,-0.5,-1.5,11.5,-6*50,6*50,12,'')
                axis2.SetTitle("Distance from beam in x or y axis [mm]")
                axis2.SetTitleOffset(0.8)
                axis2.Draw()

                
                
                # 0,12,0,12,80506,"+L")
                r.gStyle.SetOptStat("")
                label2D()   


            
            # == 'energy response vs. energy' or plotName == 'energy response vs. angle' or plotName == 'energy response vs. position'
            # elif plotName in fittyPlots:
            elif True:
                dualPlotMode=False
                prepareDualPlots(dualPlotMode,c)   
                c.SetBottomMargin(0.14)
                lines=[]
                legend = r.TLegend(0.0,0.9,0.18,1)
                # r.gStyle.SetOptStat("n")
                r.gStyle.SetOptStat("")

                for i in range(len(plot)):
                    plotName = plot[i][0]
                    # hist=inFile.Get(plotName+barName(id)+";")
                    hist=inFile.Get(plotName+barName(id)+";"+str(i+1))
                    # if id != False: hist.SetName(barName(id)) 

                    # print(hist)
                    # hist.GetYaxis().SetRangeUser(0, 800)

                    # hist.GetYaxis().SetRangeUser(0, 70000)
                    # hist.GetYaxis().SetRangeUser(0, 6000)
                    # hist.GetYaxis().SetRangeUser(0, 600)
                    # hist.GetYaxis().SetRangeUser(0, 1100)
                    # hist.GetXaxis().SetRangeUser(100, 1030)
                    # hist.GetXaxis().SetRangeUser(0, 1030)
                    # hist.GetXaxis().SetRangeUser(0, 0.25)
                    # hist.GetYaxis().SetRangeUser(0, 1000)

                    # hist.GetXaxis().SetRangeUser(0, 40)
                    # hist.GetXaxis().SetRangeUser(0, 10000)
                    hist.SetLineColor(rootColors[i])  
                    # if id != False: hist.SetName(barName(id)) 
                    lines.append(copy.deepcopy(hist))
                    # legend.AddEntry(lines[-1],LegendName(plot[i][1]),"f")
                    legend.AddEntry(lines[-1],prettyLegendName(plot[i][1]),"f")
                 

                    # legend.AddEntry(lines[-1],LegendName2(plot[i][0]),"f")
                for line in lines:
                    # line.Draw("same hist e")  
                    line.Draw("same e")  
                    # print(line.GetBinContent (3)) 
                    # line.Draw("same hist")    
                    # if len(lines)==1: line.Draw("HIST")  
                    # try:

                    # par=[0,1,2,3,4,5]

                    # g1 = r.TF1("g1", "gaus", 0, 0.14);
                    # g2 = r.TF1("g2", "gaus", 0, 0.14);
                    # # g1 = r.TF1("g1", "gaus", 85, 95);

                    # # g2 = r.TF1("g2", "gaus", 98, 108);
                    # # g1 = r.TF1('gaus','Sq');
                    # # g2 = r.TF1('gaus','Sq');
                    

                    # total = r.TF1("total", "gaus(0)+gaus(3)", 85, 125);
                    # total.SetLineColor(2);
                    

                    # fit1=line.Fit(g1, "R");
                    # fit2=line.Fit(g2, "R+");
                    
                    # par[0]=fit1.Parameter(0)
                    # par[1]=fit1.Parameter(1)
                    # par[2]=fit1.Parameter(2)
                    # par[3]=fit2.Parameter(0)
                    # par[4]=fit2.Parameter(1)
                    # par[5]=fit2.Parameter(2)
                    # # g1.GetParameters(par[0]);
                    # # g2.GetParameters(par[3]);
                    
                    # // Use the parameters on the sum.
                    # total.SetParameters(par);
                    # fit=line.Fit(total, "R+");





                    # fit = line.Fit('gaus','Sq')
                    # μ = fit.Parameter(1)
                    # Δμ = fit.ParError(1)
                    # σ = fit.Parameter(2)
                    # Δσ = fit.ParError(2)
                    # resolution=σ/μ
                    # Δresolution=resolution*(Δμ/μ+Δσ/σ)
                    # resolutionList.append(resolution)     
                    # ΔresolutionList.append(Δresolution)     
                    # EresponseList.append(μ)     
                    # ΔEresponseList.append(σ)   
                    # χ2=fit.Chi2()
                    # line.GetFunction("gaus").SetLineColor(rootColors[lines.index(line)])

                    # if len(plot) ==1: line.GetFunction("gaus").SetLineColor(2)
                    # labelμ(lines,line,fit)
                    # except: pass
                
                # labelSiPMResponseRatio(lines)    
                # labelLayer(lines)    
                # labelTSbar(lines)    
                # IDcounter=labelELink(lines,IDcounter)    

                # print()    

                    
                # r.gStyle.SetOptStat("")
                # r.gStyle.SetOptStat("nerm")
               
                styleHistogramEnergyResponse(lines[-1],legend)
                if len(lines)>1:
                    c.SetLogy()   
                    
                    c.GetPad(0).SetGrid() 
                    legend.Draw()

            # elif dimension == 1:
            #     c.SetLeftMargin(0.12)   
            #     c.SetBottomMargin(0.14)
            #     # labelNone()
            #     # r.gStyle.SetOptStat("ne")
            #     # r.gStyle.SetOptStat("")
            #     dualPlotMode=False
            #     prepareDualPlots(dualPlotMode,c)                                       
            #     # if id != False: hist.SetName(barName(id)) 
            #     hist.GetRMS()     #this ONE CURSED LINE is somehow the key that makes hist2.GetXaxis().SetRangeUser(50,150) work. Wtf?!?!?!?!             
            #     hist.Draw("HIST")      
            #     # hist.GetYaxis().SetRangeUser(0, 400)

            #     # c.SetLogy()

            # if dualPlotMode:
            #         hist2=copy.deepcopy(hist)
            #         if plotName == 'Distribution of PEs per HCal bar':                       
            #             hist2.GetXaxis().SetRangeUser(50,150) 
            #             hist2.SetTitle('Distribution of PEs per HCal bar (MIP range only)') 
            #         elif plotName == 'TS plots with muons (light yield)':                     
            #             hist2.GetXaxis().SetRangeUser(50,100) 
            #             hist2.SetTitle('TS plots with muons (light yield) (zoomed in)') 
            #         else:
            #             hist2.SetTitle(hist2.GetTitle()+' (log plot)')     
            #         # r.gStyle.SetOptStat("nerm")
            #         c.cd(2)                     
            #         c.GetPad(2).SetGrid()
            #         c.GetPad(1).SetGrid()
            #         hist2.Draw("E")
            #         c.GetPad(2).SetLogy()
            #         if plotName == 'Distribution of PEs per HCal bar':   
            #             fit = hist2.Fit('landau','Sq')
            #             try:
            #                 σ = fit.Parameter(2)
            #                 μ = fit.Parameter(1)    
            #             except: pass #sometimes, nothing hits the bar    
            #         c.cd(0) 

            c.cd()
            # if μ: c.SetBottomMargin(0.15)
            createContext(fileName,plotName,μ,σ,χ2)
            skipUninterestingPlots=False
            # skipUninterestingPlots=True

            if skipUninterestingPlots:
                # if id in [False,5,402654208+4]:
                # if DD.HcalID(id).strip()==3 and DD.HcalID(id).layer()<10:
                # if DD.HcalID(id).layer()<3:
                # condition=False
                # if id>20000:
                #     # try: condition=DD.HcalID(id).layer()<3
                #     try: condition= DD.HcalID(id).strip()==5
                #     except: pass

                # if id<300 or condition:
                    # if DD.HcalID(id).layer()%2==0 :
                # if DD.HcalID(id).strip()==3 and DD.HcalID(id).layer()<10:
                # if DD.HcalID(id).layer()<10:
                if 'bar 6' in extractionName:
                        c.SaveAs("plots/"+extractionName+".png")                
                        # c.SaveAs("plots/"+extractionName+".pdf")                
            else: 
                c.SaveAs("plots/"+extractionName+".png")
                # c.SaveAs("plots/"+extractionName+".pdf")
            c.Close()

        # print(resolutionList)
        [resolutionList,ΔresolutionList] = plotResolution(resolutionList,ΔresolutionList,plotName)
        # [EresponseList,ΔEresponseList] = plotEresponse(EresponseList,ΔEresponseList,plotName)




main()