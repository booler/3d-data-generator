import bpy
import os
import math
import mathutils
import numpy
import sys
sys.path.append('./scripts/util')
from helper import set_prop_val

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1024
bpy.data.scenes['Scene'].render.resolution_y = 768
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

angles = mathutils.Vector((-20.0, 0.0, 20.0)) * math.pi / 180.0
ndim = 3 # number of angles, 3
nimg = 20 # number of patterns, 20

# name of object
obj_name = ['bottle', 'cup', 'king', 'knight']
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the projection patterns
idir = '%s/textures/sl' % rdir
# list of properties
ind_prop = numpy.matrix([[2, 8, 2, 8], [2, 8, 5, 2], [8, 8, 2, 8], [8, 8, 5, 2]])

# hide all objects except the projector
bpy.data.objects['Sphere'].hide_render = True
bpy.data.objects['ball'].hide_render = True
bpy.data.objects['bottle'].hide_render = True
bpy.data.objects['cup'].hide_render = True
bpy.data.objects['king'].hide_render = True
bpy.data.objects['knight'].hide_render = True
bpy.data.objects['Lamp'].hide_render = False
bpy.data.objects['Point'].hide_render = True
bpy.data.objects['Plane'].hide_render = True

# get material nodes and projector texture image node
nodes = bpy.data.materials['Material'].node_tree.nodes
proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
tex_node = proj_nodes.get('Image Texture')

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

        outdir = '%s/sl/%s' % (odir, subdir)

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        for ind_img in range(0, nimg):
            proj_ptn = bpy.data.images.load("%s/sl_v%d.jpg" % (idir, ind_img))
            tex_node.image = proj_ptn
            bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img)
            bpy.ops.render.render(write_still=True)
            
            proj_ptn = bpy.data.images.load("%s/sl_h%d.jpg" % (idir, ind_img))
            tex_node.image = proj_ptn
            bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + nimg)
            bpy.ops.render.render(write_still=True)
        
        for ind_img in range(0, 2):
            proj_ptn = bpy.data.images.load("%s/sl_a%d.jpg" % (idir, 1 - ind_img))
            tex_node.image = proj_ptn
            bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + 2 * nimg)
            bpy.ops.render.render(write_still=True)
    
    bpy.data.objects[obj_name[ind_obj]].hide_render = True
