#!/bin/sh
cd /home/chris/Projects/codeEnforcement
for code in `ls -fd *`; do
	cd $code
	scrape-accela.py -c $code -y `date +%y`
	analyze-accela-parcel-report.py -o $code.csv
	psql -d gis -c "truncate code_enforcement; copy code_enforcement from '/home/chris/Projects/codeEnforcement/$code/$code.csv' with csv header"
	pgsql2shp -g st_centroid -f $code-`date +%Y%m%d`.shp gis "select *, ST_Centroid(geom) from parcels_20130530 as p left join code_enforcement as c on c.parcel = p.parcel_c where c.parcel is not null"
	cd ..
done
