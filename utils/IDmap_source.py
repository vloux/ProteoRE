# -*- coding: utf-8 -*-

def human_id_mapping(human_id_mapping_filename, nextprot_filename):
    """
    - Read HUMAN_9606_idmapping_selected.txt file and extract list of IDs:
        1. UniProtKB-AC: Uniprot accession number; only one ID => P31946
        2. UniProtKB-ID: Uniprot protein identifier; only one ID => 1433B_HUMAN
        3. GeneID (EntrezGene): gene ID from Entrez; only one ID or no mapping (empty) => 7529
        4. RefSeq: protein ID from Refseq (NCBI); list of IDs separated by a “;” => NP_003395.1; NP_647539.1; XP_016883528.1
        5. GI: sequence ID from NCBI; list of IDs separated by a “;” => 4507949; 377656702; 67464628; 1345590; 1034625756; 21328448; 377656701; 67464627; 78101741
        6. PDB: ID from Protein Data Bank (structures); list of IDs separated by a “;” => 2BQ0:A; 2BQ0:B; 2C23:A; 4DNK:A; 4DNK:B; 5N10:A; 5N10:B
        7. GO: Gene Ontology ID; list of IDs separated by a “;” => GO:0003714; GO:0051220; GO:0035329; GO:0000165; GO:0061024; GO:0045744; GO:0035308; GO:0045892; GO:0043085; GO:1900740; GO:0051291; GO:0006605; GO:0043488; GO:0016032
        8. PIR: ID from Protein Information Resource (NCBI); list of IDs separated by a “;” => A61235; I38947
        9. MIM: ID from OMIM database; list of IDs separated by a “;” => 142800; 608579
        10. UniGene: trancripts ID from Unigene NCBI); list of IDs separated by a “;” => Hs.175437; Hs.708933; Hs.712722
        11. Ensembl: gene ID from Ensembl; list of IDs separated by a “;” => ENSG00000108953; ENSG00000274474
        12. Ensembl_TRS: transcript ID from Ensembl; list of IDs separated by a “;” => ENST00000353703; ENST00000372839
        13. Ensembl_PRO: protein ID from Ensembl; list of IDs separated by a “;” => ENSP00000300161; ENSP00000361930
    - Read nextprot_ac_list_all.txt file and compare neXtProt ID to UniProt ID
    """
    # Read source files
    f1 = open(human_id_mapping_filename, "r")
    human_id_mapping_file = f1.readlines()

    f2 = open(nextprot_filename, "r")
    nextprot_file = f2.readlines()
    nextprot_file = [line.replace("\n", "") for line in nextprot_file] 

    # Index
    uniprot_ac_index = 0
    uniprot_id_index = 1
    gene_id_index = 2
    refseq_index = 3
    gi_index = 4
    pdb_index = 5
    go_index = 6
    pir_index = 11
    mim_index = 13
    unigene_index = 14
    ensembl_index = 18
    ensembl_trs_index = 19
    ensembl_pro_index = 20

    string = "UniProtKB-AC\tUniProtKB-ID\tGeneID\tRefSeq\tGI\tPDB\tGO\tPIR\tMIM\tUniGene\tEnsembl\tEnsembl_TRS\tEnsembl_PRO\n"
    uniprot_ac = []
    for line in human_id_mapping_file:
        columns = line.split("\t")
        # Compare nextprot id to uniprot id
        expected_nextprot = "".join(["NX_", columns[uniprot_ac_index]])
        if expected_nextprot in nextprot_file:
            string += expected_nextprot + "\t"
        else:
            string += "NA" + "\t"

        # Join selected ids
	string += columns[uniprot_ac_index] + "\t"
	string += columns[uniprot_id_index] + "\t"
	string += columns[gene_id_index] + "\t"
	string += columns[refseq_index] + "\t"
	string += columns[gi_index] + "\t"
	string += columns[pdb_index] + "\t"
	string += columns[go_index] + "\t"
	string += columns[pir_index] + "\t"
	string += columns[mim_index] + "\t"
	string += columns[unigene_index] + "\t"
	string += columns[ensembl_index] + "\t"
	string += columns[ensembl_trs_index] + "\t"
	string += columns[ensembl_pro_index] + "\n"
	uniprot_ac.append(columns[uniprot_ac_index])

    f1.close()
    f2.close()
    return string

def write_output(content, filename):
    f = open(filename, "w")
    f.write(content)
    f.close()

def main():
    """
    Parse arguments:
        --human_id_mapping_file: pathway to the human ID mapping file
        --nextprot_file: pathway to the nextprot IDs file
        --output: output filename
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--human_id_mapping_file", help="pathway to the human ID mapping file", required=True)
    parser.add_argument("--nextprot_file", help="pathway to the nextprot IDs file", required=True)
    parser.add_argument("--output", help="output filename") 

    args = parser.parse_args()
    
    human_id_mapping_filename = args.human_id_mapping_file 
    nextprot_filename = args.nextprot_file 
    content = human_id_mapping(human_id_mapping_filename, nextprot_filename)
    write_output(content, args.output)

if __name__ == "__main__":
    main()
		
# python IDmap_source.py --human_id_mapping_file "/Users/LinCun/Documents/ProteoRE/mapping/HUMAN_9606_idmapping_selected.txt" --nextprot_file "/Users/LinCun/Documents/ProteoRE/mapping/nextprot_ac_list_all.txt" --output "mapping_file.txt"	

    
