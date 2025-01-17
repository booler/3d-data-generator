import bpy
import os
import numpy
import sys
sys.path.append('./scripts/util')
from helper import set_prop_val

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1280 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 720 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

# name of object
obj_name = ['bottle', 'cup', 'king', 'knight']
# number of images
nimages = 41 # len(bpy.data.objects) - 3
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# list of properties
ind_prop = numpy.matrix([[2, 8, 2, 8], [2, 8, 5, 2], [8, 8, 2, 8], [8, 8, 5, 2]])

# hide all objects
bpy.data.objects['Sphere'].hide_render = True
bpy.data.objects['ball'].hide_render = True
bpy.data.objects['bottle'].hide_render = True
bpy.data.objects['cup'].hide_render = True
bpy.data.objects['king'].hide_render = True
bpy.data.objects['knight'].hide_render = True

# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes

for ind_obj in range(0, len(obj_name)):
    # output directory of rendered images
    odir = '%s/testing/%s' % (rdir, obj_name[ind_obj])
    bpy.data.objects[obj_name[ind_obj]].hide_render = False

    for row in range(0, len(ind_prop)):
        subdir = '%02d%02d%02d%02d' % (ind_prop[row, 0], ind_prop[row, 1], ind_prop[row, 2], ind_prop[row, 3])

        # set the other properties to default values
        nodes["Group"].inputs[1].default_value = ind_prop[row, 0] / 10.0 # Texture
        nodes["Group"].inputs[2].default_value = ind_prop[row, 1] / 10.0 # Albedo
        nodes.get("Principled BSDF").inputs[5].default_value = ind_prop[row, 2] # Specular
        nodes.get("Principled BSDF").inputs[7].default_value = ind_prop[row, 3] / 10.0 # Roughness

        outdir = '%s/mvs/%s/visualize' % (odir, subdir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        for ind_cam in range(0, nimages):
            bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % ind_cam]
            bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_cam)
            bpy.ops.render.render(write_still=True)

    bpy.data.objects[obj_name[ind_obj]].hide_render = True
