<?php
#01234567890
#VBO12-01576
$caseNumber =  $_GET['casenumber'] ;
$prefix = substr($caseNumber, 0,3);
$year = substr($caseNumber, 3,2);
$number = substr($caseNumber, 6);
$url = "http://permitsandcases.indy.gov/CitizenAccess/Cap/CapDetail.aspx?Module=HHC&TabName=HHC&capID1={$year}{$prefix}&capID2=00000&capID3={$number}&agencyCode=INDY&IsToShowInspection=";
header("Location: ".$url) ;
#echo $caseNumber.'</br>';
#echo $prefix.'</br>';
#echo $year.'</br>';
#echo $number.'</br>';
#echo $url.'</br>';
?>
