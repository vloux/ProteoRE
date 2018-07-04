#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This script is used to build a pathways list file for Pathview tool

import argparse, csv, sys
csv.field_size_limit(sys.maxsize) # to handle big files

"""
Source files:
    - http://rest.kegg.jp/list/pathway/hsa
    - http://rest.kegg.jp/list/pathway/mmu
    - http://rest.kegg.jp/list/pathway/example
"""

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="file from http://rest.kegg.jp/list/pathway/, example : hsa", required=True)
parser.add_argument("-o","--output", help="output filename") 

args = parser.parse_args()

tab=[['#value',"name"]]
#import pathways from file :
with open(args.input,"r") as tab_file :
        tab_file = csv.reader(tab_file,delimiter="\t")
        for line in tab_file :
            tmp = [line[0].replace("path:","")]             #remove 'path:' from value
            tmp.append(line[1].split(" - ")[0])     #remove suffix from name
            tab.append(tmp)

with open(args.output,"w") as out :
    writer = csv.writer(out,delimiter="\t")
    writer.writerows(tab)

