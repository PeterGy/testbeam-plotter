def hcalBinning():
    num_layers=9+10
    layer_thickness=45
    dz=num_layers * layer_thickness
    first_layer_zpos=-dz/2
    absorber_thickness=20
    bar_mounting_plate_thickness=3
    scint_adhesive_thickness=0.5
    scint_thickness=20
    binning=[]
    for i in range(num_layers):    
        binning.append(i*layer_thickness + first_layer_zpos + absorber_thickness + bar_mounting_plate_thickness + scint_adhesive_thickness )
        binning.append(i*layer_thickness + first_layer_zpos + absorber_thickness + bar_mounting_plate_thickness + scint_adhesive_thickness + scint_thickness +0.0001)
    return binning

def hcalBarIDs():
    barIDs=[]
    startID=402654208
    for layer in range(0,19):
        if layer <=8:
            for bar in range(0,8):
                barIDs.append(startID + layer*1024 + bar)
        else:    
            for bar in range(0,12):
                barIDs.append(startID + layer*1024 + bar)
    return barIDs  

def trigScintBarIDs():
    return range(0,12) 

def barName(id):
    if id is False: return ''#"Machine"
    if id <20: return "bar"+str(id) #it means it is TS
    shortID = id-402654208
    layer = int(shortID/1024)
    bar = shortID%1024
    return "layer"+str(layer)+"_bar"+str(bar)    

def barNamePretty(id):
    if id is False: return ''
    if id <20: return "bar "+str(id) #it means it is TS
    shortID = id-402654208
    layer = int(shortID/1024)
    bar = shortID%1024
    return "layer "+str(layer)+" bar "+str(bar)    

barBinsX = range(-1000,1001,50)
barBinsY = range(-1000,1001,50)
barBinsZ = hcalBinning()

plotDict = {
    'Total number of hits per event'   :{'xaxis' : 'Hits', 'yaxis' : 'Event count', 'binning' : {'nBins':1000, 'min':0, 'max':0}, 'dimension' : 1 }, #0,0 min-max makes the xrange automatic. nbins must be 10 so my program can manually set nbins to be the value it should really be automatically
    'Total number of hits per run'   :{'xaxis' : 'Hits', 'yaxis' : 'Run count', 'binning' : {'nBins':1000, 'min':0, 'max':0}, 'dimension' : 1 }, #0,0 min-max makes the xrange automatic. nbins must be 10 so my program can manually set nbins to be the value it should really be automatically
    'Sum of pulse height per event' :{'xaxis' : 'Pulse height [mV]', 'yaxis' : 'Event count', 'binning' : {'nBins':1000, 'min':0, 'max':0}, 'dimension' : 1 },
    'Sum of pulse height per run' :{'xaxis' : 'Pulse height [mV]', 'yaxis' : 'Run count', 'binning' : {'nBins':1000, 'min':0, 'max':0}, 'dimension' : 1 },


    'simE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
    'simEH1' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
    'simEH2' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':10}, 'dimension' : 1 },
    'simEBar' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
    'recEBar' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40}, 'dimension' : 1 },
    'simX' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'simY' :{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    # 'simZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},
    'simZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : barBinsZ, 'dimension' : 1},
    
    # 'recEventBar':{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':402654210, 'max':402668549}, 'dimension' : 1},
    'recEventBar':{'xaxis' : 'Bar ID', 'yaxis' : 'Counts', 'binning' : {'nBins':402672650-402656200, 'min':402656200, 'max':402672650}, 'dimension' : 1},
    
    'recBarEvent':{'xaxis' : 'Bar number', 'yaxis' : 'Counts', 'binning' : {'nBins':19, 'min':-0.5, 'max':18.5}, 'dimension' : 1},



    'recE' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
    'recENoisy' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
    'recPE' :{'xaxis' : 'Number of Photo-electrons', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},
    'recX' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'recY' :{'xaxis' : 'Y Displacement [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':200, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'recZ' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':90, 'min':-450, 'max':450}, 'dimension' : 1},        
    'recAmp' :{'xaxis' : 'Amplitude [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':140, 'min':0, 'max':14}, 'dimension' : 1},        
    
    
    
    # 'simX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,   
    #                 'binningX' : barBinsZ,                         
    #                 'binningY' : barBinsX},                         
    # 'simY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsZ, 
    #                 'binningY' : barBinsY},        
    # 'simY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsX, 
    #                 'binningY' : barBinsY},
    'simE(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                    'binningX' : {'nBins':2000, 'min':-1000, 'max':1000},  
                    'binningY' : {'nBins':200, 'min':0, 'max':0.1}}, 
    'simE(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                    'binningY' : {'nBins':200, 'min':0, 'max':10}},                                
                    


    # 'recX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,   
    #                 'binningX' : barBinsZ,                         
    #                 'binningY' : barBinsX},                         
    # 'recY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsZ, 
    #                 'binningY' : barBinsY},        
    # 'recY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
    #                 'binningX' : barBinsX, 
    #                 'binningY' : barBinsY},

    'simX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'simY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'simY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':40, 'min':-1000, 'max':1000}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},

    'recX(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'recY(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},
    'recY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':40, 'min':-1000, 'max':1000}, 
                    'binningY' : {'nBins':40, 'min':-1000, 'max':1000}},

    'recE(Z)' :{'xaxis' : 'Penetration depth Z [mm]', 'yaxis' : 'Energy [MeV]', 'dimension' : 2,
                    'binningX' : {'nBins':1000, 'min':-500, 'max':500},  
                    'binningY' : {'nBins':200, 'min':0, 'max':10}},    

    'trigSimX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':80, 'min':-40, 'max':40}, 'dimension' : 1},
    'trigRecX' :{'xaxis' : 'Distance [mm]', 'yaxis' : 'Counts', 'binning' : {'nBins':80, 'min':-1000, 'max':1000}, 'dimension' : 1},
    'trigRecT' :{'xaxis' : 'Time [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':20, 'min':0, 'max':10}, 'dimension' : 1}, #machine has a resolution of 0.5 ns apparently
    'trigSimE'   :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':1}, 'dimension' : 1 },
    
    'trigSimX(Z)' :{'xaxis' : 'Penetration depth [mm]', 'yaxis' : 'X Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':200, 'min':-20, 'max':20}, 
                    # 'binningY' : {'nBins':200, 'min':-20, 'max':20}},    
                    # 'binningX' : {'nBins':100, 'min':-400, 'max':900}, 
                    'binningY' : {'nBins':200, 'min':-20, 'max':20}},                         
    'trigSimY(Z)' :{'xaxis' : 'Penetration depth [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':200, 'min':-20, 'max':20}, 
                    'binningY' : {'nBins':200, 'min':-20, 'max':20}},         
    'trigSimY(X)' :{'xaxis' : 'X Displacement [mm]', 'yaxis' : 'Y Displacement [mm]', 'dimension' : 2,
                    'binningX' : {'nBins':200, 'min':-20, 'max':20}, 
                    'binningY' : {'nBins':200, 'min':-20, 'max':20}},  

    'Distribution of number of hits for TS bars':{'xaxis' : 'Bar ID', 'yaxis' : 'Counts', 'binning' : {'nBins':12, 'min':-0.5, 'max':11.5}, 'dimension' : 1,},
    'Distribution of signal amplitude for TS bars':{'xaxis' : 'Bar ID', 'yaxis' : 'Signal Amplitude [nC]', 'binning' : {'nBins':12, 'min':-0.5, 'max':11.5}, 'dimension' : 1,},
    'Distribution of signal amplitude for TS bars (individual bars)':{'xaxis' : 'Amplitude [nC]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40000}, 'dimension' : 1, 'bars' : trigScintBarIDs()},
    'Time difference between TS and HCal':{'xaxis' : 'Time difference [ns]', 'yaxis' : 'Counts', 'binning' : {'nBins':50, 'min':0, 'max':50}, 'dimension' : 1},
    'barTest' :{'xaxis' : 'Energy [MeV]', 'yaxis' : 'Counts', 'binning' : {'nBins':40, 'min':0, 'max':40} , 'dimension' : 1},


    'Distribution of number of hits of each bar':{'xaxis' : 'Hit count', 'yaxis' : 'Number of events', 'binning' : {'nBins':2, 'min':0, 'max':2}, 'dimension' : 1},
    'Distribution of pulse height of each bar':{'xaxis' : 'Amplitude [mV]', 'yaxis' : 'Number of events', 'binning' : {'nBins':100, 'min':0, 'max':0}, 'dimension' : 1, 'bars' : hcalBarIDs()},

    'Mapped distribution of number of hits of each bar':{'xaxis' : 'Layer number', 'yaxis' : 'Bar number', 'dimension' : 2,
                    'binningX' : {'nBins':19, 'min':-0.5, 'max':18.5}, 
                    'binningY' : {'nBins':12, 'min':-0.5, 'max':11.5}}, 
    #2
    'Reconstructed energy for tags':{'xaxis' : 'Detector response [#frac{GeV}{GeV}]', 'yaxis' : 'Number of events', 'binning' : {'nBins':60, 'min':0, 'max':0.3}, 'dimension' : 1},                
    'Energy as a function of the incoming particle angle':{'xaxis' : 'Angle [deg]', 'yaxis' : 'Energy deposited [MeV]', 'binning' : {'nBins':50, 'min':0, 'max':50}, 'dimension' : 1},
    #3
    'Distribution of PEs per HCal bar':{'xaxis' : 'PE count', 'yaxis' : 'Number of events', 'binning' : {'nBins':100, 'min':0, 'max':0}, 'dimension' : 1, 'bars' : hcalBarIDs()},
    'Mapped Distribution of PEs per HCal bar':{'xaxis' : 'Layer number', 'yaxis' : 'Bar number', 'dimension' : 2,
                    'binningX' : {'nBins':19, 'min':-0.5, 'max':18.5}, 
                    'binningY' : {'nBins':12, 'min':-0.5, 'max':11.5}}, 
    'Mapped Distribution of average PEs':{'xaxis' : 'Layer number', 'yaxis' : 'Bar number', 'dimension' : 2,
                    'binningX' : {'nBins':19, 'min':-0.5, 'max':18.5}, 
                    'binningY' : {'nBins':12, 'min':-0.5, 'max':11.5}}, 
    'TS plots with muons (hit efficiency) (1 plot per bar)':{'xaxis' : 'Hits per event', 'yaxis' : 'Number of events', 'binning' : {'nBins':1000, 'min':0, 'max':0}, 'dimension' : 1, 'bars' : trigScintBarIDs()},
    'TS plots with muons (hit efficiency)':{'xaxis' : 'Bar', 'yaxis' : 'Hits', 'binning' : {'nBins':12, 'min':-0.5, 'max':11.5}, 'dimension' : 1,},
    'TS plots with muons (light yield)':{'xaxis' : 'PE count', 'yaxis' : 'Number of events', 'binning' : {'nBins':50, 'min':50, 'max':100}, 'dimension' : 1, 'bars' : trigScintBarIDs()},
    'TS plots with muons (pulse shape)':{'xaxis' : 'Time [ns]', 'yaxis' : 'Amplitude [mV]', 'binning' : {'nBins':100, 'min':2, 'max':3}, 'dimension' : 1, 'bars' : trigScintBarIDs()}, #can be autobinned badly
    'energy response vs. energy'  :{'xaxis' : 'Detector response [#frac{GeV}{GeV}]', 'yaxis' : 'Number of events', 'binning' : {'nBins':60, 'min':0, 'max':0.6}, 'dimension' : 1},
    'energy response vs. angle'   :{'xaxis' : 'Detector response [#frac{GeV}{GeV}]', 'yaxis' : 'Number of events', 'binning' : {'nBins':60, 'min':0, 'max':0.6}, 'dimension' : 1},
    'energy response vs. position':{'xaxis' : 'Detector response [#frac{GeV}{GeV}]', 'yaxis' : 'Number of events', 'binning' : {'nBins':60, 'min':0, 'max':0.6}, 'dimension' : 1},
    'rec vs sim':{'xaxis' : 'Detector response [GeV/GeV]', 'yaxis' : 'Number of events', 'binning' : {'nBins':110, 'min':0, 'max':1.1}, 'dimension' : 1},
    }    