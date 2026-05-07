"""
Тесты для класса Aeroplane.
"""
import pytest

from src.aeroplane import Aeroplane


class TestAeroplane:
    """Тесты для класса Aeroplane."""

    def test_aeroplane_creation_valid(self):
        """Создание самолёта с корректными данными."""
        plane = Aeroplane("abc123", "TEST123", "France", 10000.0, 200.0, 2.0, 48.0)
        assert plane.icao24 == "abc123"
        assert plane.callsign == "TEST123"
        assert plane.country == "France"
        assert plane.altitude == 10000.0
        assert plane.velocity == 200.0
        assert plane.longitude == 2.0
        assert plane.latitude == 48.0

    def test_aeroplane_negative_altitude_raises_error(self):
        """Отрицательная высота вызывает ValueError."""
        with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
            Aeroplane("abc123", "TEST123", "France", -100.0, 200.0, 2.0, 48.0)

    def test_aeroplane_negative_velocity_raises_error(self):
        """Отрицательная скорость вызывает ValueError."""
        with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
            Aeroplane("abc123", "TEST123", "France", 10000.0, -50.0, 2.0, 48.0)

    def test_aeroplane_str(self):
        """Проверка строкового представления."""
        plane = Aeroplane("abc123", "TEST123", "France", 10000.0, 200.0, 2.0, 48.0)
        assert "TEST123 (abc123)" in str(plane)
        assert "France" in str(plane)
        assert "10000.0" in str(plane)
        assert "200.0" in str(plane)

    def test_aeroplane_lt(self):
        """Сравнение по высоте (меньше)."""
        low = Aeroplane("a", "A", "C1", 1000.0, 200.0, 0.0, 0.0)
        high = Aeroplane("b", "B", "C2", 2000.0, 200.0, 0.0, 0.0)
        assert low < high
        assert not high < low

    def test_aeroplane_gt(self):
        """Сравнение по высоте (больше)."""
        low = Aeroplane("a", "A", "C1", 1000.0, 200.0, 0.0, 0.0)
        high = Aeroplane("b", "B", "C2", 2000.0, 200.0, 0.0, 0.0)
        assert high > low
        assert not low > high

    def test_cast_to_object_list_empty(self):
        """Пустые данные возвращают пустой список."""
        result = Aeroplane.cast_to_object_list(None)
        assert result == []

        result = Aeroplane.cast_to_object_list({})
        assert result == []

        result = Aeroplane.cast_to_object_list({"states": None})
        assert result == []

    def test_cast_to_object_list_valid(self):
        """Преобразование валидных данных."""
        data = {
            "states": [
                ["icao1", "CALL1", "France", None, None, 2.0, 48.0, None, None, 200.0, None, None, None, 10000.0]
            ]
        }
        result = Aeroplane.cast_to_object_list(data)
        assert len(result) == 1
        assert result[0].icao24 == "icao1"
        assert result[0].callsign == "CALL1"
        assert result[0].altitude == 10000.0
        assert result[0].velocity == 200.0
