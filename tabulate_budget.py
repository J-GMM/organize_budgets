import os
import datetime
import pandas as pd
from pyperclip import copy

# Get date range from the table.
def determine_date_range():
    dates = pd.read_csv('dates.csv',delimiter='\t')
    dates['Start Date'] = pd.to_datetime(dates['Start Date'], format='%m/%d/%Y')
    dates['End Date'] = pd.to_datetime(dates['End Date'], format='%m/%d/%Y')
    start_before_today = dates.where(dates['Start Date'] < pd.to_datetime('today')).dropna()
    date_range = dates.where(start_before_today['End Date'] > pd.to_datetime('today')).dropna().reset_index(drop=True)
    print("Current budget period:", date_range)
    return date_range

date_range = determine_date_range()

# Gather all .csv file names in the input folder, then iterate through each file.
files = ['input/' + x for x in os.listdir('input/') if ".csv" in x]
for csv_file in files:

    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values(by=['Date'])

    budget_df = df[df['Date'] > date_range['Start Date'][0]][df['Date'] < date_range['End Date'][0]].drop(columns=['Balance'])
    print("Output has been copied to clipboard:", budget_df)
    budget_df.to_clipboard(excel=True, index=False, sep='\t', header=False)

    if 'checkingAccountActivityExport.csv' in csv_file:
        account = "Checking"
    if csv_file == 'creditCardAccountActivityExport' in csv_file:
        account = "Credit Card"
    else:
        account = "Bank Account"
    input(account+" Copied. Press enter to continue.")

print("All files processed.")
