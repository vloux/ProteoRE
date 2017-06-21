import argparse
from protein import Protein
from readMQ import *

"""
Different functions for each of filtering options
"""

def readOption(filename):
    f = open(filename, "r")
    file = f.read()
    #print(file)
    filter_list = file.split("\n")
    #print(filter_list)
    filters = ""
    for i in filter_list:
        filters += i + ":"
    filters = filters[:-1]
    #print(filters)
    return filters

def filter_tech(proteins):
    filtered_prots = []
    for prot in proteins:
        #print("1 " + prot.c2iBAQ + "2 " + prot.c3iBAQ + "3 " + prot.s2iBAQ + "4 " + prot.s3iBAQ)
        if prot.iBAQ == "NaN":
            #print("1 " + prot.c2iBAQ + " 2 " + prot.c3iBAQ + " 3 " + prot.s2iBAQ + " 4 " + prot.s3iBAQ)
            filtered_prots.append(prot)
	elif prot.iBAQ == "":
	    filtered_prots.append(prot)
        else:
            if float(prot.c2iBAQ) != 0 and float(prot.c3iBAQ) != 0:
                #print("1 " + prot.c2iBAQ + " 2 " + prot.c3iBAQ + " 3 " + prot.s2iBAQ + " 4 " + prot.s3iBAQ)
                if float(prot.s2iBAQ)/float(prot.c2iBAQ) >= 100 and float(prot.s3iBAQ)/float(prot.c3iBAQ) >= 100:
                    filtered_prots.append(prot)
            else:
                filtered_prots.append(prot)
    return filtered_prots

def filter_protIDs(proteins, filterIDs):
    ids = filterIDs.split(":")
    filtered_prots = []
    for prot in proteins:
        if not any (n in ids for n in prot.proteinIDs.split(";")):
            filtered_prots.append(prot)
    return filtered_prots

def filter_prot_names(proteins, filter_names):
    names = filter_names.split(":")
    filtered_prots = []
    for prot in proteins:
        if not any (n in names for n in prot.protein_names.split(";")):
            filtered_prots.append(prot)
    return filtered_prots

def filter_gene_names(proteins, filter_names):
    names = filter_names.split(":")
    filtered_prots = []
    for prot in proteins:
        if not any (n in names for n in prot.gene_names.split(";")):
            filtered_prots.append(prot)
    return filtered_prots

def filter_pep(proteins, filter_value, opt):
    # Filter by value, opt: >, >= or <, <= or =
    filtered_prots = []
    filter_value = int(filter_value)
    if opt == "<":
        for prot in proteins:
            if int(prot.peptides) < filter_value:
                filtered_prots.append(prot)
    elif opt == "<=":
        for prot in proteins:
            if int(prot.peptides) <= filter_value:
                filtered_prots.append(prot)
    elif opt == ">":
        for prot in proteins:
            #print(prot.peptides, filter_value, int(prot.peptides) > filter_value)
            if int(prot.peptides) > filter_value:
                filtered_prots.append(prot)
    elif opt == ">=":
        for prot in proteins:
            if int(prot.peptides) >= filter_value:
                filtered_prots.append(prot)
    else:
        for prot in proteins:
            if int(prot.peptides) == filter_value:
                filtered_prots.append(prot)
    return filtered_prots

def filter_fasta(proteins, filter_names):
    names = filter_names.split(":")
    filtered_prots = []
    for prot in proteins:
        if not any (n in names for n in prot.fasta_headers.split(";")):
            filtered_prots.append(prot)
    return filtered_prots

def filter_noProt(proteins, filter_value, opt):
    filtered_prots = []
    filter_value = int(filter_value)
    if opt == "<":
        for prot in proteins:
            if int(prot.number_of_prots) < filter_value:
                filtered_prots.append(prot)
    elif opt == "<=":
        for prot in proteins:
            if int(prot.number_of_prots) <= filter_value:
                filtered_prots.append(prot)
    elif opt == ">":
        for prot in proteins:
            #print(prot.number_of_prots, filter_value, int(prot.number_of_prots) > filter_value)
            if int(prot.number_of_prots) > filter_value:
                filtered_prots.append(prot)
    elif opt == ">=":
        for prot in proteins:
            if int(prot.number_of_prots) >= filter_value:
                filtered_prots.append(prot)
    else:
        for prot in proteins:
            if int(prot.number_of_prots) == filter_value:
                filtered_prots.append(prot)
    return filtered_prots

def filter_qVal(proteins,  filter_value, opt):
    filtered_prots = []
    filter_value = float(filter_value)
    if opt == "<":
        for prot in proteins:
            if float(prot.q_value) < filter_value:
                filtered_prots.append(prot)
    elif opt == "<=":
        for prot in proteins:
            if float(prot.q_value) <= filter_value:
                filtered_prots.append(prot)
    elif opt == ">":
        for prot in proteins:
            #print(prot.q_value, filter_value, prot.q_value > filter_value)
            if float(prot.q_value) > filter_value:
                filtered_prots.append(prot)
    elif opt == ">=":
        for prot in proteins:
            if float(prot.q_value) >= filter_value:
                filtered_prots.append(prot)
    else:
        for prot in proteins:
            if float(prot.q_value) == filter_value:
                filtered_prots.append(prot)
    return filtered_prots

def filter_score(proteins,  filter_value, opt):
    filtered_prots = []
    filter_value = float(filter_value)
    if opt == "<":
        for prot in proteins:
            if float(prot.score) < filter_value:
                filtered_prots.append(prot)
    elif opt == "<=":
        for prot in proteins:
            if float(prot.score) <= filter_value:
                filtered_prots.append(prot)
    elif opt == ">":
        for prot in proteins:
            #print(float(prot.score), filter_value, float(prot.score) > filter_value)
            if float(prot.score) > filter_value:
                filtered_prots.append(prot)
    elif opt == ">=":
        for prot in proteins:
            #print(float(prot.score), filter_value, float(prot.score) >= filter_value)
            if float(prot.score) >= filter_value:
                filtered_prots.append(prot)
    else:
        for prot in proteins:
            if float(prot.score) == filter_value:
                filtered_prots.append(prot)
    return filtered_prots

def filter_intensity(proteins, filter_value, opt):
    filtered_prots = []
    filter_value = int(filter_value)
    if opt == "<":
        for prot in proteins:
            if int(prot.intensity) < filter_value:
                filtered_prots.append(prot)
    elif opt == "<=":
        for prot in proteins:
            if int(prot.intensity) <= filter_value:
                filtered_prots.append(prot)
    elif opt == ">":
        for prot in proteins:
            #print(prot.number_of_prots, filter_value, int(prot.number_of_prots) > filter_value)
            if int(prot.intensity) > filter_value:
                filtered_prots.append(prot)
    elif opt == ">=":
        for prot in proteins:
            #print(int(prot.intensity), filter_value, int(prot.intensity) >= filter_value)
            if int(prot.intensity) >= filter_value:
                filtered_prots.append(prot)
    else:
        for prot in proteins:
            if int(prot.intensity) == filter_value:
                filtered_prots.append(prot)
    return filtered_prots

def filter_iBAQ(proteins,  filter_value, opt):
    filtered_prots = []
    filter_value = float(filter_value)
    if opt == "<":
        for prot in proteins:
            if float(prot.iBAQ) < filter_value:
                filtered_prots.append(prot)
    elif opt == "<=":
        for prot in proteins:
            if float(prot.iBAQ) <= filter_value:
                filtered_prots.append(prot)
    elif opt == ">":
        for prot in proteins:
            #print(float(prot.score), filter_value, float(prot.score) > filter_value)
            if float(prot.iBAQ) > filter_value:
                filtered_prots.append(prot)
    elif opt == ">=":
        for prot in proteins:
            #print(float(prot.score), filter_value, float(prot.score) >= filter_value)
            if float(prot.iBAQ) >= filter_value:
                filtered_prots.append(prot)
    else:
        for prot in proteins:
            if float(prot.iBAQ) == filter_value:
                filtered_prots.append(prot)
    return filtered_prots

def prot_to_file(proteins, filename):
    string = "Protein IDs\tProtein names\tGene names\tFasta headers\tNumber of proteins\tPeptides\tQ-value\tScore\tIntensity\tiBAQ\tiBAQ LYOP2\tiBAQ LYOP3\tiBAQ TNEG2\tiBAQ TNEG3\n"
    for prot in proteins:
        string += prot.proteinIDs + "\t"
        string += prot.protein_names + "\t"
        string += prot.gene_names + "\t"
        string += prot.fasta_headers + "\t"
        string += prot.number_of_prots + "\t"
        string += prot.peptides + "\t"
        string += prot.q_value + "\t"
        string += prot.score + "\t"
        string += prot.intensity + "\t"
        string += prot.iBAQ + "\t"
        string += prot.s2iBAQ + "\t"
        string += prot.s3iBAQ + "\t"
        string += prot.c2iBAQ + "\t"
        string += prot.c3iBAQ + "\n"
        #print(prot.c3iBAQ)
    string = string[:-1]
    #print(string)
    file = open(filename, "w")
    file.write(string)
    return filename

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("--protein_IDs", help="Protein IDs to filter, separated by ';'")
    parser.add_argument("--protein_IDs_file", help="File contains protein IDs to filter, tab format")
    parser.add_argument("--protein_names", help="Protein names to filter, separated by ';'")
    parser.add_argument("--protein_names_file", help="File contains protein names to filter, separated by ';'")
    parser.add_argument("--gene_names", help="Gene names to filter, separated by ';'")
    parser.add_argument("--gene_names_file", help="Gene names to filter, separated by ';'")
    parser.add_argument("--fasta_headers", help="Fasta headers to filter, separated by ';'")
    parser.add_argument("--fasta_headers_file", help="Fasta headers to filter, separated by ';'")
    parser.add_argument("--peptides", nargs=2, metavar=("VALUE", "EQUATION"), help="Peptides to filter, separated by ';'")
    parser.add_argument("--iBAQ", nargs=2, metavar=("VALUE", "EQUATION"))
    parser.add_argument("--number_of_proteins", nargs=2, metavar=("VALUE", "EQUATION"))
    parser.add_argument("--intensity", nargs=2, metavar=("VALUE", "EQUATION"))
    parser.add_argument("--q_value", nargs=2, metavar=("value", "equation"))
    parser.add_argument("--score", nargs=2, metavar=("VALUE", "EQUATION"))
    parser.add_argument("--identification_type")
    parser.add_argument("-o", "--output", default="output.txt")

    args = parser.parse_args()

    # Read input file
    proteins = MQparse(args.input)
    results = filter_tech(proteins)
    if args.protein_IDs:
        results = filter_protIDs(results, args.protein_IDs)
    if args.protein_IDs_file:
        filters = readOption(args.protein_IDs_file)
        results = filter_protIDs(results, filters)
    if args.protein_names:
        results = filter_prot_names(results, args.protein_names)
    if args.protein_names_file:
        filters = readOption(args.protein_names_file)
        results = filter_prot_names(results, filters)
    if args.gene_names:
        results = filter_gene_names(results, args.gene_names)
    if args.gene_names_file:
        filters = readOption(args.gene_names_file)
        results = filter_gene_names(results, filters)
    if args.fasta_headers:
        results = filter_fasta(results, args.fasta_headers)
    if args.fasta_headers_file:
        filters = readOption(args.fasta_headers_file)
        results = filter_fasta(results, filters)
    if args.peptides:
        #print(args.peptides)
        results = filter_pep(results, args.peptides[0], args.peptides[1])
    if args.number_of_proteins:
        results = filter_noProt(results, args.number_of_proteins[0], args.number_of_proteins[1])
    if args.q_value:
        results = filter_qVal(results, args.q_value[0], args.q_value[1])
    if args.score:
        results = filter_score(results, args.score[0], args.score[1])
    if args.intensity:
        results = filter_intensity(results, args.intensity[0], args.intensity[1])
    if args.iBAQ:
        results = filter_iBAQ(results, args.iBAQ[0], args.iBAQ[1])
    """print(results[0].string())
    print(len(results))
    return results"""
    if args.output:
        prot_to_file(results, args.output)

if __name__ == "__main__":
    options()#[0].string()
    #test protein ids file
    #python3 filter.py -i proteinGroups_Maud.txt -o test-data/output.txt --protein_IDs_file prot_id.txt
    #test protein names file
    #python3 filter.py -i proteinGroups_Maud.txt -o test-data/output_pnames.txt --protein_names_file prot_names.txt
    #test gene names file
    #python3 filter.py -i proteinGroups_Maud.txt -o test-data/output_gnames.txt --gene_names_file gene_names.txt
    #test fasta header file
    #python3 filter.py -i proteinGroups_Maud.txt -o test-data/output_hfasta.txt --fasta_headers_file hfasta.txt
    #planemo tool_init --id "uc1" --name "PREF1" --description "Filter MaxQuant output file by keyworks or values" --example_command "python3 filter.py -i proteinGroups_Maud.txt -o meo.txt --iBAQ 34655 '>='" --example_input proteinGroups_Maud.txt --example_output meo.txt
