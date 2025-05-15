import csv
import os
from typing import Dict, List, Set
import requests
from collections import defaultdict

API_URL = "https://ru.wikipedia.org/w/api.php"
CATEGORY = "Категория:Животные_по_алфавиту"


# Так как реализация выполнена через API, возможны небольшие различия в данных по сравнению с парсингом каждой отдельной страницы через переход к следующей
def fetch_all_animals() -> List[str]:
    session = requests.Session()
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": CATEGORY,
        "cmlimit": "500",
        "format": "json",
    }
    animals: List[str] = []
    while True:
        res = session.get(API_URL, params=params)
        res.raise_for_status()
        data = res.json()
        animals += [
            m["title"].strip() for m in data.get("query", {}).get("categorymembers", [])
        ]
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break
        params["cmcontinue"] = cont
    return animals


def count_by_first_letter(names: List[str]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    seen: Set[str] = set()
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        ch: str = name[0].upper()
        if "\u0400" <= ch <= "\u04ff":
            counts[ch] += 1
    return counts


def save_to_csv(counts: Dict[str, int], filename: str = "beasts.csv") -> None:
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for letter, count in counts.items():
            writer.writerow([letter, count])


def main() -> None:
    animals: List[str] = fetch_all_animals()
    counts: Dict[str, int] = count_by_first_letter(animals)
    save_to_csv(counts)
    print(f"Всего животных: {len(animals)}")
    print("Результаты сохранены в beasts.csv")


# ---Тесты---
def test_count_by_first_letter():
    names = ["Аист", "Архар", "Белка", "Барсук", "Ёж", "Енот", "Ёж"]
    result = count_by_first_letter(names)
    assert result["А"] == 2
    assert result["Б"] == 2
    assert result["Е"] == 1
    assert result["Ё"] == 1
    assert "Ж" not in result
    print("test_count_by_first_letter passed")


def test_save_to_csv():
    test_counts = {"А": 2, "Б": 3}
    test_filename = "test_output.csv"
    save_to_csv(test_counts, test_filename)
    with open(test_filename, encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
    assert lines == ["А,2", "Б,3"]
    os.remove(test_filename)
    print("test_save_to_csv passed")


if __name__ == "__main__":
    test_count_by_first_letter()
    test_save_to_csv()
    main()
