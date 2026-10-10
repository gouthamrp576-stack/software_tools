"""
===========================================================
PART A — MODULAR PYTHON (Random Numbers Processing)
===========================================================
"""

import random
from typing import List, Optional


def generate_numbers(count: int = 10, low: int = 1, high: int = 100) -> List[int]:
    """
    Generate a list of random integers.

    Args:
        count (int): Number of integers to generate.
        low (int): Minimum possible value.
        high (int): Maximum possible value.

    Returns:
        List[int]: List of generated integers.
    """
    return [random.randint(low, high) for _ in range(count)]


def calculate_average(numbers: List[int]) -> Optional[float]:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (List[int]): List of numbers.

    Returns:
        float or None: Average value, or None if list is empty.
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def find_max(numbers: List[int]) -> Optional[int]:
    """
    Find the maximum number in a list.

    Args:
        numbers (List[int]): List of numbers.

    Returns:
        int or None: Maximum value, or None if list is empty.
    """
    if not numbers:
        return None
    return max(numbers)


def main_random_processing():
    """Main workflow for random number processing."""
    numbers = generate_numbers()
    print("Generated numbers:", numbers)

    avg = calculate_average(numbers)
    print("Average:", avg)

    mx = find_max(numbers)
    print("Max:", mx)


# Run Part A
main_random_processing()


"""
===========================================================
PART B — MODULAR PANDAS (Iris Dataset Processing)
===========================================================
"""

import pandas as pd


def load_csv(url: str) -> pd.DataFrame:
    """
    Load a CSV file from a URL.

    Args:
        url (str): URL of the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.

    Raises:
        ValueError: If the CSV cannot be loaded.
    """
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        raise ValueError(f"Failed to load CSV: {e}")


def compute_stat(df: pd.DataFrame, column: str, stat: str):
    """
    Compute a statistical value (mean, max) for a column.

    Args:
        df (pd.DataFrame): DataFrame.
        column (str): Column name.
        stat (str): 'mean' or 'max'.

    Returns:
        float or None: Computed value.

    Raises:
        ValueError: If column does not exist.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    if stat == "mean":
        return df[column].mean()
    elif stat == "max":
        return df[column].max()
    else:
        raise ValueError("Stat must be 'mean' or 'max'.")


def filter_rows(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """
    Filter rows based on a column value.

    Args:
        df (pd.DataFrame): DataFrame.
        column (str): Column name.
        value (str): Value to filter by.

    Returns:
        pd.DataFrame: Filtered DataFrame.

    Raises:
        ValueError: If column does not exist.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    return df[df[column] == value]


def main_pandas_processing():
    """Main workflow for Iris dataset processing."""
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    df = load_csv(url)

    avg_sepal = compute_stat(df, "sepal_length", "mean")
    print("Average sepal length:", avg_sepal)

    max_petal = compute_stat(df, "petal_width", "max")
    print("Max petal width:", max_petal)

    setosa_rows = filter_rows(df, "species", "setosa")
    print("Setosa sample:")
    print(setosa_rows.head())


# Run Part B
main_pandas_processing()
