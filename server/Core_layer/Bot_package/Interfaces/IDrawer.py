from abc import ABC, abstractmethod

class IDrawer:
    """
    It is entity of drawing
    """
    @abstractmethod
    def draw(self):
        pass