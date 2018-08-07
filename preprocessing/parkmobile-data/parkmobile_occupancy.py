###########################################
#      DSFG ~ Katie House ~ 8/6/18
# DESCTIPTION: analyze ParkMobile data
# INPUT: parkmobile csvs
# OUTPUT: output.csv, preporcessed data
###########################################

# ~~~ IMOPORT LIBRARIES ~~~
import pandas as pd
import glob
import xlrd
import csv
import os

# ~~~ FUNCTIONS ~~~
def csv_from_excel(xls_file_name, first_run):
	# Open the *.xls file
    wb = xlrd.open_workbook(xls_file_name)
    sh = wb.sheet_by_name('TransactionDetailsWithLocationA')
    your_csv_file = open('output.csv', 'a',newline='', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    # Test if first run to add header or not
    if first_run == True:
    	start_rownum = 11
    else:
    	start_rownum = 12
    # Write the new CSV
    for rownum in range(start_rownum,sh.nrows):
        	wr.writerow(sh.row_values(rownum))
    your_csv_file.close()

# ~~~ MAIN FUNCTION ~~~
def main(): 
	path = "csvs/*.xls"

	try:
	    os.remove('output.csv')
	except:
		print('Creating: output.csv...')

	first_run = True # Initialize the Header

	for fname in glob.glob(path):
	    csv_from_excel(fname, first_run)
	    first_run = False
	print('COMPLETE: Conversion from xls to csv')

	# Format Dataframe
	pm_df = pd.read_csv('output.csv', encoding='utf-8', sep=',', index_col=0)
	df['time'] = df['time'].astype('datetime64[ns]')

	pm_df.reset_index(drop = True, inplace = True)
	pm_df['parkingMinutes'] = pm_df['Parking Amount'] * 60
	print(pm_df)
	for index, row in pm_df.iterrows():
		minute_window = row['parkingMinutes'] / 15
		for i in range(minute_window):
			time_step = pm_d['Insert Date'] + minute_window
			pm_output.append(time_step)


if __name__ == "__main__":
    main()