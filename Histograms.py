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
    # (('Pulse shape (end0) (pedestal subtraction)','287'),),
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

    # (('Pulses','fpga0_287'),),    
    # (('3D','fpga0_287_1k'),),    
    (('3D','287'),),    



    ]     

# plotGroups = testbeamPlotGroups   
# plotGroups = testbeamPlotGroupsBig   

