#!/usr/bin/env python3
"""Поправка PERT на одного исполнителя (ЛР 1, задание 1.5).

pert_cpm.py считает срок по критическому пути, то есть предполагает, что
независимые истории делаются параллельно. Один человек параллельно работать
не может, поэтому реальный срок — сумма длительностей ВСЕХ историй.
Скрипт считает вероятность уложиться в дедлайн для такого случая и для
сценариев «выбросить историю».

Запуск:
    python scripts/pert_single_worker.py docs/01-planning/data/tasks.csv --deadline 46.2 --drop US-10
"""
import argparse
import csv
import math


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def calc(rows, deadline):
    e = sum((r["o"] + 4 * r["m"] + r["p"]) / 6 for r in rows)
    var = sum(((r["p"] - r["o"]) / 6) ** 2 for r in rows)
    s = math.sqrt(var)
    return e, s, phi((deadline - e) / s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--deadline", type=float, required=True)
    ap.add_argument("--drop", action="append", default=[], help="id истории, которую исключить (можно несколько раз)")
    a = ap.parse_args()
    with open(a.csv, encoding="utf-8-sig") as f:
        rows = [{"id": r["id"], "o": float(r["o"]), "m": float(r["m"]), "p": float(r["p"])} for r in csv.DictReader(f)]
    for title, rs in (("Все истории MVP", rows), (f"Без {', '.join(a.drop) or '—'}", [r for r in rows if r["id"] not in a.drop])):
        e, s, pr = calc(rs, a.deadline)
        z85 = e + 1.04 * s
        print(f"{title}: {len(rs)} ист., E = {e:.2f} ч, σ = {s:.2f} ч, срок с P=85%: {z85:.2f} ч, вероятность уложиться в {a.deadline:g} ч: {pr * 100:.1f}%")


if __name__ == "__main__":
    main()