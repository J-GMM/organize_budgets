# Budget Organizer
Takes transaction output tables from online banking, filters and sorts transactions by date using Pandas, then copies the export to clipboard.

# Running this script
This script requires .csv files formatted like the existing ones in the 'input' folder, as well as the dates.csv file to determine budget period.

Dates.csv is a tracking table delimiting budget periods.

Clone to your machine, install requirements using `pip install -r requirements.txt`, and run the script. The tool will export transactions in the current budget period to your clipboard.