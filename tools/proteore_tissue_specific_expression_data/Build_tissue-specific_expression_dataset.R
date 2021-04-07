

select_hpaimmunohisto <- function(hpa_ref, tissue, level, reliability) {
  hpa_normal <- read.table(hpa_ref, header = TRUE, sep = "\t",
                           stringsAsFactors = FALSE)
  # nolint start
  hpa_normal$Tissue <- sapply(hpa_normal$Tissue,
                              function(string) gsub(
                                "cervix, uterine", "cervix_uterine", string),
                              USE.NAMES = F)
  # nolint end
  if (tissue == "tissue") {
    tissue <- unique(hpa_normal$Tissue)
  }
  if (level == "level") {
    level <- unique(hpa_normal$Level)
  }
  if (reliability == "reliability") {
    reliability <- unique(hpa_normal$Reliability)
  }
  res_imm <- subset(hpa_normal, Tissue %in% tissue & Level %in% level
                    & Reliability %in% reliability)
  return(res_imm)
}

select_hparnaseq <- function(hpa_ref, sample) {
  hpa_rnatissue <- read.table(hpa_ref, header = TRUE, sep = "\t",
                              stringsAsFactors = FALSE)
  names(hpa_rnatissue) <- sapply(names(hpa_rnatissue), function(string)
    gsub("Sample", "Tissue", string), USE.NAMES = F)
  # nolint start
  hpa_rnatissue$Tissue <- sapply(hpa_rnatissue$Tissue, function(string)
    gsub("cervix, uterine", "cervix_uterine", string), USE.NAMES = F)
  # nolint end
  res_rna <- subset(hpa_rnatissue, Tissue %in% sample)
  if ("Unit" %in% names(res_rna)) {
    res_rna <- subset(res_rna, select = -Unit)
    colnames(res_rna)[which(colnames(res_rna) == "Value")] <- "Value (TPM unit)"
  }

  return(res_rna)
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
        --data_source: IHC/RNAseq
        --hpe_ref: path to reference file normal_tissue.tsv/rna_tissue.tsv)
          if IHC:
            --tissue: list of tissues
            --level: Not detected, Low, Medium, High
            --reliability: Supported, Approved, Enhanced, Uncertain
          if RNAseq:
            --sample: Sample tissues
        --output: output filename \n")

    q(save = "no")
  }

  # Parse arguments
  parseargs <- function(x) strsplit(sub("^--", "", x), "=")
  argsdf <- as.data.frame(do.call("rbind", parseargs(args)))
  args <- as.list(as.character(argsdf$V2))
  names(args) <- argsdf$V1

  # Extract options
  data_source <- args$data_source
  hpa_ref <- args$hpa_ref
  if (data_source == "IHC") {
    tissue <- strsplit(args$tissue, ",")[[1]]
    level <- strsplit(args$level, ",")[[1]]
    reliability <- strsplit(args$reliability, ",")[[1]]
    # Calculation
    res <- suppressWarnings(select_hpaimmunohisto(
      hpa_ref, tissue, level, reliability))
  }
  else if (data_source == "RNAseq") {
    sample <- strsplit(args$sample, ",")[[1]]
    # Calculation
    res <- suppressWarnings(select_hparnaseq(hpa_ref, sample))
  }

  # Write output
  output <- args$output
  write.table(res, output, sep = "\t", quote = FALSE, row.names = FALSE)
}

main()
