import pandas as pd
from pathlib import Path
from season_loader import load_season
from validate_merge import validate_merge
from validators import validate_season
#file_path = 'data/raw/wages_tables_raw/wg_2022_23.html'
#season_df = load_season(file_path, '2022_23')
# print(validate_season(season_df))
#print(season_df.head())
#season_df.to_csv(Path('data/processed/processed_wage_tables/wg_2022_23.csv'), index=False)
merged_df = pd.read_csv('data/processed/merged_datasets/merged_wages_points.csv')
print(validate_merge(merged_df))