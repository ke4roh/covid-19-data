#!/bin/sh

set -e

[[ $( ls 2020*.svg | wc -l ) > 0 ]] || rm 2020*.svg && rm -f latest.svg 

./analyze.py
convert latest.svg covid-19_rate_anim/latest.png

rsync -rv covid-19_rate_anim jimes@home.hiwaay.net:public_html/.
