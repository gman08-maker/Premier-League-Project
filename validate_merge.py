def validate_merge(merged_df):
    """
    Validates the merged DataFrame for Premier League data.
    It checks for the following:
    1. The merged DataFrame does not contain any missing values.
    2. The merged DataFrame has the expected number of rows based on the number of unique teams and seasons.

    Args:
        merged_df (pd.DataFrame): The merged DataFrame to validate.
    Returns:
        bool: True if all validations pass, otherwise raises an appropriate error
    """
    # Check if the merged DataFrame contains any missing values
    if merged_df.isna().sum().sum() != 0:
        raise ValueError("Merged DataFrame contains missing values.")

    # Check if the merged DataFrame has the expected number of 200 rows

    expected_rows = 200

    actual_rows = merged_df.shape[0]
    if actual_rows != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows in the merged DataFrame, but found {actual_rows}.")

    if merged_df[merged_df["_merge"] != "both"].shape[0] > 0:
        raise ValueError("Merged DataFrame contains rows that are not present in both datasets.")

    return True