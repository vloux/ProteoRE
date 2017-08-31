#!/bin/bash
# Goal : Retrieve all information from nextprot for all the proteins in
# netxtprot (listed in
# ftp://ftp.nextprot.org/pub/current_release/ac_lists/nextprot_ac_list_all.txt)
# For each id in the nextprot_ac_list_all.txt file, the script
# query_nextprot_v2.js is executed and its result is added to
# result_nextprot.txt
# NB : Sometimes the connection to nextprot
# can be lost and the process is stopped. In that case you need to execute the
# script with a file of accession ids from the last id you retrieved to the
# last id of the nextprot_ac_list_all.txt file.


nextprot=`cat nextprot_ac_list_all.txt`

echo -e "NextprotID\tMW\tSeqLength\tIsoPoint\tChr\tSubcellLocations\tDiseases\tTMDomains\tProteinExistence">> result_nextprot.txt 
for i in $nextprot;do
	node query_nextprot_v2.js $i >> result_nextprot.txt 
	echo $i
done
