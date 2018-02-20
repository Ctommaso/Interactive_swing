import sys

def load_csv(fn):
	
	try:
		assert(fn.split('.')[-1] == 'csv')
	except AssertionError:
		sys.exit("Selected file is not  *.csv")

	f = open(fn, "r")
	text_lines = iter(f.readlines())
	f.close()

	bus_section = "### buses"
	line_section = "### lines"
	empty_line = "\n"

	in_bus_section = False
	in_line_section = False

	buses = []
	lines = []

	for l in text_lines:
		
		if l.startswith(bus_section):
			in_bus_section = True
			in_line_section = False
			continue
			
		if l.startswith(line_section):
			in_bus_section = False
			in_line_section = True
			continue
		
		if l.startswith(empty_line):
			continue
		
		if in_bus_section:
			
			data = l.split(',')
			
			bus_id = int(data[0])
			
			bus_dict = {}
			bus_dict['name'] = data[1]
			bus_dict['coord'] = [float(data[2]), float(data[3])]
			bus_dict['sm'] = bool(int(data[4]))
			bus_dict['power'] = float(data[5])
			bus_dict['damping'] = float(data[6])
			try:
				bus_dict['inertia'] = float(data[7])
			except ValueError:
				pass
			
			buses.append( (bus_id, bus_dict) )
		
		if in_line_section:
			
			data = l.split(',')
			
			source = int(data[0])
			sink = int(data[1])
			
			line_dict = {}
			line_dict['susceptance'] = float(data[2])
			line_dict['status'] = bool(int(data[3]))
			lines.append((source, sink, line_dict))
		
	return buses, lines
