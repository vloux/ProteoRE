# Read file and return file content as data.frame
read_file <- function(path, header) {
  file <- try(
    read.csv(path, header = header, sep = "\t", stringsAsFactors = FALSE,
             quote = "\"", check.names = F),
    silent = TRUE)
  if (inherits(file, "try-error")) {
    stop("File not found !")
  }else{
    return(file)
  }
}

str2bool <- function(x) {
  if (any(is.element(c("t", "true"), tolower(x)))) {
    return(TRUE)
  }else if (any(is.element(c("f", false), tolower(x)))) {
    return(FALSE)
  }else{
    return(NULL)
  }
}

# input has to be a list of IDs in ENSG format
# tissue is one of unique(HPA.normal.tissue$Tissue)
# level is one, or several, or 0 (=ALL) of "Not detected","Medium","High","Low"
# reliability is one, or several, or 0 (=ALL)
# of "Approved","Supported","Uncertain"
annot_hpanorm <- function(input, hpa_normal_tissue, tissue, level,
                          reliability, not_mapped_option) {
  dat <- subset(hpa_normal_tissue, Gene %in% input)
  res_tissue <- subset(dat, Tissue %in% tissue)
  res_level <- subset(res_tissue, Level %in% level)
  res_rel <- subset(res_level, Reliability %in% reliability)

    if (not_mapped_option) {
    if (length(setdiff(intersect(input, unique(dat$Gene)),
                       unique(res_rel$Gene))) > 0) {
      not_match_ids <- matrix(setdiff(intersect(
        input, unique(dat$Gene)), unique(res_rel$Gene)),
        ncol = 1, nrow = length(setdiff(intersect(input, unique(dat$Gene)),
                                        unique(res_rel$Gene))))
      not_match <- matrix("no match",
                          ncol = ncol(hpa_normal_tissue) - 1,
                          nrow = length(not_match_ids))
      not_match <- cbind(not_match_ids, unname(not_match))
      colnames(not.match) <- colnames(hpa_normal_tissue)
      res <- rbind(res_rel, not.match)
    } else {
      res <- res_rel
    }

      if (length(setdiff(input, unique(dat$Gene))) > 0) {
      not_mapped <- matrix(ncol = ncol(hpa_normal_tissue) - 1,
                           nrow = length(setdiff(input, unique(dat$Gene))))
      not_mapped <- cbind(matrix(setdiff(input, unique(dat$Gene)),
                                 ncol = 1,
                                 nrow = length(
                                   setdiff(input, unique(dat$Gene)))),
                          unname(not_mapped))
      colnames(not_mapped) <- colnames(hpa_normal_tissue)
      res <- rbind(res, not_mapped)
    }

  } else {
    res <- res_rel
  }

  return(res)

}

annot_hpacancer <- function(input,
                            hpa_cancer_tissue, cancer, not_mapped_option) {
  dat <- subset(hpa_cancer_tissue, Gene %in% input)
  res_cancer <- subset(dat, Cancer %in% cancer)

  if (not_mapped_option) {
    not_mapped <- matrix(ncol = ncol(hpa_cancer_tissue) - 1,
                         nrow = length(setdiff(input, unique(dat$Gene))))
    not_mapped <- cbind(matrix(setdiff(input, unique(dat$Gene)),
                               ncol = 1,
                               nrow = length(setdiff(input, unique(dat$Gene)))),
                        unname(not_mapped))
    colnames(not_mapped) <- colnames(hpa_cancer_tissue)
    res <- rbind(res_cancer, not_mapped)
  } else {
    res <- res_cancer
  }
  return(res)
}

clean_ids <- function(ids) {

  ids <- gsub(" ", "", ids)
  ids <- ids[which(ids != "")]
  ids <- ids[which(ids != "NA")]
  ids <- ids[!is.na(ids)]

  return(ids)
}

main <- function() {
  args <- commandArgs(TRUE)
  if (length(args) < 1) {
    args <- c("--help")
  }

  # Help section
  if ("--help" %in% args) {
    cat("Selection and Annotation HPA
    Arguments:
        --ref_file: HPA normal/cancer tissue file path
        --input_type: type of input (list of id or filename)
        --input: list of IDs in ENSG format
        --column_number: the column number which you would like to apply...
        --header: true/false if your file contains a header
        --atlas: normal/cancer
          if normal:
            --tissue: list of tissues
            --level: Not detected, Low, Medium, High
            --reliability: Supportive, Uncertain
          if cancer:
            --cancer: Cancer tissues
        --not_mapped: true/false if your output file should
        contain not-mapped and not-match IDs
        --output: output filename \n")
    q(save = "no")
}

# Parse arguments
parseargs <- function(x) strsplit(sub("^--", "", x), "=")
argsdf <- as.data.frame(do.call("rbind", parseargs(args)))
args <- as.list(as.character(argsdf$V2))
names(args) <- argsdf$V1


  # Extract input
  input_type <- args$input_type
  if (input_type == "list") {
    ids <- unlist(strsplit(strsplit(args$input, "[ \t\n]+")[[1]], ";"))
  } else if (input_type == "file") {
    filename <- args$input
    column_number <- as.numeric(gsub("c", "", args$column_number))
    header <- str2bool(args$header)
    file <- read_file(filename, header)
    ids <- unlist(strsplit(file[, column_number], ";"))
  }
  #filter ids
  ids <- clean_ids(ids)

  # Read reference file
  reference_file <- read_file(args$ref_file, TRUE)

  # Extract other options
  atlas <- args$atlas
  not_mapped_option <- str2bool(args$not_mapped)
  if (atlas == "normal") {
    tissue <- strsplit(args$tissue, ",")[[1]]
    level <- strsplit(args$level, ",")[[1]]
    reliability <- strsplit(args$reliability, ",")[[1]]
    # Calculation
    res <- annot_hpanorm(ids, reference_file,
                         tissue, level, reliability, not_mapped_option)
  } else if (atlas == "cancer") {
    cancer <- strsplit(args$cancer, ",")[[1]]
    # Calculation
    res <- annot_hpacancer(ids, reference_file, cancer, not_mapped_option)
 }

 # Write output
 output <- args$output
 res <- apply(res, c(1, 2), function(x) gsub("^$|^ $", NA, x))
 write.table(res, output, sep = "\t", quote = FALSE, row.names = FALSE)
}

main()
