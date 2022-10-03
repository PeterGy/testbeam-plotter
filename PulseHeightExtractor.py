#processName is actually protosim on aurora
import ROOT as r
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window

from numpy import *
import libDetDescr as DD
import csv
from HCal3Dmodel import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import scipy.optimize
import matplotlib
matplotlib.use('Agg')
r.gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?

def landau(x,a,b,c,d):
    x=x*c-d
    p = 1/sqrt(2*pi)*np.exp(-(x+np.exp(-x)/2))*a +b
    return p

def labelLayer(text):
    label = r.TLatex()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.SetTextColor(1)
    label.SetNDC()    
    # r.gStyle.SetOptStat("")
    # label.DrawLatex(0.5,  0.85,  'Just raw ADC sums')
    label.DrawLatex(0.3,  0.85,  'Strict track-like cuts on layers 1 & 15')
    label.DrawLatex(0.4,  0.8,  'MIPeq >= 0.9')
    label.DrawLatex(0.4,  0.75,  text)
    return label     

fileName= '287_both_sides_170k'
pedestals ={}
if '287' in fileName:     
    csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')
    for row in csv_reader:
        try:  pedestals[int(row[0],0)] = float(row[1])
        except:pass    

calibrations ={}
csv_reader = csv.reader(open('calibrations/mip_calib_phase3_run287_adcsum_1stpedexcl_pass1_v1.csv'), delimiter=',')
for row in csv_reader:
    try:  calibrations[int(row[0],0)] = float(row[1])
    except:pass    

# print(calibrations)

inFile = r.TFile("reconstructions/"+fileName+".root","READ")
allData = inFile.Get("LDMX_Events") 

print(allData)

# targetLayer = 6
# targetStrip = 4
# targetEnd = 1

targetLayer = 7
targetStrip = 6
targetEnd = 1


def passes_threshold(id,adc):
    MIP_equivalent_threshold_factor = 0.9
    # print(adc , MIP_equivalent_threshold_factor * calibrations[id])
    if adc > MIP_equivalent_threshold_factor * calibrations[id]: return True
    else: return False

def get_inID(targetLayer,targetStrip,targetEnd):
    layer = 1
    if layer <= 9:
        return  DD.HcalDigiID(0, layer,targetStrip,targetEnd).raw()
    elif layer >= 10:
        return  DD.HcalDigiID(0, layer,targetStrip+2,targetEnd).raw()    

def get_outID(targetLayer,targetStrip,targetEnd):
    layer = 15
    if layer <= 9:
        return  DD.HcalDigiID(0, layer,targetStrip,targetEnd).raw()
    elif layer >= 10:
        return  DD.HcalDigiID(0, layer,targetStrip+2,targetEnd).raw()   



def recreate_MIP_response_plot(targetLayer,targetStrip,targetEnd,diagonal=0):
    plotsMade=0
    eventsRecorded=0
    inID =  get_inID(targetLayer,targetStrip+diagonal,targetEnd)
    targetID = DD.HcalDigiID(0,targetLayer ,targetStrip,targetEnd).raw()
    outID =  get_outID(targetLayer,targetStrip-diagonal,targetEnd)


    MIPeq=calibrations[targetID]


    c=r.TCanvas('t','The canvas of anything', 1100, 900)
    hist=r.TH1F('cuts','4 GeV muons', 60,0,6)
    # hist2=r.TH1F('no cuts','Sum ADC EID '+str(targetID), 60,0,2000)

    hist.SetYTitle('Events')
    hist.SetXTitle('Number of MIP equivalents')
    hist.SetMarkerSize(0.75)  
    hist.SetMarkerStyle(8)  
    # hist2.SetMarkerSize(0.75)  
    # hist2.SetMarkerStyle(34)  
    # hist2.SetMarkerColor(4)  

    MIPequivalents=[]
    for event in allData: 
        # muonComesIn=False
        # muonComesOut=False
        MIPresponse = -10000

        
        # for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
        for ih,h in enumerate(getattr(event, "HcalRawDigis_")):
            ID=h.id()
            # print(h.id(),ID.raw())

            if ID == inID:
                ADCs = [h.at(i).adc_t()-pedestals[inID] for i in range(h.size())] 
                ADCsum = sum(ADCs[1:])
                if not passes_threshold(inID,ADCsum): break
                #     muonComesIn=True
                # else:
                #     break

            elif ID == targetID:
                ADCs = [h.at(i).adc_t()-pedestals[targetID] for i in range(h.size())] 
                ADCsum = sum(ADCs[1:])
                MIPresponse = ADCsum   

            elif ID == outID:
                ADCs = [h.at(i).adc_t()-pedestals[outID] for i in range(h.size())] 
                ADCsum = sum(ADCs[1:])
                if not passes_threshold(outID,ADCsum): break
                #     muonComesOut=True
                # else:
                #     break

            # else: 
            #     pass
                # ADCs = [h.at(i).adc_t()-pedestals[outID] for i in range(h.size())] 
                # ADCsum = sum(ADCs[1:])
                # investigatingID = DD.HcalDigiID(ID)  
                # if investigatingID.layer()<=9  and targetStrip == investigatingID.strip():
                #     pass
                # elif investigatingID.layer()>=10 and targetStrip == investigatingID.strip()+2 :
                #     pass
                # elif passes_threshold(ID,ADCsum): break      
      
        else: 
            if MIPresponse != -10000:
                hist.Fill(MIPresponse/MIPeq)
            # hist.Fill(MIPresponse)


        eventsRecorded+=1
        if eventsRecorded%30000 == 0: print(eventsRecorded)
        if eventsRecorded>300000: break   



    hist.Scale(1/hist.GetEntries())
    hist.GetXaxis().SetRangeUser(0, 6)

    # hist2.Scale(1/hist.GetEntries())
    # hist2.GetYaxis().SetRangeUser(0, 1)

    # print(MIPequivalents)

    # MIPequivalents = np.array(MIPequivalents)/MIPeq
    # error=[sqrt(i) for i in MIPequivalents]

    # plt.hist(MIPequivalents,bins=np.linspace(0,6,60))
    # plt.savefig("plots/PulseHeight.png")
    # plt.close()
    # hist2.Draw("same e")  
    hist.Draw("e")  
    label = "Layer: "+str(targetLayer)+", Strip: "+str(targetStrip)+", End: "+str(targetEnd)
    labelLayer(label)

    
    if diagonal == 0:
        # c.SaveAs("plots/PulseHeightROOT"+label+".png")
        file = r.TFile("extractions/Pulse height analysis layer "+str(targetLayer)+', strip '+str(targetStrip)+', end '+str(targetEnd)+".root", "RECREATE")
        print ('Extracted',"extractions/Pulse height analysis layer "+str(targetLayer)+', strip '+str(targetStrip)+', end '+str(targetEnd)+".root")
    hist.SetDirectory(file)
    hist.Write()
    file.Close()
    del(hist)
    c.Close()



# for layer in (3,5,7,9):
for layer in (7,):
    for strip in range(0,8):
        for end in (0,1):
            recreate_MIP_response_plot(layer, strip, end)
# for layer in (7,):
#     for strip in (6,):
#         for end in (0,1):
#             recreate_MIP_response_plot(layer, strip, end)                

# ID=DD.HcalDigiID(411567620)
# print(ID.layer(),ID.strip(),ID.end())


# recreate_MIP_response_plot(targetLayer, targetStrip, targetEnd)
