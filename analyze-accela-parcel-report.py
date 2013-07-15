#!/usr/bin/python
from lxml import etree
import lxml.html
import StringIO
import string
import glob
import csv
import argparse
import sys

parser = argparse.ArgumentParser(description='Scrape the Indianapolis Citizens Access Portal')
parser.add_argument('-o', '--output', help='the filename to write the csv data to', required=True)
parser.add_argument('-i', '--input', help='the txt file to read file names from', required=False)
args = parser.parse_args()

csvFile = args.output
fileWriter = csv.writer(open(csvFile, 'wb'), dialect='excel')

if args.input:
	inputFileName = args.input
	inputFile = open(args.input, 'r')
	htmlFiles2 = inputFile.read()
	htmlFiles = htmlFiles2.split('\n') 
else:
	htmlFiles = glob.glob('*.html')
	htmlFiles.sort()	
totalSize = len(htmlFiles)
counter = 0
lxmlErrors = 0
errorMessages = 0
indexErrors = 0

fileWriter.writerow(['Parcel Number', 'Case Number'])

print "Analysing {0} files, writing to {1}".format(totalSize, csvFile)

for htmlFile in htmlFiles:
	counter = counter + 1
	try: fileName = open(htmlFile, 'r')
	except: continue
	html = fileName.read()
	try: 
		tree = lxml.html.fromstring(html)
	except: 
		print "\rLXML error with " + htmlFile
		lxmlErrors = lxmlErrors + 1
		continue
	if tree.xpath('//*[@id="ctl00_PlaceHolderMain_systemErrorMessage_lblMessageTitle"]/text()'): 
		print "\rError Message in " + htmlFile
		errorMessages = errorMessages + 1
		continue
	caseNumber = tree.xpath('//span[@id="ctl00_PlaceHolderMain_lblPermitNumber"]/text()')
	parcel = tree.xpath('//div[@id="ctl00_PlaceHolderMain_PermitDetailList1_palParceList"]/div[1]/div/text()')
	report = ' '.join(tree.xpath('//table[@class="ACA_TableWordBreak"][1]//span/text()'))
	try: 
		fileWriter.writerow([parcel[0], caseNumber[0]])
	except IndexError:
		print "\rIndexError with " + htmlFile
		indexErrors = indexErrors + 1
	progress = counter / float(totalSize) * 100
	sys.stdout.write( '\r[{0}] {1:.2f}%'.format('#'*(int(progress)/10), progress))
fileName.close()
print "\n{0} saved.".format(csvFile)
print "{0} files complete, {1} lxml errors, {2} files with error messages, {3} index errors".format(totalSize, lxmlErrors, errorMessages, indexErrors)
