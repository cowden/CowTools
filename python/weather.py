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
  return html.document_fromstring(result)

   

#
# parse the results of the pull
def parseResults(result):
  '''Format and display the results of the forecast query.'''

  # get the body text
  body = re.sub('(^ +)|( +$)','',re.sub('[\n]','',''.join(result.xpath('//div[@class="body"]/p/text()'))))


  # get the current conditions
  cur_cond = result.xpath('//div[@id="current-conditions"]')[0]
  cc = {'station': cur_cond.xpath('div[@class="panel-heading"]/div/h2/text()')[0]
    ,'station_info': ' '.join(cur_cond.xpath('div/div/span/b/text()|div/div/span/text()'))
    }

  # collect all of the current condition details
  cc_table_elements = cur_cond.xpath('div[@class="panel-body" and @id="current-conditions-body"]')[0]
  cc['current'] = cc_table_elements.xpath('div[@id="current_conditions-summary"]/p[@class="myforecast-current"]/text()')[0]
  cc['lrg'] = cc_table_elements.xpath('div[@id="current_conditions-summary"]/p[@class="myforecast-current-lrg"]/text()')[0]
  cc['sm'] = cc_table_elements.xpath('div[@id="current_conditions-summary"]/p[@class="myforecast-current-sm"]/text()')[0]

  for element in cc_table_elements.xpath('div[@id="current_conditions_detail"]/table/tr'):
    cc[ element.xpath('td/b/text()')[0] ] = element.xpath('td/text()')[0]
  
  
  # get the 7 day forecast
  fc = []
  for p in result.xpath('//div[@class="tombstone-container"]'):
    forecast = p.xpath('p/text()')
    fc.append(forecast) 
  

  # get station information

  # return the current conditions and forecast
  return [cc,fc]

#
# format and print the results
# print the current conditions
def printCurrentConditions(current):

  print('\033[1mCurrent Conditions\033[0m')
  print('Station: %s' % current['station'])
  print('\033[32mTemp: %s (%s)\033[0m' % (current['lrg'],current['sm']))

  for k,v in current.items():
    if k in ('lrg','sm','current','station'):
      continue

    print('\t%s: %s' % (k,v))

#
# print the 7 day forecast
def printForecast(forecast):

  print('\033[1m7 Day Forecast\033[0m')
  for fc in forecast:
    print('\t%s: %s' % (fc[0],' '.join(fc[1:])) )

 


#class
# print usage
def printUsage():
  usage = '''weather CLI forecast tool..
\tweather <[City, State] or [Lat Long]>
  '''

  print(usage)



#
# main function for CLI usage
if __name__ == '__main__':

  # parse command line arguments
  # if two arguments -> assume lat/long
  # else assume a search string for weather.gov homepage

  if len(sys.argv[1:]) == 1:
    # search for location
    result = locationSearch(sys.argv[1])

  elif len(sys.argv[1:]) == 2:
    # go to lat/long page for forecast
    result = getForecast(lat,lng)

  else:
    # print usage and terminate
    printUsage()
    sys.exit(0)

  result = parseResults(result)

  # print the formatted forecast and conditions
  printCurrentConditions(result[0])
  printForecast(result[1])


