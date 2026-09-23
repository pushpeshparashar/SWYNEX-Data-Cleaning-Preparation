# SWYNEX Data Cleaning & Preparation – Netflix Dataset

## Task 1

This project focuses on cleaning and preparing a raw Netflix Movies and TV Shows dataset for analysis.

## Dataset

The dataset contains information about Netflix movies and TV shows, including:

- Show ID
- Type
- Title
- Director
- Cast
- Country
- Date Added
- Release Year
- Rating
- Duration
- Listed In
- Description

The original dataset contains 7,787 records and 12 columns.

## Data Quality Issues Identified

The dataset was checked for:

- Missing values
- Duplicate records
- Incorrect data types
- Inconsistent text values
- Invalid numeric values
- Date formatting issues

## Cleaning Performed

The Python cleaning script performs the following steps:

1. Standardizes column names.
2. Removes duplicate records.
3. Removes extra spaces from text fields.
4. Standardizes values in categorical columns.
5. Converts `date_added` into a proper date format.
6. Handles missing values in director, cast, country and rating.
7. Validates the `release_year` column.
8. Cleans the duration field.
9. Saves the cleaned dataset.
10. Generates a data-quality report.

## Tools Used

- Python
- Pandas
- GitHub

## Project Structure

```text
SWYNEX-Data-Cleaning-Preparation
│
├── README.md
├── requirements.txt
│
├── data
│   └── netflix_raw.csv
│
└── scripts
    └── clean_netflix.py
