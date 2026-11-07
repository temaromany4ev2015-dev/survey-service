#!/usr/bin/env python3
"""WSJF: приоритизация историй (ЛР 1, задание 1.4).

    WSJF = (ценность + срочность + снижение риска) / размер

Ценность, срочность и снижение риска оцениваются по шкале Фибоначчи
(1, 2, 3, 5, 8, 13), размер берётся из оценки в story points.

Читает docs/01-planning/data/wsjf.csv, печатает таблицу по убыванию WSJF
и записывает docs/01-planning/data/release_backlog.csv в формате
release_planner.py (value = ценность + срочность + снижение риска,
effort = размер в story points).

Использование (из корня репозитория):
    python scripts/wsjf.py
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "docs" / "01-planning" / "data"
FIB = {1, 2, 3, 5, 8, 13, 21}


def main():
    with open(DATA / "wsjf.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        for key in ("biz_value", "time_criticality", "risk_reduction"):
            if int(r[key]) not in FIB:
                raise SystemExit(f"{r['id']}: {key}={r[key]} не из шкалы Фибоначчи")
        r["cod"] = int(r["biz_value"]) + int(r["time_criticality"]) + int(r["risk_reduction"])
        r["size"] = int(r["size_sp"])
        r["wsjf"] = r["cod"] / r["size"]

    print(f"{'ID':<6}{'V':>3}{'T':>4}{'R':>4}{'CoD':>5}{'SP':>4}{'WSJF':>7}  История")
    for r in sorted(rows, key=lambda x: (-x["wsjf"], x["id"])):
        print(f"{r['id']:<6}{r['biz_value']:>3}{r['time_criticality']:>4}{r['risk_reduction']:>4}"
              f"{r['cod']:>5}{r['size']:>4}{r['wsjf']:>7.2f}  {r['title']}")

    out = DATA / "release_backlog.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "value", "effort", "depends_on", "must"])
        for r in rows:
            w.writerow([r["id"], r["title"], r["cod"], r["size"], r["depends_on"], r["must"]])
    print(f"\nЗаписано: {out.relative_to(DATA.parent.parent.parent)}")


if __name__ == "__main__":
    main()
