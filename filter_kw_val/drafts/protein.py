class Protein:
    "I'm a pretty protein"

    """
    Define all necessary information to keep from input file - to be completed
    """
    def __init__(self, protIDs, prot_names, gene_names, fasta_headers,
                 peptides, iBAQ, s2iBAQ, s3iBAQ, c2iBAQ, c3iBAQ, no_prots,
                 intensity, q_value, score, iden_type):
        self.proteinIDs = protIDs
        self.protein_names = prot_names
        self.gene_names = gene_names
        self.fasta_headers = fasta_headers
        self.peptides = peptides
        self.iBAQ = iBAQ
        self.s2iBAQ = s2iBAQ
        self.s3iBAQ = s3iBAQ
        self.c2iBAQ = c2iBAQ
        self.c3iBAQ = c3iBAQ
        self.number_of_prots = no_prots
        self.intensity = intensity
        self.q_value = q_value
        self.score = score
        self.identification_type = iden_type

    """
    Setting how we will print out in the output file
    Protein IDs\tProtein names\tGene names...
    """
    def string(self):
        string = self.proteinIDs + "\t" + self.protein_names + "\t"
        string += self.gene_names + "\t" + self.fasta_headers + "\t"
        string += self.number_of_prots + "\t" + self.peptides + "\t"
        string += self.q_value + "\t" + self.score + "\t" + self.intensity 
        string += "\t" + self.iBAQ + "\t" + self.s2iBAQ + "\t" + self.s3iBAQ 
        string += "\t" + self.c2iBAQ + "\t" + self.c3iBAQ
        return(string)
