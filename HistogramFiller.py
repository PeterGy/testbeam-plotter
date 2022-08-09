#processName is actually protosim on aurora
from HistogramProperties import *
import ROOT as r
from numpy import *
import platform 
# import libDetDescr as DD
import csv
from HCal3Dmodel import *
# import HCal3Dmodel.py

# def pedestal_subtractor(hist):

# print(pedestals)    
    # for digi_ID in pedestals:    
    #     ID=DD.HcalDigiID(digi_ID)
    #     HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
    #     hist[HCal_ID].Add(1)
    # print(pedestals)


#hist can actually be a single histogram or a dictionary of 12 or 192 histograms
def fillHist(hist, plotVar, allData, processName="protosim" , minEDeposit=0, maxEDeposit=float('inf'), barID=False, angle=0, beamEnergy=1, eventOfInterest=None, fileName=''): 
    # print('doing one', fileName)

    if '279' in fileName:     csv_reader = csv.reader(open('pedestals/pedestals_20220424_07.csv'), delimiter=',')
    if '287' in fileName:     csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')
    if '235' in fileName or '241' in fileName or '243' in fileName:     csv_reader = csv.reader(open('pedestals/pedestals_20220422_07.csv'), delimiter=',')
    if '225' in fileName or '226' in fileName:     csv_reader = csv.reader(open('pedestals/pedestals_20220421_07.csv'), delimiter=',')
    else: csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')
    # csv_reader = csv.reader(open('pedestals/pedestals_20220424.csv'), delimiter=',')

    pedestals ={}
    if '(pedestal subtraction)' in plotVar:
        for row in csv_reader:
            try:  pedestals[int(row[0],0)] = float(row[1])
            except:pass
    if '(no pedestal subtraction)' in plotVar:
        for row in csv_reader:
            try:  pedestals[int(row[0],0)] = 0.0
            except:pass        
    else:     
        for row in csv_reader:
            try:  pedestals[int(row[0],0)] = float(row[1])
            except:pass    


    if len(hist)==1:
        hist=hist[0]
        
    energyErrorCorrection = 0.5 #they did an oopsie in the coding and now I got to correct for it
    allowNoise= False

    if 'Pulses' == plotVar:  
        plotsMade=0
        for event in allData: 
            

            for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
            # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):
                
                # ID=DD.HcalDigiID(h.id())

                # if ID.layer()==4 and ID.strip()==4 and ID.end()==0:
                    ADCs = [h.at(i).adc_t() for i in range(h.size())] 
                    if max(ADCs)>200:
                        c=r.TCanvas('t','The canvas of anything', 1100, 900)
                        pulseHist =  r.TH1F("timeSampleEventDisplay", "Time samples ", 8,0,8) 
                        pulseHist.SetYTitle('ADC')
                        pulseHist.SetXTitle('Time sample') 
                        pulseHist.GetYaxis().SetRangeUser(0, 1024)
                        for i in range(h.size()):
                                # print(pedestals)
                                pulseHist.Fill(i,ADCs[i]-pedestals[h.id()])
                                # if h.at(i).tot() >1000:
                                # if True:
                                #     print('Timestamp',i)
                                #     print('adc',h.at(i).adc_t())
                                #     print('toa',h.at(i).toa())
                                #     print('tot',h.at(i).tot())
                                
                        
                        pulseHist.Draw("HIST")
                        c.SaveAs("plots/pulses/"+str(plotsMade)+".png")  
                        c.Close()
                        del(pulseHist)
                        plotsMade+=1
                        print(h.id())
                        break

    elif   plotVar == 'simX': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[0])                     
    elif plotVar == 'simY': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[1])  
    elif plotVar == 'simZ': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2]) 
    elif plotVar == 'simE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getEdep()) 
    elif plotVar == 'simETot': 
        for event in allData: 
            Energy=0
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    Energy+=h.getEdep() 
            hist.Fill(Energy)             
                # print("Sim id",h.getID()-4026e5)               
    elif plotVar == 'simEH1': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getPosition()[2] < 0: hist.Fill(h.getEdep())              
    elif plotVar == 'simEH2': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getPosition()[2] > 0: hist.Fill(h.getEdep()) 
    elif plotVar == 'simEBar': 
        for event in allData: 
            bars={}
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                try: bars[h.getID()]+=h.getEdep()
                except: bars[h.getID()]=h.getEdep()                            
            for bar in bars:
                hist.Fill(bars[bar])     

    elif plotVar == 'recEBar': 
        for event in allData: 
            bars={}
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                try: bars[h.getID()]+=h.getPE()
                except: bars[h.getID()]=h.getPE()                           
            for bar in bars:
                hist.Fill(bars[bar])   

    # elif plotVar == 'recE': 
    #     valuesDigi={}
    #     valuesRec={}
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):
    #             # print(h.id())     
    #             valuesDigi[h.id()] =1   
    #         for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
    #             valuesRec[h.getID()] =1
    #     # print(valuesDigi)
    #     # print(valuesRec)

        listDigi=[]
        for i in valuesDigi:
            listDigi.append(i)
        listDigi.sort()
        print(listDigi)  
        print(len(listDigi))  
        listRec=[]
        for i in valuesRec:
            listRec.append(i)
        listRec.sort()
        print(listRec)
        print(len(listRec))
                    



    elif plotVar == 'recE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                   hist.Fill(h.getEnergy()*energyErrorCorrection) 

                
  
    elif plotVar == 'recENoisy': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                    hist.Fill(h.getEnergy()*energyErrorCorrection) 
  
    elif plotVar == 'recX': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if getLayer(h.getID())%2==1:
                    hist.Fill(h.getXPos()) 
    elif plotVar == 'recY': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist.Fill(h.getYPos()) 
    elif plotVar == 'recZ': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist.Fill(h.getZPos()) 




    elif plotVar == 'recAmp': 
        eventCount=0
        for event in allData: 
            eventCount+=1
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getAmplitude()) 
        print(eventCount)            

    elif plotVar == 'recPE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getPE()) 


    elif plotVar == 'simX(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit: 
                    hist.Fill(h.getPosition()[2],h.getPosition()[0])       
    elif plotVar == 'simY(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2],h.getPosition()[1])            
    elif plotVar == 'simY(X)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[1],h.getPosition()[0])                 
    elif plotVar == 'simE(X)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[0],h.getEdep()) 
    elif plotVar == 'simE(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2],h.getEdep()) 

    elif plotVar == 'recX(Z)': #only for pion checking!
        for event in allData: 
            eventE=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                eventE+=h.getEnergy()*energyErrorCorrection
            # if 70<eventE     and eventE<90:
            # if 70>eventE  or eventE>90:
            if 0<eventE     and eventE<1000000:
                for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                # if 22> h.getTime() or h.getTime() >23: 
                    hist.Fill(h.getZPos(),h.getXPos()) 


    elif plotVar == 'recX(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: 
                # if 22> h.getTime() or h.getTime() >23: 
                    hist.Fill(h.getZPos(),h.getXPos()) 
    elif plotVar == 'recY(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos(),h.getYPos()) 
    elif plotVar == 'recY(X)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getYPos(),h.getXPos()) 

    elif plotVar == 'trigSimX':  #unimplemented
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0])       
         
    elif plotVar == 'trigSimX(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getPosition()[0])   
                # print(h)
    elif plotVar == 'trigSimY(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getPosition()[1])            
    elif plotVar == 'trigSimY(X)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0],h.getPosition()[1])                 
    elif plotVar == 'trigSimE(X)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[0],h.getEdep()) 
    elif plotVar == 'trigSimE(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getEdep()) 
    # elif plotVar == 'trigRecX': #last I checked these were bad
        # for event in allData: 
            # for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                # hist.Fill(h.getXPos()) 
    elif plotVar == 'trigRecT': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                if h.getBarID() ==6: hist.Fill(h.getTime()) 
                # print(h.getBarID())
                # print(h.items()) 



    elif plotVar == 'timeHCal': 
        for event in allData: #I define time difference based on the first event's time
            # trigTimes=[]
            hcalTimes=[]
            # for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
            #     trigTimes.append(h.getTime())
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist.Fill(h.getTime())
                print(h.getTime())
                # hcalTimes.append(h.getTime())   
            # hist.Fill(min(hcalTimes)) 

    # elif plotVar == 'simX(Z)': 
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
    #             if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
    #                 hist.Fill(h.getPosition()[2],h.getPosition()[0])
    
    
    elif plotVar == 'mean light yield vs bar ID': 
        PEs={}
        barHits={}
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                if h.getBarID() in PEs:
                    PEs[h.getBarID()] +=h.getPE()
                    barHits[h.getBarID()] +=1
                else:
                    PEs[h.getBarID()] =h.getPE()
                    barHits[h.getBarID()] =1

        for barID in PEs:    
            hist.Fill(barID,PEs[barID]/barHits[barID])  
                # if h.getBarID() ==6: hist.Fill(h.getTime()) -
        print(PEs)        
        print(barHits)        





#The testbeam functions
    #1.1
    elif plotVar == 'Mapped distribution of number of hits of each bar': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                LayerBar = barMapLocation(h.getID())
                hist.Fill(LayerBar[0],LayerBar[1])   
    elif plotVar == 'Distribution of number of hits of each bar': 
        for event in allData: 
            hits=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() == barID: 
                    hits+=1
            hist.Fill(hits)              
    #1.2
    if plotVar == 'Distribution of pulse height of each bar': 
        for event in allData: 
            amplitudes = {}
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() in amplitudes:
                    amplitudes[h.getID()] += h.getAmplitude()
                else:
                    amplitudes[h.getID()] = h.getAmplitude()    
            for barID in amplitudes:    
                hist[barID].Fill(amplitudes[barID])     
    #1.3
    elif plotVar == 'Total number of hits per event': 
        for event in allData: 
            totalCount=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalCount+=1
            hist.Fill(totalCount) 
        
    elif plotVar == 'Total number of hits per run':
        runs={}
        for event in allData: 
            run=event.EventHeader.getRun()
            if run not in runs: runs[run]=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                runs[run]+=1        
        for run in runs:
            hist.Fill(runs[run]) 
        
    # elif plotVar == 'Sum of pulse height per event': 
    #     for event in allData: 
    #         totalAmplitude=0
    #         for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
    #             totalAmplitude+=h.getAmplitude()
    #         hist.Fill(totalAmplitude) 
        
    elif plotVar == 'Sum of pulse height per run': 
        runs={}
        for event in allData: 
            run=event.EventHeader.getRun()
            if run not in runs: runs[run]=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                runs[run]+=h.getAmplitude()       
        for run in runs:
            hist.Fill(runs[run]) 
        
    #1.4
    # elif plotVar == 'Distribution of number of hits for TS bars': 
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
    #             hist.Fill(h.getBarID())

    elif plotVar == 'Distribution of signal amplitude for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID(),h.getAmplitude())

    #  elif plotVar == 'Distribution of signal amplitude for TS bars (individual bars)': 
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
    #             hist[h.getBarID()].Fill(h.getAmplitude()/1000.)       #WARNING: this makes them go from fC to pC
    #             if h.getBarID() not in range(0,13): print (h.getBarID())

    elif plotVar == 'Distribution of signal amplitude for TS bars (individual bars)': 
        if len(fileName)==5: eventDataFormat = "testBeamHitsUp_hits"
        else:    eventDataFormat = "trigScintRecHitsUp_protosim"
        eventCount=0
        for event in allData: 
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                if h.getPE() >50:
                    hist[h.getBarID()].Fill(h.getAmplitude()/1000)    
            eventCount+=1
            if eventCount>4000 and   eventDataFormat == "trigScintRecHitsUp_protosim": break      



    #1.5
    elif plotVar == 'Time difference between TS and HCal': 
        for event in allData: #I define time difference based on the first event's time
            trigTimes=[]
            hcalTimes=[]
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                trigTimes.append(h.getTime())
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hcalTimes.append(h.getTime())   
            hist.Fill(min(hcalTimes)-min(trigTimes))     

                


    #2
    
    elif plotVar == 'Reconstructed energy for tags': 
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                print(h.getEnergy())
                energy+=h.getEnergy()*energyErrorCorrection
            print(energy)    
            hist.Fill(energy/beamEnergy) 



    elif plotVar == 'Reconstructed energy for tags (absolute energy)':
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                energy+=h.getEnergy()*energyErrorCorrection
            hist.Fill(energy)             

    elif plotVar == 'Energy as a function of the incoming particle angle':
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist.Fill(angle,h.getEnergy()*energyErrorCorrection)      

    elif plotVar == 'Mapped Distribution of PEs per HCal bar': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                LayerBar = barMapLocation(h.getID())
                hist.Fill(LayerBar[0],LayerBar[1],h.getPE())      

    elif plotVar == 'Mapped Distribution of average PEs': 
        countMap = zeros((19,12))
        PEMap = zeros((19,12))
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                LayerBar = barMapLocation(h.getID())
                countMap[LayerBar[0]-1,LayerBar[1]] += 1
                PEMap[LayerBar[0]-1,LayerBar[1]] += h.getPE()
        countMap[countMap == 0 ] = 1        
        for i in range(19):
            for j in range(12):
                hist.Fill(i+1,j,PEMap[i,j]/countMap[i,j])
 
    #3.2
    elif plotVar == 'TS plots with muons (hit efficiency) (1 plot per bar)': 
        for event in allData: 
            hits=0
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                    if h.getBarID() == barID: 
                        hits+=1
            hist.Fill(hits)  
          
    elif plotVar == 'TS plots with muons (hit efficiency)': 
        eventCount=allData.GetEntries()
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                # print(h.getBarID())
                hist.Fill(h.getBarID(),1/eventCount)  

    elif plotVar == 'TS plots with muons (pulse shape)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                    if h.getBarID() == barID: 
                        # hist.Fill(h.getTime())  
                        hist.Fill(h.getTime(),h.getAmplitude())  
                        # if barID == 5: 
                        #     if h.getTime() !=2.5:
                        #         print(h.getTime())
        

    elif plotVar == 'energy response vs. energy' or plotVar == 'energy response vs. angle' or plotVar == 'energy response vs. position'  or plotVar == 'energy response vs. bar displacement': 
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                energy+=h.getEnergy()*energyErrorCorrection
            hist.Fill(energy/beamEnergy) 

    elif plotVar == 'rec vs sim':
        recE=0
        simE=0
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                recE+=h.getEnergy()*energyErrorCorrection
                hist.Fill(h.getEnergy()*energyErrorCorrection)
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                simE+=h.getEdep()
                hist.Fill(h.getEdep())  
        print ("Total simulated energy deposit:",simE)          
        print ("Total reconstructed energy deposit:",recE)   
 
#     return hist   

# def fillhist(hist, plotVar, allData, processName="protosim"):     
#     # print('hmmmm',type(hist) != type({}))
#     energyErrorCorrection = 0.5
       
            

        

    

    #3
    elif plotVar == 'Distribution of PEs per HCal bar': 
        for event in allData: 
            # PEs = 0
            # for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
            #     if h.getID() == barID: 
            #         PEs += h.getPE() 
            # hist.Fill(PEs)    

            PEs = {}
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() in PEs:
                    PEs[h.getID()] += h.getPE()
                else:
                    PEs[h.getID()] = h.getPE()    
                # if h.getID() == barID: 
                #     amplitude += h.getAmplitude() 
            for barID in PEs:    
                hist[barID].Fill(PEs[barID]) 

    #3.2
    elif plotVar == 'TS plots with muons (light yield)': 
        values={}
        for event in allData: 
            PEs = {}
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                if  70<h.getPE() and h.getPE()<80:
                    values[h.getPE()] =1

                if h.getBarID() in PEs:
                    PEs[h.getBarID()] += h.getPE()
                else:
                    PEs[h.getBarID()] = h.getPE()    
            for barID in PEs:    
                hist[barID].Fill(PEs[barID])   
        print(values)            

    elif plotVar == 'simE (individual bars)': 
        for event in allData: 
            Energies={}
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getID() in Energies:
                    Energies[h.getID()]+=h.getEdep() 
                else:
                    Energies[h.getID()]=h.getEdep()    
            for barID in Energies:    
                # if Energies[barID] > 17: Energies[barID] = 17
                hist[barID].Fill(Energies[barID]) 

    elif plotVar == 'recE (individual bars)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist[h.getID()].Fill(h.getEnergy()*energyErrorCorrection) 


    # elif plotVar == 'Mapped distribution of number of hits of each bar': 
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    #             print(dir(h))
    #             # print(h.id())
    #             # print(h.isTOT())
         
    #         break    

    # elif plotVar == 'Mapped distribution of number of hits of each bar': 
    #     for event in allData: 
    #         recoList=[]
    #         digiList=[]
    #         PEList=[]
    #         import libDetDescr as DD
    #         for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
    #             # LayerBar = barMapLocation(h.getID())
    #             # hist.Fill(LayerBar[0],LayerBar[1])  
    #             recoList.append(h.getID()) 
    #             PEList.append(h.getPE())
    #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    #         # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):  
    #             digiList.append(h.id()) 
    #         print('The following reco IDs are present in an event:')
    #         print('rawID,layer,strip')
    #         for i in range(0,len(recoList)):
    #             h=DD.HcalID(recoList[i])
    #             print('recID',h.raw(),h.layer(),h.strip(),'which had PEs',PEList[i])
    #         print('The following digi IDs are present in an event:')    
    #         print('rawID,layer,strip,end')
    #         for i in range(0,len(digiList)):    
    #             d=DD.HcalDigiID(digiList[i])

    #             d_translated=DD.HcalID(d.section(),d.layer(),d.strip()).raw()
    #             print('digiID',d.raw(),d.layer(),d.strip(),d.end(),'which should convert into','recID',d_translated,' Is in the event?:',(d_translated in recoList)  )
                

    #         break    

#experimental
    elif plotVar == 'Mapped SiPM hits': 
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):   
                LayerBarSide = sipmMapLocation(h.id()) 
                if LayerBarSide[2]==1: LayerBarSide[0] +=20
                hist.Fill(LayerBarSide[0],LayerBarSide[1])  

    elif plotVar == 'Mapped SiPM hits (individual event)': 
        eventCounter=0
        for event in allData:             
            eventCounter+=1            
            if eventCounter == int(eventOfInterest):
                for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):   
                    LayerBarSide = sipmMapLocation(h.id()) 
                    if LayerBarSide[2]==1: LayerBarSide[0] +=20
                    hist.Fill(LayerBarSide[0],LayerBarSide[1])  



    # elif plotVar == 'Mapped ADC average': 
    #     countMap = zeros((39,12))
    #     ADCMap = zeros((39,12))
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    #             # print("HcalDigis_"+processName)      
    #             #for i in 'at', 'id', 'isADC', 'isTOT', 'size', 'soi', 'tot']
    #             # print(h.at(3).adc_t())      
      

    #             LayerBarSide = sipmMapLocation(h.id()) 
    #             if LayerBarSide[2]==1: LayerBarSide[0] +=20
                
    #             for i in range(h.size()) :
    #                 countMap[LayerBarSide[0]-1,LayerBarSide[1]] += 1
    #                 ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()
    #     countMap[countMap == 0 ] = 1
    #     for i in range(39):
    #         for j in range(12):
    #             hist.Fill(i+1,j,ADCMap[i,j]/countMap[i,j])

    # elif plotVar == 'Mapped ADC average': 
    #     countMap = zeros((39,12))
    #     ADCMap = zeros((39,12))
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    #         # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):
    #         # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):   
    #             # print("HcalDigis_"+processName)      
    #             #for i in 'at', 'id', 'isADC', 'isTOT', 'size', 'soi', 'tot']
    #             # print(h.at(3).adc_t())      
    #             ID=DD.HcalDigiID(h.id())
    #             # HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
      

    #             # LayerBarSide = sipmMapLocation(h.id()) 
    #             LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
    #             if LayerBarSide[2]==1: LayerBarSide[0] +=20
                
    #             for i in range(h.size()) :
    #                 countMap[LayerBarSide[0]-1,LayerBarSide[1]] += 1
    #                 ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()
    #     countMap[countMap == 0 ] = 1
    #     for i in range(39):
    #         for j in range(12):
    #             hist.Fill(i+1,j,ADCMap[i,j]/countMap[i,j])


    elif plotVar == 'Mapped Distribution of average PEs': 
        countMap = zeros((19,12))
        PEMap = zeros((19,12))
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                LayerBar = barMapLocation(h.getID())
                countMap[LayerBar[0]-1,LayerBar[1]] += 1
                PEMap[LayerBar[0]-1,LayerBar[1]] += h.getPE()
        countMap[countMap == 0 ] = 1        
        for i in range(19):
            for j in range(12):
                hist.Fill(i+1,j,PEMap[i,j]/countMap[i,j])

    elif plotVar == 'trigRecE (per bar)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):    
                hist[h.getBarID()].Fill(h.getEnergy())      
                # print(h.getEnergy())            
    elif plotVar == 'trigRecE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):   
                hist.Fill(h.getEnergy()) 
                print(h.getBarID())  
    elif plotVar == 'trigRecPE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):   
                hist.Fill(h.getPE())                 
    elif plotVar == 'trigRecQ': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):   
                hist.Fill(h.getAmplitude())                 
    elif plotVar == 'trigRecQ (per bar)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):   
                hist[h.getBarID()].Fill(h.getAmplitude())                 

    elif plotVar == 'trigSimE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getEdep())    
                print(h.getID())
    elif plotVar == 'trigSimEBar': 
        for event in allData: 
            IDs={}
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                if h.getID() in IDs: IDs[h.getID()] += h.getEdep()
                else: IDs[h.getID()] = h.getEdep()
                
            for id in IDs:    
                hist.Fill(IDs[id])    
                print(IDs[id])

    elif plotVar == 'reconstructed energy': 
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                energy+=h.getEnergy()*energyErrorCorrection
            hist.Fill(energy) 

    elif plotVar == 'total energy deposited FPGA0': 
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                # print(getLayer(h.getID()))
                if getLayer(h.getID())<=11:
                    energy+=h.getEnergy()*energyErrorCorrection
            hist.Fill(energy) 
    elif plotVar == 'total energy deposited FPGA0 horizontal bars': 
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                # print(getLayer(h.getID()))
                if getLayer(h.getID())<=11 and getLayer(h.getID())%2==1:
                    energy+=h.getEnergy()*energyErrorCorrection
            hist.Fill(energy)    

    # getLayer(h.getID())%2==1 these are the horizontal bars



    # elif plotVar == 'Pulse shape' or plotVar == 'Pulse shape (end0)': 
    #     hitCount={}
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    #             ID=DD.HcalDigiID(h.id())
    #             HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                
    #             if HCal_ID not in hitCount: hitCount[HCal_ID]=0
    #             if ID.end()==0:
    #                 ADCs=[h.at(i).adc_t() for i in range(h.size())]
    #                 if max(ADCs)>200:
    #                     hitCount[HCal_ID]+=1
    #                     for i in range(h.size()):
    #                         # hist[HCal_ID].Fill(i,h.at(i).adc_t()-pedestals[h.id()]) 
    #                         hist[HCal_ID].Fill(i,h.at(i).adc_t()-0) 
    #     for h in hist:
    #         try:
    #             hist[h].Scale(1./hitCount[h])
    #         except: pass    
        # pedestal_subtractor(hist)

    # elif plotVar == 'Pulse shape (end1)': 
    #     hitCount={}
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
    #             ID=DD.HcalDigiID(h.id())
    #             HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                
    #             if HCal_ID not in hitCount: hitCount[HCal_ID]=0
    #             if ID.end()==1:
    #                 ADCs=[h.at(i).adc_t() for i in range(h.size())]
    #                 if max(ADCs)>200:
    #                     hitCount[HCal_ID]+=1
    #                     for i in range(h.size()):
    #                         hist[HCal_ID].Fill(i,h.at(i).adc_t()-pedestals[h.id()]) 
    #     for h in hist:
    #         try:
    #             hist[h].Scale(1./hitCount[h])
    #         except: pass   
        # pedestal_subtractor(hist)    
                       
    #'at', 'id', 'isADC', 'isTOT', 'size', 'soi', 'tot'


    elif plotVar == 'Mapped ADC average': 
        countMap = zeros((39,12))
        ADCMap = zeros((39,12))
        for event in allData: 
            for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
            # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):
            # for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):   
                # print("HcalDigis_"+processName)      
                #for i in 'at', 'id', 'isADC', 'isTOT', 'size', 'soi', 'tot']
                # print(h.at(3).adc_t())      
                ID=DD.HcalDigiID(h.id())
                # HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
      

                # LayerBarSide = sipmMapLocation(h.id()) 
                LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
                if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
                if LayerBarSide[2]==1: LayerBarSide[0] +=20
                
                for i in range(h.size()) :
                    countMap[LayerBarSide[0]-1,LayerBarSide[1]] += 1
                    try: ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()-pedestals[h.id()]
                    except: ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()
                    # print(-pedestals[h.id()])
        countMap[countMap == 0 ] = 1
        for i in range(39):
            for j in range(12):
                hist.Fill(i+1,j,ADCMap[i,j]/countMap[i,j])

    elif 'Pulse shape' in plotVar:
        if '(end0)' in plotVar: end=0
        elif '(end1)' in plotVar: end=1
        else: end=0
        if '(no pedestal subtraction)' in plotVar: subtractPedestals=False
        elif '(pedestal subtraction)' in plotVar: subtractPedestals=True
        else: subtractPedestals=False


        

        hitCount={}

        for event in allData: 
            this_sipm_adc={}
            opposing_sipm_adc={}

            for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
                ID=DD.HcalDigiID(h.id())
                HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                if HCal_ID not in hitCount: hitCount[HCal_ID]=0
                

                if ID.end()!=end:
                    ADCs = [h.at(i).adc_t() for i in range(h.size())] 
                    opposing_sipm_adc[HCal_ID] = ADCs

                elif ID.end()==end:
                    ADCs2 = [h.at(i).adc_t() for i in range(h.size())]
                    this_sipm_adc[HCal_ID] = ADCs2


                if HCal_ID in opposing_sipm_adc and HCal_ID in this_sipm_adc:
                    if max(opposing_sipm_adc[HCal_ID])>200 and max(this_sipm_adc[HCal_ID])>200 and max(opposing_sipm_adc[HCal_ID])<1000 and max(this_sipm_adc[HCal_ID])<1000:
                        # print(max(opposing_sipm_adc[HCal_ID]), max(this_sipm_adc[HCal_ID]))
                        for i in range(h.size()):
                            # print(pedestals)
                            hist[HCal_ID].Fill(i,this_sipm_adc[HCal_ID][i]-pedestals[h.id()])
                        hitCount[HCal_ID]+=1



                            # if HCal_ID in opposing_sipm_adc:
                            #     if subtractPedestals: 
                            #         hist[HCal_ID].Fill(i,opposing_sipm_adc[HCal_ID]  ) 
                            #         hist[HCal_ID].Fill(i,h.at(i).adc_t()-pedestals[h.id()]) 
                            #         hitCount[HCal_ID]+=2

                            #     else:   
                            #         hist[HCal_ID].Fill(i,opposing_sipm_adc[HCal_ID]  ) 
                            #         hist[HCal_ID].Fill(i,h.at(i).adc_t()) 
                            #         hitCount[HCal_ID]+=2
                            # else:  
                            #     if subtractPedestals: 
                            #         opposing_sipm_adc[HCal_ID]=h.at(i).adc_t()-pedestals[h.id()]) 
                            #         hitCount[HCal_ID]+=2

                            #     else:   
                            #         opposing_sipm_adc[HCal_ID]=h.at(i).adc_t()) 
                            #         hitCount[HCal_ID]+=2      

                            # print(pedestals[h.id()])
                    # else: opposing_sipm_adc[HCal_ID] = False       
                    # else: pass       
       
        for h in hist:
            try:
                hist[h].Scale(1./hitCount[h])
            except: pass 

         





    elif '3D' == plotVar:  
        #event 10 in gpga0 run 287 works
        countMap = zeros((39,12))
        ADCMap = zeros((39,12))
        event_of_interest=10 #10 works great for 287
        eventN=0
        for event in allData: 
            eventN+=1
            if eventN == event_of_interest or eventN==event_of_interest+10000:
            # if eventN==10009 or eventN==9:
                for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
                    ID=DD.HcalDigiID(h.id())
                    LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
                    if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
                    if LayerBarSide[2]==1: LayerBarSide[0] +=20
                    
                    try: ADCs = [h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())] 
                    except: 
                        ADCs = [0 for i in range(h.size())] 
                        print('pedestal missing for',LayerBarSide,h.id(),hex(h.id()))
                    # if max(ADCs)>1:
                    ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] =max(ADCs)

                    # for i in range(h.size()) :
                    #     countMap[LayerBarSide[0]-1,LayerBarSide[1]] += 1
                    #     try: ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()-pedestals[h.id()]
                    #     except: ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()
                        # print(-pedestals[h.id()])


        # hits=[]                
        hits={}                
        countMap[countMap == 0 ] = 1
        threshold=15
        for i in range(20):
            for j in range(12):
                
                if ADCMap[i,j] >threshold and ADCMap[i+20,j] >threshold:
                    hist.Fill(i+1,j,ADCMap[i,j]/countMap[i,j])
                    # hits.append([str(i+1)+','+str(j),ADCMap[i,j]])
                    hits[str(i+1)+','+str(j)] =ADCMap[i,j]/countMap[i,j]
        print(hits)
        render_event_display(hits)           

    elif 'Hit map' == plotVar:  
        # for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
        if len(fileName)==3: eventDataFormat = "ChipSettingsTestDigis_unpack"
        else:    eventDataFormat = "HcalDigis_protosim"
            # print('aaah agh agh')
            

        ADCMap = zeros((39,12))
        for event in allData: 
            countMap = zeros((39,12))
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                ID=DD.HcalDigiID(h.id())
                LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
                if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
                if LayerBarSide[2]==1: LayerBarSide[0] +=20           
                try: 
                    if eventDataFormat == "ChipSettingsTestDigis_unpack": 
                        ADCs = [h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())] 
                    elif eventDataFormat == "HcalDigis_protosim": 
                        ADCs = [h.at(i).adc_t() for i in range(h.size())]                     
                except:   ADCs = [0 for i in range(h.size())] 
                if max(ADCs) > 100: countMap[LayerBarSide[0]-1,LayerBarSide[1]] =1

            for i in range(20):
                for j in range(12):
                    if countMap[i,j] == 1 and countMap[i+20,j] == 1:
                        hist.Fill(i+1,j,countMap[i,j])




    elif plotVar in ['Sum of pulse height per event','Sum of pulse height per event end0','Sum of pulse height per event end1', 'Sum of pulse height per event (no pedestal)']: 
        if len(fileName)==3: eventDataFormat = "ChipSettingsTestDigis_unpack"
        else:    eventDataFormat = "HcalDigis_protosim"
        if 'end0' in plotVar: endOfInterest=0
        elif 'end1' in plotVar: endOfInterest=1
        else: endOfInterest='both'
        print(endOfInterest)
        for event in allData: 
            
            totalAmplitude=0
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                ID=DD.HcalDigiID(h.id())


                if ID.end()==endOfInterest or endOfInterest=='both':
                # if True:
                    HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                    if plotVar =='Sum of pulse height per event (no pedestal)': 
                        amplitude = max([h.at(i).adc_t() for i in range(h.size())])
                    elif 'Sum of pulse height per event' in plotVar:
                        try: 
                            if eventDataFormat == "ChipSettingsTestDigis_unpack": 
                                amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
                            elif eventDataFormat == "HcalDigis_protosim": 
                                amplitude = max([h.at(i).adc_t() for i in range(h.size())])                      
                        except: amplitude = -10000
                        
                    totalAmplitude += amplitude 

            hist.Fill(totalAmplitude)       
        #   
        # if len(fileName)==3: eventDataFormat = "ChipSettingsTestDigis_unpack"
        # else:    eventDataFormat = "HcalDigis_protosim"

        # for event in allData: 
        #     amplitudeMap = zeros((40,12))
        #     for ih,h in enumerate(getattr(event, eventDataFormat)):
        #         ID=DD.HcalDigiID(h.id())
        #         LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
        #         if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
        #         if LayerBarSide[2]==1: LayerBarSide[0] +=20
        #         # HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
        #         # amplitude = max([h.at(i).adc_t() for i in range(h.size())])
        #         try: 
        #             if eventDataFormat == "ChipSettingsTestDigis_unpack": 
        #                 # amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
        #                 amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
        #                 # if LayerBarSide[0]==1 and LayerBarSide[1] ==4: print(amplitude)

        #             elif eventDataFormat == "HcalDigis_protosim": 
        #                 amplitude = max([h.at(i).adc_t() for i in range(h.size())])                      
        #         except: amplitude =-10000
        #         amplitudeMap[LayerBarSide[0],LayerBarSide[1]] = amplitude
        #     threshold=00
        #     for i in range(1,20):
        #         for j in range(12):
        #             if amplitudeMap[i,j] >threshold and amplitudeMap[i+20,j] >threshold:
        #                 # print('threshold passe')
                        
        #                 try:
        #                     # barID=DD.HcalID(1,i,j).raw()
        #                     barID=i*100+j
        #                     # print(barID)
        #                     hist[barID].Fill( (amplitudeMap[i,j]+amplitudeMap[i+20,j])/2 )
        #                 except: pass#print(barID)

    elif plotVar == 'SiPM hits per event': 
        if len(fileName)==3: eventDataFormat = "ChipSettingsTestDigis_unpack"
        else:    eventDataFormat = "HcalDigis_protosim"

        for event in allData: 
            
            totalHits=0
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                ID=DD.HcalDigiID(h.id())
                HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                try: 
                    if eventDataFormat == "ChipSettingsTestDigis_unpack": 
                        amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
                    elif eventDataFormat == "HcalDigis_protosim": 
                        amplitude = max([h.at(i).adc_t() for i in range(h.size())])                      
                except: amplitude = max([h.at(i).adc_t()-100 for i in range(h.size())])
                if amplitude >100: totalHits += 1 

            hist.Fill(totalHits) 


        # for event in allData: 
        #     totalCount=0
        #     for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
        #         totalCount+=1
        #     hist.Fill(totalCount) 

    if plotVar == 'Pulse height of an individual bar': 
        if len(fileName)==3: eventDataFormat = "ChipSettingsTestDigis_unpack"
        else:    eventDataFormat = "HcalDigis_protosim"

        for event in allData: 
            amplitudeMap = zeros((40,12))
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                ID=DD.HcalDigiID(h.id())
                LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
                if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
                if LayerBarSide[2]==1: LayerBarSide[0] +=20
                # HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                # amplitude = max([h.at(i).adc_t() for i in range(h.size())])
                try: 
                    if eventDataFormat == "ChipSettingsTestDigis_unpack": 
                        # amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
                        amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
                        # if LayerBarSide[0]==1 and LayerBarSide[1] ==4: print(amplitude)

                    elif eventDataFormat == "HcalDigis_protosim": 
                        amplitude = max([h.at(i).adc_t() for i in range(h.size())])                      
                except: amplitude =-10000
                amplitudeMap[LayerBarSide[0],LayerBarSide[1]] = amplitude
            threshold=00
            for i in range(1,20):
                for j in range(12):
                    if amplitudeMap[i,j] >threshold and amplitudeMap[i+20,j] >threshold:
                        # print('threshold passe')
                        
                        try:
                            # barID=DD.HcalID(1,i,j).raw()
                            barID=i*100+j
                            # print(barID)
                            hist[barID].Fill( (amplitudeMap[i,j]+amplitudeMap[i+20,j])/2 )
                        except: pass#print(barID)
            # break            
        
    if plotVar == 'pulse height of each SiPM': 
        if len(fileName)==3: eventDataFormat = "ChipSettingsTestDigis_unpack"
        else:    eventDataFormat = "HcalDigis_protosim"
        for event in allData: 
            amplitudes = {}
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                ID=DD.HcalDigiID(h.id())
                HCal_ID=DD.HcalID(ID.section(),ID.layer(),ID.strip()).raw()
                LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
                if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
                if LayerBarSide[2]==1: LayerBarSide[0] +=20
                try: 
                    if eventDataFormat == "ChipSettingsTestDigis_unpack": 
                        amplitude = max([h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())]) 
                        # if LayerBarSide[0]==1 and LayerBarSide[1] ==4: print(amplitude)

                    elif eventDataFormat == "HcalDigis_protosim": 
                        amplitude = max([h.at(i).adc_t() for i in range(h.size())])                      
                except: amplitude =-10000
                # if HCal_ID in amplitudes:
                #     amplitudes[HCal_ID] += amplitude 
                # else:
                #     amplitudes[HCal_ID] = amplitude    
                amplitudes[HCal_ID] = amplitude    
            for barID in amplitudes:    
                hist[barID].Fill(amplitudes[barID]) 
            # break    

        # amplitudeMap = zeros((39,12))

        # ADCMap = zeros((39,12))
        # event_of_interest=10 #10 works great for 287
        # eventN=0
        # for event in allData: 
        #     eventN+=1
        #     if eventN == event_of_interest or eventN==event_of_interest+10000:
        #     # if eventN==10009 or eventN==9:
        #         for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
        #             ID=DD.HcalDigiID(h.id())
        #             LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
        #             if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
        #             if LayerBarSide[2]==1: LayerBarSide[0] +=20
                    
        #             try: ADCs = [h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())] 
        #             except: 
        #                 ADCs = [0 for i in range(h.size())] 
        #                 print('pedestal missing for',LayerBarSide,h.id(),hex(h.id()))
        #             # if max(ADCs)>1:
        #             ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] =max(ADCs)

                    # for i in range(h.size()) :
                    #     countMap[LayerBarSide[0]-1,LayerBarSide[1]] += 1
                    #     try: ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()-pedestals[h.id()]
                    #     except: ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] += h.at(i).adc_t()
                        # print(-pedestals[h.id()])


        # hits=[]                
        # hits={}                
        # countMap[countMap == 0 ] = 1
        # threshold=50
        # for i in range(20):
        #     for j in range(12):
                
        #         if ADCMap[i,j] >threshold and ADCMap[i+20,j] >threshold:
        #             hist.Fill(i+1,j,ADCMap[i,j]/countMap[i,j])
        #             # hits.append([str(i+1)+','+str(j),ADCMap[i,j]])
        #             hits[str(i+1)+','+str(j)] =ADCMap[i,j]/countMap[i,j]
        # print(hits)
        # render_event_display(hits)

    elif plotVar == 'TB hits for TS bars' or plotVar == 'Distribution of number of hits for TS bars': 
        if len(fileName)==5: eventDataFormat = "testBeamHitsUp_hits"
        else:    eventDataFormat = "trigScintRecHitsUp_protosim"
        eventCount=0
        for event in allData: 
            eventCount+=1
            for ih,h in enumerate(getattr(event, eventDataFormat)):
                # print(dir(h))
                # if h.getEnergy()>0.01:
                # if h.getHitQuality()>0.01:
                if h.getPE() >50:
                    hist.Fill(h.getBarID())
                # print(ih)
                # print(h.getSampAboveThr())
                # if h.getHitQuality() !=0:
                #  print(h.getHitQuality())
                # print(dir(h))
            if eventCount> 4000 and eventDataFormat == "trigScintRecHitsUp_protosim": break   
        # print(eventCount)

    elif plotVar == 'TS above threshold': 
        for event in allData: 
            # for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
            for ih,h in enumerate(getattr(event, "testBeamHitsUp_hits")):
                if h.getSampAboveThr() != 0:
                    hist.Fill(h.getBarID())

    elif plotVar == 'TS above threshold (individual bars)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "testBeamHitsUp_hits")):
                # if h.getSampAboveThr() != 0:
                    # hist[h.getBarID()].Fill(h.getSampAboveThr())     
                    hist[h.getBarID()].Fill(1)     
                # if h.getBarID() not in range(0,13): print (h.getBarID())                    

    elif plotVar == 'TS ADCs (individual bars)': 
        eventCount=0
        for event in allData: 
            for ih,h in enumerate(getattr(event, "decodedQIEUp_unpack")):
                # getChanID
                # print(dir(h))
                if h.getChanID() in range(0,12):#what are the other 4 channels???
                # print(h.getChanID())
                # pass
                # if h.getSampAboveThr() != 0:
                    # hist[h.getBarID()].Fill(h.getSampAboveThr())     
                    # hist[h.getBarID()].Fill(max(h.getADC()))     
                    hist[h.getChanID()].Fill(max(h.getADC()))     

                # if h.getBarID() not in range(0,13): print (h.getBarID())    
            eventCount+=1
        print (eventCount)

    if type(hist) != type({}): return {False:hist}
    return hist    




'''

'getAmplitude', 'getBarID', 'getBeamEfrac', 'getEarlyPedestal', 'getEnergy', 'getHitQuality', 'getID', 'getMinPE', 'getModuleID', 
'getPE', 'getPedestal', 'getPulseWidth', 'getQ', 'getQualityFlag', 'getSampAbovePed', 'getSampAboveThr', 'getStartSample', 'getTime', 
'getXPos', 'getYPos', 'getZPos', 'isNoise', 
'''