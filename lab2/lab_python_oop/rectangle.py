from .geometric_figure import GeometricFigure
from .color import Color

class Rectangle(GeometricFigure):
    NAME = 'Прямоугольник'

    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color = Color(color)

    def area(self) -> float:
        return self.width * self.height

    def __repr__(self) -> str:
        return f"{self.get_name()}: width={self.width}; height={self.height}; color={self.color.color}; area={self.area():.2f}"