# planeweather_backend

### Overview
This is an implementation of the API for the backend of the PlaneWeather problem.
See here for details: https://bitbucket.org/snippets/plotwatt/q7oR

Thanks to Google Maps geocoding and Forecast IO APIs

### Todos (stopped after 4 hours)
- Finding waypoints is done in a very naive way
- Time zones aren't resolved for the waypoints
- No tests
- Lots of locations/times fail the API requests for humidity, temperature, or wind speed, because the weather forecasts don't have the precision necessary to have this information at every time

### Examples
https://shrouded-retreat-9801.herokuapp.com/resolve/RDU
https://shrouded-retreat-9801.herokuapp.com/forecast/LHR/LAX/2015-12-16T12:00:00/500/1