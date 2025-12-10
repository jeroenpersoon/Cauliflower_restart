
#TODO: set the working directory to the folder where classied_groups.csv is in
setwd("C:/Users/jeroe/DocumentenPC/Jeroen/Master Bioinformatics/Thesis/Data/classification_c4_pangenome")


#install.packages("tidyverse")
#install.packages("readxl")
#install.packages("ggtext")
#install.packages("patchwork")
#install.packages("cowplot")
#install.packages("UpSetR")
#install.packages("ComplexUpset")

library(tidyverse)
library(readxl)
library(ggtext)
library(patchwork)
library(cowplot)
library(UpSetR)
library(ComplexUpset)

hom_groups<-read.csv("classified_groups.csv",header=T)

hom_groups <- hom_groups[,-1] # delete the first column (homology group id)

#TODO: change the name of the accessions
names_sort<-c("Korso", "Cauliflower", "T25", "T21" ) #Put the colnames

#TODO: change the size of the range of the columns accordingly
colnames(hom_groups)[c(2:5)] <- names_sort #Assign the colnames

hom_groups[which(hom_groups[,1]== "core & single copy orthologous"), 1] <- "core" #everything what is set as core & single copy orthologous is set to core

complexData <- hom_groups
complexData[names_sort] <- complexData[names_sort] != 0 #makes a new table and put True or False instead of numbers (amount of occurence per homology group)
complexData$class <- factor(as.factor(complexData$class), levels = c("unique", "accessory", "core"))

#TODO: change the names of the accessions and their species name
assembly_class <- data.frame(set=c("Korso", "Cauliflower", "T25", "T21"),
                               taxon=c("botrytis", "botrytis", "botrytis", "botrytis")) #Makes a new table with the names of the accessions and their taxon


p1 <- ComplexUpset::upset(
  complexData,
  names_sort,
  sort_sets=FALSE,
  # sort_intersections = FALSE,
  sort_intersections_by =c('degree', 'cardinality'),
  #n_intersections=15,
  #min_size=250,
   set_sizes = (
     upset_set_size(
       geom = geom_bar(
         fill = "#a780ba",
         #aes(fill = "botrytis"),
         width = 0.6,
         show.legend = FALSE
       ),
       position="left"
     ) +
    scale_y_continuous(breaks = c(0, 20000, 40000), labels = c("0", "20.000", "40.000"))
   ),
  base_annotations=list(
    'Intersection size'=intersection_size(
        #geom=geom_bar(
        aes(fill=class),
        #colors = c(
        #  "core" = "#66c2a5",
        #  "accessory" = "#fc8d62",
        #  "unique" = "#8da0cb"),
        #stat='count'
      #),
      text=list(
        vjust=-0.7,
        hjust=0.3,
        angle=25,
        color = 'black'
      )
    )
  ),
  height_ratio = 1.8,
  width_ratio=0.2,
  stripes=upset_stripes(
    mapping=aes(color= ""),
    #colors=c(
      #"botrytis"="#D3D3D3"
      #"botrytis"="#f3766e"
      #"Rhamnaceae"="#a780ba",
      #"Amygdaloideae"="#1bbdc2",
      #"Rosoideae" = "#7baf42"
    #),
    data=assembly_class
  ),
  themes=upset_default_themes(text=element_text(face='italic'))
)+theme_classic(base_size = 20)+
  theme(axis.text.x = element_blank(), axis.title.x = element_blank())
  

p1
