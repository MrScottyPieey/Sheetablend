import bpy
import os
from PIL import Image
import bmesh

class SpriteSheetImporter:
    """Handles importing sprite sheets and creating frames"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.frames = []
        
    def load_image(self):
        """Load the sprite sheet image"""
        try:
            self.image = Image.open(self.image_path)
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def generate_grid_frames(self, cols, rows, spacing_x=0, spacing_y=0):
        """Generate frames based on grid layout"""
        if not self.image:
            return False
        
        img_width, img_height = self.image.size
        frame_width = (img_width - spacing_x * (cols - 1)) // cols
        frame_height = (img_height - spacing_y * (rows - 1)) // rows
        
        self.frames = []
        for row in range(rows):
            for col in range(cols):
                x = col * (frame_width + spacing_x)
                y = row * (frame_height + spacing_y)
                
                self.frames.append({
                    'x': x,
                    'y': y,
                    'width': frame_width,
                    'height': frame_height,
                    'name': f"Frame_{row}_{col}"
                })
        
        return True
    
    def create_blender_image(self, image_name="SpriteSheet"):
        """Create a Blender image from the sprite sheet"""
        if not os.path.exists(self.image_path):
            return None
        
        # Check if image already exists
        if image_name in bpy.data.images:
            return bpy.data.images[image_name]
        
        img = bpy.data.images.load(self.image_path)
        img.name = image_name
        return img
    
    def create_sprite_plane(self, image, sprite_name="Sprite"):
        """Create a plane mesh for the sprite"""
        # Create mesh and object
        mesh = bpy.data.meshes.new(f"{sprite_name}_Mesh")
        obj = bpy.data.objects.new(sprite_name, mesh)
        
        # Link to scene
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Create plane geometry
        bm = bmesh.new()
        verts = [
            bm.verts.new((-1, -1, 0)),
            bm.verts.new((1, -1, 0)),
            bm.verts.new((1, 1, 0)),
            bm.verts.new((-1, 1, 0))
        ]
        bm.faces.new(verts)
        
        # Add UVs
        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        uv_layer = bm.loops.layers.uv.new()
        face = bm.faces[0]
        face.loops[0][uv_layer].uv = (0, 0)
        face.loops[1][uv_layer].uv = (1, 0)
        face.loops[2][uv_layer].uv = (1, 1)
        face.loops[3][uv_layer].uv = (0, 1)
        
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        
        # Create material with image
        mat = bpy.data.materials.new(f"{sprite_name}_Material")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        image_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        image_node.image = image
        mat.node_tree.links.new(bsdf.inputs['Base Color'], image_node.outputs['Color'])
        
        mesh.materials.append(mat)
        
        return obj

def import_sprite_sheet(context, image_path, cols, rows, spacing_x=0, spacing_y=0):
    """Main function to import a sprite sheet"""
    importer = SpriteSheetImporter(image_path)
    
    if not importer.load_image():
        return None
    
    if not importer.generate_grid_frames(cols, rows, spacing_x, spacing_y):
        return None
    
    blender_image = importer.create_blender_image()
    if not blender_image:
        return None
    
    sprite_obj = importer.create_sprite_plane(blender_image)
    
    # Store frames in properties
    sprite_props = context.scene.sheetablend_props
    sprite_props.sprite_image_path = image_path
    
    # Clear existing animations and create default
    sprite_props.animations.clear()
    anim = sprite_props.animations.add()
    anim.name = "Default"
    
    for frame_data in importer.frames:
        frame = anim.frames.add()
        frame.name = frame_data['name']
        frame.x = frame_data['x']
        frame.y = frame_data['y']
        frame.width = frame_data['width']
        frame.height = frame_data['height']
    
    return sprite_obj