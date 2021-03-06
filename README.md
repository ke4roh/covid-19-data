# Coronavirus (Covid-19) Trend in the United States

This set of scripts, in conjunction with the New York Times Covid-19 data and a map from Wikimedia Commons 
presents an animation of the trend of Covid-19 as it has worked its way through the United States.

For a county to be colored on this map, it must have at least 5 confirmed cases.

The hue displayed is the log of the running average of new cases as a proportion of new cases for the 
preceding month.  A similar metric was highlighted as an indicator on the YouTube video "How To 
tell if We're Beating COVID-19" (see below).

Purple is the worst rate at .14% increase daily; green is under control.  The worse colors are also a little darker to help with colorblindness.

Saturation of the color corresponds to the log of population saturation.  As more people in an area are infected,
the color becomes more saturated.  

Dark green indicates no new cases in the past 30 days when there previously were at least 5 cases.

There are a few places in the NYT data set where the cumulative number of cases decreases because
of some data error.  This is treated as a 0 growth for the day of the decrease.

![The latest map](latest.svg "A map of the United States by county showing the latest data for Covid-19 spread.  The spreadsheet gives similar information by state on the tab labeled By State.")

See [The animated map](http://home.hiwaay.net/~jimes/covid-19_rate_anim/) and [accompanying spreadsheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vSTIhpyzdht8F1abRa27Cxd69EVToTh4E45sCa5hXEmdhHNu8T5As-mrWkUlK8DCCJ0WAN3FhEMcFDV/pubhtml)

# Resources
* [How To Tell If We are Beating COVID-19](https://youtu.be/54XLXg4fYsc) (YouTube)
* [The New York Times Coronavirus tracking](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html), CC-BY-SA-NC
* [US Counties Map](https://commons.wikimedia.org/wiki/File:Usa_counties_large.svg) PD
* [US Census County Populations](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html#par_textimage_70769902) PD
* [JQuery UI](https://jqueryui.com/) MIT
