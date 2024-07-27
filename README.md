# Image to Palette
A [Krita](https://krita.org/en/) docker plugin for quickly generating color palettes from images.

Inspiration: Procreate's [Palette Capture](https://help.procreate.com/procreate/handbook/colors/colors-palettes) feature and [PaletteGenerator](https://github.com/kaichi1342/PaletteGenerator?tab=readme-ov-file).
## Breakdown
<img src="screenshots\breakdown.png" width="250"></img>

| # | Feature | Description |
|---|---------|-------------|
| 1 | Create Palette From Image | Button to load a new palette from an image file. |
| 2 | Load Palette | Button to load a palette JSON file.
| 3 | Save Palette | Button to save the current palette data as a JSON file.
| 4 | Regenerate Palette | Button that regenerates the color palette from the currently loaded image. |
| 5 | Recent Palette History | Drop-down that lists the 5 most recently opened palette JSON files to select from.
| 6 | Source Image Name | Name of the loaded palette's source image.
| 7 | Generated Color Output | Grid of the selectable colors pulled from the image. |

## Demo
<video src="screenshots\demo.mp4" controls></video>
v1.1.0

## Setup

### Download
[ZIP](https://github.com/meredithscott131/ImageToPalette/archive/refs/heads/main.zip)

### Install
1. Open Krita
2. Go to ```Tools``` &#8594; ```Scrips``` &#8594; ```Import Python Plugin from File```
3. Select **image_to_palette_plugin.zip**
4. Restart Krita
5. Enable Image to Palette by going to ```Settings``` &#8594; ```Configure Krita``` &#8594; ```Python Plugin Manager```
6. Restart Krita
7. Go to ```Settings``` &#8594; ```Dockers``` and enable ```Image to Palette```. 

### Tested Platforms
Krita 5.2.3

07/26/2024 **v1.1.0**
- Added saving and JSON palette files.
- Implemented drag-and-drop functionality.
- Added recent palette history.
- Improved error handling.

### License
Image to Palette is shared under the GNU General Public License (GPL), version 3.
