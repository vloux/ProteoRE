#!/bin/bash --login                                                                                                                                                                                                                                                             
BANK=/db/KEGG_pathways   
DATE=`date +%d-%m-%y`
#DATE=00-12-00

mkdir -p $BANK/KEGG_pathways-$DATE/flat
mkdir -p $BANK/KEGG_pathways-$DATE/merged
mkdir -p $BANK/KEGG_pathways-$DATE/info

cd $BANK/KEGG_pathways-$DATE/flat

#get files from kegg
wget http://rest.kegg.jp/list/pathway/hsa
wget http://rest.kegg.jp/list/pathway/mmu

cd $BANK/KEGG_pathways-$DATE/merged

python ./pathways_list.py -i hsa -o hsa_pathways.tsv
python ./pathways_list.py -i mmu -o mmu_pathways.tsv

cd $BANK/KEGG_pathways-$DATE/info
ln -s /db/outils/kegg_pathways/README.txt .

cd $BANK

rm -f current
ln -s $BANK/KEGG_pathways-$DATE current

exit 0