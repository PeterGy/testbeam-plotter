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
    legend.SetY1(0.5)               
    legend.SetY2(0.8)   

def createLabel(fwhm=None):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.03)
    label.SetNDC()    
    if fwhm: label.DrawLatex(0,  0.005, "FWHM:  "+str(round(fwhm,6)))
    return label

def main():   
    fwhmList=[]   
    for plot in plotGroups:
        plotName = plot[-1][0]
        fileName = plot[-1][1] 
        try: bars = plotDict[plotName]['bars']
        except: bars = [False] 
        for id in bars: 
            extractionName = plotName+"___"+fileName+barName(id)
            dimension = plotDict[plotName]['dimension']

            inFile = r.TFile("extractions/"+extractionName+".root","READ")  
            
            
            hist=inFile.Get(plotName)

            c=r.TCanvas('t','Total energy with fits', 900, 900)
            c.cd()
            
            legend = inFile.Get("legend")
            # inFile.Print("toponly")


            if dimension == 2:
                print(c.GetPad(0).GetRightMargin())
                c.GetPad(0).SetRightMargin(0.12)
                styleHistogram2D(hist)
                hist.Draw("COLZ")
                r.gStyle.SetOptStat("")
            
            elif plotName == 'energy response vs. energy':
                lines=[]
                
                for line in range(len(plot)):
                    hist=inFile.Get(plotName+";"+str(line+1))
                    lines.append(copy.deepcopy(hist))
                for line in lines:
                    line.Draw("same e")    
                    line.Fit('gaus', '', '', 0, 400)
                    line.GetFunction("gaus").SetLineColor(rootColors[lines.index(line)])
                    # fit.SetLineColor(4)
                    fwhm=2.355*line.GetRMS()
                    # print(fwhm)
                    fwhmList.append(fwhm)     
                c.SetLogy()   
                c.GetPad(0).SetGrid()
                styleHistogramEnergyResponse(lines[-1],legend)
                legend.Draw()
                r.gStyle.SetOptStat("ne")

            elif plotName == 'Distribution of PEs per HCal bar':
                c.SetCanvasSize(2000, 900)
                c.Divide(2,1) 
                c.cd(1)  
                legend.Draw()
                hist.SetName(barName(id)) 
                # hist.GetXaxis().SetRangeUser(50,150) 
                hist.Draw("")
                r.gStyle.SetOptStat("nerm")        

                hist2=copy.deepcopy(hist)
                hist2.SetTitle('MIP peak focus') 
                hist2.GetXaxis().SetRangeUser(50,150) 
                c.cd(2) 
                # c.GetPad(2).SetLogy()
                c.GetPad(2).SetGrid()
                hist2.Draw("")
                c.cd(0)
                styleHistogramCommon(hist,hist2,legend)

            elif dimension == 1:
                c.SetCanvasSize(2000, 900)
                c.Divide(2,1) 
                c.cd(1)             
                
                
                

                if id != False:                    
                    legend.Draw()
                    hist.SetName(barName(id)) 
                    hist.Draw("")
                    r.gStyle.SetOptStat("ne") 
                    

                else:  
                    legend.Draw()     
                    # hist.SetTitle(plotName)
                    
                    hist.Draw("B")
                    r.gStyle.SetOptStat("e")           
                    fwhm=2.355*hist.GetRMS()
                    createLabel(fwhm)         

                    
                    
    
                
                hist2=copy.deepcopy(hist)
                c.cd(2) 
                c.GetPad(2).SetLogy()
                c.GetPad(2).SetGrid()
                c.GetPad(1).SetGrid()
                hist2.Draw("E")
                c.cd(0)
                styleHistogramCommon(hist,hist2,legend)
                
             

            c.SaveAs("plots/"+extractionName+".png")
            c.Close()


    if len(fwhmList)>1:        
        def expected(E,s=1):
            return s*1/sqrt(E)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        # plt.ioff()
        if len(fwhmList)==5:
            plt.plot((8,4,2,1,0.5),fwhmList,"b*")
        elif len(fwhmList)==10:
            xfit=linspace(0.5,8,30)
            plt.plot((8,4,2,1,0.5),fwhmList[0:5],"r*",label='Pions')
            plt.plot((8,4,2,1,0.5),fwhmList[5:10],"b*",label='Electrons')
            from scipy import optimize
            paramsPion,e_ = optimize.curve_fit(expected,(8,4,2,1,0.5),fwhmList[0:5])
            paramsElec,e_ = optimize.curve_fit(expected,(8,4,2,1,0.5),fwhmList[5:10])
            yfitPion=[expected(E,s=paramsPion[0]) for E in xfit]
            yfitElec=[expected(E,s=paramsElec[0]) for E in xfit]
            plt.plot(xfit,yfitPion,"r-",label='Pion 1/√E fit')
            plt.plot(xfit,yfitElec,"b-",label='Electron 1/√E fit')         

        elif len(fwhmList)==8:
            xfit=linspace(0.1,0.4,30)
            plt.plot((0.4,0.3,0.2,0.1),fwhmList[0:4],"r*",label='Pions')
            plt.plot((0.4,0.3,0.2,0.1),fwhmList[4:8],"b*",label='Electrons')
            from scipy import optimize
            paramsPion,e_ = optimize.curve_fit(expected,(0.4,0.3,0.2,0.1),fwhmList[0:4])
            paramsElec,e_ = optimize.curve_fit(expected,(0.4,0.3,0.2,0.1),fwhmList[4:8])
            yfitPion=[expected(E,s=paramsPion[0]) for E in xfit]
            yfitElec=[expected(E,s=paramsElec[0]) for E in xfit]
            plt.plot(xfit,yfitPion,"r-",label='Pion 1/√E fit')
            plt.plot(xfit,yfitElec,"b-",label='Electron 1/√E fit')  
               
        plt.ylabel("FWHMs")
        plt.xlabel("Energy [GeV]")
        plt.title('FWHMs')
        plt.legend()
        # plt.xscale('log')
        plt.grid(visible=True)
        plt.savefig('plots/fwhms.png')
        

   




main()