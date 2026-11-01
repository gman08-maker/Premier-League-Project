# Premier-League-Project
# Does Money Buy Points? Premier League Wages vs. Performance (2013-14 to 2022-23)

How strongly is a club's wage bill associated with its league performance, and do some clubs consistently beat or miss what their wages predict?

This project cleans and merges FBref wage and league-table data for ten Premier League seasons (200 club-seasons), then uses correlation, regression, and residual analysis to answer that question.

The motivating example is Leicester City's 2015-16 title: one of the smaller wage bills in the league, yet champions. Was that a one-off, or do some clubs reliably do more with less?

---

## Key findings

| Question | Result |
|---|---|
| How much of the variation in points do wages explain? | About half. Regressing points on log wage share gives **R² = 0.51** (Pearson r = 0.72, Spearman ρ = 0.71). |
| How big is the effect? | Slope of about **24 points per unit of log wage share**, roughly **+17 points for a doubling of wage share** (clustered 95% CI for the slope: 18.2 to 29.9, or about +13 to +21 points per doubling). |
| Is it stable across seasons? | Always positive, but it varies. Per-season Spearman ranges from **0.49 (2015-16)** to **0.87 (2017-18)**, with no clear trend over the decade. |
| Which clubs consistently beat their wages? | Over long stays: **Liverpool, Manchester City, and Tottenham** (average residual of about +10 to +12 points). Short-stay clubs such as Brentford and Sheffield United have larger averages but too few seasons to be reliable. |
| Which clubs consistently miss? | Over long stays: **Manchester United** (about -8), Aston Villa, Everton, Crystal Palace, and West Ham. The most negative averages (QPR, Middlesbrough, Huddersfield, Sunderland) come from one to a few seasons, often ending in relegation. |
| Does overperformance persist? | Moderately. A club's residual correlates about **0.42** with its own residual from the previous season. This is preliminary, and part of it likely reflects model misfit and omitted club traits rather than efficiency. |

All results describe **association, not causation**. Successful clubs earn more revenue and can then pay higher wages, so the arrow runs both ways.

---

## Data

- **Source:** [FBref](https://fbref.com/), collected 16 October 2026. Each season has two tables: annual wages and the final league table.
- **Scope:** 2013-14 through 2022-23, 20 clubs per season, 200 club-seasons, 33 distinct clubs.
- **Caveat:** wage figures are FBref estimates, not audited payroll and not an exact measure of first-team pay. The `% Estimated` column records how much of each figure is estimated, and early seasons are largely or fully estimated.

### Merged dataset columns

| Column | Meaning |
|---|---|
| `Squad`, `Season` | Club and season (e.g. `2015_16`). Together they form the merge key. |
| `Wage_Rk`, `Points_Rk` | Rank by wages and by league finish within the season |
| `Wages_GBP`, `Wages_EUR`, `Wages_USD` | Annual wages parsed from FBref's text string |
| `% Estimated` | Share of the wage figure that is estimated |
| `# Pl` | Players used |
| `MP`, `W`, `D`, `L`, `GD`, `Pts` | Standard league table columns |

### Derived variables (added in the notebook)

- **`Wage_Share`** = club wages divided by the league's total wages that season. Normalising within each season removes inflation, so a 2014 club and a 2022 club are comparable.
- **`Log_Wage_Share`** = natural log of `Wage_Share`. Raw wages are heavily right-skewed, and the log gives a closer-to-linear relationship with points.
- **`Rank_Gap`** = `Wage_Rk` - `Points_Rk`. Positive means the club finished higher than its wage rank.

---

## Method

1. **Load and validate each season** (`season_loader.py`, `validators.py`). Raw FBref HTML is read into a DataFrame with a `Season` column, then checked: 20 rows, no missing values, goal difference sums to 0, `Pts = 3W + D`, and `MP = W + D + L`.
2. **Merge wages and points** (`merged_data.py`). Seasons are stacked, merged on `Squad` + `Season`, and the wage text (e.g. `£113,254,000 (€135,062,723, $137,628,660)`) is parsed into numeric GBP, EUR, and USD columns.
3. **Exploratory analysis** (`Exploratory_data.ipynb`). Distributions, league-wide wage growth, wage vs points scatterplots, Pearson and Spearman correlations (pooled and per season), wage-rank vs points-rank, and club-level averages.
4. **Model.** OLS of `Pts ~ Log_Wage_Share` with standard errors clustered by club, since the same clubs appear in many seasons. Diagnostics: residuals vs fitted values and a Q-Q plot.
5. **Residual analysis.** Average residual per club shows who consistently beats or misses the line. A persistence test correlates each club's residual with its previous season's.

---

## Predictions vs. results

Before the analysis, I wrote down what I expected. Here is how it held up.

| Prediction | Outcome |
|---|---|
| The relationship will be relatively strong | **Supported.** r ≈ 0.72, R² ≈ 0.51. Strong, but half the variation is left unexplained. |
| Manchester City, Manchester United, Chelsea, Liverpool, Tottenham, and Arsenal will beat their wages | **Mostly supported.** City, Liverpool, and Tottenham are clearly positive, Arsenal and Chelsea slightly positive, and **Manchester United is negative**. Positive top-club residuals are also partly an artifact of the straight line underfitting the top of the range. |
| Clubs expected to perform poorly will miss their wages | **Not directly testable here**, since no performance-based forecast was built. The most negative clubs are short-stay clubs that were relegated, which produces negative residuals almost by construction. |
| Leicester (motivating example) | **A one-off.** Their 2015-16 gap is the largest in the data (wage rank 17, points rank 1), but their ten-year average residual is close to zero. |

---

## Figures

**Wages explain a lot of the ranking, but not equally every season**
![Per-season Spearman correlation]

**Wage rank vs points rank (red line = finished exactly where wages predicted)**
![Wage rank vs points rank]

**Club averages show a clear top tier, and a noisy, flatter relationship below it**
![Average wage share vs average points]

**Model diagnostics: mild curvature, wider spread at the extremes, right-skewed residuals**
![Residuals vs fitted]
![Q-Q plot]

**Average residual by club**
![Average residual by club]

---

## Repository structure

```
.
├── Exploratory_data.ipynb      # EDA, regression, residuals, persistence test
├── season_loader.py            # Reads one raw FBref HTML file into a DataFrame
├── validators.py               # Sanity checks on a single season table
├── merged_data.py              # Stacks seasons, merges wages + points, parses wage text
├── validate_merge.py           # Sanity checks on the merged table
├── requirements.txt            # Pinned dependencies
├── figures/                    # Exported plots used in this README
└── data/
    ├── raw/                    # Saved FBref HTML pages (folder name may differ)
    └── processed/
        ├── processed_wage_tables/     # wg_<season>.csv
        ├── processed_points_tables/   # <season>.csv
        └── merged_datasets/           # merged_wages_points.csv
```

---

## Reproducing the analysis

```bash
git clone https://github.com/<gman08-maker>/<Premier-League-Project>.git
cd <Premier-League-Project>
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The pinned versions look resolved for Python 3.9, so use 3.9 or newer.

1. **Collect the raw tables.** Save each season's FBref wage and league-table pages as `.html` files. `load_season` requires the season string (e.g. `2013_14`) to appear in the file name and the page to contain exactly one table.
2. **Load, validate, and save per-season CSVs** into `data/processed/processed_wage_tables/` (named `wg_<season>.csv`) and `data/processed/processed_points_tables/`.
3. **Merge:**
   ```bash
   python merged_data.py
   ```
4. **Run the analysis:** open `Exploratory_data.ipynb` and run all cells.

---

## Limitations

- **Wages are estimates**, and they are a partial picture of cost. Transfer fees, academy value, and revenue are not captured, so "overperformer" means relative to wages only.
- **Observations are not independent.** The same clubs recur across seasons, so effective sample size is smaller than 200. Clustered standard errors help, but the 200 points are not 200 independent draws.
- **A straight line in log wage share is only approximate.** Residuals show mild curvature and wider spread at the richest and poorest ends, so extreme club averages partly reflect model shape.
- **Uneven club tenure.** Clubs that appear for one or two seasons have noisy averages, and many of them are in the sample because they were relegated.
- **Ten seasons, one league.** Nothing here says whether the pattern holds elsewhere or in other periods.
- **Association only.** Wages are often set before points are earned, and success drives revenue.

---

## Known issues / Still Working On

- [ ] **Persistence interval.** The 95% interval (about 0.29 to 0.54) ignores that pairs overlap and cluster within clubs, so it is too narrow. Cluster by club or bootstrap by club.
- [ ] **Separate persistence from misfit.** Refit with a quadratic term or club effects and see how much of the 0.42 survives.

---

## Data source and licence

Data comes from FBref (Sports Reference Data). 
