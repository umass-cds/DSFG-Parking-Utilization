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
import datetime as dt
# ~~~ FUNCTIONS ~~~
def mobile_excel(xls_file_name, first_run):
	# Open the *.xls file
    wb = xlrd.open_workbook(xls_file_name)
    sh = wb.sheet_by_name('TransactionDetailsWithLocationA')
    your_csv_file = open('mobile.csv', 'a',newline='', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    # Test if first run to add header or not
    if first_run == True:
    	start_rownum = 4
    else:
    	start_rownum = 5
    # Write the new CSV
    for rownum in range(start_rownum,sh.nrows):
        	wr.writerow(sh.row_values(rownum))

def kiosk_excel(xls_file_name, first_run):
	# Open the *.xls file
    wb = xlrd.open_workbook(xls_file_name)
    sh = wb.sheet_by_name('transaction_history')
    your_csv_file = open('kiosk.csv', 'a',newline='', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    # Test if first run to add header or not
    if first_run == True:
    	start_rownum = 3
    else:
    	start_rownum = 4
    # Write the new CSV
    for rownum in range(start_rownum,sh.nrows):
        	wr.writerow(sh.row_values(rownum))
    your_csv_file.close()

# ~~~ MAIN FUNCTION ~~~
def main(): 
	try:
	    os.remove('kiosk.csv')
	    os.remove('mobile.csv')
	except:
		print('Creating: output.csv...')

	# Import mobile data
	first_run = True # Initialize the Header
	mobile_path = "csvs/mobile/*.xlsx"
	for fname in glob.glob(mobile_path):
	    mobile_excel(fname, first_run)
	    first_run = False
	
	# Import kiosk data 
	first_run =  True # Initialize the Header
	kiosk_path = "csvs/kiosk/*.xlsx"
	for fname in glob.glob(kiosk_path):
	    kiosk_excel(fname, first_run)
	    first_run = False

	# Combine both kiosk and mobile data
	pm_df = pd.read_csv('mobile.csv', encoding='utf-8', sep=',', index_col=None)
	ki_df = pd.read_csv('kiosk.csv', encoding='utf-8', sep=',', index_col=None)
	pm_df = pm_df[['Insert Date', 'Parking Amount']]
	ki_df = ki_df[['Terminal Date', 'Amount']]
	ki_df.columns = ['Insert Date', 'Parking Amount']
	pm_df = pm_df.append(ki_df) # Add data together

	# Format Dataframe
	pm_df['datetime'] = pd.TimedeltaIndex(pm_df['Insert Date'], unit='d') + dt.datetime(1899, 12, 30)
	pm_df['start_time'] = pd.to_datetime(pm_df['datetime'])
	pm_df['parking_mins'] = pm_df['Parking Amount'] * 60
	pm_df['minute_delta'] = pd.to_timedelta(pm_df['parking_mins'], unit='m')
	pm_df['end_time'] = pm_df['start_time'] + pm_df['minute_delta'] 

	# Initialize new Dataframe for timestamping cars
	d = []
	for index, row in pm_df.iterrows():
		minute_window = int(row['parking_mins'])
		minutes = 0 # Initialize Minutes
		# Create a car timestamp for every minute
		for i in range(minute_window):
			occ_time = row['start_time'] + pd.Timedelta(minutes=minutes)
			d.append({'occupancy': occ_time})
			minutes += 1

	# Create a new dataframe from those timestamps		
	df =  pd.DataFrame(data=d)

	# Filter out 15 minute intervals
	df = df[(df.occupancy.dt.minute == 15) | (df.occupancy.dt.minute == 45)\
					 | (df.occupancy.dt.minute == 30)  | (df.occupancy.dt.minute == 0)]

	# Count cars in 15 minute intervals
	agg_by_15 = df.groupby([df.occupancy.dt.month,df.occupancy.dt.day,\
							df.occupancy.dt.hour,\
							round(df.occupancy.dt.minute/15,0)]).count()
	agg_by_15.index.names = ['mnth','dy','hr','15_min']
	agg_by_15 = agg_by_15.reset_index()
	agg_by_15['mn'] = (agg_by_15['15_min'] * 15).astype(int)
	agg_by_15['datetime'] = agg_by_15['mnth'].astype(str) + "/" + agg_by_15['dy'].astype(str) +\
								"/2018 " + agg_by_15['hr'].astype(str) \
										+ ":" + agg_by_15['mn'].astype(str)
	agg_by_15 = agg_by_15[['datetime', 'occupancy']]							
	agg_by_15.to_csv('occupancy.csv', index=False)
	
	
if __name__ == "__main__":
    main()