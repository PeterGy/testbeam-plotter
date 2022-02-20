from HistogramProperties import *



#One element for each plot. Each plot is a list of pairs, each element in the list being a line on the plot. 
#The pair holds the plotvar, then the file it stems from   

testbeamPlotGroups = [

    # #1.1
    # # (('Distribution of number of hits of each bar',"e-1GeV1k"),), 
    (('Mapped distribution of number of hits of each bar',"e-1GeV1k"),),
    #1.2
    # (('Distribution of pulse height of each bar',"e-1GeV1k"),), #192
    
    #1.3
    (('Sum of pulse height per run',"runs"),),
    (('Sum of pulse height per event',"runs"),),    
    (('Total number of hits per event',"runs"),),
    (('Total number of hits per run',"runs"),),    
    #1.4
    (('Distribution of number of hits for TS bars',"e-1GeV1k"),), 
    (('Distribution of signal amplitude for TS bars',"e-1GeV1k"),), 
    (('Distribution of signal amplitude for TS bars (individual bars)',"e-1GeV1k"),), #12
    #1.5
    (('Time difference between TS and HCal',"e-1GeV1k"),), 
    #2.1
    (('Reconstructed energy for tags',"e-1GeV10k"),), 
    #2.2
    (('Reconstructed energy for tags',"pi-1GeV10k"),), 
    #2.3
    (('Energy as a function of the incoming particle angle',"e-1GeV5k0deg"),),
    (('energy response vs. angle',"e-1GeV5k0deg"),('energy response vs. angle',"e-1GeV5k10deg"),('energy response vs. angle',"e-1GeV5k20deg"),('energy response vs. angle',"e-1GeV5k30deg"),('energy response vs. angle',"e-1GeV5k40deg"),),
    (('energy response vs. position',"e-1GeV1k"),('energy response vs. position',"e-1GeV1k100xpos"),('energy response vs. position',"e-1GeV1k200xpos"),('energy response vs. position',"e-1GeV1k300xpos"),('energy response vs. position',"e-1GeV1k400xpos"),),
    #3.1
    # (('Distribution of PEs per HCal bar',"mu-4GeV1k"),), #192
    (('Mapped Distribution of PEs per HCal bar',"mu-4GeV1k"),),
    (('Mapped Distribution of average PEs',"mu-4GeV1k"),),

    # 3.2
    (('TS plots with muons (hit efficiency)',"mu-4GeV1k"),), #1
    (('TS plots with muons (light yield)',"mu-4GeV1k"),), #12
    (('TS plots with muons (pulse shape)',"mu-4GeV1k"),), #12
    #5
    # (('energy response vs. energy',"pi-8GeV1k"),), #1
    # (('energy response vs. energy',"pi-4GeV1k"),), #1
    # (('energy response vs. energy',"pi-2GeV1k"),), #1
    # (('energy response vs. energy',"pi-1GeV1k"),), #1
    # (('energy response vs. energy',"pi-0.5GeV1k"),), #1
    # (('energy response vs. energy',"e-8GeV1k"),), #1
    # (('energy response vs. energy',"e-4GeV1k"),), #1
    # (('energy response vs. energy',"e-2GeV1k"),), #1
    # (('energy response vs. energy',"e-1GeV1k"),), #1
    # (('energy response vs. energy',"e-0.5GeV1k"),), #1
    (('energy response vs. energy',"pi-8GeV1k"),('energy response vs. energy',"pi-4GeV1k"),('energy response vs. energy',"pi-2GeV1k"),('energy response vs. energy',"pi-1GeV1k"),('energy response vs. energy',"pi-0.5GeV1k"),), #1
    (('energy response vs. energy',"e-8GeV1k"),('energy response vs. energy',"e-4GeV1k"),('energy response vs. energy',"e-2GeV1k"),('energy response vs. energy',"e-1GeV1k"),('energy response vs. energy',"e-0.5GeV1k"),), #1
    #6
    (('energy response vs. energy',"pi-0.5GeV1k"),('energy response vs. energy',"pi-0.4GeV1k"),('energy response vs. energy',"pi-0.3GeV1k"),('energy response vs. energy',"pi-0.2GeV1k"),('energy response vs. energy',"pi-0.1GeV1k"),), #1
    (('energy response vs. energy',"e-0.5GeV1k"),('energy response vs. energy',"e-0.4GeV1k"),('energy response vs. energy',"e-0.3GeV1k"),('energy response vs. energy',"e-0.2GeV1k"),('energy response vs. energy',"e-0.1GeV1k"),), #1
    
    

    
]

testbeamPlotGroupsBig = [


    #2.1
    (('Reconstructed energy for tags',"e-1GeV100k00deg"),), 
    (('Reconstructed energy for tags',"e-2GeV100k00deg"),), 
    #2.2
    (('Reconstructed energy for tags',"pi-1GeV100k00deg"),), 
    (('Reconstructed energy for tags',"pi-2GeV100k00deg"),), 
    #2.3
    (('Energy as a function of the incoming particle angle',"e-1GeV100k00deg"),),
    (('energy response vs. angle',"e-1GeV100k00deg"),('energy response vs. angle',"e-1GeV100k10deg"),('energy response vs. angle',"e-1GeV100k20deg"),('energy response vs. angle',"e-1GeV100k30deg"),('energy response vs. angle',"e-1GeV100k40deg"),),
    (('energy response vs. position',"e-1GeV1k"),('energy response vs. position',"e-1GeV1k100xpos"),('energy response vs. position',"e-1GeV1k200xpos"),('energy response vs. position',"e-1GeV1k300xpos"),('energy response vs. position',"e-1GeV1k400xpos"),),
    #3.1
    # (('Distribution of PEs per HCal bar',"mu-4GeV1k"),), #192
    (('Mapped Distribution of PEs per HCal bar',"mu-4GeV1k"),),
    (('Mapped Distribution of average PEs',"mu-4GeV1k"),),

    # 3.2
    (('TS plots with muons (hit efficiency)',"mu-4GeV1k"),), #1
    (('TS plots with muons (light yield)',"mu-4GeV1k"),), #12
    (('TS plots with muons (pulse shape)',"mu-4GeV1k"),), #12
    #5
    # (('energy response vs. energy',"pi-8GeV1k"),), #1
    # (('energy response vs. energy',"pi-4GeV1k"),), #1
    # (('energy response vs. energy',"pi-2GeV1k"),), #1
    # (('energy response vs. energy',"pi-1GeV1k"),), #1
    # (('energy response vs. energy',"pi-0.5GeV1k"),), #1
    # (('energy response vs. energy',"e-8GeV1k"),), #1
    # (('energy response vs. energy',"e-4GeV1k"),), #1
    # (('energy response vs. energy',"e-2GeV1k"),), #1
    # (('energy response vs. energy',"e-1GeV1k"),), #1
    # (('energy response vs. energy',"e-0.5GeV1k"),), #1
    (('energy response vs. energy',"pi-8GeV1k"),('energy response vs. energy',"pi-4GeV1k"),('energy response vs. energy',"pi-2GeV1k"),('energy response vs. energy',"pi-1GeV1k"),('energy response vs. energy',"pi-0.5GeV1k"),), #1
    (('energy response vs. energy',"e-8GeV1k"),('energy response vs. energy',"e-4GeV1k"),('energy response vs. energy',"e-2GeV1k"),('energy response vs. energy',"e-1GeV1k"),('energy response vs. energy',"e-0.5GeV1k"),), #1
    #6
    (('energy response vs. energy',"pi-0.5GeV1k"),('energy response vs. energy',"pi-0.4GeV1k"),('energy response vs. energy',"pi-0.3GeV1k"),('energy response vs. energy',"pi-0.2GeV1k"),('energy response vs. energy',"pi-0.1GeV1k"),), #1
    (('energy response vs. energy',"e-0.5GeV1k"),('energy response vs. energy',"e-0.4GeV1k"),('energy response vs. energy',"e-0.3GeV1k"),('energy response vs. energy',"e-0.2GeV1k"),('energy response vs. energy',"e-0.1GeV1k"),), #1
    
    

    
]


plotGroups = [
    (('Reconstructed energy for tags',"e-1GeV10k"),), 
    (('Reconstructed energy for tags',"pi-1GeV10k"),), 
    # (('Distribution of PEs per HCal bar',"mu-4GeV1k"),), #192
    

       ]     

plotGroups = testbeamPlotGroups   

