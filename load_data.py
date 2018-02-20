import pandas as pd
import sys

def load_xlsx(fn):
	
	try:
		assert(fn.split('.')[-1] == 'xlsx')
	except AssertionError:
		sys.exit("Selected file is not  *.xlsx")
	
	# Load Excel data
	data = pd.ExcelFile(fn)
	
	# Retrieve sheet names
	sheet_name = data.sheet_names
	
	# Test that both 'lines' and 'buses' sheets exist
	try:
		assert('lines' in sheet_name)
	except AssertionError:
		sys.exit("Network .xlsx file does not contain lines sheet")

	try:
		assert('buses' in sheet_name)
	except AssertionError:
		sys.exit("Network .xlsx file does not contain buses sheet")


	# Parse sheets
	bus_df = data.parse('buses')
	line_df = data.parse('lines')
		
	# Float conversions
	line_df['susceptance'] = line_df['susceptance'].astype('float')

	# Conversion to Boolean variables
	bus_df['sm'].replace({1: True, 0: False}, inplace = True)
	line_df['status'].replace({1: True, 0: False}, inplace = True)
	
	
	lines = []
	for n in range(line_df.shape[0]):
		l = line_df.iloc[n]
		lines.append((l['from'], l['to'], {'susceptance': l['susceptance'], 'status': l['status']}))
	
	
	buses = []
	for n in range(bus_df.shape[0]):
		b = bus_df.iloc[n]
		
		bus_id = b['id']
		bus_dict = {}
		bus_dict['name'] = b['name']
		bus_dict['coord'] = [b['coord_x'], b['coord_y']]
		bus_dict['sm'] = b['sm']
		bus_dict['power'] = b['power']
		bus_dict['damping'] = b['damping']
		if pd.isnull(b['inertia']) == False:
			bus_dict['inertia'] = b['inertia'] 
		
		buses.append( (bus_id, bus_dict) )
	 
	return buses, lines
	
if __name__ == "__main__":
	load_xlsx()
