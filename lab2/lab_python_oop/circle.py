import math
from .geometric_figure import GeometricFigure
from .color import Color

class Circle(GeometricFigure):
    NAME = 'Круг'

    def __init__(self, radius: float, color: str):
        self.radius = float(radius)
        self.color = Color(color)

    def area(self) -> float:
        return math.pi * (self.radius ** 2)

    def __repr__(self) -> str:
        return f"{self.get_name()}: radius={self.radius}; color={self.color.color}; area={self.area():.2f}"