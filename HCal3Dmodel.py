import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# hits=[[1,4],[2,4], [3,4],[4,4],[5,4],[6,4],]

def render_event_display(hits=[]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    bar_width=50
    bar_height=2000
    layer_thickness=45
    # layer_thickness=90

    def add_bar(x,y,z,layer,bar,hits,color='C0'):
        # rendered_layers=[4,7,12]

        rendered_layers=range(0,20)
        vertices = [list(zip(x,y,z))]
        # if [layer,bar,'.+'] in hits: poly = Poly3DCollection(vertices, alpha=0.2,facecolor='red',edgecolor='red')
        if str(layer)+','+str(bar) in hits: 
            yellowness = 1 - hits[str(layer)+','+str(bar)] / 1024
            poly = Poly3DCollection(vertices, alpha=0.2,facecolor=(1,yellowness,0),edgecolor=(1,yellowness,0))
        else:   
            # poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#1f77b420')
            poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#FF000000')
        if layer in rendered_layers: ax.add_collection3d(poly)


    for layer in range (1,20):
        y = [layer*layer_thickness,layer*layer_thickness,layer*layer_thickness,layer*layer_thickness]
        if layer in (1,3,5,7,9):
            for bar in range (2,10):
                x = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                z = [-1000,-1000,1000,1000]
                add_bar(x,y,z,layer,bar,hits)

        elif layer in (2,4,6,8):
            for bar in range (2,10):
                x = [-1000,-1000,1000,1000]
                z = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                add_bar(x,y,z,layer,bar,hits)
        elif layer in (11,13,15,17,19):
            for bar in range (0,12):
                x = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                z = [-1000,-1000,1000,1000]
                add_bar(x,y,z,layer,bar,hits)
        elif layer in (10,12,14,16,18):
            for bar in range (0,12):
                x = [-1000,-1000,1000,1000]
                z = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                add_bar(x,y,z,layer,bar,hits)

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
    # first_vertical_bar = 4#hits[0][1]
    # first_horizontal_bar = 5#hits[1][1]
    x_start =  (0+first_vertical_bar-6)*bar_width + bar_width/2
    z_start =  (0+first_horizontal_bar-6)*bar_width + bar_width/2

    x = [x_start,x_start]
    z = [z_start,z_start]
    y = [-1000,1000]
    ax.plot(x, y, z, label='parametric curve',color='green')
    ax.set_xlim(-1000,1000)
    ax.set_ylim(000,1000)
    ax.set_zlim(-1000,1000)

    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    custom_lines = [
                    # Patch(facecolor='#FF000000',edgecolor='#1f77b488' ),
                    Patch(facecolor='yellow',edgecolor='yellow' ),
                    Patch(facecolor='red', ),
                    Line2D([0], [0], color='green', lw=4),]


    ax.legend(custom_lines, ['HCal bar (weak hit)', 'HCal bar (strong hit)', 'Muon path'])
    # ax.legend(custom_lines, ['HCal bar (not hit)', 'HCal bar (hit)', 'presumed pion entry'])
    # ax.legend(custom_lines, ['HCal bar (weak hit)', 'HCal bar (strong hit)', 'presumed electron entry'])

    ax.set_xlabel("Horizontal axis [mm]")
    ax.set_ylabel("Beam axis [mm]")
    ax.set_zlabel("Vertical axis [mm]")


    plt.show()

 