#!/usr/bin/python
import urllib2
import cookielib
from lxml import etree
import lxml.html
import StringIO
import string
import os
import argparse

parser = argparse.ArgumentParser(description='Scrape the Indianapolis Citizens Access Portal')
parser.add_argument('-c', '--casetype', help='the case or permit prefix', required=True, choices=['TRA', 'DEM', 'REP', 'VBO', 'HIN', 'HSG', 'STR'])
parser.add_argument('-r', '--range', nargs='*', type=int, help="the starting and ending range to scrape", required=False)
parser.add_argument('-y', '--year', type=int, help='two digit year to scrape', required=True)
args = parser.parse_args()

caseType = args.casetype
caseYear = args.year
try:
	caseRange = range(args.range[0],args.range[1]+1)
except:
	try:
		caseRange = range(args.range[0],99999)
	except:
		caseRange = range(1,99999)

print "" + str(caseRange[0]) + "..." + str(caseRange[-1])
# Set up cookies to work like regular browser and access entry URL to get set up properly
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
first = opener.open("http://www.indy.gov/eGov/City/DCE/Pages/Citizen%20Access%20Portal.aspx")

# Step through all cases
for case in caseRange:
	fileName = caseType +str(caseYear)+'-'+string.zfill(case, 5)+'.html'
	print "File name: ", fileName,
	if not (os.path.isfile(fileName)):
		url = 'http://permitsandcases.indy.gov/CitizenAccess/Cap/CapDetail.aspx?Module=HHC&TabName=HHC&capID1=%(year)d%(caseType)s&capID2=00000&capID3=%(#)05d&agencyCode=INDY&IsToShowInspection="' % {"year": caseYear, "caseType": caseType , "#": case}
#http://permitsandcases.indy.gov/CitizenAccess/Cap/CapDetail.aspx?Module=HHC&TabName=HHC&capID1=13REP&capID2=00000&capID3=00796&agencyCode=INDY&IsToShowInspection=
		try: f = opener.open(url)
		except: 
			print "URL error"
			print url
		html = f.read()
	# <span id="ctl00_PlaceHolderMain_systemErrorMessage_lblMessageTitle" class="ACA_Show">An error has occurred.</span>
		isError = string.find(html, '<span id="ctl00_PlaceHolderMain_systemErrorMessage_lblMessageTitle" class="ACA_Show">An error has occurred.</span>')	
		if (isError != -1):
			print "error detected, ending"
			break
		file = open(fileName, "w")	
		file.write(html)
		print "written"
	else:
		print "skipped"

#	tree = lxml.html.fromstring(html)
#	caseNumber = tree.xpath('//span[@id="ctl00_PlaceHolderMain_lblPermitNumber"]/text()')
#	parcel = tree.xpath('//div[@id="ctl00_PlaceHolderMain_PermitDetailList1_palParceList"]/div[1]/div/text()')
#	print "Case: %(case)s Parcel: %(parcel)s " % {"case":caseNumber, "parcel":parcel}
#	i = 0
#	fileName = caseNumber[0] + '-' + str(i) + '.html'
#	while os.path.isfile(fileName): 
#		i += 1
#		fileName = caseNumber[0] + '-' + str(i) + '.html'	

