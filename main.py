"""
Главный модуль для взаимодействия с пользователем.
"""
from src.api import OpenSkyAPI
from src.aeroplane import Aeroplane
from src.file_saver import JSONSaver


def filter_aeroplanes_by_country(aeroplanes: list, countries: list) -> list:
    """Фильтрует самолёты по списку стран регистрации."""
    if not countries:
        return aeroplanes
    return [a for a in aeroplanes if a.country in countries]


def filter_aeroplanes_by_altitude(aeroplanes: list, min_alt: float, max_alt: float) -> list:
    """Фильтрует самолёты по диапазону высот."""
    return [a for a in aeroplanes if min_alt <= a.altitude <= max_alt]


def sort_aeroplanes_by_altitude(aeroplanes: list, reverse: bool = True) -> list:
    """Сортирует самолёты по высоте."""
    return sorted(aeroplanes, key=lambda a: a.altitude, reverse=reverse)


def get_top_aeroplanes(aeroplanes: list, top_n: int) -> list:
    """Возвращает топ N самолётов."""
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list) -> None:
    """Выводит список самолётов в консоль."""
    if not aeroplanes:
        print("Самолёты не найдены.")
        return
    for i, plane in enumerate(aeroplanes, 1):
        print(f"{i}. {plane}")


def user_interaction() -> None:
    """Основная функция взаимодействия с пользователем."""
    print("Добро пожаловать в программу по поиску самолётов!")

    country = input("Введите название страны: ").strip()
    if not country:
        print("Страна не введена. Завершение программы.")
        return

    print(f"Поиск самолётов для страны: {country}...")

    api = OpenSkyAPI()
    data = api.get_aeroplanes(country)

    if not data:
        print("Не удалось получить данные или страна не найдена.")
        return

    aeroplanes = Aeroplane.cast_to_object_list(data)

    if not aeroplanes:
        print("Самолёты в данном регионе не найдены.")
        return

    # Сохраняем в JSON
    saver = JSONSaver()
    for plane in aeroplanes:
        saver.add_aeroplane(plane)

    print(f"Найдено {len(aeroplanes)} самолётов. Данные сохранены.")

    # Фильтрация по стране регистрации
    filter_countries = input(
        "Введите страны регистрации для фильтрации (через пробел, или оставьте пустым): "
    ).strip().split()
    filtered = filter_aeroplanes_by_country(aeroplanes, filter_countries)

    # Фильтрация по диапазону высот
    alt_range = input("Введите диапазон высот (мин макс, через пробел): ").strip()
    min_alt, max_alt = 0, float("inf")
    if alt_range:
        parts = alt_range.split()
        if len(parts) >= 1 and parts[0].isdigit():
            min_alt = float(parts[0])
        if len(parts) >= 2 and parts[1].isdigit():
            max_alt = float(parts[1])
    filtered = filter_aeroplanes_by_altitude(filtered, min_alt, max_alt)

    if not filtered:
        print("После фильтрации самолёты не найдены.")
        return

    # Топ N по высоте
    try:
        top_n = int(input("Введите количество самолётов для топа по высоте: "))
    except ValueError:
        top_n = 5

    sorted_planes = sort_aeroplanes_by_altitude(filtered, reverse=True)
    top_planes = get_top_aeroplanes(sorted_planes, top_n)

    print(f"\nТоп {top_n} самолётов по высоте:")
    print_aeroplanes(top_planes)


if __name__ == "__main__":
    user_interaction()
