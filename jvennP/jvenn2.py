#!/usr/bin/env python2.7
#
# Copyright (C) 2015 INRA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""__author__ = 'Katia Vidal - Team NED Toulouse AND Frederic Escudie - Plateforme bioinformatique Toulouse'
__copyright__ = 'Copyright (C) 2015 INRA'
__license__ = 'GNU General Public License'
__version__ = '1.3.2'
__email__ = 'frogs@toulouse.inra.fr'
__status__ = 'prod'"""


import os
import sys
import json
import operator
import argparse
import re
from itertools import combinations

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PATH
"""BIN_DIR = os.path.abspath(os.path.join(os.path.dirname(CURRENT_DIR), "libexec"))
os.environ['PATH'] = BIN_DIR + os.pathsep + os.environ['PATH']
# PYTHONPATH
LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(CURRENT_DIR), "lib"))
sys.path.append(LIB_DIR)
if os.getenv('PYTHONPATH') is None: os.environ['PYTHONPATH'] = LIB_DIR
else: os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + os.pathsep + LIB_DIR"""



##################################################################################################################################################
#
# COMMAND LINES
#
##################################################################################################################################################



##################################################################################################################################################
#
# FUNCTIONS
#
##################################################################################################################################################

def write_summary( summary_file, inputs):#, names):
    """
    @summary: Writes the process summary.
    @param summary_file: [str] The path to the output file.
    @param input_biom: [str] The path to the BIOM before program execution.
    @param output_biom: [str] The path to the BIOM after program execution.
    @param discards: [dict] By filter the path of the file that contains the list of the removed observations.
    """
    """global_results = {
        'nb_clstr_kept': 0,
        'nb_clstr_ini': 0,
        'nb_seq_kept': 0,
        'nb_seq_ini': 0
    }
    samples_results = dict()
    filters_results = dict()"""

    a, b = input_to_dict(inputs)#, names)
    data = diagram(a, b)
    write_text_venn(data)

    to_replace = {
    	"series": [data],
    }
    #print(to_replace)

    # Global before filters
    FH_summary_tpl = open( os.path.join(CURRENT_DIR, "jvenn_tpl.html") )
    FH_summary_out = open( summary_file, "w" )
    for line in FH_summary_tpl:
        if "###JVENN_DATA###" in line:
            line = line.replace("###JVENN_DATA###", json.dumps(to_replace))
        #if "###PORCESSED_FILTERS###" in line:
        #    line = line.replace( "###PORCESSED_FILTERS###", json.dumps([filter for filter in discards]) )
        #elif "###GLOBAL_RESULTS###" in line:
        #    line = line.replace( "###GLOBAL_RESULTS###", json.dumps(global_results) )
        #elif "###SAMPLES_RESULTS###" in line:
        #    line = line.replace( "###SAMPLES_RESULTS###", json.dumps(samples_results) )
        #elif "###FILTERS_RESULTS###" in line:
        #    line = line.replace( "###FILTERS_RESULTS###", json.dumps(filters_results.values()) )
        FH_summary_out.write( line )
    
    FH_summary_out.close()
    FH_summary_tpl.close()
    
def isnumber(format, n):
    float_format = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
    int_format = re.compile("^[\-]?[1-9][0-9]*$")
    test = ""
    if format == "int":
        test = re.match(int_format, n)
    elif format == "float":
        test = re.match(float_format, n)
    if test:
        return True
    else:
        return False

def input_to_dict(inputs):#comp_files, names):
    comp_dict = {}
    title_dict = {}
    #print(len(comp_files), comp_files[0])
    c = ["A", "B", "C", "D", "E", "F"]  # "A" is for MQ file
    for i in range(len(inputs)):#comp_files)):
        input_file = inputs[i][0]
        name = inputs[i][1]
        input_type = inputs[i][2]
        title = c[i]
        title_dict[title] = name
        ids = set()
        if input_type == "mq_file":
            ncol = inputs[i][3]
            file_content = open(input_file, "r").readlines()
            
            if isnumber("int", ncol.replace("c", "")):
                file_content = [x for x in [line.split("\t")[int(ncol.replace("c", ""))-1].split(";")[0] for line in file_content[1:]]]     # take only first IDs
                #print(file_content[1:13])
            else:
                raise ValueError("Please fill in the right format of column number")
        elif input_type == "file":
            file_content = open(input_file, "r").readlines()
            file_content = [x.replace("\n", "") for x in file_content]
            file_content = [x.replace("\r", "") for x in file_content]         
        else:
            ids = set()
            file_content = inputs[i][0].split()
            
        ids.update(file_content)
        comp_dict[title] = ids
 
    return comp_dict, title_dict

def intersect(comp_dict):
    # Calculate elements frequencies
    names = set(comp_dict)
    for i in range(1, len(comp_dict) + 1):
        for group in combinations(sorted(comp_dict), i):
	        difference = {}
	        print(group)
	        intersected = set.intersection(*(comp_dict[k] for k in group))
	        #print(intersected)
	        """if len(group) == 2 and "A" in group:  #get different elements of query and each other lists
	            n = "".join(group)
	            dif = set(comp_dict["A"]).difference(set(comp_dict[group[1]]))
	            difference[n] = dif
	            print("dif", dif)"""
	        if len(group) == len(comp_dict):
		        for j in range(len(group)):
		            #print(j)
		            n = group[j]
		            g = group[:j] + group[j+1:]
		            #print(n, g)
		            #print("comp", comp_dict[n])
		            dif = set(comp_dict[n]).difference(set.union(*(comp_dict[k] for k in g)))
		            #print("dif", dif)
		            difference[n] = dif
	    	yield group, list(intersected), difference

def diagram(comp_dict, title_dict):
    # Extract protein IDs in MQfile
    prot_ids = set()
    """if MQfile[2] == "mq_file":
        mq = open(MQfile[0], "r").readlines()
        if ncol != "None":
            if isnumber("int", ncol.replace("c", "")):
                mq = [x for x in [line.split("\t")[int(ncol.replace("c", ""))-1] for line in mq[1:]]]
            else:
                raise ValueError("Please fill in the right format of column number")
        else:
            # Extract gene names and protein ids column number
            column_names = mq[0].split("\t")
            #print(column_names)
            for i in range(len(column_names)):
                #print(column_names[i])
                if column_names[i] == "Majority protein IDs":
                    ncol = i
            if ncol == "None":
                raise ValueError("Could not find 'Majority protein IDs' column")
            mq = [x for x in [line.split("\t")[ncol] for line in mq[1:]]]
    elif MQfile[2] == "list_file":
        mq = open(MQfile[0], "r").readlines()
        mq = [x for x in [line.strip() for line in mq[1:]]]
    elif MQfile[2] == "list":
        mq = MQfile[0].split()
    prot_ids.update(mq)"""
    #print(prot_ids)

    # Add MQfile into dictionary
    """mqlist = {"name": MQfile[1].replace(".txt", ""), "ids": prot_ids}
    comp_dict["A"] = mqlist["ids"]
    title_dict["A"] = mqlist["name"]"""
    #print(title_dict)
    #print(comp_dict)

    result = {}
    result["name"] = {}
    #print(comp_dict.keys())
    for k in comp_dict.keys():
	#print(k)
        result["name"][k] = title_dict[k]
        
    result["data"] = {}
    result["values"] = {}    
    #print(intersect(comp_dict))
    for group, intersected, difference in intersect(comp_dict):
        #print(group, intersected, difference)
        if len(group) > 1 and len(group) != len(comp_dict):
	        result["data"]["".join(group)] = intersected
	        result["values"]["".join(group)] = len(intersected)
	        """if len(group) == 2 and "A" in group:
                file_common = "%s_common.txt" % ("_".join([result["name"][k] for k in group]))
                file_dif = "%s_specific.txt" % ("_".join([result["name"][k] for k in group]))
                f_common = open(file_common, "w")
                f_common.write("\n".join(intersected))
                f_common.close()
                f_dif = open(file_dif, "w")
                f_dif.write("\n".join(difference["".join(group)]))
                f_dif.close()"""
                
        elif len(group) == len(comp_dict):
            #print(difference)
            result["data"]["".join(group)] = intersected
            result["values"]["".join(group)] = len(intersected)
            for k in comp_dict.keys():
                result["data"][k] = list(difference[k])
                result["values"][k] = len(difference[k])
    #print(result)
    return result
    
def write_text_venn(json_result):
    for data in json_result["data"].keys():
        name = "_".join([json_result["name"][x] for x in data])
        filename = name + "_venn.txt"
        output = open(filename, "w")
        output.write("\n".join(json_result["data"][data]))
        output.close()


def process( args ):
	
        write_summary( args.summary, args.input)#, args.names)


##################################################################################################################################################
#
# MAIN
#
##################################################################################################################################################
if __name__ == '__main__':
    # Parameters
    parser = argparse.ArgumentParser(description='Filters an abundance file')
    group_input = parser.add_argument_group( 'Inputs' )
    #group_input.add_argument('--mq', nargs=3, metaval=("INPUT", "NAME", "TYPE"), required=True)
    #group_input.add_argument('--ncol', default="None")
    # Input consists of the file/text, name and type ("file" or "list")
    group_input.add_argument('--input', nargs="+", action="append", required=True, help="The input tabular file.")
    #group_input.add_argument('--names', nargs="+")
    group_output = parser.add_argument_group( 'Outputs' )
    group_output.add_argument('--summary', default="summary.html", help="The HTML file containing the graphs. [Default: %(default)s]")
    args = parser.parse_args()
    #print(args.input)

    # Process
    process( args )
