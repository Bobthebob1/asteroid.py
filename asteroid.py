#important instructions:
#below imports is units for asteroid. Do ctrl f, type in the existing unit (i.e m) and replace all instances of m except for the variable at the top with the new variable (say km)

import requests
import json
import os
from datetime import date

#units

m = 'meters'
km = 'kilometers'
mi = 'miles'
ft = 'feet'

#Select Date
print('If you would like to search for a custom date enter 0. If you would like to search for today enter 1. Enter your response in the prompt below:')
q1 = input()
if q1 == str(0):
    print('Please enter date you would like to browse. Format must be YYYY-MM-DD: ')
    searchDate = input()
elif q1 == str(1):
    searchDate = date.today()
else:
    print('Sorry there has been an error. Please try again.')

#API
response_API = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date=' +str(searchDate)+ '&end_date=' +str(searchDate)+ '&api_key=a891sk5lkhJVt0YJTSxd5bk97uCxc95HfsfjBAHP')
data = response_API.text
parse_json = json.loads(data)
allAsteroids = parse_json['near_earth_objects'][str(searchDate)]
elementCount = parse_json['element_count']
#Data from asteroid highest on AH Index
print("Enter the highest number for # of asteroids you would like to view below. Available numbers are 1 to",elementCount, ". Enter highest value:")
maxRangeVal = int(input()) 
for i in range(0, maxRangeVal):
    class Asteroid:
        def __init__(self):
            self.array = allAsteroids[i]
            self.name = self.array['name']
            self.cADat = self.array['close_approach_data']
            self.EstD = self.array['estimated_diameter']
            self.MissDis = self.cADat[0]
            self.MissDisLuna = self.MissDis['miss_distance']
            self.AstD = self.EstD[m]
            self.MinD = self.AstD['estimated_diameter_min']
            self.MaxD = self.AstD['estimated_diameter_max']
            self.avgAstD = round(self.MinD + self.MaxD /2, 3)
            self.cADate1 = self.cADat[0]
            self.cADate2 = self.cADate1['close_approach_date']
    astDat = Asteroid()
    
    #AHI Formula (piecewise function)
    if float(astDat.MissDisLuna['lunar'])>=1 or astDat.avgAstD<10:
        ahiLevel = 0
    elif 0.1<=float(astDat.MissDisLuna['lunar'])<1 and 10<=astDat.avgAstD<25:
        ahiLevel = 1
    elif 0.1<=float(astDat.MissDisLuna['lunar'])<1 and 25<=astDat.avgAstD<50:
        ahiLevel = 2
    elif 0.1<=float(astDat.MissDisLuna['lunar'])<1 and 50<=astDat.avgAstD<100:
        ahiLevel = 3
    elif 0.1<=float(astDat.MissDisLuna['lunar'])<1 and 100<=astDat.avgAstD<200:
        ahiLevel = 4
    elif float(astDat.MissDisLuna['lunar'])<=0.01 and astDat.avgAstD>100:
        ahiLevel = 5
    elif 0.01<=float(astDat.MissDisLuna['lunar'])<0.1 and 100<=astDat.avgAstD<=500:
        ahiLevel = 3
    elif 0.01<=float(astDat.MissDisLuna['lunar'])<0.1 and astDat.avgAstD<=10:
        ahiLevel =  0
    elif float(astDat.MissDisLuna['lunar'])>=1 and astDat.avgAstD>=200:
        ahiLevel = 0
    elif 0.1<=float(astDat.MissDisLuna['lunar'])<=0.25 and 200<=astDat.avgAstD<=500:
        ahiLevel = 2
    elif 0.25<=float(astDat.MissDisLuna['lunar'])<=0.5 and 200<=astDat.avgAstD<=500:
        ahiLevel = 1
    elif 0.01<=float(astDat.MissDisLuna['lunar'])<=0.1 and astDat.avgAstD>=500:
        ahiLevel = 4
    elif 0.1<=float(astDat.MissDisLuna['lunar'])<=0.25 and astDat.avgAstD>=500:
        ahiLevel = 3
    elif 0.25<=float(astDat.MissDisLuna['lunar'])<=0.5 and astDat.avgAstD>=500:
        ahiLevel = 2
    elif float(astDat.MissDisLuna['lunar']) == None and astDat.avgAstD == None:
        print("An error has occured in gathering data. Please check the code or the data you are drawing from")
    elif float(astDat.MissDisLuna['lunar']) == None or astDat.avgAstD == None:
        print("An error has occured in gathering data. Please check the code or the data you are drawing from")
    else:
        print("An error has occured in gathering data. Please check the code or the data you are drawing from")

    #Asteroid data print out
    if ahiLevel >= 1:
        print()           
        print(" Asteroid Name:",astDat.name ,"\n", "Average Asteroid Diameter:", 
        astDat.avgAstD, m, "\n", "Asteroid miss distance in LD:", 
        round(float(astDat.MissDisLuna['lunar']), 2),"\n Date of closest approach:", astDat.cADate2)
        if float(astDat.MissDisLuna['lunar']) < 0.01:
            print(" Alert! Closest approach is less than 0.01 LD")
        elif 0.01 < float(astDat.MissDisLuna['lunar']) < 0.1:
            print(" Concern may be warrented. Closest approach is between 0.01 and 0.1 LD")
        else:
            print(" Close approach is far enough away to be safe.")
        print(" AHI Level: Level", ahiLevel)
        if astDat.array["is_potentially_hazardous_asteroid"] == True:
            print(" This asteroid is classified as a potentially hazardous asteroid.")
        elif astDat.array["is_potentially_hazardous_asteroid"] == False:
            print(" This asteroid is not classified as a potentially hazardous asteroid.")
        print()
    elif ahiLevel == 0:
        print(" Asteroid Name:",astDat.name ,"|","AHI Level: Level", ahiLevel)
    #Thank you

print(" Thank you for using Asteroid.py, have a nice day.")
