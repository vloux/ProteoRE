import argparse

def readHPA(HPAfile):
    # Read HPA file
    hpa = open(HPAfile, "r")
    hpa = hpa.readlines()
    #print(hpa[0])
    salivary_genes = [] 
    salivary_detail = []
    lung_genes = []
    lung_detail = []
    for l in hpa:
        name = l.replace('"', "").split(",")[1]
        #print(name)
        tissue = l.replace('"', "").split(",")[2]
        #print(tissue)
        if tissue == "salivary gland":
	    salivary_detail.append(l)
            if name not in salivary_genes: # Avoid duplicated gene names
                salivary_genes.append(name)
        elif tissue == "lung":
	    lung_detail.append(l)
            if name not in lung_genes: # Avoid duplicated gene names
                lung_genes.append(name)
    #print(salivary_genes)
    #print("break")
    #print(lung_genes)
    return salivary_genes, lung_genes, salivary_detail, lung_detail

def filterHPA(MQfile, HPAfile, output, trash_file, trash_file_detail, salivary_file, lung_file):
    mq = open(MQfile, "r")
    mq = mq.readlines()
    #print(mq[0])

    salivary_genes, lung_genes, salivary_detail, lung_detail = readHPA(HPAfile)

    # Extract gene names column number
    column_names = mq[0].split("\t")
    #print(column_names[2])
    gene_names_index = ""
    for i in range(len(column_names)):
        if column_names[i] == "Gene names":
            gene_names_index = i
            #print("gene name index:", i)
    if gene_names_index == "":
        raise ValueError("Could not find Gene names")

    string = mq[0].replace("\n", "")
    string = string.replace("^M", "") + "\t" + "Filtered" + "\n"
    filtered_genes = []
    for line in mq[1:]:
        prot_string = line.replace("\n", "")
        line = line.split("\t")
        #print(line[gene_names_index], "-", line[gene_names_index].split(";"))
        name = line[gene_names_index].split(";")[0]
        #print(name)
        if name not in salivary_genes:
            prot_string += "\t" + "Non-salivary"
            string += prot_string + "\n"
        else:
            if name in lung_genes:
                prot_string += "\t" + "Salivary + lung"
                string += prot_string + "\n"
            else:
                filtered_genes.append(name)

    sali_file = open(salivary_file, "w")
    sali_file.write("\n".join(salivary_genes))
    lung_file = open(lung_file, "w")
    lung_file.write("\n".join(lung_genes))

    output = open(output, "w")
    output.write(string)

    output_filtered_genes = open(trash_file, "w")
    for gene in filtered_genes:
	for s in salivary_detail:
	    name = s.replace('"', "").split(",")[1]
	    if name == gene:
        	output_filtered_genes.write(s + "\n")
	for l in lung_detail:
	    name = s.replace('"', "").split(",")[1]
	    if name == gene:
		output_filtered_genes.write(l + "\n")

    #print(filtered_genes)

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mq", required=True, help="MaxQuant file")
    parser.add_argument("--hpa", required=True, help="HPA file")
    parser.add_argument("-o", "--output", default="HPA_selection.txt")
    parser.add_argument("--trash_file", default="Trash.txt", help="Write filtered genes into a file")
    #parser.add_argument("--salivary_file", default="Salivary.txt", help="Write salivary gene names into a file")
    #parser.add_argument("--lung_file", default="Lung.txt", help="Write lung gene names into a file")
    parser.add_argument("--trash_file_detail", default="Trash_detail.txt", help="Write filtered genes with detailed information into a file")

    args = parser.parse_args()

    # Extract salivary genes list and lung genes list
    salivary_genes, lung_genes, salivary_detail, lung_detail = readHPA(args.hpa)
    #s = open("sali.txt", "w")
    #s.write("\n".join(salivary_genes))
    #l = open("lung.txt", "w")
    #l.write("\n".join(lung_genes))
    filterHPA(args.mq, args.hpa, args.output, args.trash_file, args.trash_file_detail, args.salivary_file, args.lung_file)
"""
    # Test gene names in sample files
    test = ["P12273", "Q8TAX7", "Q96DA0", "P01036", "Q9HC84", "Q9NZT1", "P01037", "P09228"]
    test_gene = []
    mq = open(args.mq, "r")
    mq = mq.readlines()
    for line in mq[1:]:
        line = line.split("\t")
        prot_id = line[0]
        gene = line[2]
        if prot_id in test:
            test_gene.append(gene)
    test_sali = [t for t in test_gene if t in salivary_genes]
    test_lung = [t for t in test_gene if t in lung_genes]
    print("List of test genes in salivary gland: ", test_sali)
    print("List of test genes in lung: ", test_lung)
"""
    
if __name__ == "__main__":
 #   MQfile = "/Users/LinCun/Documents/ProteoRE/usecase1/Check/PostSelection.143.txt"
#    hpaFile = "/Users/LinCun/Documents/ProteoRE/usecase1/normal_tissue.csv"
    options()
 #   filterHPA(MQfile, hpaFile)
    #--mq Check/PostSelection.143.txt --hpa normal_tissue.csv
    

    
