from HistogramProperties import *

#One element for each plot. Each plot is a list of pairs, each element in the list being a line on the plot. 
#The pair holds the plotvar, then the file it stems from   
testbeamPlotGroups = [
    # #1.1
    # # (('Distribution of number of hits of each bar','e-1GeV1k'),), 
    (('Mapped distribution of number of hits of each bar','e-1GeV1k'),),
    #1.2
    (('Distribution of pulse height of each bar','e-1GeV1k'),), #192
    
    #1.3
    (('Sum of pulse height per run','e-1GeV1k'),),
    (('Sum of pulse height per event','e-1GeV1k'),),    
    (('Total number of hits per event','e-1GeV1k'),),
    (('Total number of hits per run','e-1GeV1k'),),    
    #1.4
    (('Distribution of number of hits for TS bars','e-1GeV1k'),), 
    # # # #(('Distribution of signal amplitude for TS bars','e-1GeV1k'),), #useless
    (('Distribution of signal amplitude for TS bars (individual bars)','e-1GeV1k'),), #12
    #1.5
    (('Time difference between TS and HCal','e-1GeV1k'),), 
    #2.1
    (('Reconstructed energy for tags','e-1GeV1k'),), 
    #2.3
    # (('Energy as a function of the incoming particle angle','e-1GeV5k0deg'),),
    (('energy response vs. angle','e-1GeV5k0deg'),('energy response vs. angle','e-1GeV5k10deg'),('energy response vs. angle','e-1GeV5k20deg'),('energy response vs. angle','e-1GeV5k30deg'),('energy response vs. angle','e-1GeV5k40deg'),),
    (('energy response vs. position','e-1GeV1k'),('energy response vs. position','e-1GeV1k100xpos'),('energy response vs. position','e-1GeV1k200xpos'),('energy response vs. position','e-1GeV1k300xpos'),('energy response vs. position','e-1GeV1k400xpos'),),
    #3.1
    (('Distribution of PEs per HCal bar','mu-4GeV1k'),), #192
    (('Mapped Distribution of PEs per HCal bar','mu-4GeV1k'),),
    (('Mapped Distribution of average PEs','mu-4GeV1k'),),

    # 3.2
    # (('TS plots with muons (hit efficiency)','mu-4GeV1k'),), #1
    (('TS plots with muons (light yield)','mu-4GeV1k'),), #12
    # (('TS plots with muons (pulse shape)','mu-4GeV1k'),), #12
    #5
    (('energy response vs. energy','pi-8GeV1k'),('energy response vs. energy','pi-4GeV1k'),('energy response vs. energy','pi-2GeV1k'),('energy response vs. energy','pi-1GeV1k'),('energy response vs. energy','pi-0.5GeV1k'),), #1
    (('energy response vs. energy','e-8GeV1k'),('energy response vs. energy','e-4GeV1k'),('energy response vs. energy','e-2GeV1k'),('energy response vs. energy','e-1GeV1k'),('energy response vs. energy','e-0.5GeV1k'),), #1
    #6
    (('energy response vs. energy','pi-0.5GeV2k'),('energy response vs. energy','pi-0.4GeV2k'),('energy response vs. energy','pi-0.3GeV2k'),('energy response vs. energy','pi-0.2GeV2k'),('energy response vs. energy','pi-0.1GeV2k'),), #1
    (('energy response vs. energy','e-0.5GeV2k'),('energy response vs. energy','e-0.4GeV2k'),('energy response vs. energy','e-0.3GeV2k'),('energy response vs. energy','e-0.2GeV2k'),('energy response vs. energy','e-0.1GeV2k'),), #1
]

testbeamPlotGroupsBig = [
    #1.1
    # (('Distribution of number of hits of each bar','e-1GeV1k'),), 
    (('Mapped distribution of number of hits of each bar','e-1GeV100k00deg'),),
    #1.2
    (('Distribution of pulse height of each bar','e-1GeV100k00deg'),), #192
    #1.3
    (('Sum of pulse height per run','e-1GeV100k00deg'),),
    (('Sum of pulse height per event','e-1GeV100k00deg'),),    
    (('Total number of hits per event','e-1GeV100k00deg'),),
    (('Total number of hits per run','e-1GeV100k00deg'),),   
    #1.4
    (('Distribution of number of hits for TS bars','e-1GeV100k00deg'),), 
    # # # # (('Distribution of signal amplitude for TS bars','e-1GeV100k00deg'),),  #this one isunneeded
    (('Distribution of signal amplitude for TS bars (individual bars)','e-1GeV100k00deg'),), #12 
    #2.1
    (('Reconstructed energy for tags','e-1GeV100k00deg'),), 
    (('Reconstructed energy for tags','e-2GeV100k00deg'),), 
    #2.2
    (('Reconstructed energy for tags','pi-1GeV100k00deg'),), 
    (('Reconstructed energy for tags','pi-2GeV100k00deg'),), 
    # #2.3
    (('energy response vs. angle','e-1GeV100k00deg'),('energy response vs. angle','e-1GeV100k10deg'),('energy response vs. angle','e-1GeV100k20deg'),('energy response vs. angle','e-1GeV100k30deg'),('energy response vs. angle','e-1GeV100k40deg'),),
    #3.1
    # (('Distribution of PEs per HCal bar','mu-4GeV200k00deg'),), #192
    # (('Mapped Distribution of PEs per HCal bar','mu-4GeV200k00deg'),),
    # (('Mapped Distribution of average PEs','mu-4GeV200k00deg'),),

    # 3.2
    # #####(('TS plots with muons (hit efficiency)','mu-4GeV200k00deg'),), #1
    (('TS plots with muons (light yield)','mu-4GeV200k00deg'),),
    # #####(('TS plots with muons (pulse shape)','mu-4GeV200k00deg'),), #12
    #5
    (('energy response vs. energy','pi-8GeV100k00deg'),('energy response vs. energy','pi-4GeV100k00deg'),('energy response vs. energy','pi-2GeV100k00deg'),('energy response vs. energy','pi-1GeV100k00deg'),('energy response vs. energy','pi-0.5GeV100k00deg'),), #1
    (('energy response vs. energy','e-8GeV100k00deg'), ('energy response vs. energy','e-4GeV100k00deg'), ('energy response vs. energy','e-2GeV100k00deg'), ('energy response vs. energy','e-1GeV100k00deg'), ('energy response vs. energy','e-0.5GeV100k00deg'),), #1
    #6
    # (('energy response vs. energy','pi-0.5GeV2k'),('energy response vs. energy','pi-0.4GeV2k'),('energy response vs. energy','pi-0.3GeV2k'),('energy response vs. energy','pi-0.2GeV2k'),('energy response vs. energy','pi-0.1GeV2k'),), #1
    # (('energy response vs. energy','e-0.5GeV2k'),('energy response vs. energy','e-0.4GeV2k'),('energy response vs. energy','e-0.3GeV2k'),('energy response vs. energy','e-0.2GeV2k'),('energy response vs. energy','e-0.1GeV2k'),), #1
]


plotGroups = [
    # (('total energy deposited FPGA0','mu-4GeV1k'),('total energy deposited FPGA0','fpga0_287'),),
    # (('Mapped distribution of number of hits of each bar','fpga0_287'),),
    # (('Mapped ADC average','fpga0_287'),),    
 
    # (('Mapped ADC average','mu-4GeV1k'),),
    # (('Mapped distribution of number of hits of each bar','mu-4GeV1k'),),
    # (('Mapped Distribution of average PEs','fpga0_287'),),
    # (('Mapped SiPM hits','fpga0_287'),),
    # (('Distribution of pulse height of each bar','fpga0_287'),),
    # (('Mapped distribution of number of hits of each bar','mu-4GeV1k'),),
    # (('Mapped Distribution of average PEs','mu-4GeV1k'),),
    # (('Mapped distribution of number of hits of each bar','mu-4GeV1k'),),

    # (('total energy deposited FPGA0 horizontal bars','fpga0_235'),
    # ('total energy deposited FPGA0 horizontal bars','fpga0_243'),
    # ('total energy deposited FPGA0 horizontal bars','fpga0_241'),    ),
        



    # (('Pulse shape (end0) (pedestal subtraction)','fpga0_287_1k'),),
    # (('Pulse shape (end0) (pedestal subtraction)','fpga0_287'),),
    # (('Pulse shape (end1) (pedestal subtraction)','fpga0_287'),),
    # (('Pulse shape (end1) (pedestal subtraction)','287'),),

    # (('Pulse shape (end0) (no pedestal subtraction)','fpga0_235'),('Pulse shape (end0) (no pedestal subtraction)','fpga0_243'),('Pulse shape (end0) (no pedestal subtraction)','fpga0_241'),),    
    # (
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_287'),
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_235'),
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_243'),
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_241'),
    # ),    
    # (
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_287'),
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_235'),
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_243'),
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_241'),
    # ),    
    # (

    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_243'),

    # ),
    # (
    # ('Pulse shape (end1) (no pedestal subtraction)','fpga0_225'),
    # ('Pulse shape (end1) (no pedestal subtraction)','fpga0_226'),
    # ('Pulse shape (end1) (no pedestal subtraction)','fpga0_227'),
    # ('Pulse shape (end1) (no pedestal subtraction)','fpga0_228'),
    # ('Pulse shape (end1) (no pedestal subtraction)','fpga0_229'),
    # ),    
    # (
    # ('Pulse shape (end0) (no pedestal subtraction)','fpga0_287_1k'),
    # ('Pulse shape (end0) (pedestal subtraction)','fpga0_287_1k'),
    # )

    # (
    # ('Pulse shape (end1) (pedestal subtraction)','fpga0_287'),
    # ('Pulse shape (end0) (pedestal subtraction)','fpga0_287'),
    # ('Pulse shape (end1) (no pedestal subtraction)','fpga0_287'),
    # ('Pulse shape (end0) (no pedestal subtraction)','fpga0_287'),
    # )


    # (('Mapped ADC average','225'),),    
    # (('Mapped ADC average','226'),),   

    # same phase comparison
    # (
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_279'),
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_235'),
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_243'),
    #     ('Pulse shape (end0) (pedestal subtraction)','fpga0_241'),
    # ),   
    # (
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_279'),
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_235'),
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_243'),
    #     ('Pulse shape (end1) (pedestal subtraction)','fpga0_241'),
    # ),  
    # (('Mapped ADC average','fpga0_279'),),    
    # (('Mapped ADC average','287'),),    
    # (('Pulses','287'),),    

    # (('Pulses','fpga0_287'),),    
    # (('Pulses','288'),),    
    # (('3D','fpga0_287_1k'),),    
    # (('3D','287'),),  
    # (('Mapped ADC average','287'),),   
    #   
    # (('Hit map','288'),),    
    # (('Hit map','287'),),    
     

    # (('3D','225'),),    
    # (('3D','288'),),    

    # (('Hit map','226'),),   
    # (('Hit map','e-1GeV1k'),),   
    # (('Hit map','e-1GeV10k000xpos'),),   
    # (('Hit map','e-1GeV10k40smear'),),   
    # (('Hit map','e-1GeV10k80smear'),),   
    # (('Hit map','e-1GeV10k100smear'),),   
    # (('Hit map','e-1GeV10k120smear'),),   
    # (('Hit map','e-1GeV10k150smear'),),   
    # (('Hit map','e-1GeV10k200smear'),),   

    # (('Hit map','226'),),   
    # (('Hit map','e-1GeV10k120smear'),),   
    # (('Distribution of pulse height of each bar','e-1GeV10k120smear'),), #192

    # (('Pulse height of an individual bar','e-1GeV10k120smear'),),    
    # (('Pulse height of an individual bar','226'),),
    # (('Pulse height of an individual bar','e-1GeV10k120smear'),('Pulse height of an individual bar','226'),),
    # (('pulse height of each SiPM','226'),('pulse height of each SiPM','e-1GeV10k120smear'),),
    # (('Pulse height of an individual bar','226'),),
    # (('Pulse height of an individual bar','e-1GeV0k'),),
    # (('Sum of pulse height per event','e-1GeV10k120smear'),),    
    # (('Sum of pulse height per event','226'),('Sum of pulse height per event','e-1GeV10k120smear'),),    
    # (('Sum of pulse height per event end0','226'),('Sum of pulse height per event end0','e-1GeV10k120smear'),),    
    # (('Sum of pulse height per event end1','226'),('Sum of pulse height per event end1','e-1GeV10k120smear'),),    
    # (('Sum of pulse height per event','226'),('Sum of pulse height per event','e-1GeV10k120smear'),),    



    # (('Pulse height of an individual bar','e-1GeV10k120smear'),('Pulse height of an individual bar','226'),),



    # (('Sum of pulse height per event','e-1GeV10k120smear'),('Sum of pulse height per event','226'),),    
    # (('Pulse height of an individual bar','e-1GeV10k120smear'),('Pulse height of an individual bar','226'),),


    # (('Sum of pulse height per event (no pedestal)','e-1GeV10k120smear'),('Sum of pulse height per event (no pedestal)','226'),),    
    # (('SiPM hits per event','e-1GeV10k120smear'),('SiPM hits per event','226'),),    
    # (('Pulse height of an individual bar','226'),),   
    
    # (('Pulse height of an individual bar','mu-4GeV10k120smear'),('Pulse height of an individual bar','287'),),
    # (('Pulse height of an individual bar','mu-4GeV1k'),('Pulse height of an individual bar','287'),),

    # (('3D','287'),),  
    # (('TB hits for TS bars','183TS'),),  
    # (('TB hits for TS bars','183TS'),('TB hits for TS bars','e-4GeV56k30smearTSonly'),),  
    # (('Distribution of number of hits for TS bars','183TS'),('Distribution of number of hits for TS bars','e-4GeV56k30smearTSonly'),),  
    # (('Distribution of number of hits for TS bars','e-4GeV5k90smearTSonly'),), 

    # (('TS above threshold','183TS'),),  
    # (('TB hits for TS bars','183TS'),('TB hits for TS bars','e-4GeV500k30smearTSonly'),),  

    # (('TS above threshold (individual bars)','183TS'),),  
    # (('Distribution of signal amplitude for TS bars (individual bars)','183TS'),),        
    # (('TS ADCs (individual bars)','183TS'),),        
    # (('Distribution of signal amplitude for TS bars (individual bars)','183TS'),('Distribution of signal amplitude for TS bars (individual bars)','e-4GeV56k30smearTSonly'),),        
    # (('Distribution of signal amplitude for TS bars (individual bars)','183TS'),('Distribution of signal amplitude for TS bars (individual bars)','e-4GeV5k30smearTSonly'),),        

    # (('Pulse shape (end0) (pedestal subtraction)','287'),),
    # (('Pulses','287'),),    

    # (('Distribution of number of hits for TS ars','e-4GeV56k30smearTSonly'),('Distribution of number of hits for TS bars','183TS'),),  

    # (('Distribution of signal amplitude for TS bars (individual bars)','e-4GeV5k30smearTSonly'),('Distribution of signal amplitude for TS bars (individual bars)','183TS'),),        

    # (('Mapped distribution of number of hits of each bar','e-1GeV1k'),),

    # (('Pulse height of an individual bar','e-1GeV10k120smear'),('Pulse height of an individual bar','226'),),
    # (('Pulse height of an individual bar','mu-4GeV10k120smear'),('Pulse height of an individual bar','287'),),

    # (('energy response vs. position','e-1GeV10k000xpos'),('energy response vs. position','e-1GeV10k100xpos'),('energy response vs. position','e-1GeV10k200xpos'),('energy response vs. position','e-1GeV10k300xpos'),('energy response vs. position','e-1GeV10k400xpos'),),

# (('Sum of pulse height per run','e-1GeV1k'),),

   (('energy response vs. energy','pi-0.5GeV2k'),('energy response vs. energy','pi-0.4GeV2k'),('energy response vs. energy','pi-0.3GeV2k'),('energy response vs. energy','pi-0.2GeV2k'),('energy response vs. energy','pi-0.1GeV2k'),), #1
    (('energy response vs. energy','e-0.5GeV2k'),('energy response vs. energy','e-0.4GeV2k'),('energy response vs. energy','e-0.3GeV2k'),('energy response vs. energy','e-0.2GeV2k'),('energy response vs. energy','e-0.1GeV2k'),), #1


    ]     

# plotGroups = testbeamPlotGroups   
# plotGroups = testbeamPlotGroupsBig   

