#!/usr/bin/env python3

import csv
from datetime import timedelta, datetime
from sys import stdout

cases = {}
deaths = {}
day = timedelta(days=1)

def procRow(row):
     dt = row['date']
     counts[(dt,row['fips'])] = row['cases']
     dates.add(dt)
     fips.add(row['fips'])

# Read in counties and case counts
kc_rows = []
with open('us-counties.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     writer = csv.writer(stdout)
     writer.writerow("date,county,state,fips,cases_yday,cases_today,deaths_yday,deaths_today".split(","))
     for row in reader:
         date = datetime.strptime(row['date'],"%Y-%m-%d").date()
         key = (row['county'], row['state'], row['fips'])
         ctoday = cases.setdefault(key,{})[date]=int(row['cases'])
         dtoday = deaths.setdefault(key,{})[date]=int(row['deaths'])
         cyday = cases[key].get(date-day,0)
         dyday = deaths[key].get(date-day,0)
         if cyday > ctoday or dyday > dtoday:
            row = list()
            row.append(date.strftime("%Y-%m-%d"))
            row.extend(key)
            row.extend([cyday,ctoday,dyday,dtoday])
            writer.writerow(row)
