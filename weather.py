import dateutil.parser
import dateutil.relativedelta
import forecastio
import googlemaps
import json
import math
from datetime import datetime
from flask import Flask, request
from geopy.distance import great_circle
	 
DEBUG = True
AIRPORT_SUFFIX = " airport"
FORECAST_KEY = "2de2e399347cba6a0d2666ae501f59e8"
MAPS_KEY = "AIzaSyBJD1N0f9sVnhOSMQhIpFZF6oiLhK8Zi18"
saved_forecasts = {};

app = Flask(__name__)
app.config.from_object(__name__)

#Resolve a given IATA code (or lat/lng pair) to a json list of [lat, lng]
@app.route('/resolve/<location>', methods=['GET'])
def resolve_location(location):
	return json.dumps({'location': get_location(location)})
	
#Retrieve a forecast for a flight with the given parameters
@app.route('/forecast/<src>/<dest>/<departure_datetime>/<speed_mph>/<time_step>')
def forecast_route(src, dest, departure_datetime, speed_mph, time_step):
	#reformat inputs
	source = get_location(src)
	destination = get_location(dest)
	start_time = dateutil.parser.parse(departure_datetime)
	speed = float(speed_mph)
	interval = float(time_step)
	#get forecasts
	forecasts = get_forecasts(source, destination, start_time, speed, interval)
	return json.dumps(forecasts)

def get_location(location):
	formatted_location = location.replace(" ", "").upper()
	as_list = formatted_location.split(",")
	if(len(as_list) > 1):
		location = [float(as_list[0]), float(as_list[1])]
	else:
		location = get_IATA_geocode(formatted_location)
	return location
	
# calculate a waypoint a given distance along a route between two lat/long coords
# not implemented correctly
def get_waypoint(source, destination, distance, miles_travelled):
	#not exact, unsure how to calculate waypoints on a route with GPS coords
	proportion = miles_travelled / distance
	latitude = ((destination[0] - source[0]) * proportion) + source[0]
	longitude = ((destination[1] - source[1]) * proportion) + source[1]
	return [latitude, longitude]

# looks up the lat/long coordinates of a given IATA code
# using the Google Maps geocode API
def get_IATA_geocode(iata_code):
	gmaps = googlemaps.Client(key=MAPS_KEY)
	full_location = gmaps.geocode(iata_code + AIRPORT_SUFFIX)
	lat_long = full_location[0]["geometry"]["location"]
	#strip lat and long identifiers
	ret = [lat_long["lat"], lat_long["lng"]]
	return ret

# get an array of forecasts at different locations
# by calculating waypoints on the route between the start / end
# and retrieving a forecast for each one
def get_forecasts(source, destination, start_time, speed, interval):
	distance = great_circle(source, destination).miles
	num_reads = int(math.floor(distance / (speed * interval)))
	miles_travelled = 0
	all_reads = []
	for point in range (num_reads):
		miles_travelled += speed * interval
		waypoint = get_waypoint(source, destination, distance, miles_travelled)
		time = start_time + dateutil.relativedelta.relativedelta(hours=interval)
		all_reads.append(get_forecast(waypoint[0], waypoint[1], time))
	return all_reads

# get the forecast at a given latitude and longitude, at the specified time
def get_forecast(latitude, longitude, time):
	rounded_latitude = round(latitude, 2)
	rounded_longitude = round(longitude, 2)
	forecast = saved_forecasts.get((rounded_latitude, rounded_longitude, time), None);
	if(forecast is None):
		forecast = forecastio.load_forecast(FORECAST_KEY, latitude, longitude, time=time).currently()
		saved_forecasts[(rounded_latitude, rounded_longitude, time)] = forecast;
	return resolve_forecast(forecast, latitude, longitude, time);

# compile and return forecast-specific stuff
# would switch to different library if given more time; don't like these exceptions
def resolve_forecast(forecast, latitude, longitude, time):
	try:
		wind_speed = forecast.windSpeed
		incomplete = False
	except:
		incomplete = True
		wind_speed = 0
	try:
		temperature = forecast.temperature
		incomplete = False
	except:
		incomplete = True
		temperature = 0
	try:
		humidity = forecast.humidity
		incomplete = False
	except:
		incomplete = True
		humidity = 0
	
	time_utc = str(forecast.time)
	#TODO: round time
	time_rnd = str(forecast.time)
	#google maps API failing
	time_offset = 0
	
	read = {
		"humidity": humidity, 
		"incomplete": incomplete, 
		"location": [latitude, longitude], 
		"location_rnd": [round(latitude, 2), round(longitude, 2)],
		"temperature": temperature, 
		"time": time_utc, 
		"time_offset": time_offset, 
		"time_rnd": time_rnd,
		"wind_speed": wind_speed }
	return read
	

if __name__ == '__main__':
    app.run()