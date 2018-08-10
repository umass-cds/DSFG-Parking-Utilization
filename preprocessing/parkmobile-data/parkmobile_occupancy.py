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
	pm_df.reset_index(drop = True, inplace = True)
	pm_df['datetime'] = pd.TimedeltaIndex(pm_df['Insert Date'], unit='d') + dt.datetime(1899, 12, 30)
	pm_df['start_time'] = pd.to_datetime(pm_df['datetime'])
	pm_df['parking_mins'] = pm_df['Parking Amount'] * 60
	pm_df['minute_delta'] = pd.to_timedelta(pm_df['parking_mins'], unit='m')
	pm_df['end_time'] = pm_df['start_time'] + pm_df['minute_delta'] 
	print(pm_df)
	
	# Initialize new Dataframe
	d = []
	for index, row in pm_df.iterrows():
		minute_window = int((row['parking_mins'] / 15) + 15)
		minutes = 0 # Initialize Minutes
		for i in range(minute_window):
			occ_time = row['start_time']+ pd.Timedelta(minutes=minutes)
			d.append({'occupancy': occ_time})
			minutes += 15

	df =  pd.DataFrame(data=d)
	agg_by_15 = df.groupby([df.occupancy.dt.month,df.occupancy.dt.day,\
							df.occupancy.dt.hour,\
							round(df.occupancy.dt.minute/15,0)]).count()
	agg_by_15.index.names = ['month','day','hour','min']
	agg_by_15 = agg_by_15.reset_index()
	agg_by_15.to_csv('occupancy.csv', index=False)
	
	
if __name__ == "__main__":
    main()