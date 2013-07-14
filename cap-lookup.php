<?php
#01234567890
#VBO12-01576
caseNumber = $_GET['casenumber']
prefix = substr(caseNumber, 0,2)
year = substr(caseNumber, 3,4)
number = substr(caseNumber, 6,10)
header( 'http://permitsandcases.indy.gov/CitizenAccess/Cap/CapDetail.aspx?Module=HHC&TabName=HHC&capID1='+year+''+prefix+'&capID2=00000&capID3='+number+'&agencyCode=INDY&IsToShowInspection=' ) ;
?>
