# Represents a set of dominant colors in an image
class Palette:
    def __init__(self):
        self.image_name = None  # Name of the original image source
        self.cur_colors = []  # List of the current displayed colors
        self.total_colors = []  # List of the total colors found in the image
    
    # Adds the given color to the current list of colors
    def add_color(self, color):
        self.cur_colors.append(color)

    # Clears the current list of colors
    def clear_colors(self):
        self.cur_colors = []

    # Initializes the palette from a json file
    def from_json(self, data):
        self.image_name = data.get("image_name", "")
        self.cur_colors = data.get("current_colors", [])
        self.total_colors = [(color, count) for color, count in data.get("total_colors", [])]
    
    # Converts the palette to a json file
    def to_json(self):
        return {
            "current_colors": self.cur_colors,
            "total_colors": [(color, count) for color, count in self.total_colors],
            "image_name": self.image_name
        }