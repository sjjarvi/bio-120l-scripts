import urllib.request, urllib.parse, urllib.error
import json
import ssl
import csv
import time
import os

# ZIP CODES
zipCodes = dict()
zipCodes['BOS'] = '02128'
zipCodes['LA'] = '90012'
zipCodes['KC'] = '64105'

# Read the API key from a known environment variable
# For now, if not specified use a dummy key that will fail
api_key = os.environ.get('AIRNOW_API_KEY', 'INVALID_KEY')

zipCode = zipCodes['KC']
distance = 25
format = "application/json"
queryDatePrefix="2023-05-"

serviceurl = 'https://www.airnowapi.org/aq/observation/zipCode/historical/?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Static Parameters
params = dict()
params['API_KEY'] = api_key
params['zipCode'] = zipCode
params['format'] = format
params['distance'] = distance

results = list()
results.append(['Day of Month', 'Ozone AQI', 'PM2.5 AQI', 'PM10 AQI'])

for x in range(3):
    dayOfMonth = x + 1
    queryDay = ('0' + str(dayOfMonth)) if dayOfMonth < 10  else str(dayOfMonth)
    queryDate = queryDatePrefix + queryDay + 'T00-0000'
    print('Query Date:', queryDate)
    params['date'] = queryDate
    
    url = serviceurl + urllib.parse.urlencode(params)

    # print('Retrieving', url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    try:
        aqData = json.loads(data)
    except:
        aqData = None

    # print(json.dumps(aqData, indent=4))

    if not aqData :
        print('Error retrieving data for day ', queryDate)
        continue

    allTypes = dict()
    for parameter in aqData :
        type = parameter['ParameterName']
        measurement = parameter['AQI']
        category = parameter['Category']['Name']
        allTypes[type] = (measurement, category)

    ozoneData = allTypes.get('OZONE', ('', ''))
    pm25Data = allTypes.get('PM2.5', ('', ''))
    pm10Data = allTypes.get('PM10', ('', ''))

    # Flatten out into a single row
    csvData = list()
    #csvData.append(queryDate)
    csvData.append(queryDay)

    # Keep it simple for graphing, only use AQI data
    csvData.append(ozoneData[0])
    csvData.append(pm25Data[0])
    csvData.append(pm10Data[0])

    results.append(csvData)

    # Avoid being rate limited
    time.sleep(2)

csvFilename = zipCode + '_aqi_data_may2023.csv'
with open(csvFilename, 'w', newline='') as csvfile :
    csvWriter = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_MINIMAL)

    for row in results :    
        csvWriter.writerow(row)
