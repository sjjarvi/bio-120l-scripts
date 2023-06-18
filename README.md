# Python Script for Collecting AQI Data from AirNow

This repo contains a very simple script that uses the AirNow web service to collect AQI values for a range of days. This version is hard-coded to May 2023, but the script can be easily edited to accomodate other date ranges.

## Locations

The script is hard-coded to use three possible locations: Boston, Los Angeles, Kansas City.  It can be edited to use different zip codes.

## Prerequisites

You must obtain an api key from AirNow. See: https://docs.airnowapi.org/

## Running the script

```
export AIRNOW_API_KEY=<your_airnow_api_key>

python3 get-aqi-data.py
```

A CSV file containing the retrieved data will be written this directory with the name `<zipCode>_aqi_data_may2023.csv`. This can also be edited to suit your specific needs.