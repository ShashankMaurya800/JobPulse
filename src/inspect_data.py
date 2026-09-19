import pandas as pd

FILE_PATH = "data/raw/indian-job-market-dataset-2025.xlsx"

df = pd.read_excel(FILE_PATH)

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== UNIQUE JOB IDS =====")
print(df["jobId"].nunique())