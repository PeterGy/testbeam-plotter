import ROOT as r
r.gROOT.SetBatch(1); #makes root not try to display plots in a new window
import sys
import libDetDescr as DD
import csv
r.gSystem.Load("libFramework.so") #this library is vital for it to run.


fileName= '287_both_sides_170k'

#retrieve the pedestals
pedestals ={}
if '287' in fileName:     
    csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')
    for row in csv_reader:
        try:  pedestals[int(row[0],0)] = float(row[1])
        except:pass 

#retrieve the calibrations   
calibrations ={}
csv_reader = csv.reader(open('calibrations/mip_calib_phase3_run287_adcsum_1stpedexcl_pass1_v1.csv'), delimiter=',')
for row in csv_reader:
    try:  calibrations[int(row[0],0)] = float(row[1])
    except:pass    

#retrieve the test beam data
inFile = r.TFile("reconstructions/"+fileName+".root","READ")
allData = inFile.Get("LDMX_Events") 


def passes_threshold(id,adc): #determines if the MIP threshold is passed for a given bar
    MIP_equivalent_threshold_factor = 0.9
    if adc > MIP_equivalent_threshold_factor * calibrations[id]: return True
    else: return False

def get_inID(targetLayer,targetStrip,targetEnd): #obtain bar ID for the MIP threshold entry bar
    if targetLayer%2 == 1:
        layer = 1
    elif targetLayer%2 == 0:    
        layer = 2
    if layer <= 9:
        return  DD.HcalDigiID(0, layer,targetStrip,targetEnd).raw()
    elif layer >= 10:
        return  DD.HcalDigiID(0, layer,targetStrip+2,targetEnd).raw()    

def get_targetID(targetLayer,targetStrip,targetEnd): #obtain bar ID of the bar being analysed
    if targetLayer <= 9:
        return  DD.HcalDigiID(0, targetLayer,targetStrip,targetEnd).raw()
    elif targetLayer >= 10:
        return  DD.HcalDigiID(0, targetLayer,targetStrip+2,targetEnd).raw()    

def get_outID(targetLayer,targetStrip,targetEnd): #obtain bar ID for the MIP threshold exit bar
    if targetLayer%2 == 1:
        layer = 15
    elif targetLayer%2 == 0:    
        layer = 16
    if layer <= 9:
        return  DD.HcalDigiID(0, layer,targetStrip,targetEnd).raw()
    elif layer >= 10:
        return  DD.HcalDigiID(0, layer,targetStrip+2,targetEnd).raw()   


#creates an extracted Root file of the data for a given SiPM
def create_MIP_response_plot(targetLayer,targetStrip,targetEnd):
    eventsRecorded=0
    inID =  get_inID(targetLayer,targetStrip,targetEnd)
    targetID = get_targetID(targetLayer,targetStrip,targetEnd)
    outID =  get_outID(targetLayer,targetStrip,targetEnd)
    MIPeq=calibrations[targetID]

    c=r.TCanvas('t','The canvas of anything', 1100, 900)
    hist=r.TH1F('cuts','4 GeV muons', 60,0,6)
    hist.SetYTitle('Events')
    hist.SetXTitle('Number of MIP equivalents')
    hist.SetMarkerSize(0.75)  
    hist.SetMarkerStyle(8)  

    MIPequivalents=[]
    for event in allData: 
        MIPresponse = -10000
        for ih,h in enumerate(getattr(event, "HcalRawDigis_")): 
            #loops through each SiPM, identifying that the entry and exit bar both pass the threshold, 
            #and finding the MIP response for each target bar
            ID=h.id()
            if ID == inID:
                ADCs = [h.at(i).adc_t()-pedestals[inID] for i in range(h.size())] 
                ADCsum = sum(ADCs[1:])
                if not passes_threshold(inID,ADCsum): break

            elif ID == targetID:
                ADCs = [h.at(i).adc_t()-pedestals[targetID] for i in range(h.size())] 
                ADCsum = sum(ADCs[1:])
                MIPresponse = ADCsum   

            elif ID == outID:
                ADCs = [h.at(i).adc_t()-pedestals[outID] for i in range(h.size())] 
                ADCsum = sum(ADCs[1:])
                if not passes_threshold(outID,ADCsum): break  
      
        #if both entry and exit passed the threshold, for loop completes succesfully, 
        #so we check if there was a MIP response (sometimes there are no events), and add the response to the plot
        else: 
            if MIPresponse != -10000:
                hist.Fill(MIPresponse/MIPeq)

        #track progress
        eventsRecorded+=1
        if eventsRecorded%30000 == 0: print(eventsRecorded)
        if eventsRecorded>300000: break   


    #draw and save file
    hist.Scale(1/hist.GetEntries())
    hist.GetXaxis().SetRangeUser(0, 6)
    hist.Draw("e")     
    file = r.TFile("extractions/Pulse height analysis layer "+str(targetLayer)+', strip '+str(targetStrip)+', end '+str(targetEnd)+".root", "RECREATE")
    hist.SetDirectory(file)
    hist.Write()
    file.Close()
    del(hist)
    c.Close()
    print ('Extracted',"extractions/Pulse height analysis layer "+str(targetLayer)+', strip '+str(targetStrip)+', end '+str(targetEnd)+".root")



# if you run the program through arguments, this runs. Otherwise, it does the default behavior
print('Using arguments:',sys.argv)
if len(sys.argv) == 3:
    targetLayer = int(sys.argv[1])
    targetStrip = int(sys.argv[2])
    print(targetLayer,targetStrip)
    create_MIP_response_plot(targetLayer, targetStrip, 0)
    create_MIP_response_plot(targetLayer, targetStrip, 1)

else:    
    targetLayer = 13
    targetStrip = 0
    targetEnd = 0
    create_MIP_response_plot(targetLayer, targetStrip, targetEnd)
    #in case you want to loop through manually, uncomment these
    # for layer in (3,5,7,9):
    # for layer in (9,):
    #     for strip in range(0,8):
    #         for end in (0,1):
    #             create_MIP_response_plot(layer, strip, end)
