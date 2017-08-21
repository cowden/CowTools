
# Weather Data
* www.weather.gov
* www.aviationweather.gov (metars)
* http://tgftp.nws.noaa.gov/ (this is the source used by xmobar weather plugin)



I want to either get weather either by providing LAT/LONG or a city and state.

```
weather "city,state"
```
or
```
weather lat long
```
and additionally
```
weatherStation station
```

2 arguments indicates a latitude/longitude is provided whilst a single string 
argument indicates a city and state is provided.  

In the case of a single
input string, the input argument is used to search for a location in the 
weather.gov homepage.  After landing on the location's forecast page, the 
programs treats the two modes in the same way.

The data found at the ftp site provides a concise set of the current observed
conditions given a station such as KDAL for Dallas Love Field.  It has a link
to the forecast page found via weather.gov.  

Since I'm not sure if the forecast given a latitude and longitude is at all
different from the forecast given a weather station, I will implement a tool
to do each.  This will also allow a bit more flexibility in instances where
precise latitude and longitude are not known and cases in which with the nearest
weather station handle is not known.

# Weather CLI
Search on the weather homepage the main form action queries zipcity.php at
http://forecast.weather.gov/zipcity.php
After posting the search data (city,state) the local forecast is returned.
Post the following data:
* `inputstring=City, ST`
* `btnSearch=Go`

Lat/Long weather:
http://forecast.weather.gov/MapClick.php?lat=XXXXXX&lon=XXXXX
