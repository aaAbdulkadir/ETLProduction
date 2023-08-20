import pandas as pd

def change_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Changes the data types to the required types
    from the transform dataframe

    Args:
        df (pd.DataFrame): The dataframe

    returns:
        df (pd.DataFrame): The final transformed data
    """
    df = df.astype({'Rk':'int', 'Age':'int'})

    return df