import bpy
from bpy.types import Panel

class SHEETABLEND_PT_sprite_import(Panel):
    """Panel for sprite sheet import settings"""
    bl_label = "Sprite Sheet Import"
    bl_idname = "SHEETABLEND_PT_sprite_import"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        sprite_props = context.scene.sheetablend_props
        
        # File selection
        layout.label(text="Sprite Sheet:")
        layout.prop(sprite_props, "sprite_image_path")
        
        # Import button
        layout.operator("sheetablend.import_sprite_sheet", text="Import Sprite Sheet", icon='IMPORT')
        
        # Grid settings
        layout.label(text="Grid Settings:")
        col = layout.column()
        col.prop(sprite_props, "use_grid")
        if sprite_props.use_grid:
            col.prop(sprite_props, "grid_cols")
            col.prop(sprite_props, "grid_rows")
            col.prop(sprite_props, "spacing_x")
            col.prop(sprite_props, "spacing_y")
        
        # Frame settings
        layout.label(text="Frame Settings:")
        layout.prop(sprite_props, "frame_width")
        layout.prop(sprite_props, "frame_height")
        layout.prop(sprite_props, "default_frame_duration")
        
        # Import options
        layout.label(text="Import Options:")
        layout.prop(sprite_props, "import_as_plane")
        layout.prop(sprite_props, "create_material")
        layout.prop(sprite_props, "auto_uv")

class SHEETABLEND_PT_animation_editor(Panel):
    """Panel for animation management"""
    bl_label = "Animation Editor"
    bl_idname = "SHEETABLEND_PT_animation_editor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        sprite_props = context.scene.sheetablend_props
        
        # Animation list
        layout.label(text="Animations:")
        row = layout.row()
        row.template_list("UI_UL_list", "animations", sprite_props, "animations", 
                         sprite_props, "active_animation")
        
        # Create animation button
        col = row.column(align=True)
        col.operator("sheetablend.create_animation", text="", icon='ADD')
        
        # Animation settings
        if sprite_props.active_animation < len(sprite_props.animations):
            anim = sprite_props.animations[sprite_props.active_animation]
            layout.separator()
            layout.label(text="Animation Settings:")
            layout.prop(anim, "name")
            layout.prop(anim, "is_looping")
            layout.prop(anim, "speed")
            layout.prop(sprite_props, "playback_speed")
            
            # Playback controls
            row = layout.row(align=True)
            if not sprite_props.is_playing:
                row.operator("sheetablend.play_animation", text="Play", icon='PLAY')
            else:
                row.operator("sheetablend.stop_animation", text="Stop", icon='PAUSE')
            
            # Frame count
            layout.label(text=f"Frames: {len(anim.frames)}")

class SHEETABLEND_PT_frame_editor(Panel):
    """Panel for frame-by-frame editing"""
    bl_label = "Frame Editor"
    bl_idname = "SHEETABLEND_PT_frame_editor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        sprite_props = context.scene.sheetablend_props
        
        if sprite_props.active_animation >= len(sprite_props.animations):
            layout.label(text="No animation selected")
            return
        
        anim = sprite_props.animations[sprite_props.active_animation]
        
        if len(anim.frames) == 0:
            layout.label(text="No frames in animation")
            return
        
        # Frame list
        layout.label(text="Frames:")
        row = layout.row()
        row.template_list("UI_UL_list", "frames", anim, "frames", 
                         anim, "current_frame")
        
        # Add/Remove buttons
        col = row.column(align=True)
        col.operator("sheetablend.add_frame", text="", icon='ADD')
        col.operator("sheetablend.remove_frame", text="", icon='REMOVE')
        
        # Current frame properties
        if anim.current_frame < len(anim.frames):
            frame = anim.frames[anim.current_frame]
            layout.separator()
            layout.label(text="Frame Properties:")
            layout.prop(frame, "name")
            layout.prop(frame, "x")
            layout.prop(frame, "y")
            layout.prop(frame, "width")
            layout.prop(frame, "height")
            layout.prop(frame, "duration")
            layout.prop(frame, "pivot_x")
            layout.prop(frame, "pivot_y")

class SHEETABLEND_PT_rigging_tools(Panel):
    """Panel for 2D rigging tools"""
    bl_label = "2D Rigging Tools"
    bl_idname = "SHEETABLEND_PT_rigging_tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        sprite_props = context.scene.sheetablend_props
        
        # Create rig button
        if not sprite_props.has_rig:
            layout.operator("sheetablend.create_rig", text="Create Rig", icon='ADD')
            return
        
        rig = sprite_props.rig
        
        # Rig settings
        layout.label(text="Rig: " + rig.name)
        layout.prop(rig, "show_bones")
        layout.prop(rig, "bone_size")
        layout.prop(rig, "deform_mesh")
        
        # Bones list
        layout.label(text="Bones:")
        row = layout.row()
        row.template_list("UI_UL_list", "bones", rig, "bones", 
                         rig, "current_bone")
        
        # Add bone button
        col = row.column(align=True)
        col.operator("sheetablend.add_bone", text="", icon='ADD')
        
        # Selected bone properties
        if 0 <= rig.current_bone < len(rig.bones):
            bone = rig.bones[rig.current_bone]
            layout.separator()
            layout.label(text="Bone Properties:")
            layout.prop(bone, "name")
            layout.prop(bone, "x")
            layout.prop(bone, "y")
            layout.prop(bone, "length")
            layout.prop(bone, "rotation")
            layout.prop(bone, "influence")
            layout.prop(bone, "is_ik")
            
            # Weight painting
            layout.separator()
            layout.label(text="Weight Painting:")
            layout.operator("sheetablend.paint_weights", text="Paint Weights", icon='BRUSH_DATA')
