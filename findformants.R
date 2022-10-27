#!/usr/bin/env Rscript

# Install librarian
install.packages("librarian", repos="http://cran.us.r-project.org", quiet = TRUE)

# Check if required packages are installed, and if not install them. Then load all packages
librarian::shelf(phonTools, quiet = TRUE)

# Check if correct number of args given
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  stop("Only provide 1 argument - the input wav file", call.=FALSE)
}

sound <- loadsound(args[1])
print(findformants(sound))
