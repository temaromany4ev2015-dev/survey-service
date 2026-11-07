#!/usr/bin/env python3
"""Трёхточечная оценка (PERT) для историй: story points и часы.

Формулы:
    E  = (O + 4*M + P) / 6      ожидаемое значение
    SD = (P - O) / 6            стандартное отклонение

Итоговые story points = ближайшее число Фибоначчи к E (при равенстве расстояний берётся большее).

Использование (из корня репозитория):
    python scripts/three_point.py
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "docs" / "01-planning" / "data"
FIB = [1, 2, 3, 5, 8, 13, 21]


def pert(o, m, p):
    return (o + 4 * m + p) / 6, (p - o) / 6


def nearest_fib(x):
    return min(FIB, key=lambda f: (abs(f - x), -f))


def read(name):
    with open(DATA / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    print("Story points (O, M, P -> E, SD, итог)")
    total_sp = 0
    rows = []
    for r in read("estimates.csv"):
        o, m, p = (float(r[k]) for k in ("sp_o", "sp_m", "sp_p"))
        e, sd = pert(o, m, p)
        sp = nearest_fib(e)
        total_sp += sp
        rows.append((r["id"], r["title"], o, m, p, e, sd, sp))
        print(f"{r['id']}  O={o:g} M={m:g} P={p:g}  E={e:.2f}  SD={sd:.2f}  SP={sp}  ({r['title']})")
    print(f"Сумма итоговых SP: {total_sp}")
    print("Разброс P-O (для выбора самых неопределённых):")
    for r in sorted(rows, key=lambda x: -(x[4] - x[2])):
        print(f"  {r[0]}: P-O = {r[4] - r[2]:g}")

    print("\nЧасы (PERT)")
    tot_e = tot_var = 0
    for r in read("pert_hours.csv"):
        o, m, p = (float(r[k]) for k in ("h_o", "h_m", "h_p"))
        e, sd = pert(o, m, p)
        tot_e += e
        tot_var += sd ** 2
        print(f"{r['id']}  O={o:g} M={m:g} P={p:g}  E={e:.2f} ч  SD={sd:.2f} ч  Var={sd**2:.2f}")
    print(f"Сумма E = {tot_e:.2f} ч; суммарное SD = {math.sqrt(tot_var):.2f} ч (корень из суммы дисперсий)")


if __name__ == "__main__":
    main()
