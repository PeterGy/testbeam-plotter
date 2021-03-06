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

    def add_hit_squares(first_vertical_bar,first_horizontal_bar):
        for layer in range (1,20):
            y = [layer*layer_thickness,layer*layer_thickness,layer*layer_thickness,layer*layer_thickness]
            x = [x_start-bar_width/2, x_start+bar_width/2, x_start+bar_width/2, x_start-bar_width/2,]
            z = [z_start-bar_width/2, z_start-bar_width/2, z_start+bar_width/2, z_start+bar_width/2,]
            vertices = [list(zip(x,y,z))]

            # poly = Poly3DCollection(vertices,facecolor='red',edgecolor='red')
            
            poly = Poly3DCollection(vertices,alpha=0.5,facecolor=(1,0,0),edgecolor=(1,0,0))
            if layer%2==0: correct_bar = first_horizontal_bar
            elif layer%2==1: correct_bar = first_vertical_bar
            for i in hits:
                if str(layer)+','+str(correct_bar) == i: ax.add_collection3d(poly)
            

    def add_layer(x,y,z):
        vertices = [list(zip(x,y,z))]
        poly = Poly3DCollection(vertices,facecolor='#FF000000',edgecolor='#1f77b409')
        ax.add_collection3d(poly)

    def add_absorber_hit_squares(hits):
        hit_markers = [[],[],[]]
        for vert_hit in hits:
            vert_layer = int(vert_hit[0:vert_hit.find(',')])
            vert_bar = int(vert_hit[vert_hit.find(',')+1:])
            if vert_layer%2==1:
                for next_hit in hits:
                    next_layer = int(next_hit[0:next_hit.find(',')])
                    next_bar = int(next_hit[next_hit.find(',')+1:])
                    if int(next_layer)==vert_layer+1:
                        y = [(vert_layer+0.5)*layer_thickness,(vert_layer+0.5)*layer_thickness,(vert_layer+0.5)*layer_thickness,(vert_layer+0.5)*layer_thickness]
                        x_start =  (0+vert_bar-6)*bar_width + bar_width/2
                        z_start =  (0+next_bar-6)*bar_width + bar_width/2

                        x = [x_start-bar_width/2, x_start+bar_width/2, x_start+bar_width/2, x_start-bar_width/2,]
                        z = [z_start-bar_width/2, z_start-bar_width/2, z_start+bar_width/2, z_start+bar_width/2,]
                        vertices = [list(zip(x,y,z))]
                        poly = Poly3DCollection(vertices,alpha=0.5,facecolor=(1,0,0),edgecolor=(1,0,0))
                        ax.add_collection3d(poly)
                        hit_markers[0].append(x[0])
                        hit_markers[1].append(y[0])
                        hit_markers[2].append(z[0])
                        # print([x[0],y[0],z[0]])

                        # plt.plot([x[0],y[0],z[0]], marker=11)
            # ax.scatter(hit_markers, marker='+',color='red')
            # for i in np.arange(0, len(x)):  # Lines were modified here!
            #     for xval, yval, zval, zerr in zip(hit_markers[0], hit_markers[1], hit_markers[2], hit_markers[0]):
            #         ax.plot([xval, xval], [yval, yval], [zval+zerr, zval-zerr], marker="_", color='k')

            # ax.errorbar(hit_markers[0],hit_markers[1],hit_markers[2],0.1, marker=11,color='red')
            # ax.scatter(hit_markers[0],hit_markers[1],hit_markers[2], marker="$+$",color='red',s=100)






        # for vert_layer in range [1,3,5,7,9,11,13,15,17]:


    # def add_layer_outlines():
    #     for layer in range (1,20):
    #         y = [layer*layer_thickness,layer*layer_thickness,layer*layer_thickness,layer*layer_thickness]
    #         if layer in (1,3,5,7,9):
    #             for bar in range (2,10):
    #                 x = [(2-6)*bar_width, (10-6)*bar_width, (10-6)*bar_width, (2-6)*bar_width]
    #                 z = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
    #                 add_layer(x,y,z)
    #         elif layer in (2,4,6,8):
    #             for bar in range (2,10):
    #                 x = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
    #                 z = [(2-6)*bar_width, (10-6)*bar_width, (10-6)*bar_width, (2-6)*bar_width]
    #                 add_layer(x,y,z)
    #         elif layer in (11,13,15,17,19):
    #             for bar in range (0,12):
    #                 x = [(0-6)*bar_width, (12-6)*bar_width, (12-6)*bar_width, (0-6)*bar_width]
    #                 z = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
    #                 add_layer(x,y,z)
    #         elif layer in (10,12,14,16,18):
    #             for bar in range (0,12):
    #                 x = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
    #                 z = [(0-6)*bar_width, (12-6)*bar_width, (12-6)*bar_width, (0-6)*bar_width]
    #                 add_layer(x,y,z)

    def add_bar(x,y,z,layer,bar,hits,color='C0'):
        # rendered_layers=[4,7,12]

        rendered_layers=range(0,20)
        vertices = [list(zip(x,y,z))]
        # if [layer,bar,'.+'] in hits: poly = Poly3DCollection(vertices, alpha=0.2,facecolor='red',edgecolor='red')
        if str(layer)+','+str(bar) in hits: 
            yellowness = 1 - hits[str(layer)+','+str(bar)] / 1024
            # yellowness = 1 
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
                z = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
                add_bar(x,y,z,layer,bar,hits)

        elif layer in (2,4,6,8):
            for bar in range (2,10):
                x = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
                z = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                add_bar(x,y,z,layer,bar,hits)
        elif layer in (11,13,15,17,19):
            for bar in range (0,12):
                x = [(0+bar-6)*bar_width, (1+bar-6)*bar_width, (1+bar-6)*bar_width, (0+bar-6)*bar_width]
                z = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
                add_bar(x,y,z,layer,bar,hits)
        elif layer in (10,12,14,16,18):
            for bar in range (0,12):
                x = [-bar_height/2,-bar_height/2,bar_height/2,bar_height/2]
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
    #Event 14 does indeed invalidate this path determination method
    x_start =  (0+first_vertical_bar-6)*bar_width + bar_width/2
    z_start =  (0+first_horizontal_bar-6)*bar_width + bar_width/2

    x = [x_start,x_start]
    z = [z_start,z_start]
    y = [-500,900]
    
    add_hit_squares(first_vertical_bar,first_horizontal_bar)
    # add_absorber_hit_squares(hits)

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
                    Patch(facecolor='yellow',edgecolor='yellow',label='HCal bars hit' ),
                    Line2D([0], [0], color='green', linestyle='--',lw=4 , label='Apparent particle trajectory' ),
                    Patch(facecolor='red',label='Hits along particle trajectory' ),
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


 

