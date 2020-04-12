#!/usr/bin/env python3

import csv
from datetime import timedelta, datetime
from sys import exit
from math import log
from colorsys import hsv_to_rgb
from collections import defaultdict
from yaml import dump

county_pop = {}
counts = {}
dates = set()
fips = set()

def procRow(row):
     dt = row['date']
     # Some counts decrease (usually just some data blip), so hold them at the higher value until it catches up... 
     counts[(dt,row['fips'])] = max(row['cases'],counts.get((dt-timedelta(days=1),row['fips']),0))
     dates.add(dt)
     fips.add(row['fips'])

# Read in counties and their population
with open("co-est2019-alldata.csv",newline='',encoding='cp1252') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        co=row["COUNTY"].zfill(3)
        fi=row["STATE"].zfill(2) + co
        if (co != "000"):
            county_pop[fi]=int(row["POPESTIMATE2019"])

# Read in counties and case counts
kc_rows = []
with open('us-counties.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         row['date'] = datetime.strptime(row['date'],"%Y-%m-%d").date()
         row['cases'] = int(row['cases'])
         if row['county'] == "New York City":
             for c,f in (("Bronx","36005"),("Kings","36047"),("New York County","36061"),("Richmond County","36085"),("Queens","36081")):
                 r2 = dict(row)
                 r2["county"]=c
                 r2["fips"]=f
                 procRow(r2)
         elif row['county'] == "Kansas City":
             kc_rows.append(row)
         else:
             procRow(row)

# From the Covid-19 data set caveats:
# Four counties (Cass, Clay, Jackson and Platte) overlap the municipality of Kansas City, Mo. 
# The cases and deaths that we show for these four counties are only for the portions 
# exclusive of Kansas City. Cases and deaths for Kansas City are reported as their own line.
# So... assign the cases to the counties in proportion to their population.
for row in kc_rows:
    # Cass, Clay, Johnson, Platte
    for f,weight in (('29037',0.101),('29047',0.233),('29101',0.571),('29165',0.095)):
        key = (row['date'],f)
        counts[key] = counts.get(key,0) + int(row["cases"] * weight + 0.5)


dates = sorted(dates)
fips = sorted(fips)

# Compute the daily growth rate for the past week as a percentage of the sum of cases
week = timedelta(weeks=1)
rates = {}
daily_rates = {}
daily_pops = {}
first_day = None

for date in dates[6:]:
    daily_rates[date] = []
    daily_pops[date] = []
    for co in fips:
        try:
           today_sum = counts[(date,co)]
           weeks_growth = today_sum - counts[(date - week,co)]
           if today_sum > 5:
               first_day = first_day or date
               rate = weeks_growth / today_sum / 7
               rates[(date,co)]=rate
               daily_rates[date].append(rate)
               daily_pops[date].append(rate/county_pop[co])
        except KeyError:
            pass

# Calculate daily quintiles
def quintiles():
    for name,m in (("rate",daily_rates),("pop",daily_pops)):
        print("\n\n##################################### %s #######################################" % name)
        overall = []
        quintiles = {}
        for date,drates in m.items():
            srates = sorted(drates)
            overall.extend(drates)
            if (len(srates)>5):
                quintiles[date] = srates[0:len(srates):int(len(srates)/5)] # this gives the max, too
                print(str(quintiles[date]))
                print(str([x/quintiles[date][-1] for x in quintiles[date]]))

        overall = sorted(overall)
        ranks=(0,.01,.03,.05,.10,.25,.50,.75,.90,.95,.97,.99,.99999)
        print("Overall: " + " ".join(["%2.1e %d%%" %(overall[int(len(overall)*r)], int(r*100+0.5)) for r in ranks]))

# quintiles()
# exit(0)

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

def clamp(n):
    return int(max(0,min(255,n)))

def stylize(rgb): 
    # print(str(rgb))
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(rgb[0]*255), clamp(rgb[1]*255), clamp(rgb[2]*255))   
    
# Assign styles to counties
co_styles = defaultdict(dict)
for dc,rate in rates.items():
    (date,co) = dc
    if not co:
        continue

    # Overall: 0.0e+00 0% 1.8e-02 1% 3.3e-02 3% 4.2e-02 5% 5.4e-02 10% 7.4e-02 25% 9.6e-02 50% 1.2e-01 75% 1.3e-01 90% 1.3e-01 95% 1.3e-01 97% 1.4e-01 99% 1.4e-01 100%
    if (rate>0.0000000001):
        rate_factor = 1 + (log(rate) - log(0.2))/log(100)
    else: 
        rate_factor = 0
   
    # Overall: 0.0e+00 0% 2.4e-08 1% 5.2e-08 3% 7.3e-08 5% 1.2e-07 10% 2.8e-07 25% 7.3e-07 50% 1.8e-06 75% 3.7e-06 90% 5.3e-06 95% 6.5e-06 97% 1.1e-05 99% 4.3e-05 100% 
    try:
       pop_factor = 1 + (log(.1) - log(counts[dc]/county_pop[co]))/log(1e-5)
    except KeyError:
       pop_factor = .5
       print("No population for " + co)

    # For hue, 0=1=red, .333 = green, .667 = blue, -.333 = purple
    style = stylize(hsv_to_rgb(
            .5 * (1 - max(0,min(1,rate_factor))) - 1/6, 
            pop_factor,
            1 - (rate_factor*.2)
     ))
    # print("style=%s  r = %.4f  p = %.4f " % (style, rate_factor, pop_factor))
    co_styles[date].setdefault(style,[]).append(co)
    # print(",".join((date.strftime("%Y-%m-%d"),co,style)))

# Render styles for one date
def renderStyles(f,date):
    for style in co_styles[date].keys():
        f.write("#c" +  ", #c".join(co_styles[date][style]) + " { fill:" + style +" }\n" )

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

for date in [first_day + timedelta(days=x) for x in range(0, (dates[-1]-first_day).days+1)]:
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
            
