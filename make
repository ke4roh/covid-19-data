#!/bin/sh

set -e

[[ $( ls 2020*.svg | wc -l ) > 0 ]] || rm 2020*.svg && rm latest.png

./analyze.py
LAST=$(ls 2020*.svg | tail -1)
THRU=$(echo $LAST | sed  's/.svg$//' )
convert $LAST latest.png

convert -coalesce  -delay 35   -loop 0   $LAST 2020*.svg $LAST $LAST $LAST $LAST $LAST $LAST $LAST $LAST $LAST $LAST Covid-19_thru_$THRU.gif
