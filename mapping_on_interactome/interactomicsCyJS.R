#Usage : Rscript --vanilla interactomicsCyJS.R --inputtype tabfile (or
# copypaste) --input
# file.txt (can be a tabfile or Uniprot ids separated by a blank space if
# inputtype is copypaste) --column c1 --interactome
# BioPlex_interactionList_v4a.tsv --jsonoutput output.json --taboutput TRUE
# --addReactome TRUE --reactomeFile UniProt2Reactome.txt

#
# Arguments : 
# --inputtype : tabfile or copypaste : if the input you give is a tabular file
# containing Uniprot ids or a list of Uniprot ids separated by a blank space
# --input : a tabular file (e.g : file.txt) or a list of ids (e.g : P00053
# P12346)
# --column : column in which your uniprot ids are contained in the input tab
# file (e.g : c2). If the input is a list of uniprot Ids put c1 for this
# argument. 
# --interactome : a tabular file of an interactome
# --jsonoutput : filename for the json output
# --taboutput : TRUE or FALSE : if an additionnal tabular file of the ppis is
# needed 
# --addReactome : TRUE or FALSE : if the user want additional information from
# reactome (pathways) in the output
# --reactomeFile : file path to the reatome mapping file between uniprot ids
# and pathways
#
# Goal : from a list of proteins ids, extract their ppis and create
# a json graph file readable by cytoscapejs



# library 
library("rjson")

'%!in%' <- function(x,y)!('%in%'(x,y))

# Parse command line arguments

args = commandArgs(trailingOnly = TRUE)

# create a list of the arguments from the command line, separated by a blank space
hh <- paste(unlist(args),collapse=' ')

# delete the first element of the list which is always a blank space
listoptions <- unlist(strsplit(hh,'--'))[-1]

# for each input, split the arguments with blank space as separator, unlist,
# and delete the first element which is the input name (e.g --inputtype) 
options.args <- sapply(listoptions,function(x){
         unlist(strsplit(x, ' '))[-1]
        })
# same as the step above, except that only the names are kept
options.names <- sapply(listoptions,function(x){
  option <-  unlist(strsplit(x, ' '))[1]
})
names(options.args) <- unlist(options.names)



typeinput = options.args[1]
listfile = options.args[2]
column = as.numeric(gsub("c","",options.args[3]))
interactomefile = as.character(options.args[4])
filename = as.character(options.args[5])
tabfile = as.character(options.args[6])
interactometype = as.character(options.args[7])

addreactome = as.character(options.args[8])
reactomefile = as.character(options.args[9])
reactome = read.table(reactomefile,sep="\t",header = F,comment.char = "",quote="\"") 

if (typeinput=="copypaste"){
  prot_list = as.data.frame(unlist(listfile))
  prot_list = prot_list[,column]
}
if (typeinput=="tabfile"){

  prot_list = read.table(listfile,header=FALSE,sep="\t")  
  prot_list = prot_list[,column]

}

if (interactometype=="bioplex"){
  ppi_all = read.table(interactomefile,header = T,sep = "\t")
}


# get the proteins ppis and their characteristics according to the chosen
# interactome 

getProtPPIs = function(prot_list,ppi_all,interactometype){
	# ppis : list to store the ppis and the intAct miscore
	ppis = c()
	for (prot in prot_list){
    if (interactometype=="bioplex"){
			if (prot %in% ppi_all[,3]){
	
				lines = grep(prot,ppi_all[,3])
	
	      # some proteins in the Bioplex Interactome can be "UNKNOWN". So that they can be distinguished they are
	      # for now concatenated with the NCBI gene id. This step is specific to
        # Bioplex.
				p1s = paste(as.character(ppi_all[lines,3]),ppi_all[lines,1],sep=';')
				p2s = paste(as.character(ppi_all[lines,4]),ppi_all[lines,2],sep=';')
				scores = ppi_all[lines,9]
	      info = 	cbind(p1s,p2s,scores)
				ppis = rbind(ppis,info)	
	
			}
			if (prot %in% ppi_all[,4]){ 
				lines = grep(prot,ppi_all[,4])
				p1s = paste(as.character(ppi_all[lines,3]),ppi_all[lines,1],sep=';')
				p2s = paste(as.character(ppi_all[lines,4]),ppi_all[lines,2],sep=';')
				scores = ppi_all[lines,9]
	      info = 	cbind(p1s,p2s,scores)
	      ppis = rbind(ppis,info)	
			}
		}
  }

	return(ppis)
}

# For now protein and gene names are concatenated to avoid confusion between the
# multiple "UNKNOWN" proteins (indeed some proteins are "UNKNOWN" but come from
# different genes. To account for this difference, protein and genes names were
# concatenated.) The clearPPIs function split the protein and gene names and
# create a fourth and fifth column (respectively for protein 1 and protein 2) with the gene names. 
 
clearPPIs = function(ppi_list){
 
  ppis_list_final = c()

  for (i in 1:length(ppi_list[,1])){
    
    nprot1 = strsplit(ppi_list[i,1],";")[[1]][1]
    ngene1 = strsplit(ppi_list[i,1],";")[[1]][2]

    nprot2 = strsplit(ppi_list[i,2],";")[[1]][1]
    ngene2 = strsplit(ppi_list[i,2],";")[[1]][2]


    if (nprot1 == "UNKNOWN"){
      nprot1 = paste(nprot1,ngene1,sep="(")
      nprot1 = paste(nprot1,")")
    }

    if (nprot2 == "UNKNOWN"){
      nprot2 = paste(nprot2,ngene2,sep="(")
      nprot2 = paste(nprot2,")")
    }
    score = ppi_list[i,3] 
    info = 	cbind(nprot1,nprot2,score,ngene1,ngene2)
		ppis_list_final = rbind(ppis_list_final,info)	
  }
  return(ppis_list_final)
}
# Construct the data structure to then write JSON file

constructNodesList = function(data,protlist,interactometype,addreactome,reactome){

  all_nodes = as.vector(data[,1])
  all_nodes = unique(c(all_nodes,as.vector(data[,2]))) 

  # this vector will store for each node a list containing its attribute
  # the expected structure is as follow : 
  #TO COMPLETE
  vector_all_nodes = c()
  for (n in all_nodes){
  
    if (n %in% protlist){

      colour = "#d43710"
    }
    else{
      colour = "#b3c6c8"
    }
   
    if (interactometype=="bioplex"){
	    if (n %in% data[,1]){
	      line = grep(n,data[,1])
        # if the protein is present in more than one interaction the grep will
        # return all the lines where the protein is present and we will get
        # the same gene name multiple times, so we keep only the first one
        if (length(line)>1){
	        ngene = data[line,4][1]
        }else{
	        ngene = data[line,4]
        }
      }
	    if (n %in% data[,2]){
	      line = grep(n,data[,2])
        if (length(line)>1){
	        ngene = data[line,5][1]
        }else{
	        ngene = data[line,5]
        }
	    }
	    # for some reason, grep does not work with unknown so we extract the gene
	    # name directly from UNKNOWN (gene name)
	    if (length(grep("UNKNOWN",n))!=0){
	      ngene = gsub('.*\\(','',n)
	      ngene = gsub("\\)","",ngene) 
	  
	    }
      # if additional data from reactome has to be added
      if (addreactome=="TRUE"){

        pathway=c("None")
        if ((n %in% reactome[,1])==TRUE){
          lines = grep(n,reactome[,1])
          if (length(lines)>1){
            pathway=c()
            for (l in lines){
              pathway = c(pathway,as.character(reactome[l,4]))
            }

          }
        } 
	      # For now, identifiers and labels will be the same for each protein node
	      node_l3 = list(id = n, label = n, colour = colour, gene=ngene,pathway=pathway)
      }else{

	      node_l3 = list(id = n, label = n, colour = colour, gene=ngene)

      }
    }
    node_l2 = list(data = node_l3)
    node_l1 = list(node_l2)
    vector_all_nodes = c(vector_all_nodes,node_l1)
  } 

  # if some of the user not are not contained in the interactome, they are
  # still added to the output
  if (length(protlist %!in% all_nodes)!=0){
    nodes_not_in_interactome = protlist[protlist %!in% all_nodes] 

    for (n in nodes_not_in_interactome){
	   
      # if additional data from reactome has to be added
      if (addreactome=="TRUE"){

        pathway=c("None")
        if ((n %in% reactome[,1])==TRUE){
          lines = grep(n,reactome[,1])
          if (length(lines)>1){
            pathway=c()
            for (l in lines){
              pathway = c(pathway,as.character(reactome[l,4]))
            }

          }
        } 

      
        node_l3 = list(id = n, label = n, colour = "#d43710", gene="UNKNOWN",pathway = pathway)
      }else{
        node_l3 = list(id = n, label = n, colour = "#d43710", gene="UNKNOWN")
      }
      node_l2 = list(data = node_l3)
      node_l1 = list(node_l2)
      vector_all_nodes = c(vector_all_nodes,node_l1)
    }
  
  } 
  
  return(vector_all_nodes)
}

constructEdgesList = function(data,interactometype){

  vector_all_edges = c()

  for (i in 1:length(data[,1])){


    id_edge = paste(data[i,1],data[i,2],sep="_")
    source_edge = data[i,1]
    target = data[i,2]
    w = data[i,3]

    if (interactometype=="bioplex"){
      edge_l3 = list(id = id_edge, source = source_edge, target = target, weight = w)
    }

    edge_l2 = list(data = edge_l3)
    edge_l1 = list(edge_l2)   
    
    vector_all_edges = c(vector_all_edges,edge_l1)
  }
  return(vector_all_edges)
}


constructJSON = function(data,protlist, interactometype,addReactome,reactome){

  nodes_list = constructNodesList(data,protlist,interactometype,addReactome,reactome)
  edges_list = constructEdgesList(data,interactometype)
 
  elts = list(nodes = nodes_list, edges = edges_list) 
  network = list(elements = elts)
  return(network)
} 

# add unmapped proteins to the tab output 
addUnMappedProteins = function(ppi_list,protlist){

  all_nodes = as.vector(ppi_list[,1])
  all_nodes = unique(c(all_nodes,as.vector(ppi_list[,2]))) 


  if (length(protlist %!in% all_nodes)!=0){
    nodes_not_in_interactome = protlist[protlist %!in% all_nodes] 
    lines = c()
    for (n in nodes_not_in_interactome){
      line = c(n,rep("No interactants found",length(colnames(ppi_list))-1))
      lines = rbind(lines,line)
    }
    colnames(lines) = colnames(ppi_list)
    ppi_list = rbind(ppi_list,lines) 
  } 
  
  return(ppi_list)
}


# Graph construction

# Get all your data PPIs
ppi_list = getProtPPIs(prot_list,ppi_all,interactometype)
# If Bioplex was chosen as interactome, protein ids and gene names were
# concatenated due to the presence of UNKNOWN proteins (to be able to
# distinguish them). It is now necessary to separate protein and gene ids.  
if (interactometype=="bioplex"){
  ppi_list = clearPPIs(ppi_list)
}
row.names(ppi_list)=NULL
ppi_list = as.data.frame(ppi_list)
# Create a structure that can be used to write a JSON file 
network = constructJSON(ppi_list,prot_list,interactometype,addreactome,reactome)
# Write to a JSON file 
json = toJSON(network)
write(json,filename)

if (tabfile=="TRUE"){
  ppi_list = addUnMappedProteins(ppi_list,prot_list)
  if (interactometype=="bioplex"){
    colnames(ppi_list)=c("Protein1","Protein2","score","Gene1","Gene2")
  }
  write.table(ppi_list,file="result.txt",quote=FALSE, sep='\t', col.names = T, row.names = F)
}

