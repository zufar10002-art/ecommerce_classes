"""
Модуль с классом Aeroplane для представления самолёта.
"""


class Aeroplane:
    """Класс для представления самолёта с валидацией и сравнением."""

    def __init__(self, icao24: str, callsign: str, country: str,
                 altitude: float, velocity: float, longitude: float, latitude: float):
        """
        Инициализация самолёта.

        Args:
            icao24: Уникальный идентификатор борта
            callsign: Позывной рейса
            country: Страна регистрации
            altitude: Геометрическая высота (м) — не может быть отрицательной
            velocity: Горизонтальная скорость (м/с) — не может быть отрицательной
            longitude: Долгота
            latitude: Широта
        """
        self.icao24 = icao24
        self.callsign = callsign
        self.country = country

        if altitude < 0:
            raise ValueError("Высота не может быть отрицательной")
        self.altitude = altitude

        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self.velocity = velocity

        self.longitude = longitude
        self.latitude = latitude

    def __str__(self) -> str:
        """Человекочитаемое представление самолёта."""
        return (f"{self.callsign} ({self.icao24}) | Страна: {self.country} | "
                f"Высота: {self.altitude} м | Скорость: {self.velocity} м/с")

    def __lt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте (для сортировки по убыванию)."""
        return self.altitude < other.altitude

    def __gt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте (для сортировки по убыванию)."""
        return self.altitude > other.altitude

    @classmethod
    def cast_to_object_list(cls, data: dict) -> list['Aeroplane']:
        """
        Преобразование данных от OpenSky API в список объектов Aeroplane.

        Args:
            data: Словарь с ответом от API (содержит поле "states")

        Returns:
            Список объектов Aeroplane, либо пустой список если данных нет.
        """
        aeroplanes = []
        if not data or "states" not in data:
            return aeroplanes

        states = data.get("states")
        if states is None:
            return aeroplanes

        for state in states:
            if not state or len(state) < 14:
                continue

            icao24 = state[0] or "Unknown"
            callsign = (state[1] or "Unknown").strip()
            country = state[2] or "Unknown"
            altitude = state[13] if state[13] is not None else 0.0
            velocity = state[9] if state[9] is not None else 0.0
            longitude = state[5] if state[5] is not None else 0.0
            latitude = state[6] if state[6] is not None else 0.0

            try:
                aeroplane = cls(icao24, callsign, country,
                                float(altitude), float(velocity),
                                float(longitude), float(latitude))
                aeroplanes.append(aeroplane)
            except ValueError:
                continue
        return aeroplanes
