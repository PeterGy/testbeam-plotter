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
    layer_thickness=95

    def add_bar(x,y,z,layer,bar,hits,color='C0'):
        if [layer,bar] in hits:  color='red'
        vertices = [list(zip(x,y,z))]
        poly = Poly3DCollection(vertices, alpha=0.2,facecolor=color)
        ax.add_collection3d(poly)


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



    import numpy as np
    first_vertical_bar = hits[0][1]
    first_horizontal_bar = hits[1][1]
    x_start =  (0+first_vertical_bar-6)*bar_width + bar_width/2
    z_start =  (0+first_horizontal_bar-6)*bar_width + bar_width/2

    x = [x_start,x_start]
    z = [z_start,z_start]
    y = [-1000,3000]
    ax.plot(x, y, z, label='parametric curve',color='green')
    ax.set_xlim(-1000,1000)
    ax.set_ylim(-1000,1000)
    ax.set_zlim(-1000,1000)
    plt.show()

 