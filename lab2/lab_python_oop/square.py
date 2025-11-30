from .rectangle import Rectangle

class Square(Rectangle):
    NAME = 'Квадрат'

    def __init__(self, side: float, color: str):
        super().__init__(side, side, color)

    def __repr__(self) -> str:
        return f"{self.get_name()}: side={self.width}; color={self.color.color}; area={self.area():.2f}"