library(KEGGREST)

#issue with pathways with more than 400 genes (ex : path:hsa01100)
#function to convert ids with keggConv, max length of vector is 400 
id_conv <- function(ids_vector,id_type) {
  if (length(ids_vector) > 300){
    ids_vector <- as.vector(ids_vector)
    tmp_list <- split(ids_vector, ceiling(seq_along(ids_vector)/300))
    res <- unlist(lapply(tmp_list, function(genes) unique(as.character(keggConv(id_type,unlist(genes))))),use.names = FALSE)
  } else {
    res <- unique(as.character(keggConv(id_type,ids_vector)))
  }
  res <- sapply(res, function(x) strsplit(x,split=":")[[1]][2],USE.NAMES = FALSE) #remove prefix
  return(res)
}

species = "hsa"

##all available pathways for the human 
path.hsa<-keggLink("pathway", species)
tot.path.hsa<-unique(path.hsa)

##formating the dat into a list object
##key= pathway ID, value = genes of the pathway in the kegg format

l.hsa <- sapply(tot.path.hsa, function(pathway) names(which(path.hsa==pathway)))

##converting the value format to UNIPROT ('up') 
## or gene ('gene') id

l.hsa.up <- lapply(l.hsa, function(genes) id_conv(genes,"uniprot"))
l.hsa.gene <- lapply(l.hsa, function(genes) id_conv(genes,"ncbi-geneid"))

##write the data to save the data

save(l.hsa.up, file="l.hsa.up.RData")
save(l.hsa.gene, file="l.hsa.gene.RData")