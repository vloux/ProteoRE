import argparse
import re

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mq", required=True, help="MaxQuant file")
    parser.add_argument("--hpa", required=True, help="HPA file")
    parser.add_argument("--tissues_del", required=True, help="List of tissues which expressed genes in are discarded")
    parser.add_argument("--tissues_keep", help="List of tissues to keep regardless being expressed in list tissues_del..")
    parser.add_argument("-o", "--output", default="HPA_selection.txt")
    parser.add_argument("--trash", default="Trash.txt", help="Write filtered genes into a file")
    parser.add_argument("--trash_file_detail", default="Trash_detail.txt", help="Write filtered genes with detailed information into a file")
    parser.add_argument("--na_file", default="NaN.txt", help="Write genes whose name not found in HPA file")
    parser.add_argument("--ncol", default="None", help="Number of column to filter")

    args = parser.parse_args()
    #print(args.mq, args.hpa, args.tissues_del, args.tissues_keep, args.output, args.trash, args.trash_file_detail)

    filterHPA(args.mq, args.hpa, args.tissues_del, args.tissues_keep, args.output, args.trash, args.trash_file_detail, args.na_file, args.ncol)
    
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
    
def readHPA(HPAfile, tissues_del, tissues_keep):
    # Read HPA file:
    hpa = open(HPAfile, "r")
    hpa = hpa.readlines()
    # Extract tissues genes lists
    tdel_dict = {}
    tissues_del = tissues_del.split(",")
    print("List of tissues to del", tissues_del)
    tkeep_dict = {}
    tissues_keep = tissues_keep.split(",")
    print("List of tissues to keep", tissues_keep)
    for line in hpa[1:]:
        name = line.replace('"', "").split(",")[1]
        tissue = line.replace('"', "").split(",")[2]
        for t in tissues_del:
            if tissue == t:
                if t not in tdel_dict:
                    tdel_dict[t] = [name]
                else:
                    if name not in tdel_dict[t]:
                        tdel_dict[t].append(name)
        for k in tissues_keep:
            if tissue == k:
                if k not in tkeep_dict:
                    tkeep_dict[k] = [name]
                else:
                    if name not in tkeep_dict[k]:
                        tkeep_dict[k].append(name)
    
    return tdel_dict, tkeep_dict

def filterHPA(MQfile, HPAfile, tissues_del, tissues_keep, output, trash_file, trash_file_detail, na_file, ncol):
    # Read MQ file:
    mq = open(MQfile, "r")
    mq = mq.readlines()
    #print(len(mq))
    # Remove empty lines
    [mq.remove(blank) for blank in mq if blank.isspace()]

    # Read HPA file
    hpa = open(HPAfile, "r")
    hpa = hpa.readlines()

    # Get dictionary of tissues : genes
    tdel_dict, tkeep_dict = readHPA(HPAfile, tissues_del, tissues_keep)
    #print("Dictionary of tissue:genes to del", tdel_dict)
    #print("Dictionary of tissue:genes to keep", tkeep_dict)

    # Extract gene names and protein ids column number
    column_names = mq[0].split("\t")
    #print(column_names)
    gene_names_index = ""
    prot_id_index = ""
    if ncol == "None":
        for i in range(len(column_names)):
            #print(column_names[i])
            if column_names[i] == "Gene names":
                gene_names_index = i
                #print("gene name index:", i)
            elif column_names[i] == "Majority protein IDs":
                prot_id_index = i
        if gene_names_index == "":
            raise ValueError("Could not find 'Gene names' column")
        if prot_id_index == "":
            raise ValueError("Could not find 'Majority protein IDs' column")
    else:
        print(ncol.replace("c", ""))
        if isnumber("int", ncol.replace("c", "")):
            gene_names_index = int(ncol.replace("c", "")) - 1
            print(gene_names_index, type(gene_names_index))
            for i in range(len(column_names)):
                #print(column_names[i])
                if column_names[i] == "Majority protein IDs":
                    prot_id_index = i
            if prot_id_index == "":
                raise ValueError("Could not find 'Majority protein IDs' column")
        else:
            raise ValueError("Please fill in the right format of column number")

    # Filter
    string = mq[0].rstrip()
    string = string.replace("^M", "") + "\t" + "Filtered" + "\n"
    filtered_genes = []
    filtered_prots = []
    na_genes = []
    #print(len(mq))
    for line in mq[1:]:
        prot_string = line.rstrip() + "\t" #.replace("^M", "")
        line = line.split("\t")
        name = line[gene_names_index].split(";")[0].replace('"', "")
        prot = line[prot_id_index].split(";")[0].replace('"', "")
        #print([name in genes for genes in t_dict.values()])
        #print(name)
        #print(t_dict.values())
        if name == "":
            prot_string += "NaN - No gene name" + "\n"
            string += prot_string
        else:
            tissue = sorted(set([t.split(",")[2].replace('"', "") for t in hpa if name in t]))
            #print(name,[all (name not in genes for genes in tdel_dict.values())])
            if all (name not in genes for genes in tdel_dict.values()):       
                if len(tissue) != 0:
                    print("Not in del list", name, len(tissue))
                    prot_string += ",".join(tissue) + "\n"
                    string += prot_string
                else:
                    print("No tissue information", name)
                    prot_string += "NaN - no tissue information" + "\n"
                    string += prot_string
                    na_genes.append(name)
            else:
                if all (name not in genes for genes in tkeep_dict.values()):
                    print("In del list only", name)
                    filtered_genes.append(name)
                    filtered_prots.append(prot)
                else:
                    print("In both del and keep", name, len(tissue))
                    prot_string += ",".join(tissue) + "\n"
                    string += prot_string

                """for gdels in tdel_dict.values():
                    if name in gdels:
                        for gkeeps in tkeep_dict.values():
                            if name in gkeeps:
                                tissue = sorted(set([t.split(",")[2].replace('"', "") for t in hpa if name in t]))
                                print("in del and keep", name, len(tissue))
                                prot_string += ",".join(tissue) + "\n"
                                string += prot_string
                            else:
                                filtered_genes.append(name)
                                filtered_prots.append(prot)
                    else:
                        tissue = sorted(set([t.split(",")[2].replace('"', "") for t in hpa if name in t]))
                        print("not in del 2", name, len(tissue))
                        prot_string += ",".join(tissue) + "\n"
                        string += prot_string"""

    # Generate output file
    output = open(output, "w")
    output.write(string)

    # Generate file of unknown gene name
    na_file = open(na_file, "w")
    na_file.write("\n".join(na_genes))
        
    # Generate trash files
    output_trash = open(trash_file, "w")
    output_trash.write("\n".join(filtered_prots))

    output_trash_detail = open(trash_file_detail, "w")
    print("Deleted genes", filtered_genes)
    for gene in filtered_genes:
        lines = [line for line in hpa if gene in line]
        output_trash_detail.write("".join(lines))

if __name__ == "__main__":
    options()

# python biofilter2.py --mq ../proteinGroups_Maud.txt --hpa /db/proteinatlas/normal_tissue.csv --tissues_del "retina" --tissues_keep "tonsil" --trash "Trash3.txt" --trash_file_detail "Trash_detail3.txt" -o test-data/output3.txt --na_file "Unknown.txt"
