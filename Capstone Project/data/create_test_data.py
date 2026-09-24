"""Generates data/test_data.xlsx (run once: python data/create_test_data.py)."""
from pathlib import Path
from openpyxl import Workbook

rows = [
    ("search_term", "expected_name", "extra_quantity"),
    ("Blue Top", "Blue Top", 2),
    ("Men Tshirt", "Men Tshirt", 3),
    ("Sleeveless Dress", "Sleeveless Dress", 1),
]

wb = Workbook()
ws = wb.active
ws.title = "Products"
for r in rows:
    ws.append(r)
for col, width in zip("ABC", (22, 22, 16)):
    ws.column_dimensions[col].width = width

out = Path(__file__).with_name("test_data.xlsx")
wb.save(out)
print(f"Created {out}")
