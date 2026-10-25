import pandas as pd
from pathlib import Path

wage_dir = Path("data/processed/processed_wage_tables")
points_dir = Path("data/processed/processed_points_tables")

# --- Load and stack every season ---
all_wages = pd.concat(
    (pd.read_csv(f, encoding="utf-8") for f in sorted(wage_dir.glob("wg_*.csv"))),
    ignore_index=True,
)
all_points = pd.concat(
    (pd.read_csv(f, encoding="utf-8") for f in sorted(points_dir.glob("*.csv"))),
    ignore_index=True,
)

all_wages = all_wages.rename(columns={"Rk": "Wage_Rk"})
all_points = all_points.rename(columns={"Rk": "Points_Rk"})

# --- Merge ---
merged = all_wages.merge(all_points, on=["Squad", "Season"], how="inner")

# --- Clean: turn wage strings into numbers ---
wages = merged["Annual Wages"].str.extract(
    r"£\s*([\d,]+)\s*\(€\s*([\d,]+),\s*\$([\d,]+)"
)
wages.columns = ["Wages_GBP", "Wages_EUR", "Wages_USD"]
wages = wages.apply(lambda col: pd.to_numeric(col.str.replace(",", "", regex=False)))

merged = pd.concat([merged.drop(columns="Annual Wages"), wages], axis=1)

# --- Clean: turn "33%" into 33 ---
merged["% Estimated"] = merged["% Estimated"].str.rstrip("%").astype(int)

# --- Save and check ---
merged.to_csv("data/processed/merged_wages_points.csv", index=False, encoding="utf-8")
print(merged.dtypes)