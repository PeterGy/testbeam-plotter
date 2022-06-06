#3D event display

from numpy import *
import csv
import ROOT as r
import libDetDescr as DD
from HCal3Dmodel import *
r.gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?

csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')

pedestals ={}
for row in csv_reader:
    try:  pedestals[int(row[0],0)] = float(row[1])
    except:pass


run=287 #muon
# run=288 #pion
# run=278 #electron
inFile = r.TFile("reconstructions/"+str(run)+".root","READ")  
allData = inFile.Get("LDMX_Events")
# events_of_interest=[1,2,5,8,9,10,11,12,15,16]
events_of_interest=[10,5,8,9,10,11,12,15,16,17,18,19,20]
events_of_interest=[10]
# events_of_interest=[8,9,10,11,12,15,16,17,18,19,20]
# events_of_interest=[14,1,2,5,8, 9,10,11,12,14,15]
# events_of_interest=[1,2,3,4,5,6,7,8,9,10,11,12]
# events_of_interest=[2,3,4,5,6,7,8,9,10,11,12]
# events_of_interest=[3,4,5,6,7,8,9,10,11,12,13,14]

ten_plot_mode = False
# ten_plot_mode = True


def getHcalHits(event_of_interest):
    ADCMap = zeros((39,12))
    eventN=0
    for event in allData: 
        eventN+=1
        if eventN == event_of_interest or eventN==event_of_interest+10000:
        # if eventN == event_of_interest or eventN==event_of_interest+10000:
            for ih,h in enumerate(getattr(event, "ChipSettingsTestDigis_unpack")):
                ID=DD.HcalDigiID(h.id())
                LayerBarSide = [ID.layer(),ID.strip(),ID.end()] 
                if LayerBarSide[0] < 10: LayerBarSide[1] +=2 #visual offset
                if LayerBarSide[2]==1: LayerBarSide[0] +=20
                
                try: ADCs = [h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())] 
                except: 
                    ADCs = [0 for i in range(h.size())] 
                    # print('pedestal missing for',LayerBarSide,h.id(),hex(h.id()))
                ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] =max(ADCs)               
    hits={}                
    threshold=15
    for i in range(20):
        for j in range(12):
            
            if ADCMap[i,j] >threshold and ADCMap[i+20,j] >threshold:
                hits[str(i+1)+','+str(j)] =ADCMap[i,j]
    return hits

def getTSHits(event_of_interest=3):
    eventN=0
    for event in allData: 
        eventN+=1
        if eventN == event_of_interest:
            for ih,h in enumerate(getattr(event, "testBeamHitsUp_hits")):
                if h.getPE() >50:
                    hist[h.getBarID()].Fill(h.getAmplitude()/1000) 
                
                try: ADCs = [h.at(i).adc_t()-pedestals[h.id()] for i in range(h.size())] 
                except: 
                    ADCs = [0 for i in range(h.size())] 
                    # print('pedestal missing for',LayerBarSide,h.id(),hex(h.id()))
                ADCMap[LayerBarSide[0]-1,LayerBarSide[1]] =max(ADCs)               
    hits={}                
    threshold=15
    for i in range(20):
        for j in range(12):
            
            if ADCMap[i,j] >threshold and ADCMap[i+20,j] >threshold:
                hits[str(i+1)+','+str(j)] =ADCMap[i,j]
    return hits


fig = plt.figure()
# fig.set_size_inches(20, 8)
fig.set_size_inches(8, 8)
fig.tight_layout()
subplots=[]


from Set_of_hits_for_3D_HCal_ED import *
hits_set=[]
for i in range(0,len(events_of_interest)):
    hits_set.append(getHcalHits(events_of_interest[i]))
print(hits_set)

from matplotlib.lines import Line2D
from matplotlib.patches import Patch

custom_lines = [
                    # Patch(facecolor='#FF000000',edgecolor='#1f77b488',label='Detector layer outline' ),
                    Patch(facecolor='yellow',edgecolor='yellow',label='HCal bars hit' ),
                    Line2D([0], [0], color='green', linestyle='--',lw=4 , label='Apparent particle trajectory' ),
                    Patch(facecolor='red',label='Hits along particle trajectory' ),
                    # Patch(facecolor='red',label='Hit candidates' ),
                    # Patch(facecolor='green', ),
                    ]



eleven_plot_mode=True
eleven_plot_mode=False
two_plot_mode=False

if eleven_plot_mode:
    fig.set_size_inches(20, 20)
    ten_plot_mode = False
    hits=hits_set[0]
    ax = plt.subplot2grid((5,5), (0 ,1), colspan=3, rowspan=3,projection='3d')
    render_event_display(ax,hits,ten_plot_mode)      
    
    
    ten_plot_mode = True
    for i in range(0,10):
        hits=hits_set[i+1]
        ax = plt.subplot2grid((5,5), (int(i/5)+3 ,i%5), colspan=1, projection='3d')
        render_event_display(ax,hits,ten_plot_mode) 
    # fig.legend(handles=custom_lines, loc='upper right')

elif two_plot_mode:
    fig.set_size_inches(4, 8)
    for i in range(0,2):
        hits=hits_set[i]
        ax = fig.add_subplot(2,1,i+1, projection='3d')
        render_event_display(ax,hits,ten_plot_mode) 
    fig.legend(handles=custom_lines, loc='upper center')

elif ten_plot_mode:
    fig.set_size_inches(20, 8)
    for i in range(0,10):
        hits=hits_set[i]
        ax = fig.add_subplot(2,5,i+1, projection='3d')
        render_event_display(ax,hits,ten_plot_mode) 
    # fig.legend(handles=custom_lines, loc='center')

else:
    hits=hits_set[0]
    ax = fig.add_subplot(1,1,0+1, projection='3d')
    render_event_display(ax,hits,ten_plot_mode)     
    # fig.legend(handles=custom_lines, loc='upper left')      




# fig.show()
# plt.show()

plt.savefig('plots/3DED.png',dpi=500)

plt.show()


# for i, ax in enumerate(fig.axes):
#     ax.view_init(elev=0, azim=0)
# plt.savefig('plots/3DED_side.png',dpi=500)

# for i, ax in enumerate(fig.axes):
#     ax.view_init(elev=0, azim=-90)    
# plt.savefig('plots/3DED_front.png',dpi=500)    