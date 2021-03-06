import os
import datetime
import pandas as pd
from pyperclip import copy
import sys

def get_user_date_input():
    print('Please enter dates:')
    display = {
        'Start year': 0,
        'Start month': 0,
        'Start day': 0,
        'End year': 0,
        'End month': 0,
        'End day': 0,
    }
    for key in display:
        valid = False
        print(key)
        val = input()
        while valid == False:
            try:
                val = int(val)
                display[key] = val
                valid = True
            except ValueError:
                print("Wrong format. Int only. Please try again.")
    return {'Start Date':datetime.datetime(
                display['Start year'], 
                display['Start month'], 
                display['Start day'], 0, 0, 0), 
            'End Date':datetime.datetime(
                display['End year'], 
                display['End month'], 
                display['End day'], 0, 0, 0)}

if len(sys.argv) > 2:
    print('Invalid arguments.')
    quit(1)

# Get date range from the table.
def determine_date_range():
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == '-c':
                date_range = pd.DataFrame(get_user_date_input(), index={0})
            else:
                print('Invalid argument. Valid arguments:')
                print('-c for custom date input')
                quit(1)
        else:
            dates = pd.read_csv('dates.csv',delimiter='\t')
            dates['Start Date'] = pd.to_datetime(dates['Start Date'], format='%m/%d/%Y')
            dates['End Date'] = pd.to_datetime(dates['End Date'], format='%m/%d/%Y')
            start_before_today = dates.where(dates['Start Date'] < pd.to_datetime('today')).dropna()
            date_range = dates.where(start_before_today['End Date'] > pd.to_datetime('today')).dropna().reset_index(drop=True)
    finally:
        print('Current budget period:', date_range)
        return date_range

date_range = determine_date_range()

# Gather all .csv file names in the input folder, then iterate through each file.
files = ['input/' + x for x in os.listdir('input/') if '.csv' in x]
for csv_file in files:

    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values(by=['Date', 'Description'])

    budget_df = df[df['Date'] > date_range['Start Date'][0]]
    budget_df = budget_df[budget_df['Date'] < date_range['End Date'][0]].drop(columns=['Balance'])
    print('Output has been copied to clipboard:', budget_df)
    budget_df.to_clipboard(excel=True, index=False, sep='\t', header=False)

    if 'AccountActivityExport.csv' in csv_file:
        account = 'Checking'
    if csv_file == 'creditCardAccountActivityExport' in csv_file:
        account = 'Credit Card'
    else:
        account = 'Bank Account'
    input(account+' Copied. Press enter to continue.')

print('All files processed.')
