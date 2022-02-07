class filledHist: pass

def barMapLocation(id):
    shortID = id-402654208
    layer = int(shortID/1024)
    bar = shortID%1024
    if layer <=8:
        bar+=2
    return [layer,bar]

def autoBin(hist):
    hist.BufferEmpty() #figures out the xrange        
    minX = hist.GetXaxis().GetBinLowEdge(1-1)
    maxX = hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()+1)
    # print(minX,maxX)
    hist.SetBins(int(maxX)+1-int(minX),int(minX),int(maxX)+1) #makes it so there is one bin per event or ns, and the rightmost bin is still included


def fillHist(hist, plotVar, allData, processName="process" , minEDeposit=0, maxEDeposit=float('inf'), barID=False, angle=0, beamEnergy=0):
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

    elif plotVar == 'recE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: 
                    hist.Fill(h.getEnergy()) 
  
    elif plotVar == 'recENoisy': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                    hist.Fill(h.getEnergy()) 
  
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

                    #h.getID() repeats even in rec mode
                    # print("rec id",h.getID()-4026e5)
        print(eventCount)            
    elif plotVar == 'recPE': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.isNoise() == allowNoise: hist.Fill(h.getPE()) 

    #the whole hcal F(x) thing is wrong, be careful
    elif plotVar == 'simX(Z)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                if h.getEdep() > minEDeposit and h.getEdep() < maxEDeposit:
                    hist.Fill(h.getPosition()[2],h.getPosition()[0])
                # hist.Fill(h.getPosition()[2],h.getPosition()[0])
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
                if h.isNoise() == allowNoise: hist.Fill(h.getZPos(),h.getXPos()) 
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
                
    #trig f(x) works               
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


    # elif plotVar == 'trigRecX': 
        # for event in allData: 
            # for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                # print(h.getYPos())
                # hist.Fill(h.getXPos()) 
                # print(h.items()) 

    elif plotVar == 'trigRecT': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                if h.getBarID() ==6: hist.Fill(h.getTime()) 
                # print(h.getBarID())
                # print(h.items()) 






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
    elif plotVar == 'Distribution of pulse height of each bar': 
        for event in allData: 
            amplitude = 0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() == barID: 
                    amplitude += h.getAmplitude() 
            hist.Fill( amplitude)            
        autoBin(hist)    
    #1.3
    elif plotVar == 'Total number of hits per event': 
        for event in allData: 
            totalCount=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalCount+=1
            hist.Fill(totalCount) 
        autoBin(hist)
    elif plotVar == 'Total number of hits per run':
        runs={}
        for event in allData: 
            run=event.EventHeader.getRun()
            if run not in runs: runs[run]=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                runs[run]+=1        
        for run in runs:
            hist.Fill(runs[run]) 
        autoBin(hist)
    elif plotVar == 'Sum of pulse height per event': 
        for event in allData: 
            totalAmplitude=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                totalAmplitude+=h.getAmplitude()
            hist.Fill(totalAmplitude) 
        autoBin(hist)
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
        autoBin(hist)
    #1.4
    elif plotVar == 'Distribution of number of hits for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID())

    elif plotVar == 'Distribution of signal amplitude for TS bars': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                hist.Fill(h.getBarID(),h.getAmplitude())

    elif plotVar == 'Distribution of signal amplitude for TS bars (individual bars)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                    if h.getBarID() == barID: 
                        hist.Fill(h.getAmplitude())               
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
    elif plotVar == 'Reconstructed energy for tags': #might wanna make beam energy automatic
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                energy+=h.getEnergy()
            hist.Fill(energy/beamEnergy) 

    elif plotVar == 'Energy as a function of the incoming particle angle':
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                hist.Fill(angle,h.getEnergy())    

    #3
    elif plotVar == 'Distribution of PEs per HCal bar': 
        for event in allData: 
            PEs = 0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                if h.getID() == barID: 
                    PEs += h.getPE() 
            hist.Fill(PEs)            
        autoBin(hist)


    elif plotVar == 'Mapped Distribution of PEs per HCal bar': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                LayerBar = barMapLocation(h.getID())
                hist.Fill(LayerBar[0],LayerBar[1],h.getPE())            

    elif plotVar == 'TS plots with muons (hit efficiency) (1 plot per bar)': 
        for event in allData: 
            hits=0
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                    if h.getBarID() == barID: 
                        hits+=1
            hist.Fill(hits)  
        autoBin(hist)  

    elif plotVar == 'TS plots with muons (hit efficiency)': 
        eventCount=allData.GetEntries()
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                # print(h.getBarID())
                hist.Fill(h.getBarID(),1/eventCount)  
        # autoBin(hist)
        # print(eventCount)

    elif plotVar == 'TS plots with muons (light yield)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                    if h.getBarID() == barID: 
                        hist.Fill(h.getPE())  
        autoBin(hist)                

    elif plotVar == 'TS plots with muons (pulse shape)': 
        for event in allData: 
            for ih,h in enumerate(getattr(event, "trigScintRecHitsUp_"+processName)):
                    if h.getBarID() == barID: 
                        # hist.Fill(h.getTime())  
                        hist.Fill(h.getTime(),h.getAmplitude())  
                        # if barID == 5: 
                        #     if h.getTime() !=2.5:
                        #         print(h.getTime())
        # autoBin(hist)

    elif plotVar == 'energy response vs. energy': 
        for event in allData: 
            energy=0
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                energy+=h.getEnergy()
            hist.Fill(energy/beamEnergy) 

    elif plotVar == 'rec vs sim':
        recE=0
        simE=0
        for event in allData:             
            for ih,h in enumerate(getattr(event, "HcalRecHits_"+processName)):
                recE+=h.getEnergy()
                hist.Fill(h.getEnergy())
            for ih,h in enumerate(getattr(event, "HcalSimHits_"+processName)):
                simE+=h.getEdep()
                hist.Fill(h.getEdep())  
        print ("Total simulated energy deposit:",simE)          
        print ("Total reconstructed energy deposit:",recE)   


    filledHist.hist = hist
    return filledHist   

       