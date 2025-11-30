class Color:
    """Класс-хранилище цвета с проверкой через property."""

    def __init__(self, color: str):
        self._color = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        if not isinstance(value, str):
            raise TypeError('color must be a string')
        if not value:
            raise ValueError('color must not be empty')
        self._color = value

    def __repr__(self) -> str:
        return "Color({})".format(self._color)