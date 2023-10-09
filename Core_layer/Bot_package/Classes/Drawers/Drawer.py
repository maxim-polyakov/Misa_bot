from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IDrawer
class Drawer(IDrawer.IDrawer):

    @classmethod
    def draw(self):

        return ''