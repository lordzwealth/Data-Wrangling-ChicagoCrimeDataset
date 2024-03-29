# -*- coding: utf-8 -*-
"""Data Wrangling Assesment - Emmanuel Ajayi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17eRDJpkKOtYK19UrCx4_P3OYYqSXClEZ

#### Using the Chicago Crime Dataset(any of the 3 sheets you choose), perfrom the following data preparation steps:
1. Use a funtion to Drop redundant columns (a redundant colum is one that gives infromation that another column already explains: eg ID and Case number)
2. Use functions to create new columns for Months, Day, Season.
3. Use subsetting and grouping to show how the frequency of crime is distributed within Months, Days, Seasons with the most crime record and what crimes are highest and lowest?
4.  According to location description, where does crime hapen the most?
5.  Did the Types of crime change as years go by? if yes/no. let the data show the insight.
"""

# Importing necessary libraries
import pandas as pd

# Loading the Chicago Crime Dataset
file = '/content/chicago1.csv'
df = pd.read_csv(file).drop('Unnamed: 0', axis=1)

# make index start from 1
df.index = df.index + 1

df.head()

df.isnull().sum()

# Filling Missing Values with the Median (Ward & Community Area)
df['Ward'] = df['Ward'].fillna(df['Ward'].median())

df['Community Area'] = df['Community Area'].fillna(df['Community Area'].median())

df.isnull().sum()

"""

1.   Use a funtion to Drop redundant columns (a redundant colum is one that gives infromation that another column already explains: eg ID and Case number)

"""

def drop_columns(df, columns):
    for column in columns:
        if column in df.columns:
            df.drop(columns=[column], inplace=True)
        else:
            print(f"Column '{column}' not found in the dataframe.")
    return df

drop_columns(df, ['ID', 'Latitude', 'Longitude', 'col1'])

df.columns

"""2. Use functions to create new columns for Months, Day, Season."""

#Creating a function for the Month Column
from datetime import datetime

def extractMonth(date):
  date_column = pd.to_datetime(date, format='%m/%d/%Y %I:%M:%S %p')
  month_names = date_column.dt.month_name()

  return month_names

df['Month'] = extractMonth(df['Date'])

df.head(4)

#Creating a function for the Day Column
df['Day'] = df['Date'].apply(lambda date: pd.to_datetime(date, format='%m/%d/%Y %I:%M:%S %p').dayofweek)
df['Day'] = df['Day'].map({
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
})

df.head(4)

# creating a column for seasons

def createSeason(date_column):
    # Ensure the input is in datetime format
    date_column = pd.to_datetime(date_column, format='%m/%d/%Y %I:%M:%S %p')

    # Define a mapping of month to season
    month_to_season = {
        1: 'Winter', 2: 'Winter', 3: 'Spring',
        4: 'Spring', 5: 'Spring', 6: 'Summer',
        7: 'Summer', 8: 'Summer', 9: 'Fall',
        10: 'Fall', 11: 'Fall', 12: 'Winter'
    }

    # Extract the month and map to season
    seasons_column = date_column.dt.month.map(month_to_season)

    return seasons_column

df['Seasons'] = createSeason(df['Date'])

df.head(10)

"""3. Use subsetting and grouping to show how the frequency of crime is distributed within Months, Days, Seasons with the most crime record and what crimes are highest and lowest?"""

#Show the distribution of Crime in-respect to their Month
df.groupby('Month')['Primary Type'].value_counts()

# Find the month with the highest crime count
crime_counts_by_month = df.groupby('Month')['Month'].count()
highest_crime_month = crime_counts_by_month.idxmax()
lowest_crime_month = crime_counts_by_month.idxmin()

print("Month with the highest crime count:", highest_crime_month)
print("Month with thw lowest crime count:", lowest_crime_month)

#Show the distribution of Crime in-respect to their Day of the Week
df.groupby('Day')['Primary Type'].value_counts()

# Find the Day with the highest and lowest crime count
crime_counts_by_day = df.groupby('Day')['Day'].count()
highest_crime_day = crime_counts_by_day.idxmax()
lowest_crime_day = crime_counts_by_day.idxmin()

print("Day with the highest crime count:", highest_crime_day)
print("Day with thw lowest crime count:", lowest_crime_day)

#Show the distribution of Crime in-respect to their Season
df.groupby('Seasons')['Primary Type'].value_counts()

# Find the Day with the highest and lowest crime count
crime_counts_by_season = df.groupby('Seasons')['Seasons'].count()
highest_crime_season = crime_counts_by_season.idxmax()
lowest_crime_season = crime_counts_by_season.idxmin()

print("Season with the highest crime count:", highest_crime_season)
print("Season with thw lowest crime count:", lowest_crime_season)

"""4. According to location description, where does crime hapen the most?"""

# Finding the Location with the highest crime occurences
df['Location Description'].value_counts()

# Location with the highest crime occurence
crime_counts_by_location = df.groupby('Location Description')['Location Description'].count()
highest_crime_location = crime_counts_by_location.idxmax()
print("Location with the highest crime count:", highest_crime_location)

"""5. Did the Types of crime change as years go by? if yes/no. let the data show the insight."""

# Group the data by year and crime type, count the occurrences
crime_counts_by_year = df.groupby('Year')['Primary Type'].value_counts()

crime_counts_by_year.head

