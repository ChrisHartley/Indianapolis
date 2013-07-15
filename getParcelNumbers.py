#!/usr/bin/python
import urllib2
import urllib
import cookielib
from lxml import etree
import lxml.html
import StringIO
import string
import os
import argparse
import csv


parser = argparse.ArgumentParser(description='Scrape the Indianapolis Citizens Access Portal')
parser.add_argument('-o', '--output', help='the filename to write the csv data to', required=True)
parser.add_argument('-i', '--input', help='the filename to read addresses from, one per line', required=True)
args = parser.parse_args()

csvFile = args.output
fileWriter = csv.writer(open(csvFile, 'wb'), dialect='excel')
fileWriter.writerow(['Address', 'Parcel Number'])

inputFileName = args.input
addresses = open(inputFileName, 'r')
counter = 0
for address in addresses:
	counter = counter + 1
	outputFileName = "file{0}.txt".format(str(counter))
	if (os.path.isfile(outputFileName)): continue
	print address
	url = "http://imaps.indygov.org/ed/ed.asp?cmd=findbyaddress&maxx=294760.836296051&minx=99493.1637039486&miny=1579193.29563099&maxy=1722726.70436901&vis=&nvis=&p=1&t=1&x1=&y1=&label=&city=&zipcode=&selid=&s=1400&h=938&address={0}&Submit=Search".format(urllib.quote_plus(address.strip()))
	print url

	#try: 
	f = urllib2.urlopen(url)
	#except: 
	#	print "URL error " + url
	#	continue
	html = f.read()
	outputFile = open(outputFileName, 'wb')
	outputFile.write(html)
	try: 
		tree = lxml.html.fromstring(html)
	except: 
		print "LXML error with " + address
		continue
	parcel = tree.xpath("/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[3]/table/tbody/tr/td/table/tbody/tr[3]/td[2][@class='storyText']/a/text()")
	print parcel
	try: 
		fileWriter.writerow([address, parcel])
	except:
		print "Error writing"
		continue




