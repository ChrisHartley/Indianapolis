#!/bin/sh
#cd /tmp
#export URL="http://www.indy.gov/eGov/County/Treasurer/Documents/Master%20List%20as%20of%204-10-2013.pdf"
#curl $1 > /tmp/parcels.pdf 
#pdftotext -enc ASCII7 -layout /tmp/parcels.pdf - | grep "[0-9]\{7\}"
curl -o /tmp/parcels.pdf $1 
pdftotext -enc ASCII7 -layout /tmp/parcels.pdf - | grep -o "[0-9]\{7\}" > $2
