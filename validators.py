def validate_season(season_df):
    """
    Validates the given DataFrame for a Premier League season.
    It checks for the following:
    1. The DataFrame has exactly 20 rows (teams).
    2. The DataFrame does not contain any missing values.
    3. The Goal Difference (GD) column sums to 0.
    4. The Points (Pts) column matches the expected value based on wins and draws.
    5. The total matches played (MP) for each team equals the sum of wins, draws, and losses.

    Args:
        season_df (pd.DataFrame): The DataFrame to validate.
    Returns:
        bool: True if all validations pass, otherwise raises an appropriate error.
    """
    # Checks if the DataFrame has 20 teams
    row_count = season_df.shape[0]
    if row_count != 20:
        raise ValueError(f"Expected 20 rows in the DataFrame, but found {row_count}.")

    # Checks if the DataFrame contains any missing values
    if season_df.isna().sum().sum() != 0:
        raise ValueError("DataFrame contains missing values.")

    # Checks if Goal Difference (GD) column sums to 0
    count = 0
    for point in season_df['GD']:
        count += point
    if count != 0:
        raise ValueError(f"Expected the sum of the 'GD' column to be 0, but found {count}.")

    # Check if Points (Pts) match (3 * W + D)
    expected_pts = season_df['W'] * 3 + season_df['D']
    pts_mismatch = season_df[season_df['Pts'] != expected_pts]

    if not pts_mismatch.empty:
        invalid_teams = pts_mismatch['Squad'].tolist()
        raise ValueError(f"Points do not match for teams: {invalid_teams}")

    # Check if Matches Played (MP) match (W + D + L)
    expected_mp = season_df['W'] + season_df['D'] + season_df['L']
    mp_mismatch = season_df[season_df['MP'] != expected_mp]

    if not mp_mismatch.empty:
        invalid_teams = mp_mismatch['Squad'].tolist()
        raise ValueError(f"Total matches (MP) do not sum to W-D-L for teams: {invalid_teams}")


    return True

