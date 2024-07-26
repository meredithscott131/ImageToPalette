from krita import DockWidgetFactory, DockWidgetFactoryBase
from .ImageToPalette import ImageToPalette

# Defining an ID for the docker
DOCKER_ID = 'image_to_palette_docker'

# Getting the current instance of Krita
instance = Krita.instance()

# Creating a factory for the docker widget
dock_widget_factory = DockWidgetFactory(DOCKER_ID, #ID
                                        DockWidgetFactoryBase.DockRight, # Default docking position
                                        ImageToPalette # Class of the docker widget
                                        )

# Registering the docker widget factory with Krita
instance.addDockWidgetFactory(dock_widget_factory)
