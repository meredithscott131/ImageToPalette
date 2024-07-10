# Image to Palette
A docker plugin for [Krita](https://krita.org/en/) that allows you to quickly generate color palettes from images.

Inspiration: [PaletteGenerator](https://github.com/kaichi1342/PaletteGenerator?tab=readme-ov-file)

## Breakdown
<img src="screenshots\interfaceBreakdown.png" width="500"></img>

| Feature | Description |
| ----------- | ----------- |
| Load Image | Button that launches the dialog to select an image file. |
| Regenerate Palette | Button that regenerates the color palette from the current loaded image. |
| Generated Color Output | Grid of selectable colors. |

## Demo
<video src="screenshots\demo.mp4" controls></video>
Done with v1.0.0

## Setup

### Download
[ZIP](https://github.com/meredithscott131/ImageToPalette/archive/refs/heads/main.zip)

### Install
1. Open Krita
2. Go to **Tools** &#8594; **Scrips** &#8594; **Import Python Plugins**
3. Select **image_to_palette_plugin.zip**
4. Restart Krita
5. Enable Image to Palette by going to **Settings** &#8594; **Configure Krita** &#8594; **Python Plugin Manager**
6. Restart Krita
7. Go to **Settings** &#8594; **Dockers** and enable **Image to Palette**. 

### Tested Platforms
Krita 5.2.3

### Release Log
07/04/2024 **Version 1.0.0**
- First released version

07/08/2024 **Version 1.1.0**
- Added drag and drop
- Added saving

### License
Image to Palette is shared under the GNU General Public License (GPL), version 3.