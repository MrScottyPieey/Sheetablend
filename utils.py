import bpy
import os
from pathlib import Path

def get_addon_prefs():
    """Get addon preferences"""
    prefs = bpy.context.preferences.addons[__name__].preferences
    return prefs

def get_asset_path(filename):
    """Get path to addon asset files"""
    addon_path = Path(__file__).parent
    return addon_path / filename

def log_message(message, message_type='INFO'):
    """Log a message in Blender"""
    print(f"[Sheetablend] {message_type}: {message}")

def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))

def normalize(value, min_val, max_val):
    """Normalize a value to 0-1 range"""
    if max_val == min_val:
        return 0
    return (value - min_val) / (max_val - min_val)

def lerp(a, b, t):
    """Linear interpolation between two values"""
    return a + (b - a) * t

def distance_2d(x1, y1, x2, y2):
    """Calculate 2D distance between two points"""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def get_selected_objects():
    """Get currently selected objects"""
    return [obj for obj in bpy.context.selected_objects]

def get_active_object():
    """Get the active object"""
    return bpy.context.active_object

def set_active_object(obj):
    """Set the active object"""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
