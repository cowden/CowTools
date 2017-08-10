#!/usr/bin/env python
# on my system python => python 3

#########################################
# C S Cowden           5 August 2017
# Tools to check weather from the command line.
# This is written for python3, some of the buffer
# stuff will not work in python2.
#########################################

'''
Tools to check weather from the command line.
'''


import os,sys,re
import pycurl
from io import BytesIO
from lxml import html
from urllib.parse import urlencode


# ------------------------
# global defs
zipcity = u'http://forecast.weather.gov/zipcity.php'
user_agent = u'Mozilla/5.0 (X11; Linux x86_6… Gecko/20100101 Firefox/54.0'




#
# search and retrieve location weather
def locationSearch(query):
  '''Search for the location (if found) 
return the forecast.'''

  post_data = urlencode({'inputstring':query,'btnSearch':'Go'})

  # construct the curl object
  buffer = BytesIO()
  c = pycurl.Curl()
  c.setopt(c.URL,zipcity)
  c.setopt(c.WRITEDATA,buffer)
  c.setopt(c.FOLLOWLOCATION,True)
  c.setopt(c.POSTFIELDS,post_data)
  
  
  # perform task
  c.perform()
  result = buffer.getvalue()

  # examine the results and check that
  # a valid forecast was found.

  c.close()

  # format forecast data
  return result
   


#
# format and print results
def printResults(result):
  '''Format and display the results of the forecast query.'''

  pass


#
# print usage
def printUsage():
  pass


#
# main function for CLI usage
if __name__ == '__main__':

  # parse command line arguments
  # if two arguments -> assume lat/long
  # else assume a search string for weather.gov homepage

  if len(sys.argv[1:]) == 1:
    # search for location
    result = locationSearch(query)

  elif len(sys.argv[1:]) == 2:
    # go to lat/long page for forecast
    result = getForecast(lat,lng)

  else:
    # print usage and terminate
    printUsage()


  # print the formatted forecast and conditions
  printResults(result)

