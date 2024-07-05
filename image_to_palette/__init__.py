from krita import DockWidgetFactory, DockWidgetFactoryBase
from .ImageToPalette import ImageToPalette

DOCKER_ID = 'image_to_palette_docker'
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        ImageToPalette)

instance.addDockWidgetFactory(dock_widget_factory)
