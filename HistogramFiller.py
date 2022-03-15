#processName is actually protosim on aurora
from HistogramProperties import *
from numpy import *
import platform 

def fillHist(hist, plotVar, allData, processName="protosim" , minEDeposit=0, maxEDeposit=float('inf'), barID=False, angle=0, beamEnergy=0): 
    
    # type(hists) != type({})
    # print('hmmmm',type(hists) != type({}))
    # print('hist type',type(hist))
    energyErrorCorrection = 0.5 #they did an oopsie in the coding and now I got to correct for it
    allowNoise= False
    if   plotVar == 'simX': 
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

    elif plotVar == 'recEventBar': 
        for event in allData: 
            bars={}
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist.Fill(h.getID())
                #402654211:402668549

    elif plotVar == 'recBarEvent': #redo with autobinning
        layers={}
        bars={}
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                try: bars[h.getID()]+=1
                except: bars[h.getID()]=1
        barOrder=[]                               
        for bar in bars:
            barOrder.append(bar)
        barOrder.sort()      
        hist = r.TH1F(plotVar,"Event counts in each bar", len(bars) ,0,len(bars)) 
        for i in range(len(barOrder)):
            hist.Fill(i,bars[barOrder[i]])

        hist.SetYTitle('counts')
        hist.SetXTitle('bar ranking in bar ID')

    # elif plotVar == 'recE': 
    #     for event in allData: 
    #         for ih,h in enumerate(getattr(event, "HcalDigis_"+processName)):
    #             print(h.id(),h.isADC(),h.size(),h.soi(),)        

    #             'at', 'id', 'isADC', 'isTOT', 'size', 'soi', 'tot' 

    elif plotVar == 'recE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: 
                    hist.Fill(h.getEnergy()*energyErrorCorrection) 

                
  
    elif plotVar == 'recENoisy': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                    hist.Fill(h.getEnergy()*energyErrorCorrection) 
  
    elif plotVar == 'recX': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getXPos()) 
    elif plotVar == 'recY': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getYPos()) 
    elif plotVar == 'recZ': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos()) 




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
    elif plotVar == 'trigSimE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getEdep())             
    elif plotVar == 'trigSimX(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "TriggerPadUpSimHits_"+processName)):
                hist.Fill(h.getPosition()[2],h.getPosition()[0])   
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

    elif plotVar == 'TS plots with muons (light yield)': 
        for event in allData: 
            PEs = {}
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                if h.getBarID() in PEs:
                    PEs[h.getBarID()] += h.getPE()
                else:
                    PEs[h.getBarID()] = h.getPE()    
            for barID in PEs:    
                hists[barID].Fill(PEs[barID])  



#The testbeam functions
    #1.1
    elif plotVar == 'Mapped distribution of number of hits of each bar': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise(): raise("yo this sample has noise")
                LayerBar = barMapLocation(h.getID())
                hist.Fill(LayerBar[0],LayerBar[1])   
    elif plotVar == 'Distribution of number of hits of each bar': 
        for event in allData: 
            hits=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() == barID: 
                    hits+=1
            hist.Fill(hits)              

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
        
    elif plotVar == 'Sum of pulse height per event': 
        for event in allData: 
            totalAmplitude=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalAmplitude+=h.getAmplitude()
            hist.Fill(totalAmplitude) 
        
    elif plotVar == 'Sum of pulse height per run': 
        runs={}
        for event in allData: 
            run=event.EventHeader.getRun()
            if run not in runs: runs[run]=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                runs[run]+=h.getAmplitude()       
        for run in runs:
            hist.Fill(runs[run]) 
            print(runs[run])
        
    #1.4
    elif plotVar == 'Distribution of number of hits for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID())

    elif plotVar == 'Distribution of signal amplitude for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID(),h.getAmplitude())
   
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
                energy+=h.getEnergy()*energyErrorCorrection
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

    #3.1
    elif plotVar == 'Distribution of PEs per HCal bar': 
        for event in allData: 
            PEs = 0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() == barID: 
                    PEs += h.getPE() 
            hist.Fill(PEs)            

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
        

    elif plotVar == 'energy response vs. energy' or plotVar == 'energy response vs. angle' or plotVar == 'energy response vs. position': 
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
 
    return hist   

def fillHists(hists, plotVar, allData, processName="protosim"):     
    # print('hmmmm',type(hists) != type({}))
    energyErrorCorrection = 0.5
    #1.2
    if plotVar == 'Distribution of pulse height of each bar': 
        for event in allData: 
            # amplitude = 0
            amplitudes = {}
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() in amplitudes:
                    amplitudes[h.getID()] += h.getAmplitude()
                else:
                    amplitudes[h.getID()] = h.getAmplitude()    
                # if h.getID() == barID: 
                #     amplitude += h.getAmplitude() 
            for barID in amplitudes:    
                hists[barID].Fill(amplitudes[barID])            
            

        
    #1.4
    elif plotVar == 'Distribution of signal amplitude for TS bars (individual bars)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hists[h.getBarID()].Fill(h.getAmplitude()/1000.)       #WARNING: this makes them go from fC to pC
                if h.getBarID() not in range(0,13): print (h.getBarID())
    

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
                hists[barID].Fill(PEs[barID]) 

    #3.2
    elif plotVar == 'TS plots with muons (light yield)': 
        for event in allData: 
            PEs = {}
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                if h.getBarID() in PEs:
                    PEs[h.getBarID()] += h.getPE()
                else:
                    PEs[h.getBarID()] = h.getPE()    
            for barID in PEs:    
                hists[barID].Fill(PEs[barID])       

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
                hists[barID].Fill(Energies[barID]) 

    elif plotVar == 'recE (individual bars)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hists[h.getID()].Fill(h.getEnergy()*energyErrorCorrection) 

    return hists    