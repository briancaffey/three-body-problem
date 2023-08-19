import bpy
import random

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Parameters for the 2D array of cubes
num_rows = 3
num_columns = 6
cube_spacing = 1.2

# Create an empty collection to hold the cubes
cube_collection = bpy.data.collections.new("CubeCollection")
bpy.context.scene.collection.children.link(cube_collection)

# Create cubes in a 2D array, set random heights, colors, and align to the bottom
for row in range(num_rows):
    for col in range(num_columns):
        cube_height = random.uniform(1.0, 5.0)
        cube = bpy.ops.mesh.primitive_cube_add(size=1, location=(col * cube_spacing, row * cube_spacing, cube_height / 2.0))
        cube_obj = bpy.context.active_object
        cube_obj.scale.z = cube_height
        cube_obj.name = f"Cube_{row}_{col}"
        cube_collection.objects.link(cube_obj)

        # Assign a random color to each cube
        material = bpy.data.materials.new(name=f"Material_{row}_{col}")
        material.diffuse_color = (random.random(), random.random(), random.random(), 1.0)
        cube_obj.data.materials.append(material)

# Select all cubes
bpy.ops.object.select_all(action='DESELECT')
for cube_obj in cube_collection.objects:
    cube_obj.select_set(True)

# Create an array modifier for rows
bpy.ops.object.modifier_add(type='ARRAY')
array_modifier_rows = bpy.context.object.modifiers["Array"]
array_modifier_rows.count = num_rows
array_modifier_rows.use_relative_offset = False
array_modifier_rows.use_constant_offset = True
array_modifier_rows.constant_offset_displace[1] = cube_spacing

# Apply the row array modifier
bpy.ops.object.modifier_apply(modifier=array_modifier_rows.name)

# Select all cubes again
bpy.ops.object.select_all(action='DESELECT')
for cube_obj in cube_collection.objects:
    cube_obj.select_set(True)

# Create an array modifier for columns
bpy.ops.object.modifier_add(type='ARRAY')
array_modifier_cols = bpy.context.object.modifiers["Array"]
array_modifier_cols.count = num_columns
array_modifier_cols.use_relative_offset = False
array_modifier_cols.use_constant_offset = True
array_modifier_cols.constant_offset_displace[0] = cube_spacing

# Apply the column array modifier
bpy.ops.object.modifier_apply(modifier=array_modifier_cols.name)
