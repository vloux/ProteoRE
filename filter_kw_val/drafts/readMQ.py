from protein import Protein

keep_col = ["Protein IDs", "Protein names", "Gene names", "Fasta headers"]

"""
Parse a MQoutput file to get information of proteins
"""
def MQparse(filename):
    # Read input file
    input = open(filename, "r")
    MQfile = input.readlines()
    print(MQfile)

    # Extract column titles
    col_titles = MQfile[0].replace("\n","").split("\t")
    print(col_titles)

    # Extract information
    prot_list = []
    for protein in MQfile[1:]:
        prot = protein.replace("\n","").split("\t")
        print(prot)
        prot_IDs = ""
        prot_names = ""
        gene_names = ""
        fasta_hd = ""
        pep = ""
        iBAQ = ""
        s2iBAQ = ""
        s3iBAQ = ""
        c2iBAQ = ""
        c3iBAQ = ""
        no_prot = ""
        inten = ""
        q_value = ""
        score = ""
        iden_type = ""
        for i in range(len(col_titles)):
            if col_titles[i] == "Protein IDs":
                print(i)
                prot_IDs = prot[i]
            elif col_titles[i] == "Protein names":
                print(i, "abc")
                print(prot[i] + "def")
                prot_names = prot[i]
            elif col_titles[i] == "Gene names":
                print(i)
                gene_names = prot[i]
            elif col_titles[i] == "Fasta headers":
                fasta_hd = prot[i]
            elif col_titles[i] == "Peptides":
                pep = prot[i]
            elif col_titles[i] == "iBAQ":
                iBAQ = prot[i]
            elif col_titles[i] == "iBAQ LYOP2":
                s2iBAQ = prot[i]
            elif col_titles[i] == "iBAQ LYOP3":
                s3iBAQ = prot[i]
            elif col_titles[i] == "iBAQ TNEG2":
                c2iBAQ = prot[i]
            elif col_titles[i] == "iBAQ TNEG3":
                c3iBAQ = prot[i]
            elif col_titles[i] == "Number of proteins":
                no_prot = prot[i]
            elif col_titles[i] == "Intensity":
                inten = prot[i]
            elif col_titles[i] == "Q-value":
                q_value = prot[i]
            elif col_titles[i] == "Score":
                print(i)
                score = prot[i]
            # Identification type: TO-DO
            elif col_titles[i] == "Identification type":
                iden_type = prot[i]
                
        protein = Protein(prot_IDs, prot_names, gene_names, fasta_hd, pep,
                          iBAQ, s2iBAQ, s3iBAQ, c2iBAQ, c3iBAQ, no_prot,
                          inten, q_value, score, iden_type)
        prot_list.append(protein)
    return prot_list

if __name__ == "__main__":
    filename = "/Users/LinCun/Documents/ProteoRE/usecase1/test-data/output.txt"
    filename2 = "/Users/LinCun/Documents/ProteoRE/usecase1/proteinGroups_Maud.txt"
    prot = MQparse(filename)
    """for p in prot:
        if p.s2iBAQ == "":
            print("1: " + p.s2iBAQ)
            print("2: " + p.s3iBAQ)
            print("3: " + p.c2iBAQ)
            print("4: " + p.c3iBAQ)
        if p.s3iBAQ == "":
            print("1: " + p.s2iBAQ)
            print("2: " + p.s3iBAQ)
            print("3: " + p.c2iBAQ)
            print("4: " + p.c3iBAQ)
        if p.c2iBAQ == "":
            print("1: " + p.s2iBAQ)
            print("2: " + p.s3iBAQ)
            print("3: " + p.c2iBAQ)
            print("4: " + p.c3iBAQ)
        if p.c3iBAQ == "":
            print("1: " + p.s2iBAQ)
            print("2: " + p.s3iBAQ)
            print("3: " + p.c2iBAQ)
            print("4: " + p.c3iBAQ)

        print("s")
        print(p.s2iBAQ)
        print(p.s3iBAQ)
        print(p.c2iBAQ)
        print(p.c3iBAQ)
        print()"""
    print(prot[2].string())
    
