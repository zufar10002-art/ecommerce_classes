"""
Модуль с абстрактным классом для работы с API и реализацией для OpenSky.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import requests


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с API."""

    @abstractmethod
    def get_country_boundingbox(self, country: str) -> Optional[List[str]]:
        """Получение boundingbox страны через Nominatim API."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> Optional[Dict]:
        """Получение данных о самолётах через OpenSky API."""
        pass


class OpenSkyAPI(BaseAPI):
    """Класс для работы с API OpenSky и Nominatim."""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.headers = {"User-Agent": "coursework-app/1.0"}

    def get_country_boundingbox(self, country: str) -> Optional[List[str]]:
        """
        Получение boundingbox страны.

        Args:
            country: Название страны

        Returns:
            Список [юг, север, запад, восток] или None, если страна не найдена.
        """
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        try:
            response = requests.get(
                self.nominatim_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0].get("boundingbox")
            return None
        except (requests.RequestException, KeyError, IndexError):
            return None

    def get_aeroplanes(self, country: str) -> Optional[Dict]:
        """
        Получение данных о самолётах в воздушном пространстве страны.

        Args:
            country: Название страны

        Returns:
            Словарь с ответом OpenSky API или None в случае ошибки.
        """
        boundingbox = self.get_country_boundingbox(country)
        if not boundingbox:
            return None

        lamin, lamax, lomin, lomax = boundingbox
        params = {
            "lamin": lamin,
            "lamax": lamax,
            "lomin": lomin,
            "lomax": lomax,
        }
        try:
            response = requests.get(
                self.opensky_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
