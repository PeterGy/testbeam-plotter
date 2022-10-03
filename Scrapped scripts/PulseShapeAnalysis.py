#processName is actually protosim on aurora
import ROOT as r
from numpy import *
import libDetDescr as DD
import csv
from HCal3Dmodel import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import matplotlib
matplotlib.use('Agg')
r.gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?

def landau(x,a,b,c,d):
    x=x*c-d
    p = 1/sqrt(2*pi)*np.exp(-(x+np.exp(-x)/2))*a +b
    # if p > 900: return 900
    return p


fileName= '287'


pedestals ={}

if '287' in fileName:     
    csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')
    for row in csv_reader:
        try:  pedestals[int(row[0],0)] = float(row[1])
        except:pass    







inFile = r.TFile("reconstructions/"+fileName+".root","READ")
allData = inFile.Get("LDMX_Events") 

plotsMade=0
targetStrip=6
MIPequivalents=[]
for event in allData: 
    muonComesIn=False
    muonComesOut=False
    for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):
        ID=DD.HcalDigiID(h.id())
        if ID.layer()==7 and ID.strip()==targetStrip and ID.end()==0:
            ADCs = [h.at(i).adc_t() for i in range(h.size())] 
            if max(ADCs)>200 and max(ADCs)<900:
                plotsMade+=1
                plt.figure(plotsMade)
                x=[]
                y=[]
                for i in range(h.size()):
                    x.append(i)
                    y.append(ADCs[i]-pedestals[h.id()])
                params,_ = scipy.optimize.curve_fit(landau, x, y, p0=(400,100,1,3), bounds=((100,0,0.1,0),(1500,500,4,5)) , maxfev=5000 )
                print(params)                      
                x_new = np.linspace(x[0], x[-1], 50)
                y_new = landau(x_new,*params)
                plt.plot(x,y,'o')
                plt.plot(x_new, y_new)
                plt.xlim([x[0]-1, x[-1] + 1 ])
                text= str(round(params[0],4))+'; '+str(round(params[1],4))+'; '+str(round(params[2],4))+'; '+str(round(params[3],4))+'; '
                plt.title(text)
                MIPeqqivalent = max(y_new)/410
                MIPequivalents.append(MIPeqqivalent)

                plt.xlabel('Time sample')
                plt.ylabel('ADC')
                plt.savefig("plots/pulses/"+str(plotsMade)+".png")
                plt.close()
        elif ID.layer()==1 and ID.strip()==targetStrip and ID.end()==0: 
            ADCs = [h.at(i).adc_t() for i in range(h.size())] 
            if max(ADCs)>200:
                muonComesIn=True
        elif ID.layer()==19 and ID.strip()==targetStrip and ID.end()==0: 
            ADCs = [h.at(i).adc_t() for i in range(h.size())] 
            if max(ADCs)>200:
                muonComesOut=True
            

    
    if muonComesIn and muonComesOut:  
        plt.savefig("plots/pulses/"+str(plotsMade)+".png")
    # else:
    #     print(muonComesIn,muonComesOut)    
    plt.close()
    if plotsMade>35:
        plt.hist(MIPequivalents)
        plt.savefig("plots/MIP.png")

        
        break        

