#!/bin/sh

set -e

[[ -e 2020*.svg ]] && rm 2020*.svg

./analyze.py
LAST=$(ls 2020*.svg | tail -1)
THRU=$(echo $LAST | sed  's/.svg$//' )

convert -coalesce  -delay 35   -loop 0   $LAST 2020*.svg $LAST $LAST $LAST $LAST $LAST $LAST $LAST $LAST $LAST $LAST Covid-19_thru_$THRU.gif
