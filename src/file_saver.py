"""
Модуль для сохранения и загрузки данных о самолётах в JSON-файл.
"""
import json
import os
from typing import List

from src.aeroplane import Aeroplane


class JSONSaver:
    """Класс для работы с JSON-файлом."""

    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Создаёт директорию для файла, если её нет."""
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_data(self) -> List[dict]:
        """Загружает данные из JSON-файла."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: List[dict]) -> None:
        """Сохраняет данные в JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавляет самолёт в файл.

        Args:
            aeroplane: Объект Aeroplane
        """
        data = self._load_data()
        # Проверяем, нет ли уже такого самолёта по icao24
        for item in data:
            if item.get("icao24") == aeroplane.icao24:
                return
        data.append(aeroplane.__dict__)
        self._save_data(data)

    def get_aeroplanes(self) -> List[Aeroplane]:
        """
        Загружает все самолёты из файла.

        Returns:
            Список объектов Aeroplane
        """
        data = self._load_data()
        aeroplanes = []
        for item in data:
            try:
                aeroplane = Aeroplane(
                    icao24=item["icao24"],
                    callsign=item["callsign"],
                    country=item["country"],
                    altitude=item["altitude"],
                    velocity=item["velocity"],
                    longitude=item["longitude"],
                    latitude=item["latitude"]
                )
                aeroplanes.append(aeroplane)
            except (KeyError, ValueError):
                continue
        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Удаляет самолёт из файла.

        Args:
            aeroplane: Объект Aeroplane
        """
        data = self._load_data()
        data = [item for item in data if item.get("icao24") != aeroplane.icao24]
        self._save_data(data)
