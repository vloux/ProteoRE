# Command line arguments : Rscript --vanilla getData.R proteinatlas.csv genelist.txt filtertissue filterIF filterIH filename
# e.g : Rscript --vanilla get_data_HPA_v2.R --protatlas proteinatlas.csv --protlist prots_insoluble_fraction_mapped.txt --tissueCat tenriched tenhanced --IF approved --IH approved --output output.txt 
# INPUTS : 
#	- proteinatlas tab file
#	- protein list of interest
#	- tissue enriched (tenriched), tissue enhanced (tenhanced), group enriched(genriched), expressed in all (exprall), mixed (mixed), not detected (ndetected)
#	  or multiple combination with terms separated by a comma (e.g : tenriched,tenhanced) 
#	- reliability IF (approved,uncertain,supported,validated) or multiple combination with terms separated by a comma
#	- reliability IH (approved,uncertain,supported) or multiple combination with terms separated by a comma

args = commandArgs(trailingOnly = TRUE)

# create a list of the arguments from the command line, separated by a blank space
hh <- paste(unlist(args),collapse=' ')
# delete the first element of the list which is always a blank space
listoptions <- unlist(strsplit(hh,'--'))[-1]
# for each input, split the arguments with blank space as separator, unlist, and delete the first element which is the input name (e.g --protalas) 
options.args <- sapply(listoptions,function(x){
         unlist(strsplit(x, ' '))[-1]
        })
# same as the step above, except that only the names are kept
options.names <- sapply(listoptions,function(x){
  option <-  unlist(strsplit(x, ' '))[1]
})
names(options.args) <- unlist(options.names)


proteinatlas = read.table(as.character(options.args[1]),header=TRUE,sep="\t",fill=TRUE,blank.lines.skip=TRUE,quote="\"")
genes = read.table(as.character(options.args[2]),header=FALSE,sep="\t")
genes = genes$V1

tissues=options.args[3]
tissues = strsplit(tissues[[1]], ",")[[1]]
IF=options.args[4]
IF=strsplit(IF[[1]], ",")[[1]]
IH=options.args[5]
IH=strsplit(IH[[1]], ",")[[1]]

filename = options.args[6]
filename = filename[[1]][1]
'%!in%' <- function(x,y)!('%in%'(x,y))

# Delete unused columns in protein atlas and select only the genes of interest
cutData = function(proteinatlas,genes){
	
	# Delete unused columns
	proteinatlas = proteinatlas[,-which(colnames(proteinatlas) %!in% c("Gene","Ensembl","Antibody","Reliability..IH.","Reliability..IF.","Subcellular.location","RNA.tissue.category","RNA.TS","RNA.TS.TPM","TPM.max.in.non.specific"))]
	# Keep only genes of the user gene list
	proteinatlas = proteinatlas[which(proteinatlas$Ensembl %in% genes),]

	return(proteinatlas)
}




# Filter according to the tissue category (RNA.tissue.category)
filterTissue = function(proteinatlas, tissues){
	data = list()
	info=FALSE
	if (length(tissues)>0){
		info=TRUE
		for (t in tissues){
			print("tissue")
			print(t)
			if (t == "tenriched"){
				if ("Tissue enriched" %in% proteinatlas$RNA.tissue.category){
					lines = grep("Tissue enriched",proteinatlas$RNA.tissue.category)
					data=rbind(data,proteinatlas[lines,])
				}
			}		

			if (t == "tenhanced"){

				if ("Tissue enhanced" %in% proteinatlas$RNA.tissue.category){
					lines  = grep("Tissue enhanced",proteinatlas$RNA.tissue.category)
					data=rbind(data,proteinatlas[lines,])
				}
			}

			if (t == "genriched"){

				if ("Group enriched" %in% proteinatlas$RNA.tissue.category){
					lines = grep("Group enriched",proteinatlas$RNA.tissue.category)
					data=rbind(data,proteinatlas[lines,])
				}
			}

			if (t == "exprall"){

				if ("Expressed in all" %in% proteinatlas$RNA.tissue.category){
					lines = grep("Expressed in all",proteinatlas$RNA.tissue.category)
					data=rbind(data,proteinatlas[lines,])
				}
			}
			if (t == "mixed"){

				if ("Mixed" %in% proteinatlas$RNA.tissue.category){
					lines = grep("Mixed",proteinatlas$RNA.tissue.category)
					data=rbind(data,proteinatlas[lines,])
				} 

			}

			if (t == "ndetected"){

				if ("Not detected" %in% proteinatlas$RNA.tissue.category){
					lines = grep("Not detected",proteinatlas$RNA.tissue.category)
					data=rbind(data,proteinatlas[lines,])
				}
			}
			
		}
	}
	if (info == TRUE){
		return(data)
	}
	else{
		return(proteinatlas)
	}
} 

# filter the input file 
filterIH = function(data,IH){
		
	newdata = list()
	info=FALSE
	
	print("IH hereee")
	print(IH)
	
	if (length(IH)>0){
		info=TRUE
		for (term in IH){
		    print(term)
			if (term == "approved"){
				if ("Approved" %in% data$Reliability..IH.){
					lines = grep("Approved",data$Reliability..IH.)
					newdata = rbind(newdata,data[lines,])
				}
			}	

			if (term == "uncertain"){

				if ("Uncertain" %in% data$Reliability..IH.){
					lines = grep("Uncertain",data$Reliability..IH.)
					newdata = rbind(newdata,data[lines,])
				}
			}

			if (term == "supported"){

				if ("Supported" %in% data$Reliability..IH.){
					lines = grep("Supported",data$Reliability..IH.)
					newdata = rbind(newdata,data[lines,])
				}
			}	
		}
	}

	if (info == TRUE){
		return(newdata)
	}
	else{
		return(data)
	}
}

 
filterIF = function(data, IF){

	newdata = list()
	info=FALSE
	
	if (length(IF)>0){
		info=TRUE
		for (term in IF){
			if (term == "approved"){
				if ("Approved" %in% data$Reliability..IF.){
					lines = grep("Approved",data$Reliability..IF.)
					newdata = rbind(newdata,data[lines,])
				}
			}	

			if (term == "uncertain"){

				if ("Uncertain" %in% data$Reliability..IF.){
					lines = grep("Uncertain",data$Reliability..IF.)
					newdata = rbind(newdata,data[lines,])
					}
				}

				if (term == "supported"){

					if ("Supported" %in% data$Reliability..IF.){
						lines = grep("Supported",data$Reliability..IF.)
						newdata = rbind(newdata,data[lines,])
					}
				}	
				if (term == "validated"){

					if ("Validated" %in% data$Reliability..IF.){
						lines = grep("Validated",data$Reliability..IF.)
						newdata = rbind(newdata,data[lines,])
					}
				}
			}
	}
	if (info == TRUE){
		return(newdata)
	}
	else{
		return(data)
	}
		
}

writeData = function(data,filename){

	write.table(data,file=filename,sep="\t",quote=FALSE,col.names=TRUE,row.names=FALSE)
}

# Run 
data = cutData(proteinatlas,genes)

data = filterTissue(data, tissues)
data = filterIH(data,IH)
data = filterIF(data, IF)

writeData(data,filename)
