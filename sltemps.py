import re
import json
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
#options.headless = True
#options.add_argument("--window-size=1920,1200")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

dbConn = sqlite3.connect('WL_WEATHER.db')
dbCursor = dbConn.cursor()

def create_table():
    dbCursor.execute('CREATE TABLE IF NOT EXISTS WL_WEATHER (lastTimestamp INTEGER, sStation TEXT, temperature INTEGER, temperatureUnit TEXT, windSpeed INTEGER, windSpeedUnit TEXT, windDirection INTEGER, barometer NUMERIC, barometerUnit TEXT, barometerTrend INTEGER, humidity INTEGER, dailyRain NUMERIC, rainUnit TEXT, lat NUMERIC, lng NUMERIC, lastUpdatedAt TEXT) ')
  

def data_entry(weatherEntry):
    dbCursor.execute("INSERT INTO WL_WEATHER (lastTimestamp, sStation, temperature, temperatureUnit, windSpeed, windSpeedUnit, windDirection, barometer, barometerUnit, barometerTrend, humidity, dailyRain, rainUnit, lat, lng, lastUpdatedAt) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  (weatherEntry['lastTimestamp'], weatherEntry['sStation'], weatherEntry['temperature'], weatherEntry['temperatureUnit'], weatherEntry['windSpeed'], weatherEntry['windSpeedUnit'], weatherEntry['windDirection'], weatherEntry['barometer'], weatherEntry['barometerUnit'], weatherEntry['barometerTrend'], weatherEntry['humidity'], weatherEntry['dailyRain'], weatherEntry['rainUnit'], weatherEntry['lat'], weatherEntry['lng'], weatherEntry['lastUpdatedAt']))
    dbConn.commit()

create_table()

# Get Base Temp
driver.get('https://www.weatherlink.com/map/data/station/c0d9838e-95c4-4b39-bfd2-c7bd7c2f550b')
weatherData = re.findall(r'.+\<pre[^>]+\>(\{\"sStation.+})', driver.page_source)
weatherDataDict = json.loads(weatherData[0])

#for key in weatherDataDict:
#  print(key, ":", weatherDataDict[key]) 
# Add Base Temp to DB
data_entry(weatherDataDict)

# Get Summit Temp
driver.get('https://www.weatherlink.com/map/data/station/4e059d3a-930e-40f3-964d-696297904466')
weatherData = re.findall(r'.+\<pre[^>]+\>(\{\"sStation.+})', driver.page_source)
weatherDataDict = json.loads(weatherData[0])

#for key in weatherDataDict:
#  print(key, ":", weatherDataDict[key]) 
# Add Base Temp to DB
data_entry(weatherDataDict)

# Print DB
dbCursor.execute("SELECT * FROM WL_WEATHER")
dbConn.commit()
for item in dbCursor.fetchall():
    print(item)

# Cleanup
driver.quit()

dbCursor.close()
dbConn.close()


