# all the imports
import sqlite3
import json
from flask import Flask, request
	 
DEBUG = True

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/resolve/<location>', methods=['GET'])
def resolve_location(location):
	latitude = 33.942536
	longitude = -118.408075
	return json.dumps({'location': [latitude, longitude]})
	
@app.route('/forecast/<src>/<dest>/<departure_datetime>/<speed_mph>/<time_step>')
def forecast_route(src, dest, departure_datetime, speed_mph, time_step):
	num_reads = 1;
	all_reads = [];
	for point in range (num_reads):
		latitude = 33.942536
		longitude = -118.408075
		all_reads.append(get_weather(latitude, longitude))
	return json.dumps(all_reads)
	
def get_weather(latitude, longitude):
	humidity = 0.64
	incomplete = False
	temperature = 60.65
	time = 1425182400
	time_offset = -8
	time_rnd = 1425182400
	wind_speed = 7.14
	read = {
		"humidity": humidity, 
		"incomplete": incomplete, 
		"location": [latitude, longitude], 
		"location_rnd": [round(latitude, 2), round(longitude, 2)],
		"temperature": temperature, 
		"time": time, 
		"time_offset": time_offset, 
		"time_rnd": time - (time%100),
		"wind_speed": wind_speed }
	return read
	

if __name__ == '__main__':
    app.run()