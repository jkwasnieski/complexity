#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(tidyr))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(tibble))

# arg[1] is --args
# arg[2] is complexity report file
# arg[3] is output pdf file


args <- commandArgs(trailingOnly = T)

raw_complexity <- read.table(args[2], header=T)

complexity <- as.tibble(raw_complexity) %>%
gather( key=metric, value=value, -barcode, -condition)

p1<- ggplot(complexity, aes(condition, value)) + 
geom_bar(stat="identity", position="dodge") +
facet_wrap(~metric, nrow=3, scales="free_y")  + 
scale_y_log10() + 
theme_bw(base_size=16) + 
theme(axis.text.x=element_text(angle=90, hjust=1))

ggsave(args[3], plot=p1, device="pdf", width=7, height=7)
