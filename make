#!/bin/sh

./analyze.sh
convert   -delay 20   -loop 0   2020*.svg   Covid-19.gif
