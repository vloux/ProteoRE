# Command line arguments : Rscript --vanilla getData.R proteinatlas.csv genelist.txt filtertissue filterIF filterIH filename
# e.g : Rscript --vanilla get_data_HPA_v2.R proteinatlas.csv prots_insoluble_fraction_mapped.txt tenriched,tenhanced approved approved get_data_insoluble_enriched_IF_approved_IH_approved.txt
# INPUT : 
#	- proteinatlas tab file
#	- protein list of interest
#	- tissue enriched (tenriched), tissue enhanced (tenhanced), group enriched(genriched), expressed in all (exprall), mixed (mixed), not detected (ndetected)
#	  or multiple combination with terms separated by a comma (e.g : tenriched,tenhanced) 
#	- reliability IF (approved,uncertain,supported,validated) or multiple combination with terms separated by a comma
#	- reliability IH (approved,uncertain,supported) or multiple combination with terms separated by a comma
#	- output file name

args = commandArgs(trailingOnly = TRUE)

proteinatlas = read.table(args[1],header=TRUE,sep="\t",fill=TRUE,blank.lines.skip=TRUE,quote="\"")
genes = read.table(args[2],header=FALSE,sep="\t")
genes = genes$V1

tissue=args[3]
IF=args[4]
IH=args[5]
filename=as.character(args[6])

'%!in%' <- function(x,y)!('%in%'(x,y))

# Delete unused columns in protein atlas and select only the genes of interest
cutData = function(proteinatlas,genes){
	
	# Delete unused columns
	proteinatlas = proteinatlas[,-which(colnames(proteinatlas) %!in% c("Gene","Ensembl","Antibody","Reliability..IH.","Reliability..IF.","Subcellular.location","RNA.tissue.category","RNA.TS","RNA.TS.TPM","TPM.max.in.non.specific"))]
	# Keep only genes of the user gene list
	proteinatlas = proteinatlas[which(proteinatlas$Ensembl %in% genes),]

	return(proteinatlas)
}


# Parse the arguments if multiple arguments were given as input in one argument (e.g for argument tissue tenriched,tenhanced )
parseInput = function(arg){
	arglist = strsplit(arg,",")
	arglist = arglist[[1]]
	arglist=as.character(arglist)
	return(arglist)
}


# Filter according to the tissue category (RNA.tissue.category)
filterTissue = function(proteinatlas, tissue){
	data = list()
	info=FALSE
	for (t in tissue){

		if (t == "tenriched"){
			if ("Tissue enriched" %in% proteinatlas$RNA.tissue.category){
				lines = grep("Tissue enriched",proteinatlas$RNA.tissue.category)
				data=rbind(data,proteinatlas[lines,])
				info = TRUE 
			}
		}		

		if (t == "tenhanced"){

			if ("Tissue enhanced" %in% proteinatlas$RNA.tissue.category){
				lines  = grep("Tissue enhanced",proteinatlas$RNA.tissue.category)
				data=rbind(data,proteinatlas[lines,])
				info = TRUE 
			}
		}

		if (t == "genriched"){
		
			if ("Group enriched" %in% proteinatlas$RNA.tissue.category){
				lines = grep("Group enriched",proteinatlas$RNA.tissue.category)
				data=rbind(data,proteinatlas[lines,])
				info = TRUE 
			}

		}

		if (t == "exprall"){

			if ("Expressed in all" %in% proteinatlas$RNA.tissue.category){
				lines = grep("Expressed in all",proteinatlas$RNA.tissue.category)
				data=rbind(data,proteinatlas[lines,])
				info = TRUE 
			}
		}
		if (t == "mixed"){

			if ("Mixed" %in% proteinatlas$RNA.tissue.category){
				lines = grep("Mixed",proteinatlas$RNA.tissue.category)
				data=rbind(data,proteinatlas[lines,])
				info = TRUE
			} 

		}

		if (t == "ndetected"){
			
			if ("Not detected" %in% proteinatlas$RNA.tissue.category){
				lines = grep("Not detected",proteinatlas$RNA.tissue.category)
				data=rbind(data,proteinatlas[lines,])
				info = TRUE 
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
	for (term in IH){
		if (term == "approved"){
			if ("Approved" %in% data$Reliability..IH.){
				lines = grep("Approved",data$Reliability..IH.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
			}
		}	

		if (term == "uncertain"){

			if ("Uncertain" %in% data$Reliability..IH.){
				lines = grep("Uncertain",data$Reliability..IH.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
			}
		}

		if (term == "supported"){

			if ("Supported" %in% data$Reliability..IH.){
				lines = grep("Supported",data$Reliability..IH.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
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

	for (term in IF){
		if (term == "approved"){
			if ("Approved" %in% data$Reliability..IF.){
				lines = grep("Approved",data$Reliability..IF.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
			}
		}	

		if (term == "uncertain"){

			if ("Uncertain" %in% data$Reliability..IF.){
				lines = grep("Uncertain",data$Reliability..IF.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
			}
		}

		if (term == "supported"){

			if ("Supported" %in% data$Reliability..IF.){
				lines = grep("Supported",data$Reliability..IF.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
			}
		}	
		if (term == "validated"){

			if ("Validated" %in% data$Reliability..IF.){
				lines = grep("Validated",data$Reliability..IF.)
				newdata = rbind(newdata,data[lines,])
				info=TRUE
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
tissue = parseInput(tissue)
IH = parseInput(IH)
IF = parseInput(IF)
data = filterTissue(data, tissue)
data = filterIH(data,IH)
data = filterIF(data, IF)

writeData(data,filename)
