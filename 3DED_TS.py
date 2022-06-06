#3D event display

from numpy import *
import csv
import ROOT as r
import libDetDescr as DD
from TS3Dmodel import *
r.gSystem.Load("libFramework.so") #this library is vital for it to run. It might be old though?

csv_reader = csv.reader(open('pedestals/pedestals_20220424_22.csv'), delimiter=',')

pedestals ={}
for row in csv_reader:
    try:  pedestals[int(row[0],0)] = float(row[1])
    except:pass


run=183
inFile = r.TFile("reconstructions/"+str(run)+"TS.root","READ")  
allData = inFile.Get("LDMX_Events")
events_of_interest=[1,2,5,8,9,10,11,12,15,16]
# events_of_interest=[14,1,2,5,8, 9,10,11,12,14,15]




def getTSHits(event_of_interest=8):
    eventN=0
    realEvents=[]
    for event in allData: 
        hits={} 
        eventN+=1
        for ih,h in enumerate(getattr(event, "testBeamHitsUp_hits")):
            if h.getPE() >50:
                hits[h.getBarID()] = h.getAmplitude()
                if eventN not in realEvents: realEvents.append(eventN)
        if len(realEvents) == event_of_interest: return hits
        # if len(hits) !=0: print(hits)

    return hits



hits=getTSHits()
print(hits)

fig = plt.figure()
ax = fig.add_subplot(1,1,0+1, projection='3d')
render_event_display(ax,hits) 



# fig = plt.figure()
# # fig.set_size_inches(20, 8)
# fig.set_size_inches(8, 8)
# fig.tight_layout()
# subplots=[]


# from Set_of_hits_for_3D_HCal_ED import *
# # hits_set=[]
# # for i in range(0,10):
# #     hits_set.append(getHcalHits(events_of_interest[i]))
# # print(hits_set)


# fig.set_size_inches(20, 8)
# for i in range(0,10):
#     hits=hits_set[i]
#     ax = fig.add_subplot(2,5,i+1, projection='3d')
#     render_event_display(ax,hits) 


# # hits=hits_set[0]
# # ax = fig.add_subplot(1,1,0+1, projection='3d')
# # render_event_display(ax,hits)           


# from matplotlib.lines import Line2D
# from matplotlib.patches import Patch

# custom_lines = [
#                     # Patch(facecolor='#FF000000',edgecolor='#1f77b488',label='Detector layer outline' ),
#                     Patch(facecolor='yellow',edgecolor='yellow',label='HCal bars hit' ),
#                     Line2D([0], [0], color='green', lw=4 , label='Apparent particle trajectory' ),
#                     Patch(facecolor='red',label='Hits along particle trajectory' ),
#                     # Patch(facecolor='green', ),
#                     ]

# fig.legend(handles=custom_lines, loc='center')
# # fig.show()
# # plt.show()

# plt.savefig('plots/3DED.png',dpi=500)

# # plt.show()


# for i, ax in enumerate(fig.axes):
#     ax.view_init(elev=0, azim=0)
# plt.savefig('plots/3DED_side.png',dpi=500)

# for i, ax in enumerate(fig.axes):
#     ax.view_init(elev=0, azim=-90)    
# plt.savefig('plots/3DED_front.png',dpi=500)    