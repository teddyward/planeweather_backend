# planeweather_backend

### Overview
This is an implementation of the API for the backend of the PlaneWeather problem.
See here for details: https://bitbucket.org/snippets/plotwatt/q7oR

### Flaws
- Time zones aren't resolved correctly
- Lots of locations fail the API requests for humidity, temperature, or wind speed at a given time, because the weather forecasts don't have the precision necessary
