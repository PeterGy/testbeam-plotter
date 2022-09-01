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

inFile = r.TFile("reconstructions/"+str(run)+".root","READ")  
allData = inFile.Get("LDMX_Events")

events_of_interest=[10,5,8,9,10,11,12,15,16,17,18,19,20]
events_of_interest=[10]


ten_plot_mode = False
# ten_plot_mode = True


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# hits=[[1,4],[2,4], [3,4],[4,4],[5,4],[6,4],]






def render_event_display(ax,hits,ten_plot_mode=False):

    bar_width=50
    # bar_height=2000
    bar_height=700

    layer_thickness=45
    # layer_thickness=90


            

    def add_layer(x,y,z):
        vertices = [list(zip(x,y,z))]
        poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#1f77b409')
        ax.add_collection3d(poly)



    def add_bar(x,y,z,layer,bar,hits,color='C0'):
        # rendered_layers=[4,7,12]

        rendered_layers=range(0,20)
        vertices = [list(zip(x,y,z))]
        # if [layer,bar,'.+'] in hits: poly = Poly3DCollection(vertices, alpha=0.2,facecolor='red',edgecolor='red')
        if str(layer)+','+str(bar) in hits: 
            if layer in (1,11):
                poly = Poly3DCollection(vertices, alpha=0.2,facecolor=(1,1,0),edgecolor=(1,1,0))
            elif layer in (7,):
                poly = Poly3DCollection(vertices, alpha=0.2,facecolor=(0,0,1),edgecolor=(0,0,1))
            else:    
                poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#FF000000')


        else:   
            # poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#1f77b420')
            poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#FF000000')

        if layer in rendered_layers: ax.add_collection3d(poly)


    for layer in range (1,20):
        y = [layer*layer_thickness,layer*layer_thickness,layer*layer_thickness,layer*layer_thickness]
        if layer in (1,3,5,7,9):
            for bar in range (2,10):
                x = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                z = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
                add_bar(x,y,z,layer,bar,hits)

        # elif layer in (2,4,6,8):
        #     for bar in range (2,10):
        #         x = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
        #         z = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
        #         add_bar(x,y,z,layer,bar,hits)
        elif layer in (11,):
            for bar in range (0,12):
                x = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                z = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
                add_bar(x,y,z,layer,bar,hits)
        # elif layer in (10,12,14,16,18):
        #     for bar in range (0,12):
        #         x = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
        #         z = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
        #         add_bar(x,y,z,layer,bar,hits)

    # def get_x_entryhits(hits):
    first_layer_max=0
    entry_bar=99
    for i in hits:
        if i[0:2]=='1,':
            if hits[i]>first_layer_max:
                entry_bar=int(i[2])
                first_layer_max=hits[i]
    first_vertical_bar = entry_bar        

    first_layer_max=0
    entry_bar=99
    for i in hits:
        if i[0:2]=='2,':
            if hits[i]>first_layer_max:
                entry_bar=int(i[2])
                first_layer_max=hits[i]
    first_horizontal_bar = entry_bar     



    import numpy as np

    x_start =  (0+first_vertical_bar-6)*bar_width + bar_width/2
    z_start =  (0+first_horizontal_bar-6)*bar_width + bar_width/2

    x = [x_start,x_start]
    z = [z_start,z_start]
    y = [-500,900]
    


    ax.plot(x, y, z, label='parametric curve',linestyle='--',color='green')





    #bar outlin
    # add_layer_outlines()







    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    custom_lines = [
                    # Patch(facecolor='#FF000000',edgecolor='#1f77b488',label='Detector layer outline' ),
                    # Patch(facecolor='yellow',edgecolor='yellow',label='HCal bars hit' ),
                    # Line2D([0], [0], color='green', lw=4 , label='Apparent particle trajectory' ),
                    # Patch(facecolor='red',label='Hits along particle trajectory' ),
                    # Patch(facecolor='green', ),
                    Patch(facecolor='yellow',edgecolor='yellow',label='Bars that must pass MIPeq > 0.9' ),
                    Patch(facecolor='blue',edgecolor='blue',label='Bar of which MIP response is measured' ),
                    Line2D([0], [0], color='green', linestyle='--',lw=4 , label='Apparent particle trajectory' ),
                    # Patch(facecolor='red',label='Hits along particle trajectory' ),
                    ]

    if ten_plot_mode == False:   
    # if True:
        ax.legend(handles=custom_lines)
        ax.set_xlabel("Horizontal axis [mm]")
        ax.set_ylabel("Beam axis [mm]")
        ax.set_zlabel("Vertical axis [mm]")
        

    else:
        ax.dist=8
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])    

    ax.set_xlim(-bar_height/2,bar_height/2)
    ax.set_ylim(000,855)
    ax.set_zlim(-bar_height/2,bar_height/2)


    # ax.view_init(elev=0, azim=90)
    # ax.view_init(elev=0, azim=0)
    # plt.show()


 




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

