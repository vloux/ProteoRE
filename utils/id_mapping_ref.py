#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This script is used to build a reference file "human_id_mapping.tsv" for ID_converter tool
#It replace the old one written by Lien Nguyen (IDmap_source.py)
# ex : ./id_mapping_ref.py -1 HUMAN_9606_idmapping.dat -2 HUMAN_9606_idmapping_selected.tab -3 nextprot_ac_list_all.txt
#for mus musculus, we do not need nextprot ID
# ex : ./id_mapping_ref.py -1 MOUSE_10090_idmapping.dat -2 MOUSE_10090_idmapping_selected.tab -o mouse_id_mapping.tsv

import argparse, csv, sys
csv.field_size_limit(sys.maxsize) # to handle big files

"""
Source files:
    - HUMAN_9606_idmapping.dat
    - HUMAN_9606_idmapping_selected.tab
      Tarball downloaded from ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/
    - nextprot_ac_list_all.txt 
      Downloaded from ftp://ftp.nextprot.org/pub/current_release/ac_lists/
"""

def human_id_mapping(dat_file, tab_file, all_nextprot):

    """
    header of HUMAN_9606_idmapping_selected.tab :
    1. UniProtKB-AC
    2. UniProtKB-ID
    3. GeneID (EntrezGene)
    4. RefSeq
    5. GI
    6. PDB
    7. GO
    8. UniRef100
    9. UniRef90
    10. UniRef50
    11. UniParc
    12. PIR
    13. NCBI-taxon
    14. MIM
    15. UniGene
    16. PubMed
    17. EMBL
    18. EMBL-CDS
    19. Ensembl
    20. Ensembl_TRS
    21. Ensembl_PRO
    22. Additional PubMed
    """

    #header
    if all_nextprot : tab = [["UniProt-AC","UniProt-ID","GeneID","RefSeq","GI","PDB","GO","PIR","MIM","UniGene","Ensembl","Ensembl_TRS","Ensembl_PRO","neXtProt","BioGrid","STRING","KEGG"]]
    else : tab = [["UniProt-AC","UniProt-ID","GeneID","RefSeq","GI","PDB","GO","PIR","MIM","UniGene","Ensembl","Ensembl_TRS","Ensembl_PRO","BioGrid","STRING","KEGG"]]

    #import HUMAN_9606_idmapping_selected.tab and keep only ids of interest
    with open(tab_file,"r") as tab_file :
        tab_file = csv.reader(tab_file,delimiter="\t")
        for line in tab_file :
            tab.append([line[i] for i in [0,1,2,3,4,5,6,11,13,14,18,19,20]])

    """
    Supplementary ID to get from HUMAN_9606_idmapping.dat :
    -NextProt
    -BioGrid
    -STRING
    -KEGG
    """

    if all_nextprot : ids = ['neXtProt','BioGrid','STRING','KEGG' ]   #ids to get from dat_file
    else : ids = ['BioGrid','STRING','KEGG' ]
    unidict = {}

    #import HUMAN_9606_idmapping.dat and keep only ids of interest in dictionaries
    with open(dat_file,"r") as dat_file :
        dat_file = csv.reader(dat_file,delimiter="\t")
        for line in dat_file :
            uniprotID=line[0]       #UniProtID as key
            id_type=line[1]         #ID type of corresponding id, key of sub-dictionnary
            cor_id=line[2]          #corresponding id
            if "-" not in id_type :                                 #we don't keep isoform
                if id_type in ids and uniprotID in unidict :
                    if id_type in unidict[uniprotID] :
                        unidict[uniprotID][id_type]= ";".join([unidict[uniprotID][id_type],cor_id])    #if there is already a value in the dictionnary
                    else :          
                        unidict[uniprotID].update({ id_type : cor_id })
                elif  id_type in ids :
                    unidict[uniprotID]={id_type : cor_id}

    #add ids from HUMAN_9606_idmapping.dat to the final tab
    for line in tab[1:] :
        uniprotID=line[0]
        if all_nextprot :
            if uniprotID in unidict :
                nextprot = access_dictionary(unidict,uniprotID,'neXtProt')
                if nextprot != '' : nextprot = clean_nextprot_id(nextprot,line[0])
                line.extend([nextprot,access_dictionary(unidict,uniprotID,'BioGrid'),access_dictionary(unidict,uniprotID,'STRING'),
                        access_dictionary(unidict,uniprotID,'KEGG')])
            else :
                line.extend(["","","",""])
        else :
            if uniprotID in unidict :
                line.extend([access_dictionary(unidict,uniprotID,'BioGrid'),access_dictionary(unidict,uniprotID,'STRING'),
                        access_dictionary(unidict,uniprotID,'KEGG')])
            else :
                line.extend(["","",""])

    
    if all_nextprot : 
        #build next_dict
        with open(all_nextprot,"r") as next_file :
            next_file = next_file.read().splitlines()
            next_dict = {}
            for nextid in next_file : 
                next_dict[nextid.replace("NX_","")] = nextid

        #add missing nextprot ID
        for line in tab[1:] : 
            uniprotID=line[0]
            nextprotID=line[13]
            if nextprotID == '' and uniprotID in next_dict :
                line[13]=next_dict[uniprotID]

    return (tab)


#return '' if there's no value in a dictionary, avoid error
def access_dictionary (dico,key1,key2) :
    if key1 in dico :
        if key2 in dico[key1] :
            return (dico[key1][key2])
        else :
            return ("")
            #print (key2,"not in ",dico,"[",key1,"]")
    else :
        return ('')

#if there are several nextprot ID for one uniprotID, return the uniprot like ID
def clean_nextprot_id (next_id,uniprotAc) :
    if len(next_id.split(";")) > 1 :
        tmp = next_id.split(";")
        if "NX_"+uniprotAc in tmp :
            return ("NX_"+uniprotAc)
        else :
            return (tmp[1])
    else :
        return (next_id)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-1","--dat_file", help="human ID mapping file (.dat)", required=True)
    parser.add_argument("-2","--tab_file", help="human ID mapping file (_selected.tab)", required=True)
    parser.add_argument("-3","--next_file", help="list of all nextprot ID")
    parser.add_argument("-o","--output", default="./human_id_mapping_file.tsv", help="output filename") 

    args = parser.parse_args()

    human_mapping = args.dat_file
    human_mapping_selected = args.tab_file
    all_nextprot = args.next_file

    output = human_id_mapping(human_mapping, human_mapping_selected, all_nextprot)
    
    with open(args.output,"w") as out :
        writer = csv.writer(out,delimiter="\t")
        writer.writerows(output)

if __name__ == "__main__":
    main()
