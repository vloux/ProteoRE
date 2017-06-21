# enrichment.R
# Command line arguments : Rscript --vanilla enrichment.R protlist.txt annotationmap.txt "BP/CC/MF" test(e.g :fisher) option (e.g : classic/elim...) correction threshold output1,output2,...
# e.g : Rscript --vanilla enrichment.R prot_reactome_EGFR.txt goa_human_restructured.txt BP fisher classic holm 1e-15 text,graph,wordcloud 
# INPUT : 
#	- protein list containing protein of interest
#	- annotation mapping file : file mapping between protein ids and GO term ids
#	- gene ontology category : Biological Process (BP), Cellular Component (CC), Molecular Function (MF)
#	- test option (relative to topGO algorithms) : elim, weight01, parentchild, or no option (classic)
#	- correction for multiple testing (see p.adjust options : holm, hochberg, hommel, bonferroni, BH, BY,fdr,none
#	- threshold for enriched GO term pvalues (e.g : 1e-15)     
#	- outputs wanted separeted by a comma (e.g : text,graph,wordcloud)
#
# OUTPUT :
# 	- text file prots_without_go_terms.txt listing proteins for which no GO terms where found in the mapping file
#	- output commanded by the user



'%!in%' <- function(x,y)!('%in%'(x,y))


# Parse command line arguments

args = commandArgs(trailingOnly = TRUE)

if (length(args) != 8) {
    stop("Not enough/Too many arguments", call. = FALSE)
  }


protlistfile = args[1]
annotfile = args[2]
onto = args[3]
test = args[4]
option = args[5]
correction = args[6]
threshold = as.numeric(args[7])
outputs = args[8]

prot_sample = read.table(protlistfile,header=FALSE)
prot_sample = prot_sample$V1


#topGO enrichment 

# loading topGO library
library("topGO") 

# reading mapping file prot id <-> GO term ids
protID2GO <- readMappings(file = annotfile)  

# Get the proteins not associated with any GO term ids
prots_without_goterm=c()


for (prot in prot_sample){
	if (prot %!in% names(protID2GO)){

		prots_without_goterm=c(prots_without_goterm,prot)
	}
}

write.table(prots_without_goterm,file='prots_without_go_terms.tsv',quote=FALSE,sep='\t',col.names=F,row.names=F)

# Get the names of all the human proteins from the GOA mapping file and use it as the background for enrichment analysis
protUniverse <- names(protID2GO)
prot_sample = as.character(prot_sample)  


# indicates the positions of our sample s proteins in the protein universe
protList <- as.integer(protUniverse %in% prot_sample)
protList <- factor(as.integer(protUniverse %in% prot_sample))

# the protList object tells TopGO which proteins in the protein universe are of interest
names(protList) <- protUniverse

# Now all the data need to be associated into an object of type topGOdata
# It will contain : the list of prot of interest, the GO annotations and the GO hierarchy
# Parameters : 
# ontology : character string specifying the ontology of interest (BP, CC, MF)
# allGenes : named vector of type numeric or factor (potential problem?)
# annot : tells topGO how to map genes to GO annotations. 'annot'=annFUN.gene2GO means that the user provides gene-to-GO annotations, and we specify here that they are in object 'protID2GO' 
# argument not used here : nodeSize : at which minimal number of GO annotations do we consider a protein 
 
myGOdata = new("topGOdata", description="SEA with TopGO", ontology=onto, allGenes=protList,  annot = annFUN.gene2GO, gene2GO = protID2GO)


# Performing enrichment tests
result <- runTest(myGOdata, algorithm=option, statistic=test)


# adjust for multiple testing
if (correction!="none"){

	adjusted_pvalues = p.adjust(attributes(result)$score, method = as.character(correction), n = length(attributes(result)$score))
	attributes(result)$score = adjusted_pvalues

}

# see how many results we get for pvalues scores under the user threshold
mysummary <- summary(attributes(result)$score <= threshold)
numsignif <- as.integer(mysummary[[3]]) # how many terms is it true that P <= threshold

# get all significant nodes 

allRes <- GenTable(myGOdata, test = result, orderBy = "result", ranksOf = "result",topNodes=numsignif)


# get outputs
# Parse the arguments if multiple arguments were given as input in one argument (e.g for text,graph )
parseInput = function(arg){
        arglist = strsplit(arg,",")
        arglist = arglist[[1]]
        arglist=as.character(arglist)
        return(arglist)
}


outputs = parseInput(outputs)

# Load GOsummaries
library("GOsummaries")

# Some libraries such as GOsummaries won't be able to treat the values such as "< 1e-30" produced by topGO. As such it is important to delete the < char. Nevertheless the data in allRes won't be modified, and the user will have access to the original results in the text output.  
deleteInfChar = function(allRes){

	lines = grep("<",allRes$test)
	if (length(lines)!=0){
		for (line in lines){
			allRes$test[line]=as.numeric(gsub("<","",allRes$test[line]))
		}
	}
	return(allRes$test)
}
 
# Produce the different outputs
for (output in outputs){

	if (output=="text"){
		write.table(allRes, file='result.tsv', quote=FALSE, sep='\t', col.names = NA)
	}

	if (output=="graph"){

		# obtain the induced graph of nodes with showSigOfNodes (gives the graph with the top 5 most significant GO terms (more than 5 is a visual horror)) 
		showSigOfNodes(myGOdata, score(result), firstSigNodes = 5, sigForAll=FALSE, useInfo ='all', useFullNames = TRUE)
		# get the pdf image
		printGraph(myGOdata, result, firstSigNodes = 5, useInfo = "all",fn.prefix = "enrichment", pdfSW = TRUE) 
	}

	if (output=="wordcloud"){
		sigPvalues = deleteInfChar(allRes)
		data = data.frame(Term=allRes$Term,Score=as.numeric(sigPvalues))
		gs = gosummaries(wc_data = list(Results = data))
		plot(gs, filename = "GOsummaries.png")
	}
}
