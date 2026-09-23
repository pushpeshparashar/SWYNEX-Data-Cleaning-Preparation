import pandas as pd
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "netflix_raw.csv"
OUTPUT_FILE = BASE_DIR / "data" / "netflix_cleaned.csv"
REPORT_FILE = BASE_DIR / "data" / "data_quality_report.csv"

# Load raw dataset
df = pd.read_csv(INPUT_FILE)

# -----------------------------
# 1. Quality checks BEFORE cleaning
# -----------------------------
rows_before = len(df)
duplicates_before = df.duplicated().sum()
missing_before = df.isnull().sum()

# -----------------------------
# 2. Standardize column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -----------------------------
# 3. Remove duplicate records
# -----------------------------
df = df.drop_duplicates().copy()

# -----------------------------
# 4. Clean text columns
# -----------------------------
text_columns = [
    "type",
    "title",
    "director",
    "cast",
    "country",
    "rating",
    "duration",
    "listed_in",
    "description"
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].astype("string").str.strip()

# Standardize category values
df["type"] = df["type"].str.title()
df["rating"] = df["rating"].str.upper()

# -----------------------------
# 5. Convert date_added to date
# -----------------------------
df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

# -----------------------------
# 6. Handle missing values
# -----------------------------

# Text columns
for column in ["director", "cast", "country"]:
    df[column] = df[column].fillna("Unknown")

# Rating
df["rating"] = df["rating"].fillna("Unknown")

# Date
df["date_added"] = df["date_added"].fillna(
    pd.Timestamp("1900-01-01")
)

# -----------------------------
# 7. Validate numeric columns
# -----------------------------
df["release_year"] = pd.to_numeric(
    df["release_year"],
    errors="coerce"
)

# Invalid release years are replaced with missing values
df.loc[
    (df["release_year"] < 1900) |
    (df["release_year"] > pd.Timestamp.now().year),
    "release_year"
] = pd.NA

# -----------------------------
# 8. Clean duration
# -----------------------------
df["duration"] = df["duration"].astype("string").str.strip()

# -----------------------------
# 9. Quality checks AFTER cleaning
# -----------------------------
duplicates_after = df.duplicated().sum()
missing_after = df.isnull().sum()

# -----------------------------
# 10. Save cleaned dataset
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

# -----------------------------
# 11. Create quality report
# -----------------------------
report = pd.DataFrame({
    "column": df.columns,
    "missing_before": [
        missing_before.get(col, 0)
        for col in df.columns
    ],
    "missing_after": [
        missing_after.get(col, 0)
        for col in df.columns
    ],
    "data_type_after": [
        str(df[col].dtype)
        for col in df.columns
    ],
    "unique_values": [
        df[col].nunique(dropna=True)
        for col in df.columns
    ]
})

summary = pd.DataFrame({
    "metric": [
        "Rows before cleaning",
        "Rows after cleaning",
        "Duplicates before cleaning",
        "Duplicates after cleaning",
        "Missing cells before cleaning",
        "Missing cells after cleaning"
    ],
    "value": [
        rows_before,
        len(df),
        duplicates_before,
        duplicates_after,
        missing_before.sum(),
        missing_after.sum()
    ]
})

summary.to_csv(
    REPORT_FILE,
    index=False
)

print("Data cleaning completed successfully.")
print(f"Cleaned dataset: {OUTPUT_FILE}")
print(f"Quality report: {REPORT_FILE}")
