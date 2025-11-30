from abc import ABC, abstractmethod

class GeometricFigure(ABC):

    @abstractmethod
    def area(self) -> float:
        """Вычислить площадь фигуры."""
        raise NotImplementedError


    @classmethod
    def get_name(cls) -> str:
        """Возвращает название фигуры из поля класса NAME."""
        return getattr(cls, 'NAME', 'Фигура')