# Sheetablend

A comprehensive Blender addon for importing 2D sprite sheets with advanced animation, frame-by-frame control, and 2D skeletal rigging capabilities.

## Features

### 🎨 Sprite Sheet Importing
- Automatic sprite sheet parsing and frame extraction
- Grid-based frame detection with customizable spacing
- Support for PNG, JPG, and other common image formats
- Automatic material and UV mapping creation

### 🎬 Animation System
- Create multiple animations from sprite frames
- Frame-by-frame animation editor with individual frame timing
- Real-time animation preview and playback
- Adjustable playback speed and looping controls
- Timeline integration for keyframe animation

### 🦴 2D Skeletal Rigging
- Create and manage 2D bone hierarchies
- Weight painting for vertex-bone relationships
- Inverse Kinematics (IK) support for natural bone movement
- Real-time mesh deformation based on bone positions
- Bone influence controls for fine-tuned deformation

### 🎮 Game Engine Ready
- Export animations for use in game engines
- Frame sequence export capabilities
- Compatible with Unity and Godot sprite systems

## Installation

1. Download the Sheetablend addon
2. Open Blender and go to Edit > Preferences > Add-ons
3. Click "Install" and select the Sheetablend folder
4. Enable the addon by checking the checkbox
5. Access Sheetablend from the Properties panel (Scene properties)

## Quick Start

### Importing a Sprite Sheet
1. Open the "Sprite Sheet Import" panel
2. Select your sprite sheet image
3. Configure grid settings (columns, rows, spacing)
4. Adjust frame dimensions if needed
5. Click "Import Sprite Sheet"

### Creating Animations
1. Open the "Animation Editor" panel
2. Click the "+" button to create a new animation
3. Add frames using the "Frame Editor" panel
4. Set individual frame durations
5. Use Play/Stop buttons to preview

### Setting Up 2D Rigging
1. Open the "2D Rigging Tools" panel
2. Click "Create Rig"
3. Add bones using the "+" button
4. Position bones and set their properties
5. Use "Paint Weights" to define vertex deformation
6. Enable "Deform Mesh" to see real-time deformation

## UI Panels

### Sprite Sheet Import
- File path selection
- Grid configuration (columns, rows, spacing)
- Frame size settings
- Import options (material creation, auto UV)

### Animation Editor
- Animation list management
- Create/delete animations
- Playback controls
- Speed and looping settings

### Frame Editor
- Frame list with visual management
- Individual frame properties:
  - Position (X, Y) in sprite sheet
  - Dimensions (Width, Height)
  - Duration (frame timing)
  - Pivot points for rotation

### 2D Rigging Tools
- Rig creation and management
- Bone creation and hierarchy
- Bone properties:
  - Position and rotation
  - Length and influence
  - IK (Inverse Kinematics) support
  - Parent/child relationships
- Weight painting interface
- Mesh deformation controls

## Advanced Features

### Inverse Kinematics
Automatically solve bone rotations to reach a target position. Enable "IK" on a bone and set the target coordinates.

### Weight Painting
Control how much each bone influences nearby vertices. Higher weights mean more influence.

### Frame Pivots
Set custom pivot points for each frame to control rotation centers during animation.

## Keyboard Shortcuts

- **Space** - Play/Stop animation preview
- **Right Arrow** - Next frame
- **Left Arrow** - Previous frame

## Troubleshooting

### Animation not playing
- Ensure animation has frames added
- Check that "Is Playing" is enabled
- Verify playback speed is greater than 0

### Mesh not deforming
- Ensure "Deform Mesh" is enabled
- Check that weights are painted
- Verify bone positions are correct

### Frames not appearing
- Confirm sprite sheet file exists and is accessible
- Check grid settings match your sprite sheet layout
- Verify frame dimensions are correct

## Performance Tips

- Keep sprite sheets under 4096x4096 pixels for optimal performance
- Use reasonable bone counts (10-30 bones recommended)
- Paint weights selectively rather than on entire mesh
- Disable real-time deformation during weight painting for better performance

## Export

Export your animated sprites for use in game engines:
1. Select the sprite object
2. File > Export > [Choose format]
3. Configure export settings
4. Export with animation data

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This addon is released under the MIT License. See LICENSE file for details.

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/MrScottyPieey/Sheetablend/issues
- Documentation: https://github.com/MrScottyPieey/Sheetablend/wiki

## Credits

Developed by MrScottyPieey

Special thanks to the Blender community for inspiration and feedback.

## Changelog

### Version 1.0.0
- Initial release
- Sprite sheet import
- Animation system
- Frame-by-frame editor
- 2D skeletal rigging
- Weight painting
- IK solver