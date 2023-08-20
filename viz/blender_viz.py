import bpy
import random
import json
import bmesh
import math

FONT_PATH = "/Users/brian/git/github/three-body-problem/SongTi.ttf"

# Create a new font
font = bpy.data.fonts.load(FONT_PATH)

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Parameters for the 2D array of cubes
num_rows = 3
num_columns = 5
cube_spacing = 1.2

# Create an empty collection to hold the cubes
cube_collection = bpy.data.collections.new("CubeCollection")
bpy.context.scene.collection.children.link(cube_collection)


def arrange_data(arr, r_len, c_len):
    diff = len(arr) - (r_len * c_len)
    if diff >= 0:
        arr = arr[:r_len*c_len]
        ret_arr = []
        for c in range(c_len):
            sub_arr = []
            for r in range(r_len):
                sub_arr.append(arr[c*r_len + r])
            ret_arr.append(sub_arr)
        return ret_arr
    else:
        raise Exception("array too short")


with open("/Users/brian/git/github/three-body-problem/output.json", "r") as f:
#    pass
    data = json.loads(f.read())

    print(data[0])




rows_cols = arrange_data(data, 20, 20)


# Create cubes in a 2D array, set random heights, colors, and align to the bottom
for row_count, row in enumerate(rows_cols):
    for col_count, col in enumerate(rows_cols[row_count]):
        cube_height = rows_cols[row_count][col_count]["occurences"]/300 #random.uniform(1.0, 5.0)
        cube_data = rows_cols[row_count][col_count]
        cube = bpy.ops.mesh.primitive_cube_add(size=1, location=(col_count * cube_spacing, row_count * cube_spacing, cube_height / 2))
        cube_obj = bpy.context.active_object
        cube_obj.scale.z = cube_height
        cube_obj.name = f"Cube_{row_count}_{col_count}"
        cube_collection.objects.link(cube_obj)

        # Assign a random color to each cube
        # "character": "的", "rank": 1, "overall_rank": 1, "occurences": 7944,
        # color_tuple = (234, 46, 144, 1.0)
        material = bpy.data.materials.new(name=f"Material_{row}_{col}")
        material.diffuse_color = (cube_data["rank"]/cube_data["overall_rank"], 100.0, 100.0, 1.0)
        # material.diffuse_color = color_tuple
        cube_obj.data.materials.append(material)

        # Select all cubes
        bpy.ops.object.select_all(action='DESELECT')

        # Add character on top of column
        # Create a text object
        text = bpy.data.objects.new(name="Custom_Text", object_data=bpy.data.curves.new(name="TextCurve", type='FONT'))
        text.data.body = cube_data["character"]
        text.data.font = font
        text.location = (col_count * cube_spacing, row_count * cube_spacing - 0.5, cube_height + 0.3)

        # Link the text object to the scene
        bpy.context.collection.objects.link(text)

        # Select the text object
        text.select_set(True)
        bpy.context.view_layer.objects.active = text

        # Rotate the text object along the Y-axis
        bpy.ops.transform.rotate(value=3*math.pi/2, orient_axis='X')
        bpy.ops.transform.rotate(value=3*math.pi/2, orient_axis='Z')

        material = bpy.data.materials.new(name=f"Material_{row}_{col}")
        material.diffuse_color = (0, 0, 0.0, 1.0)
        # material.diffuse_color = color_tuple
        text.data.materials.append(material)


        bpy.ops.object.convert(target='MESH')

        # Go to edit mode, face selection mode and select all faces
        bpy.ops.object.mode_set( mode = 'EDIT' )     # Toggle edit mode
        bpy.ops.mesh.select_mode( type = 'FACE' )    # Change to face selection
        bpy.ops.mesh.select_all( action = 'SELECT' ) # Select all faces

        # Create Bmesh
        bm = bmesh.new()
        bm = bmesh.from_edit_mesh( bpy.context.object.data )

        for f in bm.faces:
            face = f.normal

        r = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])

        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        TranslateDirection = face * 0.1 # Extrude Strength/Length
        bmesh.ops.translate(bm, vec = TranslateDirection, verts=verts)

        # Update & Destroy Bmesh
        bmesh.update_edit_mesh(bpy.context.object.data) # Write the bmesh back to the mesh
        bm.free()  # free and prevent further access

        bpy.ops.object.mode_set(mode='OBJECT')

# Select all cubes
bpy.ops.object.select_all(action='DESELECT')
for cube_obj in cube_collection.objects:
    cube_obj.select_set(True)
