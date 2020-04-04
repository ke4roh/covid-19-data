#!/usr/bin/env python3

import csv
from datetime import timedelta, datetime

counts = {}
dates = set()
fips = set()

def procRow(row):
     dt = datetime.strptime(row['date'],"%Y-%m-%d").date()
     counts[(dt,row['fips'])] = int(row['cases'])
     dates.add(dt)
     fips.add(row['fips'])

# Read in counties and case counts
with open('us-counties.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         if row['county'] == "New York City":
             for c,f in (("Bronx","36005"),("Kings","36047"),("New York County","36061"),("Richmond County","36085"),("Queens","36081")):
                 r2 = dict(row)
                 r2["county"]=c
                 r2["fips"]=f
                 procRow(r2)
         else:
             procRow(row)

dates = sorted(dates)
fips = sorted(fips)

# Compute the daily growth rate for the past week as a percentage of the sum of cases
week = timedelta(weeks=1)
rates = {}
daily_rates = {}
first_day = None

for date in dates[6:]:
    daily_rates[date] = []
    for co in fips:
        try:
           today_sum = counts[(date,co)]
           weeks_growth = today_sum - counts[(date - week,co)]
           if today_sum > 5:
               first_day = first_day or date
               rate = weeks_growth / today_sum / 7
               rates[(date,co)]=rate
               daily_rates[date].append(rate)
        except KeyError:
            pass

# Calculate daily quintiles
# quintiles = {}
# for date,drates in daily_rates.items():
#     srates = sorted(drates)
#     if (len(srates)>5):
#         quintiles[date] = srates[0:len(srates):int(len(srates)/5)]
#         print(str(quintiles[date]))

styles= """#00876c
#439981
#6aaa96
#8cbcac
#aecdc2
#cfdfd9
#f1f1f1
#f1d4d4
#f0b8b8
#ec9c9d
#e67f83
#de6069
#d43d51""".split("\n")

# Assign styles to counties
co_styles = { }
for dc,rate in rates.items():
    (date,co) = dc
    style = styles[min(len(styles)-1,max(0,int((rate+.14)/.14*7)))]
    co_styles.setdefault((date,style),[] ).append(co)
    # print(",".join((date.strftime("%Y-%m-%d"),co,style)))

# Render styles for one date
def renderStyles(f,date):
    for style in styles:
        if (date,style) in co_styles:
            f.write("#c" +  ", #c".join(co_styles[(date,style)]) + " { fill:" + style +" }\n" )

# Render animation styles
def renderAnim(f):
    f.write("@keyframes country_anim {\n")
    for i in range(0, len(dates)):
        f.write( str(int(i/len(dates)*100)) + "% {\n")
        renderStyles(f,date)
        f.write("}\n")
    f.write("""
}
.country_anim {
  animation: country_anim 20s linear infinite;
}
""")

for date in [first_day + timedelta(days=x) for x in range(0, (dates[-1]-first_day).days)]:
    with open('Usa_counties_large.svg') as carta:
        #with open(dates[-1].strftime("%Y-%m-%d") + ".svg",'w') as cartb:
        with open(date.strftime("%Y-%m-%d") + ".svg",'w') as cartb:
            for line in carta:
                if "</style>" in line:
                    #renderAnim(cartb)
                    renderStyles(cartb,date)
                elif "</tspan>" in line:
                    cartb.write(date.strftime("%Y-%m-%d"))
                cartb.write(line)
            
