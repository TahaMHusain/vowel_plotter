#!/usr/bin/env Rscript

# Install librarian
install.packages("librarian", repos="http://cran.us.r-project.org", quiet = TRUE)

# Check if required packages are installed, and if not install them. Then load all packages
librarian::shelf(ggplot2, svglite, quiet = TRUE)

# Check if correct number of args given
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  stop("Only provide 1 argument - the input csv file", call.=FALSE)
}

# Set path to save ggplot
graph_outpath <- paste(substr(args[1], 1, nchar(args[1]) - 4), ".svg", sep = "")

# Load csv into dataframe
vowels <- read.csv(args[1])

# Create ggplot  
graph <- ggplot(data = vowels, aes(x = F2, y = F1, color = vowel, label = vowel)) +
  geom_text() +
  theme_classic()

# Save ggplot
ggsave(file = graph_outpath, plot = graph, width = 10, height = 8)