#map generator. Takes input .cfg file and prepares a .map file of the same name.
import ConfigParser,sys

def parse(filename):
	parsed_objects = ""
	parser = ConfigParser.ConfigParser()
	parser.read(filename)
	for option in parser.options("Header"):
		raw = parser.get("Header",option)
		for number in raw.split(","):
			parsed_objects = parsed_objects + number
	for option in parser.options("Tiles"):
		raw = parser.get("Tiles",option)
		for number in raw.split(","):
			parsed_objects = parsed_objects + number
	for option in parser.options("Events"):
		raw = parser.get("Events",option)
		for number in raw.split(","):
			parsed_objects = parsed_objects + number
	for option in parser.options("Exits"):
		raw = parser.get("Exits",option)
		for number in raw.split(","):
			parsed_objects = parsed_objects + number
	for option in parser.options("Objects"):
		raw = parser.get("Objects",option)
		for number in raw.split(","):
			parsed_objects = parsed_objects + number
	for option in parser.options("NPCs"):
		raw = parser.get("NPCs",option)
		for number in raw.split(","):
			parsed_objects = parsed_objects + number
	return parsed_objects
	
def write_data(filename,parsed_data):
	write_file = open(filename,"w")
	write_file.write(parsed_data)
	write_file.close()

if len(sys.argv) == 2:
	output_name_tuple = sys.argv[1].split(".")
	output_file_name = output_name_tuple[0] + ".map"
	parsed_data = parse(sys.argv[1])
	write_data(output_file_name,parsed_data)
	print "Success!"
else:
	print "Expected .cfg filename as argument."