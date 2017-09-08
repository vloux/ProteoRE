# Goal : merge parisWprob.txt and nodeTable.txt from hu.MAP so
# to map the gene id in the interactions to their corresponding uniprot ids 

# open huMAP nodes and network files
network = read.table("pairsWprob.txt",header=F,sep="\t")
nodes = read.table("nodeTable.txt",header=T,sep=",",na.strings=c("","NA"," "))

# Due to different node clusters Uniprot IDs are duplicated, so only unique
# nodes are selected 
unique_nodes = nodes[!(duplicated(nodes[,5])),]

# data is merged on the first column of the network file and on the key column
# of the nodes file
data = merge(network,unique_nodes,by.x=1,by.y=5,all.x=T)

# rename acc Uniprot Ids into Uniprot1 (Uniprot IDs for genes in column 1) 
nb = grep("acc",colnames(data))
colnames(data)[nb] = "Uniprot1"


# data is merged on the second column of the network file and on the key column
# of the nodes file
data = merge(data,unique_nodes,by.x=2,by.y=5,all.x=T)

# rename acc Uniprot Ids into Uniprot2 (Uniprot IDs for genes in column 2) 
nb = grep("acc",colnames(data))
colnames(data)[nb] = "Uniprot2"

# keep only the neccessary columns (gene1, gene2, humap score, uniprot id 1,
# uniprot id 2)
final_data = data[,c("V1","V2","V3","Uniprot1","Uniprot2")]

print(length(final_data$V1))
# Sometimes gene id were given without corresponding Uniprot IDs resulting in
# NAs in columns Uniprot1 and Uniprot2. These columns have to be deleted
lines = which(is.na(final_data$Uniprot1))
final_data = final_data[-lines,]

lines = which(is.na(final_data$Uniprot2))

final_data = final_data[-lines,]
# write results
write.table(final_data,"huMAP_genes_Uniprot_mapping_no_ENSG.txt",row.names=F,col.names=F,quote=F,sep="\t")
