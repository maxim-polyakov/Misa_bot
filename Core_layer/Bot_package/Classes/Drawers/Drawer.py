from abc import ABC, abstractmethod
from Core_layer.Bot_package.Interfaces import IDrawer
class Drawer(IDrawer.IDrawer):


    """

    That's a class drawer. It describes an image drawing algorithm.

    """
    @classmethod
    def draw(self):

        return ''